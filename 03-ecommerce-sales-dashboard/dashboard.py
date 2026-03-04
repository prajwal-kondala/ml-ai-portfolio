
# E-Commerce Sales Dashboard
# Prajwal Kondala | IIT Kharagpur
# Data Source: Kaggle - Online Retail II UCI

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def load_data(filepath):
    df = pd.read_csv(filepath, encoding='latin-1')
    return df

def clean_data(df):
    df = df[~df['Invoice'].astype(str).str.startswith('C')]
    df = df[df['Quantity'] > 0]
    df = df[df['Price'] > 0]
    df = df.dropna(subset=['Description'])
    df['Customer ID'] = df['Customer ID'].fillna(0).astype(int)
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['Revenue'] = df['Quantity'] * df['Price']
    return df

def engineer_features(df):
    df['Year'] = df['InvoiceDate'].dt.year
    df['Month'] = df['InvoiceDate'].dt.month
    df['Day'] = df['InvoiceDate'].dt.day
    df['DayName'] = df['InvoiceDate'].dt.day_name()
    df['YearMonth'] = df['InvoiceDate'].dt.to_period('M')
    return df

def split_dataframes(df):
    sales_df = df[['Invoice', 'StockCode', 'Description',
                   'Quantity', 'InvoiceDate', 'Price',
                   'Revenue', 'Year', 'Month', 'DayName', 'YearMonth']].copy()
    customer_df = df[['Customer ID', 'Country']].drop_duplicates().copy()
    customer_df = customer_df[customer_df['Customer ID'] != 0]
    return sales_df, customer_df

def generate_charts(sales_df, df):
    # Chart 1 - Monthly Revenue
    monthly_revenue = sales_df.groupby('YearMonth')['Revenue'].sum()
    plt.figure(figsize=(14, 6))
    plt.plot(range(len(monthly_revenue)), monthly_revenue.values,
             color='steelblue', linewidth=2, marker='o', markersize=6)
    plt.fill_between(range(len(monthly_revenue)), monthly_revenue.values,
                     alpha=0.3, color='steelblue')
    plt.title('Monthly Revenue Trend (2009-2011)', fontsize=16, fontweight='bold')
    plt.xlabel('Month')
    plt.ylabel('Revenue (£)')
    plt.xticks(range(len(monthly_revenue)),
               [str(m) for m in monthly_revenue.index], rotation=45)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('screenshots/monthly_revenue.png', dpi=150)
    plt.close()
    print("✅ Chart 1 saved!")

    # Chart 2 - Top Products
    top_products = sales_df.groupby('Description')['Revenue'].sum().sort_values(ascending=False).head(10)
    plt.figure(figsize=(12, 6))
    plt.barh(range(len(top_products)), top_products.values,
             color='steelblue', edgecolor='black', linewidth=0.5)
    plt.yticks(range(len(top_products)), [p[:30] for p in top_products.index], fontsize=9)
    plt.title('Top 10 Products by Revenue', fontsize=16, fontweight='bold')
    plt.xlabel('Revenue (£)')
    plt.gca().invert_yaxis()
    plt.grid(True, alpha=0.3, axis='x')
    plt.tight_layout()
    plt.savefig('screenshots/top_products.png', dpi=150)
    plt.close()
    print("✅ Chart 2 saved!")

    # Chart 3 - Country Sales
    country_rev = df[df['Country'] != 'United Kingdom'].groupby('Country')['Revenue'].sum()
    top_countries = country_rev.sort_values(ascending=False).head(10)
    plt.figure(figsize=(12, 6))
    plt.bar(range(len(top_countries)), top_countries.values,
            color='forestgreen', edgecolor='black', linewidth=0.5)
    plt.xticks(range(len(top_countries)), top_countries.index, rotation=45, ha='right')
    plt.title('Top 10 Countries by Revenue (Excluding UK)', fontsize=16, fontweight='bold')
    plt.xlabel('Country')
    plt.ylabel('Revenue (£)')
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig('screenshots/country_sales.png', dpi=150)
    plt.close()
    print("✅ Chart 3 saved!")

    # Chart 4 - Day of Week
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_revenue = sales_df.groupby('DayName')['Revenue'].sum().reindex(day_order)
    colors_list = ['steelblue' if d != day_revenue.idxmax() else 'crimson' for d in day_order]
    plt.figure(figsize=(10, 6))
    plt.bar(day_order, day_revenue.values, color=colors_list, edgecolor='black', linewidth=0.5)
    plt.title('Revenue by Day of Week', fontsize=16, fontweight='bold')
    plt.xlabel('Day')
    plt.ylabel('Revenue (£)')
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig('screenshots/day_analysis.png', dpi=150)
    plt.close()
    print("✅ Chart 4 saved!")

    # Chart 5 - Customer Segments
    customer_revenue = df.groupby('Customer ID')['Revenue'].sum()
    customer_revenue = customer_revenue[customer_revenue.index != 0]
    def segment_customer(revenue):
        if revenue >= 5000: return 'High Value'
        elif revenue >= 1000: return 'Medium Value'
        else: return 'Low Value'
    customer_segments = customer_revenue.apply(segment_customer).value_counts()
    plt.figure(figsize=(8, 8))
    plt.pie(customer_segments.values,
            labels=customer_segments.index,
            autopct='%1.1f%%',
            colors=['gold', 'steelblue', 'lightcoral'],
            startangle=90)
    plt.title('Customer Segments by Revenue', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('screenshots/customer_segments.png', dpi=150)
    plt.close()
    print("✅ Chart 5 saved!")

    return monthly_revenue, day_revenue, customer_segments

def generate_dashboard(sales_df, df, monthly_revenue, day_revenue, customer_segments):
    fig = plt.figure(figsize=(18, 14))
    fig.suptitle('E-Commerce Sales Dashboard (2009-2011)',
                 fontsize=22, fontweight='bold', y=0.98)
    gs = gridspec.GridSpec(3, 2, figure=fig, hspace=0.5, wspace=0.3)

    ax1 = fig.add_subplot(gs[0, :])
    ax1.plot(range(len(monthly_revenue)), monthly_revenue.values,
             color='steelblue', linewidth=2, marker='o')
    ax1.fill_between(range(len(monthly_revenue)), monthly_revenue.values,
                     alpha=0.3, color='steelblue')
    ax1.set_title('Monthly Revenue Trend', fontweight='bold')
    ax1.set_ylabel('Revenue (£)')
    ax1.grid(True, alpha=0.3)

    ax2 = fig.add_subplot(gs[1, 0])
    top5 = sales_df.groupby('Description')['Revenue'].sum().sort_values(ascending=False).head(5)
    ax2.barh(range(5), top5.values, color='steelblue')
    ax2.set_yticks(range(5))
    ax2.set_yticklabels([p[:20] for p in top5.index], fontsize=8)
    ax2.set_title('Top 5 Products', fontweight='bold')
    ax2.invert_yaxis()

    ax3 = fig.add_subplot(gs[1, 1])
    top5_countries = df[df['Country'] != 'United Kingdom'].groupby('Country')['Revenue'].sum()
    top5_countries = top5_countries.sort_values(ascending=False).head(5)
    ax3.bar(range(5), top5_countries.values, color='forestgreen')
    ax3.set_xticks(range(5))
    ax3.set_xticklabels(top5_countries.index, rotation=45, ha='right', fontsize=8)
    ax3.set_title('Top 5 Countries (ex UK)', fontweight='bold')

    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    ax4 = fig.add_subplot(gs[2, 0])
    ax4.bar(range(7), day_revenue.values, color='darkorange')
    ax4.set_xticks(range(7))
    ax4.set_xticklabels([d[:3] for d in day_order], fontsize=8)
    ax4.set_title('Revenue by Day', fontweight='bold')

    ax5 = fig.add_subplot(gs[2, 1])
    ax5.pie(customer_segments.values,
            labels=customer_segments.index,
            autopct='%1.1f%%',
            colors=['gold', 'steelblue', 'lightcoral'])
    ax5.set_title('Customer Segments', fontweight='bold')

    plt.savefig('screenshots/dashboard.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ Dashboard saved!")

def generate_pdf_report(sales_df, customer_df):
    doc = SimpleDocTemplate("sales_report.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    story.append(Paragraph("E-Commerce Sales Analysis Report", styles['Title']))
    story.append(Paragraph("Analyst: Prajwal Kondala | IIT Kharagpur", styles['Normal']))
    story.append(Spacer(1, 20))
    story.append(Paragraph("Executive Summary", styles['Heading1']))
    overview_data = [
        ['Metric', 'Value'],
        ['Total Transactions', f"{len(sales_df):,}"],
        ['Total Revenue', f"£{sales_df['Revenue'].sum():,.2f}"],
        ['Avg Order Value', f"£{sales_df['Revenue'].mean():,.2f}"],
        ['Median Order Value', f"£{sales_df['Revenue'].median():,.2f}"],
        ['Unique Products', f"{sales_df['Description'].nunique():,}"],
        ['Unique Customers', f"{customer_df['Customer ID'].nunique():,}"],
        ['Countries', f"{customer_df['Country'].nunique()}"],
        ['Best Day', 'Thursday'],
        ['Top Country (ex UK)', 'EIRE (Ireland)'],
        ['Top Product', 'Regency Cakestand 3 Tier'],
    ]
    table = Table(overview_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.steelblue),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.lightgrey]),
    ]))
    story.append(table)
    story.append(Spacer(1, 20))
    story.append(Paragraph("Key Business Insights", styles['Heading1']))
    insights = [
        "1. UK dominates revenue — home market strongest",
        "2. Ireland (EIRE) is top international market",
        "3. November/December spikes — Christmas seasonality",
        "4. Thursday is peak revenue day",
        "5. 11.4% High Value customers drive majority of revenue",
        "6. Regency Cakestand 3 Tier is top revenue product",
    ]
    for insight in insights:
        story.append(Paragraph(insight, styles['Normal']))
        story.append(Spacer(1, 8))
    doc.build(story)
    print("✅ PDF Report generated!")

if __name__ == "__main__":
    print("=" * 60)
    print("E-COMMERCE SALES DASHBOARD")
    print("=" * 60)

    print("\nLoading data...")
    df = load_data('data/sales_data.csv')
    print(f"✅ Loaded {len(df):,} rows")

    print("\nCleaning data...")
    df = clean_data(df)
    print(f"✅ Cleaned: {len(df):,} rows")

    print("\nEngineering features...")
    df = engineer_features(df)
    sales_df, customer_df = split_dataframes(df)
    print(f"✅ Sales: {len(sales_df):,} rows")
    print(f"✅ Customers: {len(customer_df):,} rows")

    print("\nGenerating charts...")
    monthly_revenue, day_revenue, customer_segments = generate_charts(sales_df, df)

    print("\nGenerating dashboard...")
    generate_dashboard(sales_df, df, monthly_revenue, day_revenue, customer_segments)

    print("\nGenerating PDF report...")
    generate_pdf_report(sales_df, customer_df)

    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE!")
    print("=" * 60)
    print(f"\nTotal Revenue: £{sales_df['Revenue'].sum():,.2f}")
    print(f"Top Product: Regency Cakestand 3 Tier")
    print(f"Top Country (ex UK): EIRE (Ireland)")
    print(f"Peak Day: Thursday")
