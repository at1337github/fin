#!/usr/bin/env python3
"""
Fixed Spending Dashboard - Single Self-Contained HTML
All visualizations embedded directly, no iframes
"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px


# Modern color palette
COLORS = {
    'Transportation': '#FF6B6B',
    'Grocery/Daily': '#4ECDC4',
    'Dining/Restaurants': '#FFE66D',
    'Financial Services': '#A8E6CF',
    'Tech & Subs': '#95E1D3',
    'Fast Food': '#FFA07A',
    'Delivery': '#DDA15E',
    'Services/Laundry': '#B8B8FF',
    'Phone/Utilities': '#FFDAB9',
    'Retail/Shopping': '#E0BBE4',
    'Other/Uncategorized': '#D3D3D3'
}

BG_COLOR = '#FAFAFA'
GRID_COLOR = '#E5E5E5'
TEXT_COLOR = '#2C3E50'


def load_data():
    """Load the July-Dec 2025 audit data."""
    df = pd.read_csv('July_December_2025_Audit.csv')
    df['Date_parsed'] = pd.to_datetime(df['Date'], format='%m/%d/%Y', errors='coerce')
    df = df[df['Analysis_Status'] == 'Included (True Spend)'].copy()
    df['Month'] = df['Date_parsed'].dt.to_period('M')
    df['MonthName'] = df['Date_parsed'].dt.strftime('%B')
    df['MonthNum'] = df['Date_parsed'].dt.month
    return df


def create_heavy_hitters_bar(df):
    """Top categories bar chart."""
    category_totals = df.groupby('Category')['Amount'].sum().abs().sort_values(ascending=False).head(8)
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
        textfont=dict(size=13, color='white', family='Arial, sans-serif'),
        hovertemplate='<b>%{y}</b><br>$%{x:,.0f}<extra></extra>'
    ))

    fig.update_layout(
        title={'text': '🎯 Heavy Hitters: Top Spending Categories', 'font': {'size': 22, 'color': TEXT_COLOR}},
        xaxis=dict(title='', showgrid=True, gridcolor=GRID_COLOR),
        yaxis=dict(title=''),
        paper_bgcolor=BG_COLOR,
        plot_bgcolor=BG_COLOR,
        height=400,
        margin=dict(t=60, l=200, r=50, b=50),
        font=dict(family='Arial, sans-serif', size=12, color=TEXT_COLOR)
    )
    return fig


def create_monthly_trend(df):
    """Monthly spending trend."""
    monthly_total = df.groupby('Month')['Amount'].sum().abs().reset_index()
    monthly_total['MonthName'] = monthly_total['Month'].dt.strftime('%B')

    # Top 5 categories for stacking
    top_categories = df.groupby('Category')['Amount'].sum().abs().sort_values(ascending=False).head(5).index
    monthly = df.groupby(['Month', 'Category'])['Amount'].sum().abs().reset_index()
    monthly['MonthName'] = monthly['Month'].dt.strftime('%B')

    fig = go.Figure()

    # Stacked bars
    for category in top_categories:
        cat_data = monthly[monthly['Category'] == category]
        fig.add_trace(go.Bar(
            x=cat_data['MonthName'],
            y=cat_data['Amount'],
            name=category,
            marker=dict(color=COLORS.get(category, '#D3D3D3')),
            hovertemplate='<b>%{x}</b><br>%{fullData.name}: $%{y:,.0f}<extra></extra>'
        ))

    fig.update_layout(
        title={'text': '📈 Monthly Spending Trends', 'font': {'size': 22, 'color': TEXT_COLOR}},
        xaxis=dict(title=''),
        yaxis=dict(title='Spending ($)', showgrid=True, gridcolor=GRID_COLOR),
        barmode='stack',
        paper_bgcolor=BG_COLOR,
        plot_bgcolor=BG_COLOR,
        height=450,
        margin=dict(t=60, l=70, r=50, b=50),
        font=dict(family='Arial, sans-serif', size=12, color=TEXT_COLOR),
        legend=dict(orientation='h', yanchor='bottom', y=-0.25, xanchor='center', x=0.5),
        hovermode='x unified'
    )
    return fig


def create_category_pie(df):
    """Category breakdown pie chart."""
    category_totals = df.groupby('Category')['Amount'].sum().abs().sort_values(ascending=False)

    fig = go.Figure(go.Pie(
        labels=category_totals.index,
        values=category_totals.values,
        hole=0.4,
        marker=dict(
            colors=[COLORS.get(cat, '#D3D3D3') for cat in category_totals.index],
            line=dict(color='white', width=2)
        ),
        textfont=dict(size=13, color='white'),
        hovertemplate='<b>%{label}</b><br>$%{value:,.0f}<br>%{percent}<extra></extra>'
    ))

    fig.update_layout(
        title={'text': '📊 Category Distribution', 'font': {'size': 22, 'color': TEXT_COLOR}},
        paper_bgcolor=BG_COLOR,
        height=450,
        margin=dict(t=60, l=0, r=0, b=0),
        font=dict(family='Arial, sans-serif', size=12, color=TEXT_COLOR),
        showlegend=True,
        legend=dict(orientation='v', yanchor='middle', y=0.5, xanchor='left', x=1.05)
    )
    return fig


def create_monthly_comparison(df):
    """Month-to-month comparison line chart."""
    monthly_total = df.groupby('Month')['Amount'].sum().abs().reset_index()
    monthly_total['MonthName'] = monthly_total['Month'].dt.strftime('%B')

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=monthly_total['MonthName'],
        y=monthly_total['Amount'],
        mode='lines+markers+text',
        line=dict(color='#667eea', width=3),
        marker=dict(size=12, color='#667eea', line=dict(color='white', width=2)),
        text=[f'${v:,.0f}' for v in monthly_total['Amount']],
        textposition='top center',
        textfont=dict(size=11, color=TEXT_COLOR),
        hovertemplate='<b>%{x}</b><br>$%{y:,.0f}<extra></extra>'
    ))

    # Add average line
    avg = monthly_total['Amount'].mean()
    fig.add_hline(y=avg, line_dash="dash", line_color="#95a5a6",
                  annotation_text=f"Average: ${avg:,.0f}",
                  annotation_position="right")

    fig.update_layout(
        title={'text': '📉 Monthly Total Comparison', 'font': {'size': 22, 'color': TEXT_COLOR}},
        xaxis=dict(title=''),
        yaxis=dict(title='Total Spending ($)', showgrid=True, gridcolor=GRID_COLOR),
        paper_bgcolor=BG_COLOR,
        plot_bgcolor=BG_COLOR,
        height=400,
        margin=dict(t=60, l=70, r=50, b=50),
        font=dict(family='Arial, sans-serif', size=12, color=TEXT_COLOR)
    )
    return fig


def create_dashboard():
    """Create complete self-contained dashboard."""
    print("Loading data...")
    df = load_data()

    total_spend = abs(df['Amount'].sum())
    avg_monthly = total_spend / 6
    total_trans = len(df)
    avg_trans = total_spend / total_trans

    print("Creating visualizations...")
    fig1 = create_heavy_hitters_bar(df)
    fig2 = create_monthly_trend(df)
    fig3 = create_category_pie(df)
    fig4 = create_monthly_comparison(df)

    # Convert to HTML divs
    plot1_html = fig1.to_html(include_plotlyjs='cdn', div_id='plot1')
    plot2_html = fig2.to_html(include_plotlyjs=False, div_id='plot2')
    plot3_html = fig3.to_html(include_plotlyjs=False, div_id='plot3')
    plot4_html = fig4.to_html(include_plotlyjs=False, div_id='plot4')

    # Create HTML
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Spending Dashboard - July to December 2025</title>
    <meta charset="utf-8">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Arial', sans-serif;
            background-color: {BG_COLOR};
            color: {TEXT_COLOR};
            padding: 20px;
            line-height: 1.6;
        }}
        .header {{
            text-align: center;
            padding: 40px 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        .header h1 {{
            font-size: 42px;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        .header p {{
            font-size: 18px;
            opacity: 0.95;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        .metrics {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .metric-card {{
            background: white;
            padding: 25px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            transition: transform 0.2s;
        }}
        .metric-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.12);
        }}
        .metric-label {{
            font-size: 13px;
            color: #7f8c8d;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }}
        .metric-value {{
            font-size: 32px;
            font-weight: bold;
            color: {TEXT_COLOR};
        }}
        .chart {{
            background: white;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 30px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}
        .insight-box {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            margin: 30px 0;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        .insight-box h2 {{
            font-size: 24px;
            margin-bottom: 15px;
        }}
        .insight-box ul {{
            list-style-position: inside;
            font-size: 16px;
            line-height: 1.9;
        }}
        .insight-box li {{
            margin-bottom: 10px;
        }}
        .grid-2 {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(600px, 1fr));
            gap: 30px;
            margin-bottom: 30px;
        }}
        @media (max-width: 768px) {{
            .grid-2 {{
                grid-template-columns: 1fr;
            }}
            .header h1 {{
                font-size: 32px;
            }}
            .metric-value {{
                font-size: 24px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>💰 Spending Dashboard</h1>
            <p>July to December 2025 • 6 Month Analysis</p>
        </div>

        <div class="metrics">
            <div class="metric-card">
                <div class="metric-label">Total Spending</div>
                <div class="metric-value">${total_spend:,.0f}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Monthly Average</div>
                <div class="metric-value">${avg_monthly:,.0f}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Transactions</div>
                <div class="metric-value">{total_trans}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Avg per Transaction</div>
                <div class="metric-value">${avg_trans:,.0f}</div>
            </div>
        </div>

        <div class="insight-box">
            <h2>🎯 Key Insights</h2>
            <ul>
                <li><strong>Transportation dominates spending</strong> at 21.6% ($6,861), including CLEO AI rental car, rideshares, and transit</li>
                <li><strong>Food spending combined</strong> (Grocery + Dining + Fast Food + Delivery) accounts for 29.5% ($9,356) of total</li>
                <li><strong>Peak spending month</strong> was August ($7,306), while October was lowest ($3,465)</li>
                <li><strong>Top 4 categories</strong> represent 53% of all spending</li>
            </ul>
        </div>

        <div class="chart">
            {plot1_html}
        </div>

        <div class="chart">
            {plot2_html}
        </div>

        <div class="grid-2">
            <div class="chart">
                {plot3_html}
            </div>
            <div class="chart">
                {plot4_html}
            </div>
        </div>

        <div class="insight-box">
            <h2>📊 Monthly Patterns</h2>
            <ul>
                <li><strong>Highest:</strong> August at $7,306</li>
                <li><strong>Lowest:</strong> October at $3,465</li>
                <li><strong>Variance:</strong> 2.1x difference between months</li>
                <li><strong>Recommendation:</strong> Budget for ~$5,300/month to accommodate peaks</li>
            </ul>
        </div>
    </div>
</body>
</html>
"""

    with open('Dashboard.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("\n" + "="*60)
    print("✅ DASHBOARD CREATED!")
    print("="*60)
    print("\nOpen: Dashboard.html")
    print("="*60)


if __name__ == "__main__":
    create_dashboard()
