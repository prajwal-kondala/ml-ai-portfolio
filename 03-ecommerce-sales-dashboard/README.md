# E-Commerce Sales Dashboard

## 📊 Project Overview
A comprehensive Python-based e-commerce sales analysis tool that processes over 1 million real-world transactions to uncover revenue patterns, identify top performing products, analyze customer segments, and generate professional business reports. Built with a modular, production-style code architecture.

## 🎯 Problem Statement
E-commerce businesses generate massive amounts of transaction data daily. Without proper analysis, this data is just numbers. This project answers critical business questions:
- Which products generate the most revenue?
- Which countries are the best international markets?
- What is the seasonal pattern of sales?
- Which day of the week drives the most revenue?
- How are customers segmented by their purchase value?
- What percentage of customers are high value vs low value?

## ✨ Features
- ✅ Load and process 1,000,000+ real transaction records
- ✅ Professional data cleaning pipeline (cancelled orders, negatives, missing values)
- ✅ Feature engineering (Revenue column, date parts extraction)
- ✅ Split into Sales and Customer DataFrames (mimics real database design!)
- ✅ Statistical analysis with business insights
- ✅ 6 professional visualizations including dashboard
- ✅ Customer segmentation (High/Medium/Low Value)
- ✅ Day of week revenue analysis
- ✅ PDF report generation (NEW!)
- ✅ Modular code architecture (src/ folder with separate modules)

## 🛠️ Tech Stack
- **Language:** Python 3.x
- **Libraries:**
  - `numpy` — Statistical calculations
  - `pandas` — Data loading, cleaning, transformation (1M+ rows!)
  - `matplotlib` — Professional visualizations and dashboard
  - `reportlab` — PDF report generation (NEW!)

## 📁 Project Structure
```
03-ecommerce-sales-dashboard/
├── data/
│   └── sales_data.csv              # Online Retail II UCI dataset
├── screenshots/
│   ├── monthly_revenue.png         # Revenue trend 2009-2011
│   ├── top_products.png            # Top 10 products by revenue
│   ├── country_sales.png           # Top countries (ex UK)
│   ├── day_analysis.png            # Revenue by day of week
│   ├── customer_segments.png       # Customer segmentation pie
│   └── dashboard.png               # Complete dashboard view
├── src/
│   ├── data_processor.py           # Data loading, cleaning, engineering
│   └── visualizer.py               # All chart generation functions
├── dashboard.py                    # Main execution script
├── sales_report.pdf                # Generated PDF report (NEW!)
├── .gitignore                      # Git ignore file
└── README.md                       # Project documentation
```

## 📦 Dataset
- **Source:** [Online Retail II UCI — Kaggle](https://www.kaggle.com/datasets/mashlyn/online-retail-ii-uci)
- **Size:** 1,067,371 rows × 8 columns (RAW)
- **After Cleaning:** 1,041,670 rows × 9 columns
- **Coverage:** 41 countries, 2009-2011
- **Key Columns:** Invoice, StockCode, Description, Quantity, InvoiceDate, Price, Customer ID, Country

## 🚀 How to Run

### Prerequisites
```bash
pip install numpy pandas matplotlib reportlab
```

### Execute Dashboard
```bash
# Navigate to project directory
cd 03-ecommerce-sales-dashboard

# Run main dashboard
python dashboard.py
```

The script will:
1. Load 1M+ transaction records
2. Clean and filter data professionally
3. Engineer features (Revenue, date parts)
4. Split into Sales and Customer DataFrames
5. Generate 6 professional visualizations
6. Create complete dashboard PNG
7. Generate PDF sales report

## 📊 Sample Output

### Statistical Summary
```
Total Transactions:  1,041,670
Total Revenue:       £20,972,594.57
Avg Order Value:     £20.13
Median Order Value:  £9.96
Std Deviation:       £203.12
Unique Products:     5,399
Unique Customers:    5,878
Countries:           41
```

## 📈 Key Business Insights

1. **Christmas Seasonality** — Two massive revenue spikes in November/December each year. Classic retail pattern — businesses must stock up 2 months ahead!

2. **Ireland is #1 International Market** — EIRE (Ireland) leads all non-UK countries. Geographic proximity and cultural similarity drive cross-border sales.

3. **Thursday is Peak Revenue Day** — Highest revenue consistently on Thursdays. Likely wholesale buyers placing weekly orders before weekend retail.

4. **Regency Cakestand 3 Tier** — Top revenue generating product. Premium home décor items dominate top 10 — suggests affluent customer base.

5. **Pareto Principle in Action** — Only 11.4% of customers are High Value (≥£5000) but they drive majority of revenue. Retaining these VIP customers is critical!

6. **Mean vs Median Story** — Mean order = £20.13 but Median = £9.96. Large wholesale orders pull mean up — median tells the true typical order story!

## 🎓 What I Learned
- **1M+ row processing** — Handling dataset 12x larger than Project 2
- **Modular code architecture** — Separating concerns into src/ modules
- **PDF generation** — Using reportlab for professional reports
- **Feature engineering** — Creating Revenue column, extracting date parts
- **Customer segmentation** — Applying business logic with df.apply()
- **Dashboard design** — Using gridspec for multi-chart layouts
- **Data splitting** — Mimicking real database design (Sales + Customer tables)
- **RAM management** — Handling large datasets in Colab environment

## 💡 Technical Highlights
- Used `str.startswith('C')` to detect and remove cancelled orders (25,701 removed!)
- Applied `dt.to_period('M')` for year-month grouping across 2 years
- Used `gridspec` for professional dashboard layout (5 charts in one figure!)
- Installed `reportlab` via pip for PDF generation — first external library install!
- Split single CSV into Sales and Customer DataFrames — mimics real DB design
- Used conditional color mapping in bar chart (crimson for peak day!)
- `!pip install` syntax in Colab for library installation

## 🔮 Future Enhancements
- [ ] Interactive Plotly dashboard for real-time filtering
- [ ] RFM Analysis (Recency, Frequency, Monetary) for advanced segmentation
- [ ] Product recommendation system using association rules
- [ ] Forecasting next month revenue using time series analysis
- [ ] Geographic heatmap of international sales
- [ ] Customer churn prediction model

## 🎯 Use Cases
- **Retail Analytics** — Understanding sales patterns for inventory planning
- **Marketing** — Identifying high value customers for targeted campaigns
- **Operations** — Staffing and logistics planning based on peak days
- **Strategy** — International expansion decisions based on country performance
- **Finance** — Revenue forecasting based on seasonal patterns

## 👤 Author
**Prajwal Kondala**
B.Tech, IIT Kharagpur
Aspiring Data Scientist & ML Engineer

- GitHub: [@prajwal-kondala](https://github.com/prajwal-kondala)
- Portfolio: [ml-ai-portfolio](https://github.com/prajwal-kondala/ml-ai-portfolio)

## 📝 Project Details
- **Created:** March 2026
- **Duration:** 1 day (Mar 4, 2026)
- **Part of:** Data Science & ML Learning Journey (Feb-Sep 2026)
- **Project Type:** Portfolio Project #3 of 22
- **Data Source:** Kaggle — Online Retail II UCI

## 📊 Growth from Project 2
| Feature | Project 2 | Project 3 |
|---------|-----------|-----------|
| Dataset Size | 86,512 rows | 1,041,670 rows |
| Charts | 4 | 6 |
| Report Format | .txt | .pdf (NEW!) |
| Code Files | 1 | 3 (modular!) |
| New Libraries | - | reportlab |
| Architecture | Single file | src/ modules |
| Analysis Type | Statistical | Business insights |

---
*Week 3 Portfolio Project | Data Science Foundation Phase*
