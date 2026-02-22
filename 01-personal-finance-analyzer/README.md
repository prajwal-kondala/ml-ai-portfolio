# Personal Finance Analyzer

## 📊 Project Overview
A Python-based tool to analyze personal bank transactions, categorize spending, and generate detailed financial reports with visualizations.

## 🎯 Problem Statement
Managing personal finances is challenging without proper tracking. People often lose track of where their money goes each month. This tool helps analyze spending patterns, identify top expenses, and make informed financial decisions.

## ✨ Features
- ✅ Load transactions from CSV files
- ✅ Categorize spending automatically (Food, Transport, Shopping, Healthcare, Utilities, Entertainment)
- ✅ Generate comprehensive spending analysis
- ✅ Calculate category-wise spending breakdown with percentages
- ✅ Identify top 5 highest transactions
- ✅ Monthly spending trend analysis
- ✅ Create data visualizations (bar charts, line graphs, pie charts)
- ✅ Export detailed financial reports in text format

## 🛠️ Tech Stack
- **Language:** Python 3.x
- **Libraries:** 
  - `csv` - Transaction data loading and processing
  - `matplotlib` - Data visualization and chart generation
  - `collections.defaultdict` - Efficient data aggregation

## 📁 Project Structure
```
01-personal-finance-analyzer/
├── data/
│   └── transactions.csv          # Bank transaction data
├── screenshots/
│   ├── category_spending.png     # Category breakdown chart
│   ├── monthly_trend.png         # Monthly spending trend
│   └── category_pie.png          # Spending distribution
├── analyzer.py                    # Main analysis script
├── financial_report.txt           # Generated analysis report
└── README.md                      # Project documentation
```

## 🚀 How to Run

### Prerequisites
```bash
pip install matplotlib
```

### Execute Analysis
```bash
# Navigate to project directory
cd 01-personal-finance-analyzer

# Run the analyzer
python analyzer.py
```

The script will:
1. Load transactions from `data/transactions.csv`
2. Perform comprehensive spending analysis
3. Generate visualizations
4. Create `financial_report.txt`

## 📊 Sample Output

### Spending Summary
```
Total Transactions: 20
Total Spending: ₹26,249.00
Average Transaction: ₹1,312.45
```

### Category Breakdown
```
Food           ₹10,600  (40.4%)
Shopping        ₹7,500  (28.6%)
Healthcare      ₹3,200  (12.2%)
Transport       ₹3,050  (11.6%)
Utilities       ₹2,300   (8.8%)
Entertainment     ₹999   (3.8%)
```

### Monthly Analysis
```
2026-01: ₹15,549
2026-02: ₹10,700
```

## 📈 Key Insights from Sample Data
1. **Food expenses** dominate spending at 40.4% of total budget
2. Average monthly spending: ₹13,124
3. Top single transaction: Electronics purchase at ₹3,500
4. February spending decreased by 31% compared to January
5. Transport and utilities combined account for 20.4% of expenses

## 🎓 What I Learned
- **CSV data processing**: Reading and parsing structured financial data
- **Data aggregation**: Using defaultdict for efficient category-wise calculations
- **Data visualization**: Creating professional charts with Matplotlib
- **Code organization**: Structuring code into reusable, maintainable functions
- **Report generation**: Automating financial report creation
- **Error handling**: Building robust file I/O operations

## 💡 Technical Highlights
- Efficient data processing using dictionary comprehensions
- Lambda functions for sorting and filtering transactions
- Statistical calculations (totals, averages, percentages)
- Multiple visualization types (bar, line, pie charts)
- Clean, readable code with proper documentation

## 🔮 Future Enhancements
- [ ] Budget tracking with monthly limits and alerts
- [ ] Expense prediction using Linear Regression
- [ ] Comparison with previous months/years
- [ ] Export to Excel with formatted sheets
- [ ] Web dashboard using Streamlit
- [ ] Receipt scanning with OCR (Optical Character Recognition)
- [ ] Integration with bank APIs for automatic transaction import
- [ ] Multi-currency support

## 🎯 Use Cases
- **Personal Finance**: Track daily expenses and monthly budgets
- **Small Business**: Monitor business expenses and cash flow
- **Financial Planning**: Identify spending patterns for better savings
- **Tax Preparation**: Categorize expenses for tax documentation

## 👤 Author
**Prajwal Kondala**  
B.Tech, IIT Kharagpur  
Aspiring Data Scientist & ML Engineer

- GitHub: [@prajwal-kondala](https://github.com/prajwal-kondala)
- Portfolio: [ml-ai-portfolio](https://github.com/prajwal-kondala/ml-ai-portfolio)

## 📝 Project Details
- **Created:** February 2026
- **Duration:** 3 days (Feb 20-22, 2026)
- **Part of:** Data Science & ML Learning Journey (Feb-Sep 2026)
- **Project Type:** Portfolio Project #1 of 22

## 🙏 Acknowledgments
This project is part of my structured roadmap to transition into Data Science and Machine Learning roles, with a target of securing a Data Scientist position by September-October 2026.

---

*Week 1 Portfolio Project | Data Science Foundation Phase*
