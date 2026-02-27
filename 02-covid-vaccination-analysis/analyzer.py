
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def load_data(filepath):
    """Load and prepare vaccination dataset"""
    df = pd.read_csv(filepath)
    df['date'] = pd.to_datetime(df['date'])
    return df

def clean_data(df, countries):
    """Filter and clean data for focus countries"""
    df_focus = df[df['country'].isin(countries)].copy()
    cols_to_fill = ['daily_vaccinations', 'total_vaccinations',
                    'people_fully_vaccinated_per_hundred']
    df_focus[cols_to_fill] = df_focus[cols_to_fill].fillna(0)
    return df_focus

def statistical_analysis(df_focus, countries):
    """Calculate key statistics per country"""
    results = {}
    for country in countries:
        data = df_focus[df_focus['country'] == country]
        daily_vax = data['daily_vaccinations'].values
        results[country] = {
            'total': data['total_vaccinations'].max(),
            'mean_daily': np.mean(daily_vax),
            'max_daily': np.max(daily_vax),
            'std_daily': np.std(daily_vax),
            'fully_vaccinated': data['people_fully_vaccinated_per_hundred'].max()
        }
    return results

def plot_daily_trend(df_focus, countries, colors):
    """Line chart - daily vaccinations trend"""
    plt.figure(figsize=(14, 6))
    for country, color in zip(countries, colors):
        data = df_focus[df_focus['country'] == country]
        plt.plot(data['date'], data['daily_vaccinations'],
                 label=country, color=color, linewidth=1.5, alpha=0.8)
    plt.title('Daily COVID Vaccinations — Country Comparison',
              fontsize=16, fontweight='bold')
    plt.xlabel('Date')
    plt.ylabel('Daily Vaccinations')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('screenshots/daily_vaccinations.png', dpi=150)
    plt.show()
    print("✅ Chart 1 saved!")

def plot_total_vaccinations(df_focus, countries, colors):
    """Bar chart - total vaccinations comparison"""
    total_vax = []
    for country in countries:
        data = df_focus[df_focus['country'] == country]
        total_vax.append(data['total_vaccinations'].max())

    plt.figure(figsize=(10, 6))
    bars = plt.bar(countries, total_vax, color=colors,
                   edgecolor='black', linewidth=0.5)
    for bar, val in zip(bars, total_vax):
        plt.text(bar.get_x() + bar.get_width()/2,
                 bar.get_height() + 0.01 * max(total_vax),
                 f'{val/1e6:.0f}M',
                 ha='center', va='bottom', fontweight='bold')
    plt.title('Total COVID Vaccinations by Country',
              fontsize=16, fontweight='bold')
    plt.xlabel('Country')
    plt.ylabel('Total Vaccinations')
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig('screenshots/total_vaccinations.png', dpi=150)
    plt.show()
    print("✅ Chart 2 saved!")

def plot_vaccination_percentage(df_focus, countries, colors):
    """Line chart - vaccination percentage over time"""
    plt.figure(figsize=(14, 6))
    for country, color in zip(countries, colors):
        data = df_focus[df_focus['country'] == country]
        data_clean = data[data['people_fully_vaccinated_per_hundred'] > 0]
        plt.plot(data_clean['date'],
                 data_clean['people_fully_vaccinated_per_hundred'],
                 label=country, color=color, linewidth=2)
    plt.title('People Fully Vaccinated per 100 Population',
              fontsize=16, fontweight='bold')
    plt.xlabel('Date')
    plt.ylabel('% Population Fully Vaccinated')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('screenshots/vaccination_percentage.png', dpi=150)
    plt.show()
    print("✅ Chart 3 saved!")

def plot_correlation_heatmap(df_focus, countries):
    """Heatmap - correlation between vaccination metrics"""
    cols = ['total_vaccinations_per_hundred',
            'people_vaccinated_per_hundred',
            'people_fully_vaccinated_per_hundred',
            'daily_vaccinations_per_million']
    latest = df_focus.groupby('country')[cols].max()
    corr = latest.corr()

    plt.figure(figsize=(8, 6))
    im = plt.imshow(corr, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)
    plt.colorbar(im)
    labels = ['Total/100', 'Vaccinated/100', 'Fully Vax/100', 'Daily/Million']
    plt.xticks(range(len(labels)), labels, rotation=45, ha='right')
    plt.yticks(range(len(labels)), labels)
    for i in range(len(labels)):
        for j in range(len(labels)):
            plt.text(j, i, f'{corr.iloc[i,j]:.2f}',
                    ha='center', va='center', fontweight='bold',
                    color='white' if abs(corr.iloc[i,j]) > 0.5 else 'black')
    plt.title('Vaccination Metrics Correlation Matrix',
              fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('screenshots/correlation_matrix.png', dpi=150)
    plt.show()
    print("✅ Chart 4 saved!")

def generate_report(results, countries):
    """Generate statistical analysis report"""
    report = []
    report.append("=" * 55)
    report.append("COVID VACCINATION STATISTICAL REPORT")
    report.append("Analyst: Prajwal Kondala | IIT Kharagpur")
    report.append("Data: COVID World Vaccination Progress (Kaggle)")
    report.append("=" * 55)

    for country in countries:
        r = results[country]
        report.append(f"\n{country}")
        report.append("-" * 30)
        report.append(f"Total Vaccinations: {r['total']:,.0f}")
        report.append(f"Mean Daily:         {r['mean_daily']:,.0f}")
        report.append(f"Max Single Day:     {r['max_daily']:,.0f}")
        report.append(f"Std Deviation:      {r['std_daily']:,.0f}")
        report.append(f"Fully Vaccinated:   {r['fully_vaccinated']:.1f}%")

    with open('statistical_report.txt', 'w') as f:
        f.write("\n".join(report))
    print("✅ Statistical report saved!")

if __name__ == "__main__":
    # Configuration
    FOCUS_COUNTRIES = ['India', 'United States', 'United Kingdom',
                       'Brazil', 'Germany']
    COLORS = ['steelblue', 'crimson', 'forestgreen', 'darkorange', 'purple']

    print("=" * 55)
    print("COVID-19 VACCINATION ANALYSIS")
    print("=" * 55)

    # Load and clean data
    print("\nLoading data...")
    df = load_data('data/country_vaccinations.csv')
    df_focus = clean_data(df, FOCUS_COUNTRIES)
    print(f"✅ Loaded {len(df):,} rows across {df['country'].nunique()} countries")

    # Statistical analysis
    print("\nRunning statistical analysis...")
    results = statistical_analysis(df_focus, FOCUS_COUNTRIES)

    # Generate visualizations
    print("\nGenerating charts...")
    plot_daily_trend(df_focus, FOCUS_COUNTRIES, COLORS)
    plot_total_vaccinations(df_focus, FOCUS_COUNTRIES, COLORS)
    plot_vaccination_percentage(df_focus, FOCUS_COUNTRIES, COLORS)
    plot_correlation_heatmap(df_focus, FOCUS_COUNTRIES)

    # Generate report
    generate_report(results, FOCUS_COUNTRIES)

    print("\n" + "=" * 55)
    print("ANALYSIS COMPLETE!")
    print("=" * 55)
    print("\nKey Findings:")
    for country in FOCUS_COUNTRIES:
        r = results[country]
        print(f"  {country}: {r['total']/1e6:.0f}M doses | {r['fully_vaccinated']:.1f}% fully vaccinated")
