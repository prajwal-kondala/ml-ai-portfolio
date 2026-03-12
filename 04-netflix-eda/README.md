# Netflix Content Analysis — EDA Dashboard

## 📊 Project Overview
A comprehensive Python-based Exploratory Data Analysis (EDA) project on Netflix's complete content library of 8,800+ titles. This project applies the full 6-step EDA framework — from data understanding to business insights — using advanced statistical analysis, Seaborn visualizations, and hypothesis testing to uncover Netflix's content strategy, growth patterns, and audience targeting.

## 🎯 Problem Statement
Netflix hosts thousands of movies and TV shows globally, but what drives their content strategy? This project answers critical business questions:
- Does Netflix focus more on Movies or TV Shows?
- Which countries produce the most Netflix content?
- How has Netflix's content library grown over the years?
- What ratings and genres dominate Netflix?
- When does Netflix strategically add content?
- Do Movies and TV Shows differ significantly in release year?
- What is the typical Netflix movie duration?
- How many seasons do most Netflix TV Shows run?

## ✨ Features
- ✅ Load and explore real Netflix dataset (8,807 titles × 12 columns)
- ✅ Professional data cleaning pipeline (missing values, type conversion)
- ✅ Feature engineering — 4 new columns extracted (year_added, month_added, duration_value, duration_unit)
- ✅ Complete 6-step EDA framework applied systematically
- ✅ 9 professional Seaborn visualizations (Netflix themed!)
- ✅ Correlation heatmap with masked upper triangle
- ✅ Statistical analysis — skewness, distribution fingerprint
- ✅ Hypothesis testing using scipy.stats (t-test!)
- ✅ Business insights derived from every chart
- ✅ PDF report generation with Netflix branding
- ✅ requirements.txt for reproducibility (NEW!)

## 🛠️ Tech Stack
- **Language:** Python 3.x
- **Libraries:**
  - `numpy` — Statistical calculations
  - `pandas` — Data loading, cleaning, feature engineering
  - `matplotlib` — Chart layouts, multi-panel dashboards
  - `seaborn` — Advanced statistical visualizations (9 charts!)
  - `scipy.stats` — Hypothesis testing (t-test)
  - `reportlab` — PDF report generation

## 📁 Project Structure
```
04-netflix-eda/
├── data/
│   └── netflix_titles.csv          # Netflix content dataset (Kaggle)
├── notebooks/
│   └── 04_netflix_eda.ipynb        # Complete EDA notebook
├── screenshots/
│   ├── 01_content_type.png         # Movies vs TV Shows distribution
│   ├── 02_content_growth.png       # Content growth over years
│   ├── 03_top_countries.png        # Top 10 content producing countries
│   ├── 04_ratings.png              # Rating distribution
│   ├── 05_top_genres.png           # Top 10 genres
│   ├── 06_movie_duration.png       # Movie duration distribution
│   ├── 07_monthly_additions.png    # Monthly content addition pattern
│   ├── 08_tv_seasons.png           # TV Show seasons distribution
│   └── 09_correlation.png          # Correlation heatmap (masked!)
├── .gitignore                      # Git ignore file
├── requirements.txt                # Dependencies (NEW!)
├── netflix_report.pdf              # Generated PDF report
└── README.md                       # Project documentation
```

## 📦 Dataset
- **Source:** [Netflix Movies and TV Shows — Kaggle](https://www.kaggle.com/datasets/shivamb/netflix-shows)
- **Size:** 8,807 rows × 12 columns (RAW)
- **After Cleaning:** 8,804 rows × 16 columns (with engineered features)
- **Coverage:** Content added up to 2021
- **Key Columns:** type, title, director, cast, country, date_added, release_year, rating, duration, listed_in

## 🚀 How to Run

### Prerequisites
```bash
pip install -r requirements.txt
```

### Execute Analysis
```bash
# Navigate to project directory
cd 04-netflix-eda

# Open notebook
jupyter notebook notebooks/04_netflix_eda.ipynb
```

The notebook will:
1. Load Netflix dataset (8,807 titles)
2. Clean missing values professionally
3. Engineer 4 new features
4. Generate 9 Seaborn visualizations
5. Perform correlation analysis
6. Run hypothesis test
7. Generate PDF report

## 📊 Sample Output

### Dataset Overview
```
Total Titles:         8,804
Movies:               6,128 (69.6%)
TV Shows:             2,676 (30.4%)
Countries Covered:    748 unique
Release Year Range:   1925 - 2021
Avg Movie Duration:   100 minutes
Most Common Rating:   TV-MA
```

### Missing Values Treatment
```
director    → 29.91% missing → filled with 'Unknown'
cast        →  9.37% missing → filled with 'Unknown'
country     →  9.44% missing → filled with 'Unknown'
date_added  →  0.11% missing → filled with mode
rating      →  0.05% missing → filled with mode
duration    →  0.03% missing → 3 rows dropped
```

## 📈 Key Business Insights

1. **Movies Dominate Netflix** — 69.6% of all content is Movies vs 30.4% TV Shows. Netflix is primarily a movie platform, not a TV show platform!

2. **2019 Was Peak Year** — Highest content additions in 2019. Post-2019 drop confirms COVID-19 disrupted global content production significantly.

3. **USA and India Lead** — United States is #1 content producer, India is #2. Bollywood's massive output makes India a critical Netflix content partner!

4. **Adult Audience Focus** — TV-MA (Mature 17+) dominates ratings. Netflix clearly targets adult audiences — not competing with Disney+ for family content!

5. **International Movies is #1 Genre** — Beating even Dramas and Comedies! Netflix's global content strategy is working — audiences love international content!

6. **Sweet Spot Duration** — Average Netflix movie is exactly 100 minutes. Long enough to be satisfying, short enough to finish in one sitting!

7. **High Cancellation Rate** — 75%+ of TV Shows have only 1 Season. Netflix cancels most shows after Season 1 — only hits survive to Season 2!

8. **Strategic Content Timing** — July, September, and December are peak content addition months. Netflix adds content before summer, back-to-school, and holiday viewing seasons!

9. **Hypothesis Test Result** — Movies (avg release: 2013) vs TV Shows (avg release: 2016) differ significantly (p=0.000000). Netflix adds older movies but invests in recent TV Shows!

## 🎓 What I Learned
- **6-step EDA Framework** — Systematic approach: Understand → Distributions → Relationships → Outliers → Visualise → Insights
- **Feature Engineering** — Extracting year, month, duration_value from raw columns using pd.to_datetime() and str.extract()
- **pd.cut()** — Binning continuous data into meaningful categories
- **Seaborn mastery** — histplot, kdeplot, barplot, countplot, lineplot, heatmap with masked triangle
- **Hypothesis Testing** — Applied t-test using scipy.stats to statistically validate EDA findings
- **Domain Knowledge** — Making data cleaning decisions based on business context, not just statistics
- **Netflix themed visualization** — Using brand colors (#E50914) for professional presentation
- **str.split().explode()** — Handling multi-value columns like genres

## 💡 Technical Highlights
- Used `str.extract(r'(\d+)')` with raw strings to parse duration into numeric values
- Applied `np.triu()` mask to remove redundant upper triangle in correlation heatmap
- Used `.explode()` on listed_in column to analyze individual genres from comma-separated values
- Netflix brand color #E50914 used throughout for professional theming
- `pd.to_datetime().dt.year` and `.dt.month_name()` for date feature extraction
- `reindex(month_order)` to sort months chronologically in bar chart
- `scipy.stats.ttest_ind()` for hypothesis testing — p-value = 0.000000!
- Feature engineering added 4 new columns: year_added, month_added, duration_value, duration_unit

## 🔮 Future Enhancements
- [ ] Interactive Plotly dashboard for real-time filtering by genre/country
- [ ] Sentiment analysis on content descriptions using NLP
- [ ] Predict content success probability based on genre, rating, duration
- [ ] Time series forecasting — Netflix content growth prediction
- [ ] Geographic heatmap of content production by country
- [ ] Compare Netflix vs Amazon Prime vs Disney+ content strategies
- [ ] Director and cast network analysis — who collaborates most?

## 🎯 Use Cases
- **Content Strategy** — Understanding Netflix's investment priorities across genres
- **Market Analysis** — Identifying which countries Netflix targets most
- **Business Intelligence** — Seasonal patterns for content planning
- **Competitive Analysis** — Benchmarking Netflix content library composition
- **Data Science Portfolio** — Demonstrating complete EDA workflow

## 👤 Author
**Prajwal Kondala**
B.Tech, IIT Kharagpur
Aspiring Data Scientist & ML Engineer

- GitHub: [@prajwal-kondala](https://github.com/prajwal-kondala)
- Portfolio: [ml-ai-portfolio](https://github.com/prajwal-kondala/ml-ai-portfolio)

## 📝 Project Details
- **Created:** March 2026
- **Duration:** 1 day (Mar 12, 2026)
- **Part of:** Data Science & ML Learning Journey (Feb-Sep 2026)
- **Project Type:** Portfolio Project #4 of 22
- **Data Source:** Kaggle — Netflix Movies and TV Shows

## 📊 Growth from Project 3
| Feature | Project 3 | Project 4 |
|---------|-----------|-----------|
| Dataset Size | 1,041,670 rows | 8,804 rows (quality focus!) |
| Charts | 6 | 9 (Seaborn!) |
| Visualization Library | Matplotlib | Seaborn (advanced!) |
| Statistical Analysis | Basic | Skewness + Hypothesis Testing! |
| Feature Engineering | 3 features | 4 features |
| New Libraries | reportlab | seaborn, scipy |
| Analysis Type | Business dashboard | Full EDA framework |
| Hypothesis Testing | ❌ | ✅ (NEW!) |
| requirements.txt | ❌ | ✅ (NEW!) |

---
*Week 4 Portfolio Project | Data Science Foundation Phase*
