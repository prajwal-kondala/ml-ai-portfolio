# COVID-19 Vaccination Analysis

## 📊 Project Overview
A Python-based data analysis tool to study global COVID-19 vaccination progress across major countries. This project analyzes real-world vaccination data to uncover patterns, compare country performance, and derive meaningful public health insights using statistical analysis and visualizations.

## 🎯 Problem Statement
During the COVID-19 pandemic, vaccination was the primary tool to control the spread of the virus. However, vaccination progress varied significantly across countries due to population size, healthcare infrastructure, and vaccine availability. This project answers key questions:
- Which countries vaccinated the most people in absolute numbers?
- Which countries achieved the highest vaccination coverage relative to population?
- How consistent was the daily vaccination rate across countries?
- What is the correlation between different vaccination metrics?

## ✨ Features
- ✅ Load and explore real-world vaccination dataset (86,512 rows × 15 columns)
- ✅ Data cleaning — handling 45,000+ missing values professionally
- ✅ Statistical analysis per country (mean, max, std deviation)
- ✅ Country comparison — India, USA, UK, Brazil, Germany
- ✅ Daily vaccination trend analysis
- ✅ Population-adjusted vaccination percentage comparison
- ✅ Correlation analysis between vaccination metrics
- ✅ Professional visualizations (4 charts)
- ✅ Automated statistical report generation

## 🛠️ Tech Stack
- **Language:** Python 3.x
- **Libraries:**
  - `numpy` — Statistical calculations (mean, std, correlation)
  - `pandas` — Data loading, cleaning, filtering (86K+ rows)
  - `matplotlib` — Professional visualizations

## 📁 Project Structure
```
02-covid-vaccination-analysis/
├── data/
│   └── country_vaccinations.csv    # COVID vaccination dataset (Kaggle)
├── screenshots/
│   ├── daily_vaccinations.png      # Daily trend comparison
│   ├── total_vaccinations.png      # Total doses by country
│   ├── vaccination_percentage.png  # % population vaccinated
│   └── correlation_matrix.png      # Metric correlations heatmap
├── analyzer.py                      # Main analysis script
├── statistical_report.txt           # Generated statistical report
└── README.md                        # Project documentation
```

## 📦 Dataset
- **Source:** [COVID World Vaccination Progress — Kaggle](https://www.kaggle.com/datasets/gpreda/covid-world-vaccination-progress)
- **Author:** Gabriel Preda
- **Size:** 86,512 rows × 15 columns
- **Coverage:** 223 countries
- **Key Columns:** country, date, total_vaccinations, people_vaccinated, people_fully_vaccinated, daily_vaccinations, total_vaccinations_per_hundred

## 🚀 How to Run

### Prerequisites
```bash
pip install numpy pandas matplotlib
```

### Execute Analysis
```bash
# Navigate to project directory
cd 02-covid-vaccination-analysis

# Run the analyzer
python analyzer.py
```

The script will:
1. Load vaccination data from `data/country_vaccinations.csv`
2. Clean and filter data for 5 focus countries
3. Perform statistical analysis per country
4. Generate 4 professional visualizations
5. Create `statistical_report.txt` with findings

## 📊 Sample Output

### Statistical Summary
```
India:
  Total Vaccinations: 1,835,000,000
  Mean Daily:         4,200,000
  Max Single Day:     10,037,995
  Std Deviation:      2,100,000
  Fully Vaccinated:   67.2%

United States:
  Total Vaccinations: 670,000,000
  Mean Daily:         1,100,000
  Max Single Day:     4,600,000
  Std Deviation:      890,000
  Fully Vaccinated:   69.5%
```

## 📈 Key Insights
1. **India leads in absolute numbers** — 1,835M total doses administered, highest among all analyzed countries due to world's largest vaccination drive
2. **Germany leads in coverage** — Highest percentage of population fully vaccinated among focus countries, reflecting strong healthcare infrastructure
3. **India's single-day record** — 10 million vaccinations in a single day, reflecting India's massive vaccination campaign capacity
4. **High correlation** — All vaccination metrics show strong positive correlation (>0.95), meaning countries that vaccinate more people also maintain higher daily rates
5. **Consistent vs Inconsistent** — India showed highest std deviation in daily vaccinations, indicating massive surge days, while Germany showed more consistent daily rates

## 🎓 What I Learned
- **Real-world data handling** — Working with 86,512 rows and 45,000+ missing values
- **Pandas fundamentals** — Loading, filtering, groupby, and aggregating large datasets
- **Statistical thinking** — Using mean, std deviation to compare country consistency
- **Correlation analysis** — Understanding relationships between vaccination metrics
- **Data storytelling** — Converting raw numbers into meaningful public health insights
- **Population bias** — Understanding why absolute numbers vs per-hundred comparisons tell different stories

## 💡 Technical Highlights
- Handled 45,000+ missing values using domain knowledge (fillna with 0 for cumulative metrics)
- Used `groupby` to aggregate 86K rows into country-level statistics
- Applied `dropna().values` to ensure accurate NumPy calculations on Pandas columns
- Created correlation heatmap using matplotlib's `imshow` with custom color mapping
- Used `value_counts()` to analyze data distribution across 223 countries

## 🔮 Future Enhancements
- [ ] Add COVID cases and deaths data for complete pandemic analysis
- [ ] Vaccination vs Death rate correlation analysis
- [ ] Interactive Plotly dashboard for real-time exploration
- [ ] Predictive modeling — forecast vaccination completion dates
- [ ] Expand to all 223 countries with regional clustering
- [ ] Web scraping for latest vaccination data

## 🎯 Use Cases
- **Public Health** — Track vaccination progress and identify underperforming regions
- **Policy Making** — Data-driven insights for vaccination campaign planning
- **Research** — Statistical foundation for epidemiological studies
- **Awareness** — Communicate vaccination progress to general public

## 👤 Author
**Prajwal Kondala**
B.Tech, IIT Kharagpur
Aspiring Data Scientist & ML Engineer

- GitHub: [@prajwal-kondala](https://github.com/prajwal-kondala)
- Portfolio: [ml-ai-portfolio](https://github.com/prajwal-kondala/ml-ai-portfolio)

## 📝 Project Details
- **Created:** February 2026
- **Duration:** 2 days (Feb 26-27, 2026)
- **Part of:** Data Science & ML Learning Journey (Feb-Sep 2026)
- **Project Type:** Portfolio Project #2 of 22
- **Data Source:** Kaggle — COVID World Vaccination Progress

---
*Week 2 Portfolio Project | Data Science Foundation Phase*
