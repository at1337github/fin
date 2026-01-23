#!/usr/bin/env python3
"""
Spending Dashboard - July to December 2025
Clean, modern, insightful visualization of spending patterns
"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from datetime import datetime


# Modern color palette - bright but not busy
COLORS = {
    'Transportation': '#FF6B6B',      # Coral red
    'Grocery/Daily': '#4ECDC4',       # Teal
    'Dining/Restaurants': '#FFE66D',  # Yellow
    'Financial Services': '#A8E6CF',  # Mint
    'Tech & Subs': '#95E1D3',         # Aqua
    'Fast Food': '#FFA07A',           # Light salmon
    'Delivery': '#DDA15E',            # Tan
    'Services/Laundry': '#B8B8FF',    # Lavender
    'Phone/Utilities': '#FFDAB9',     # Peach
    'Retail/Shopping': '#E0BBE4',     # Mauve
    'Other/Uncategorized': '#D3D3D3'  # Light gray
}

# Background color
BG_COLOR = '#FAFAFA'
GRID_COLOR = '#E5E5E5'
TEXT_COLOR = '#2C3E50'


def load_data():
    """Load the July-Dec 2025 audit data."""
    df = pd.read_csv('July_December_2025_Audit.csv')

    # Parse dates
    df['Date_parsed'] = pd.to_datetime(df['Date'], format='%m/%d/%Y', errors='coerce')

    # Filter to included only
    df = df[df['Analysis_Status'] == 'Included (True Spend)'].copy()

    # Add time columns
    df['Month'] = df['Date_parsed'].dt.to_period('M')
    df['MonthName'] = df['Date_parsed'].dt.strftime('%B')
    df['MonthNum'] = df['Date_parsed'].dt.month

    return df


def create_summary_metrics(df):
    """Create summary metric cards."""
    total_spend = abs(df['Amount'].sum())
    avg_monthly = total_spend / 6
    total_trans = len(df)
    avg_trans = total_spend / total_trans

    metrics_html = f"""
    <div style="display: flex; justify-content: space-around; padding: 20px; background: white; border-radius: 10px; margin: 20px 0;">
        <div style="text-align: center;">
            <div style="font-size: 14px; color: #7f8c8d;">Total Spending</div>
            <div style="font-size: 36px; font-weight: bold; color: {TEXT_COLOR};">${total_spend:,.0f}</div>
        </div>
        <div style="text-align: center;">
            <div style="font-size: 14px; color: #7f8c8d;">Monthly Average</div>
            <div style="font-size: 36px; font-weight: bold; color: {TEXT_COLOR};">${avg_monthly:,.0f}</div>
        </div>
        <div style="text-align: center;">
            <div style="font-size: 14px; color: #7f8c8d;">Transactions</div>
            <div style="font-size: 36px; font-weight: bold; color: {TEXT_COLOR};">{total_trans}</div>
        </div>
        <div style="text-align: center;">
            <div style="font-size: 14px; color: #7f8c8d;">Avg per Transaction</div>
            <div style="font-size: 36px; font-weight: bold; color: {TEXT_COLOR};">${avg_trans:,.0f}</div>
        </div>
    </div>
    """
    return metrics_html


def create_category_sunburst(df):
    """Create sunburst chart showing category hierarchy."""
    # Aggregate by category
    category_totals = df.groupby('Category')['Amount'].sum().abs().sort_values(ascending=False)

    fig = go.Figure(go.Sunburst(
        labels=['Total Spending'] + list(category_totals.index),
        parents=[''] + ['Total Spending'] * len(category_totals),
        values=[category_totals.sum()] + list(category_totals.values),
        branchvalues='total',
        marker=dict(
            colors=['#FAFAFA'] + [COLORS.get(cat, '#D3D3D3') for cat in category_totals.index],
            line=dict(color='white', width=2)
        ),
        textfont=dict(size=14, color='white', family='Arial'),
        hovertemplate='<b>%{label}</b><br>$%{value:,.0f}<br>%{percentParent}<extra></extra>'
    ))

    fig.update_layout(
        title={
            'text': 'Spending Breakdown by Category',
            'font': {'size': 24, 'color': TEXT_COLOR, 'family': 'Arial'}
        },
        paper_bgcolor=BG_COLOR,
        plot_bgcolor=BG_COLOR,
        height=500,
        margin=dict(t=80, l=0, r=0, b=0)
    )

    return fig


def create_heavy_hitters_bar(df):
    """Create bar chart showing heavy hitter categories."""
    # Get top categories
    category_totals = df.groupby('Category')['Amount'].sum().abs().sort_values(ascending=False).head(8)

    # Calculate percentages
    total = category_totals.sum()
    percentages = (category_totals / total * 100).round(1)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=category_totals.values,
        y=category_totals.index,
        orientation='h',
        marker=dict(
            color=[COLORS.get(cat, '#D3D3D3') for cat in category_totals.index],
            line=dict(color='white', width=1.5)
        ),
        text=[f'${v:,.0f} ({p}%)' for v, p in zip(category_totals.values, percentages)],
        textposition='auto',
        textfont=dict(size=13, color='white', family='Arial'),
        hovertemplate='<b>%{y}</b><br>$%{x:,.0f}<extra></extra>'
    ))

    fig.update_layout(
        title={
            'text': '🎯 Heavy Hitters: Top Spending Categories',
            'font': {'size': 24, 'color': TEXT_COLOR, 'family': 'Arial'}
        },
        xaxis=dict(
            title='',
            showgrid=True,
            gridcolor=GRID_COLOR,
            zeroline=False
        ),
        yaxis=dict(
            title='',
            showgrid=False
        ),
        paper_bgcolor=BG_COLOR,
        plot_bgcolor=BG_COLOR,
        height=450,
        margin=dict(t=80, l=200, r=50, b=50),
        font=dict(family='Arial', size=12, color=TEXT_COLOR)
    )

    return fig


def create_monthly_trend(df):
    """Create monthly spending trend with breakdown by category."""
    # Monthly totals
    monthly = df.groupby(['Month', 'Category'])['Amount'].sum().abs().reset_index()
    monthly['MonthName'] = monthly['Month'].dt.strftime('%B')

    # Overall monthly total
    monthly_total = df.groupby('Month')['Amount'].sum().abs().reset_index()
    monthly_total['MonthName'] = monthly_total['Month'].dt.strftime('%B')

    # Get top 5 categories
    top_categories = df.groupby('Category')['Amount'].sum().abs().sort_values(ascending=False).head(5).index

    fig = go.Figure()

    # Add stacked bars for top categories
    for category in top_categories:
        cat_data = monthly[monthly['Category'] == category]
        fig.add_trace(go.Bar(
            x=cat_data['MonthName'],
            y=cat_data['Amount'],
            name=category,
            marker=dict(color=COLORS.get(category, '#D3D3D3')),
            hovertemplate='<b>%{x}</b><br>%{fullData.name}: $%{y:,.0f}<extra></extra>'
        ))

    # Add line showing total trend
    fig.add_trace(go.Scatter(
        x=monthly_total['MonthName'],
        y=monthly_total['Amount'],
        name='Total',
        mode='lines+markers',
        line=dict(color=TEXT_COLOR, width=3, dash='dot'),
        marker=dict(size=10, color='white', line=dict(color=TEXT_COLOR, width=2)),
        hovertemplate='<b>%{x}</b><br>Total: $%{y:,.0f}<extra></extra>',
        yaxis='y2'
    ))

    fig.update_layout(
        title={
            'text': '📈 Monthly Spending Trends & Patterns',
            'font': {'size': 24, 'color': TEXT_COLOR, 'family': 'Arial'}
        },
        xaxis=dict(
            title='',
            showgrid=False
        ),
        yaxis=dict(
            title='Category Spending ($)',
            showgrid=True,
            gridcolor=GRID_COLOR,
            zeroline=False
        ),
        yaxis2=dict(
            title='Total Spending ($)',
            overlaying='y',
            side='right',
            showgrid=False
        ),
        barmode='stack',
        paper_bgcolor=BG_COLOR,
        plot_bgcolor=BG_COLOR,
        height=500,
        margin=dict(t=80, l=70, r=70, b=50),
        font=dict(family='Arial', size=12, color=TEXT_COLOR),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.2,
            xanchor='center',
            x=0.5
        ),
        hovermode='x unified'
    )

    return fig


def create_category_flow(df):
    """Create Sankey diagram showing flow from months to categories."""
    # Prepare data for Sankey
    monthly_cat = df.groupby(['MonthName', 'Category'])['Amount'].sum().abs().reset_index()

    # Get unique months and categories
    months = df['MonthName'].unique()
    categories = df['Category'].unique()

    # Create node labels
    node_labels = list(months) + list(categories)

    # Create links
    source = []
    target = []
    value = []

    for _, row in monthly_cat.iterrows():
        month_idx = list(months).index(row['MonthName'])
        cat_idx = len(months) + list(categories).index(row['Category'])
        source.append(month_idx)
        target.append(cat_idx)
        value.append(row['Amount'])

    # Node colors
    node_colors = ['#A8DADC'] * len(months) + [COLORS.get(cat, '#D3D3D3') for cat in categories]

    fig = go.Figure(go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color='white', width=2),
            label=node_labels,
            color=node_colors
        ),
        link=dict(
            source=source,
            target=target,
            value=value,
            color='rgba(200, 200, 200, 0.4)'
        )
    ))

    fig.update_layout(
        title={
            'text': '🌊 Monthly Flow to Categories',
            'font': {'size': 24, 'color': TEXT_COLOR, 'family': 'Arial'}
        },
        paper_bgcolor=BG_COLOR,
        plot_bgcolor=BG_COLOR,
        height=600,
        margin=dict(t=80, l=0, r=0, b=0),
        font=dict(family='Arial', size=12, color=TEXT_COLOR)
    )

    return fig


def create_daily_heatmap(df):
    """Create heatmap showing spending intensity by day."""
    # Add day of week and week columns
    df['DayOfWeek'] = df['Date_parsed'].dt.day_name()
    df['Week'] = df['Date_parsed'].dt.isocalendar().week - df['Date_parsed'].iloc[0].isocalendar().week

    # Aggregate by week and day
    daily = df.groupby(['Week', 'DayOfWeek'])['Amount'].sum().abs().reset_index()

    # Pivot for heatmap
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    heatmap_data = daily.pivot(index='DayOfWeek', columns='Week', values='Amount')
    heatmap_data = heatmap_data.reindex(days_order)

    fig = go.Figure(go.Heatmap(
        z=heatmap_data.values,
        x=[f'Week {i+1}' for i in range(len(heatmap_data.columns))],
        y=heatmap_data.index,
        colorscale=[[0, '#FFFFFF'], [0.5, '#FFE66D'], [1, '#FF6B6B']],
        hovertemplate='%{y}<br>%{x}<br>$%{z:,.0f}<extra></extra>',
        colorbar=dict(title='Spending ($)')
    ))

    fig.update_layout(
        title={
            'text': '🔥 Daily Spending Intensity',
            'font': {'size': 24, 'color': TEXT_COLOR, 'family': 'Arial'}
        },
        xaxis=dict(title='', showgrid=False),
        yaxis=dict(title='', showgrid=False),
        paper_bgcolor=BG_COLOR,
        plot_bgcolor=BG_COLOR,
        height=400,
        margin=dict(t=80, l=100, r=150, b=50),
        font=dict(family='Arial', size=12, color=TEXT_COLOR)
    )

    return fig


def create_transaction_frequency(df):
    """Create bubble chart showing category by frequency and amount."""
    # Group by category
    category_stats = df.groupby('Category').agg({
        'Amount': ['sum', 'count', 'mean']
    }).reset_index()

    category_stats.columns = ['Category', 'Total', 'Count', 'Average']
    category_stats['Total'] = category_stats['Total'].abs()
    category_stats['Average'] = category_stats['Average'].abs()

    # Remove uncategorized
    category_stats = category_stats[category_stats['Category'] != 'Other/Uncategorized']

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=category_stats['Count'],
        y=category_stats['Total'],
        mode='markers+text',
        marker=dict(
            size=category_stats['Average'] * 2,
            color=[COLORS.get(cat, '#D3D3D3') for cat in category_stats['Category']],
            line=dict(color='white', width=2),
            sizemode='diameter'
        ),
        text=category_stats['Category'],
        textposition='top center',
        textfont=dict(size=10, color=TEXT_COLOR),
        hovertemplate='<b>%{text}</b><br>Transactions: %{x}<br>Total: $%{y:,.0f}<br>Avg: $%{marker.size:.0f}<extra></extra>'
    ))

    fig.update_layout(
        title={
            'text': '💡 Category Insights: Frequency vs Amount',
            'font': {'size': 24, 'color': TEXT_COLOR, 'family': 'Arial'}
        },
        xaxis=dict(
            title='Number of Transactions',
            showgrid=True,
            gridcolor=GRID_COLOR,
            zeroline=False
        ),
        yaxis=dict(
            title='Total Spending ($)',
            showgrid=True,
            gridcolor=GRID_COLOR,
            zeroline=False
        ),
        paper_bgcolor=BG_COLOR,
        plot_bgcolor=BG_COLOR,
        height=500,
        margin=dict(t=80, l=70, r=50, b=70),
        font=dict(family='Arial', size=12, color=TEXT_COLOR)
    )

    return fig


def create_dashboard():
    """Create complete dashboard."""
    print("Loading data...")
    df = load_data()

    print("Creating visualizations...")

    # Create all figures
    fig_sunburst = create_category_sunburst(df)
    fig_heavy_hitters = create_heavy_hitters_bar(df)
    fig_monthly = create_monthly_trend(df)
    fig_flow = create_category_flow(df)
    fig_heatmap = create_daily_heatmap(df)
    fig_bubble = create_transaction_frequency(df)

    # Save individual figures
    print("Saving individual visualizations...")
    fig_heavy_hitters.write_html('viz_heavy_hitters.html')
    fig_monthly.write_html('viz_monthly_trends.html')
    fig_sunburst.write_html('viz_category_breakdown.html')
    fig_flow.write_html('viz_monthly_flow.html')
    fig_heatmap.write_html('viz_daily_intensity.html')
    fig_bubble.write_html('viz_category_insights.html')

    # Create main dashboard HTML
    print("Creating main dashboard...")

    dashboard_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Spending Dashboard - July to December 2025</title>
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                background-color: {BG_COLOR};
                color: {TEXT_COLOR};
                margin: 0;
                padding: 20px;
            }}
            .header {{
                text-align: center;
                padding: 30px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border-radius: 15px;
                margin-bottom: 30px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }}
            .header h1 {{
                margin: 0;
                font-size: 42px;
                font-weight: bold;
            }}
            .header p {{
                margin: 10px 0 0 0;
                font-size: 18px;
                opacity: 0.9;
            }}
            .container {{
                max-width: 1400px;
                margin: 0 auto;
            }}
            .chart {{
                background: white;
                border-radius: 15px;
                padding: 20px;
                margin-bottom: 30px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .insight-box {{
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                color: white;
                padding: 25px;
                border-radius: 15px;
                margin: 30px 0;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }}
            .insight-box h2 {{
                margin-top: 0;
                font-size: 24px;
            }}
            .insight-box ul {{
                margin: 10px 0;
                padding-left: 20px;
                font-size: 16px;
                line-height: 1.8;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>💰 Spending Dashboard</h1>
                <p>July to December 2025 • 6 Month Analysis</p>
            </div>

            {create_summary_metrics(df)}

            <div class="insight-box">
                <h2>🎯 Key Insights</h2>
                <ul>
                    <li><strong>Transportation dominates spending</strong> at 21.6% ($6,861), including rideshares, transit, and car rentals - your biggest expense category</li>
                    <li><strong>Daily essentials add up</strong>: Grocery/Daily (15.1%, $4,789) + Dining (7.3%, $2,314) + Fast Food (3.3%, $1,049) + Delivery (3.8%, $1,205) = 29.5% of total spend</li>
                    <li><strong>Peak spending month</strong> was August ($7,306), while October was lowest ($3,465) - a 2.1x difference</li>
                    <li><strong>Top 4 categories</strong> (Transportation, Grocery, Financial Services, Dining) account for 53% of all spending</li>
                    <li><strong>Transaction frequency</strong>: 1,404 transactions over 6 months = 234 per month (7.8 per day)</li>
                </ul>
            </div>

            <div class="chart">
                <iframe src="viz_heavy_hitters.html" width="100%" height="500px" frameborder="0"></iframe>
            </div>

            <div class="chart">
                <iframe src="viz_monthly_trends.html" width="100%" height="550px" frameborder="0"></iframe>
            </div>

            <div class="chart">
                <iframe src="viz_category_breakdown.html" width="100%" height="550px" frameborder="0"></iframe>
            </div>

            <div class="chart">
                <iframe src="viz_category_insights.html" width="100%" height="550px" frameborder="0"></iframe>
            </div>

            <div class="chart">
                <iframe src="viz_monthly_flow.html" width="100%" height="650px" frameborder="0"></iframe>
            </div>

            <div class="chart">
                <iframe src="viz_daily_intensity.html" width="100%" height="450px" frameborder="0"></iframe>
            </div>

            <div class="insight-box">
                <h2>📊 Spending Patterns</h2>
                <ul>
                    <li><strong>Monthly variance:</strong> Spending fluctuates between $3,465 and $7,306 - suggest budgeting for ~$5,300/month</li>
                    <li><strong>Category concentration:</strong> Heavy reliance on transportation suggests opportunity for cost optimization</li>
                    <li><strong>Food spending:</strong> Combined food costs (Grocery + Dining + Fast Food + Delivery) total $9,356 (29.5%)</li>
                    <li><strong>Financial services:</strong> $2,885 in BNPL and fees - consider cash flow management strategies</li>
                </ul>
            </div>
        </div>
    </body>
    </html>
    """

    with open('Spending_Dashboard.html', 'w') as f:
        f.write(dashboard_html)

    print("\n" + "="*60)
    print("✅ DASHBOARD CREATED SUCCESSFULLY!")
    print("="*60)
    print("\nOpen these files in your browser:")
    print("  • Spending_Dashboard.html (Main dashboard)")
    print("  • viz_heavy_hitters.html")
    print("  • viz_monthly_trends.html")
    print("  • viz_category_breakdown.html")
    print("  • viz_category_insights.html")
    print("  • viz_monthly_flow.html")
    print("  • viz_daily_intensity.html")
    print("\n" + "="*60)


if __name__ == "__main__":
    create_dashboard()
