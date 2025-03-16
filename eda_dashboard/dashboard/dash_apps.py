# dashboard/dash_apps.py
from django_plotly_dash import DjangoDash
from dash import dcc, html
import dash_bootstrap_components as dbc
import dash_table  # Add this for the DataTable component
from .data_analyzations.analysis import get_sales_figure, get_unicorn_companies_analysis

# # Declare the DjangoDash app with Bootstrap styling
# sales_app = DjangoDash('SalesHistory', external_stylesheets=[dbc.themes.BOOTSTRAP])

# # Get the Plotly figure from analysis
# sales_fig = get_sales_figure()

# # Define the layout
# sales_app.layout = html.Div([
#     dcc.Graph(
#         id='sales-history',
#         figure=sales_fig
#     ),
# ])

# Create the Dash app
unicorn_app = DjangoDash('UnicornCompanies', external_stylesheets=[dbc.themes.BOOTSTRAP])

# Get the Plotly figure from analysis
unicorn_fig, unicorn_df = get_unicorn_companies_analysis()

# Define the layout for app2
unicorn_app.layout = html.Div([
    html.H3("Unicorn Companies Data"),  # Optional: A title for the table
    dash_table.DataTable(
        id='unicorn-table',
        columns=[{"name": col, "id": col} for col in unicorn_df.columns],
        data=unicorn_df.to_dict('records'),
        page_size=5,  # Show 10 rows per page
        style_table={'overflowX': 'auto'},  # Enable horizontal scrolling for wide tables
        sort_action='native',  # Enable sorting by clicking column headers
        style_header={
            'backgroundColor': 'lightgrey',  # Light grey header background
            'fontWeight': 'bold',  # Bold header text
            'borderBottom': '1px solid black'  # Border below header
        },
        style_cell={
            'textAlign': 'left',  # Left-align text in cells
            'padding': '5px',  # Add padding for spacing
            'borderBottom': '1px solid #ddd'  # Light border between rows
        },
        style_data={
            'whiteSpace': 'normal',  # Wrap text if it’s too long
            'height': 'auto'  # Adjust row height dynamically
        }
    ),
    dcc.Graph(
        id='unicorn-companies',  # Adjusted for consistency
        figure=unicorn_fig
    ),
])