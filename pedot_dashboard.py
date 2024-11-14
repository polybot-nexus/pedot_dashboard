import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import io

# Loading the experimental data
pedot_data = pd.read_csv('PEDOT_experiment.csv')
pedot_param_keys = [
    'DMSO concentration (Vol%)',
    'EG concentration (Vol%)',
    'Coating speed (mm/sec)',
    'Coating temperature (Celsius)',
    'Post-processing solvent No.',
    'Post coating speed (mm/sec)',
    'Post coating temperature (Celsius)',
]
pedot_output_keys = [
    "Average coverage (%)",
    "Average conductivity (S/cm)",
]

# App initialization
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Main layout
app.layout = html.Div([
    html.H1("PEDOT:PSS High-Throughput Experiment", style={"textAlign": "center", "marginBottom": "30px"}),

    html.Div([
        html.H3("Dataset"),
        dash.dash_table.DataTable(
            id='data-table',
            columns=[{"name": col, "id": col} for col in pedot_data.columns],
            data=pedot_data.to_dict('records'),
            page_size=10,
            style_table={
                'overflowX': 'auto',
                'marginLeft': '20px'
            },
            style_header={
                'backgroundColor': '#f8f9fa',
                'fontWeight': 'bold',
                'textAlign': 'center',
                'border': '1px solid #dee2e6'
            },
            style_cell={
                'padding': '10px',
                'textAlign': 'left',
                'border': '1px solid #dee2e6',
                'backgroundColor': '#ffffff',
                'color': '#333',
                'fontFamily': 'Arial, sans-serif'
            },
            style_cell_conditional=[
                {'if': {'column_id': 'Molecule ID'}, 'textAlign': 'left'},
                {'if': {'column_id': 'Formula'}, 'textAlign': 'left'}
            ],
            style_data={
                'border': '1px solid #dee2e6'
            },
            style_as_list_view=True
        )
    ], style={"padding": "40px 60px", "backgroundColor": "#ffffff"}),

    html.Div([
        html.Button("Download Dataset", id="btn-download"),
        dcc.Download(id="download-dataframe-csv")
    ], style={
        "margin": "20px 0",
        "float": "right",  
        "marginRight": "40px",
        'backgroundColor': "#e9ecef"
    }),

    html.Div([
        html.Div([
            html.P(
                "Schematic illustrating the concecutive steps in the autonomous experiment workflow" ,
                style={"marginLeft": "40px", "marginTop": "10px", "marginBottom": "10px"}  
            ),
            html.Img(src='/assets/polybot_logo.png', style={
                'width': '60%',  
                'marginTop': '10px', "marginLeft": "80px" 
            })
        ], style={'flex': '1', 'marginRight': '10px'}), 

        html.Div([
            html.Label("Select Parameter for X-axis:"),
            dcc.Dropdown(
                id='x-axis',
                options=[{"label": param, "value": param} for param in pedot_param_keys],
                value=pedot_param_keys[0],
                style={"width": "300px"}  
            ),
            html.Label("Select Parameter for Y-axis:"),
            dcc.Dropdown(
                id='y-axis',
                options=[{"label": param, "value": param} for param in pedot_output_keys],
                value=pedot_output_keys[0],
                style={"width": "300px"} 
            ),
            dcc.Graph(id='correlation-plot')
        ], style={'flex': '1', 'marginLeft': '40px'})
    ], style={'display': 'flex', 'marginTop': '20px'})
])

@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("btn-download", "n_clicks"),
    prevent_initial_call=True
)
def download_dataset(n_clicks):
    csv_string = pedot_data.to_csv(index=False, encoding='utf-8')
    return dict(content=csv_string, filename="PEDOT_experiment.csv")

@app.callback(
    Output('correlation-plot', 'figure'),
    [Input('x-axis', 'value'), Input('y-axis', 'value')]
)

def update_graph(x_axis, y_axis):
    fig = px.scatter(
        pedot_data,
        x=x_axis,
        y=y_axis,
        color=pedot_data[y_axis], 
        title=f"Correlation between {x_axis} and {y_axis}",
        labels={x_axis: x_axis, y_axis: y_axis},
        hover_data=pedot_data.columns,
        color_continuous_scale=px.colors.sequential.Viridis, 
        template="plotly_white"
    )
    
    fig.update_traces(
        marker=dict(size=10, opacity=0.7, line=dict(width=1, color='DarkSlateGrey'))
    )
    fig.update_layout(
        title_font=dict(size=20, color='DarkSlateGrey', family="Arial"),
        xaxis=dict(showgrid=True, gridcolor='lightgrey'),
        yaxis=dict(showgrid=True, gridcolor='lightgrey'),
        plot_bgcolor='white',
        margin=dict(l=40, r=40, t=40, b=40),
        legend=dict(title="Legend", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    return fig

# Running the app
if __name__ == "__main__":
    app.run_server(debug=True)
