
# Visualizer
# Prajwal Kondala | IIT Kharagpur

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

def plot_monthly_revenue(sales_df):
    """Monthly revenue trend chart"""
    monthly_revenue = sales_df.groupby('YearMonth')['Revenue'].sum()
    plt.figure(figsize=(14, 6))
    plt.plot(range(len(monthly_revenue)), monthly_revenue.values,
             color='steelblue', linewidth=2, marker='o', markersize=6)
    plt.fill_between(range(len(monthly_revenue)), monthly_revenue.values,
                     alpha=0.3, color='steelblue')
    plt.title('Monthly Revenue Trend (2009-2011)', fontsize=16, fontweight='bold')
    plt.xlabel('Month')
    plt.ylabel('Revenue (£)')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('screenshots/monthly_revenue.png', dpi=150)
    plt.close()
    print("✅ Chart 1 saved!")
    return monthly_revenue

def plot_top_products(sales_df):
    """Top 10 products bar chart"""
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

def plot_country_sales(df):
    """Country sales bar chart"""
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

def plot_day_analysis(sales_df):
    """Revenue by day of week"""
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
    return day_revenue

def plot_customer_segments(df):
    """Customer segments pie chart"""
    customer_revenue = df.groupby('Customer ID')['Revenue'].sum()
    customer_revenue = customer_revenue[customer_revenue.index != 0]
    def segment(rev):
        if rev >= 5000: return 'High Value'
        elif rev >= 1000: return 'Medium Value'
        else: return 'Low Value'
    segments = customer_revenue.apply(segment).value_counts()
    plt.figure(figsize=(8, 8))
    plt.pie(segments.values, labels=segments.index,
            autopct='%1.1f%%',
            colors=['gold', 'steelblue', 'lightcoral'],
            startangle=90)
    plt.title('Customer Segments by Revenue', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('screenshots/customer_segments.png', dpi=150)
    plt.close()
    print("✅ Chart 5 saved!")
    return segments
