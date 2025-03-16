# dashboard/data_analyzations/analysis.py
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
from django.conf import settings
import os

def get_sales_figure():
    # Load data from csv directory
    file_path = os.path.join(settings.BASE_DIR, 'csv', 'sales_data.csv')
    monthly_sales = pd.read_csv(file_path)  # Assumes columns: Date, Sales
    monthly_sales['Date'] = pd.to_datetime(monthly_sales['Date'])

    # Plot monthly sales
    plot_data = [
        go.Scatter(
            x=monthly_sales['Date'],
            y=monthly_sales['Sales'],
            name='',
            hovertemplate="<br>".join([
                "<b>Date: %{x}</b>",
                "<b>Sales: ₱%{y:,.2f} M</b>",
            ]),
        )
    ]
    plot_layout = go.Layout(title='Monthly Sales')
    fig = go.Figure(data=plot_data, layout=plot_layout)
    return fig

def get_unicorn_companies_analysis():
    file_path = os.path.join(settings.BASE_DIR, 'csv', 'Unicorn_companies.csv')
    companies = pd.read_csv(file_path)
    companies_df = companies.copy()
    print(companies_df.head())

    # Calculate Years Until Unicorn
    companies['Date Joined'] = pd.to_datetime(companies['Date Joined'], format='%m/%d/%y')
    companies['Year Joined'] = companies['Date Joined'].dt.year
    companies['Years Until Unicorn'] = companies['Year Joined'] - companies['Year Founded']

    categorized = (companies[['Industry', 'Years Until Unicorn']].groupby('Industry').max().sort_values(by='Years Until Unicorn'))
    print(categorized.head())

    # Calculate Maximum Valuation
    companies['Valuation In Numbers'] = companies['Valuation'].str.replace('$', '').str.replace('B', '').astype(int)
    categorized2 = (companies[['Industry', 'Valuation In Numbers']]
                    .groupby('Industry')
                    .max()
                    .sort_values(by='Valuation In Numbers', ascending=False))

    # Create horizontal bar chart for Years Until Unicorn
    bar1 = go.Bar(
        y=categorized.index,  # Industries on y-axis
        x=categorized['Years Until Unicorn'],  # Values on x-axis
        orientation='h',  # Horizontal bars
        name='Years until Unicorn',
        hovertemplate="<br>".join([
            "<b>Industry: %{y}</b>",
            "<b>Years Until Unicorn: %{x}</b>",
        ])
    )

    # Create horizontal bar chart for Maximum Valuation
    bar2 = go.Bar(
        y=categorized2.index,  # Industries on y-axis
        x=categorized2['Valuation In Numbers'],  # Values on x-axis
        orientation='h',  # Horizontal bars
        name='Maximum Valuation',
        hovertemplate="<br>".join([
            "<b>Industry: %{y}</b>",
            "<b>Valuation: $%{x} B</b>",
        ])
    )

    # Create a figure with two subplots (one column, two rows)
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=("Maximum Years Until Unicorn Status by Industry", "Maximum Valuation by Industry")
    )

    # Add bar charts to subplots
    fig.add_trace(bar1, row=1, col=1)
    fig.add_trace(bar2, row=2, col=1)

    # Update layout for the entire figure
    fig.update_layout(
        height=1000,  # Increase height to fit both subplots comfortably
        title_text="Unicorn Companies Analysis",
        showlegend=False  # Legend not needed as subplot titles suffice
    )

    # Update axes titles
    fig.update_yaxes(title_text="Industry", row=1, col=1)
    fig.update_yaxes(title_text="Industry", row=2, col=1)
    fig.update_xaxes(title_text="Years Until Unicorn", row=1, col=1)
    fig.update_xaxes(title_text="Valuation (Billions $)", row=2, col=1)

    return fig, companies_df