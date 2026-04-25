import streamlit as st
import numpy as np
import pickle
import os
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

# =============================================
# Page Config
# =============================================
st.set_page_config(
    page_title="Retail Demand Predictor",
    page_icon="🛒",
    layout="wide"
)

# =============================================
# Load Model — Streamlit Rule 5!
# =============================================
@st.cache_resource
def load_model():
    model_path  = os.path.join(os.path.dirname(__file__),
                               "model.pkl")
    scaler_path = os.path.join(os.path.dirname(__file__),
                               "scaler.pkl")
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)
    return model, scaler

model, scaler = load_model()

# =============================================
# Header
# =============================================
st.title("🛒 Retail Demand Prediction Engine")
st.markdown("""
> *"How much will this Rossmann store sell on a given day?"*

**Linear Regression Baseline Model** | Project 09 of 22  
*Prajwal Kondala | IIT KGP → AI/ML Engineer | April 2026*
""")
st.divider()

# =============================================
# Sidebar
# =============================================
with st.sidebar:
    st.header("📊 Model Performance")
    st.metric("R² Score", "0.1951")
    st.metric("RMSE", "€2,787")
    st.metric("Training Rows", "675,470")
    st.metric("Features", "16")

    st.divider()
    st.markdown("### 🔑 Key Insights")
    st.markdown("""
    - 🎯 **Promo** → +€1,117 sales/day
    - 📅 **Monday** → highest sales day
    - 🏫 **School holidays** → boost sales
    - 🏪 **Competition** → nearby = lower sales
    - 💰 **Month-end** → spending spike!
    - 📈 **Sales growing** year on year
    """)

    st.divider()
    st.markdown("### ℹ️ About")
    st.markdown("""
    **Dataset:** Rossmann Store Sales  
    **Source:** Kaggle Competition  
    **Stores:** 1,115 German stores  
    **Method:** Linear Regression  
    **Note:** Baseline linear model on  
    complex retail demand data.  
    Potential next upgrade:  
    Tree-based models such as XGBoost.
    """)

# =============================================
# Main Layout
# =============================================
col1, col2 = st.columns([1, 1])

with col1:
    st.header("🏪 Store & Date Details")

    store_id = st.slider("Store ID", 1, 1115, 1,
                         help="Rossmann has 1115 stores!")

    day_of_week = st.selectbox(
        "Day of Week",
        options=[1, 2, 3, 4, 5, 6, 7],
        format_func=lambda x: {
            1: '🟢 Monday (Highest Sales!)',
            2: '🔵 Tuesday',
            3: '🔵 Wednesday',
            4: '🔵 Thursday',
            5: '🔵 Friday',
            6: '🔴 Saturday (Lowest!)',
            7: '🔵 Sunday'
        }[x]
    )

    promo = st.selectbox(
        "Promotion Running?",
        options=[0, 1],
        format_func=lambda x:
        '❌ No Promotion' if x == 0 else '✅ Promotion Active! (+€1,117)'
    )

    st.markdown("---")
    st.markdown("**📅 Date Details**")

    col1a, col1b = st.columns(2)
    with col1a:
        year  = st.selectbox("Year", [2013, 2014, 2015])
        month = st.slider("Month", 1, 12, 6)
    with col1b:
        day   = st.slider("Day", 1, 31, 15)
        week_of_year = st.slider("Week of Year", 1, 52, 26)

    is_weekend     = 1 if day_of_week >= 6 else 0
    is_month_start = 1 if day == 1 else 0
    is_month_end   = 1 if day >= 28 else 0

    st.markdown("---")
    st.markdown("**🏬 Store Details**")

    store_type = st.selectbox(
        "Store Type",
        options=[1, 2, 3, 4],
        format_func=lambda x:
        ['Type A', 'Type B', 'Type C', 'Type D'][x-1]
    )

    assortment = st.selectbox(
        "Assortment Level",
        options=[1, 2, 3],
        format_func=lambda x:
        ['Basic', 'Extra', 'Extended'][x-1]
    )

    competition_distance = st.slider(
        "Competition Distance (meters)",
        0, 30000, 5000, step=100,
        help="Distance to nearest competitor store"
    )

    promo2 = st.selectbox(
        "Ongoing Promo2?",
        options=[0, 1],
        format_func=lambda x:
        'No' if x == 0 else 'Yes'
    )

    state_holiday = st.selectbox(
        "State Holiday?",
        options=[0, 1, 2, 3],
        format_func=lambda x:
        ['None', 'Public Holiday',
         'Easter Holiday', 'Christmas'][x]
    )

    school_holiday = st.selectbox(
        "School Holiday?",
        options=[0, 1],
        format_func=lambda x:
        'No' if x == 0 else 'Yes (boosts sales!)'
    )

with col2:
    st.header("🎯 Prediction")

    # Prepare features
    input_features = np.array([[
        store_id, day_of_week, promo,
        state_holiday, school_holiday,
        store_type, assortment,
        competition_distance, promo2,
        year, month, day, week_of_year,
        is_weekend, is_month_start, is_month_end
    ]])

    # Scale and predict
    input_scaled = scaler.transform(input_features)
    prediction   = model.predict(input_scaled)[0]
    prediction   = max(0, prediction)

    # Big metric
    st.metric(
        label="📦 Predicted Daily Sales",
        value=f"€{prediction:,.0f}",
    )

    # Performance category
    if prediction < 3000:
        perf = "🔴 Low Sales Day"
    elif prediction < 6000:
        perf = "🟡 Below Average"
    elif prediction < 8000:
        perf = "🟢 Good Sales Day"
    elif prediction < 12000:
        perf = "🔥 Strong Sales Day!"
    else:
        perf = "💥 Exceptional Day!"

    st.markdown(f"**Performance:** {perf}")

    st.divider()

    # Context metrics
    col2a, col2b, col2c = st.columns(3)
    with col2a:
        st.metric("Weekend", "Yes" if is_weekend else "No")
    with col2b:
        st.metric("Promo Active", "Yes 🎉" if promo else "No")
    with col2c:
        est_customers = max(0, int(prediction / 9))
        st.metric("Est. Customers", f"~{est_customers:,}")

    st.divider()

    # Feature importance chart
    st.subheader("📈 What Drives Sales?")

    feature_names = [
        'Store', 'DayOfWeek', 'Promo', 'StateHoliday',
        'SchoolHoliday', 'StoreType', 'Assortment',
        'CompetitionDist', 'Promo2', 'Year', 'Month',
        'Day', 'WeekOfYear', 'IsWeekend',
        'IsMonthStart', 'IsMonthEnd'
    ]
    coefficients = model.coef_

    fig, ax = plt.subplots(figsize=(8, 5))
    colors = ['#2ecc71' if c > 0 else '#e74c3c'
              for c in coefficients]
    ax.barh(feature_names, coefficients,
            color=colors, alpha=0.8, edgecolor='black',
            linewidth=0.5)
    ax.axvline(x=0, color='black', linewidth=1.5)
    ax.set_title('Feature Coefficients\n'
                 'Green = boosts sales | Red = reduces sales',
                 fontsize=11)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig)

# =============================================
# Bottom — Business Insights
# =============================================
st.divider()
st.header("💡 Business Insights Discovered")

col3, col4, col5 = st.columns(3)

with col3:
    st.markdown("""
    **📢 Promotions**
    - Special Promo → **+€1,117/day**
    - Promo2 shows lower coefficient in this baseline model
    - Promotional strategies may differ by store
    - Requires deeper modeling for causal interpretation
    """)

with col4:
    st.markdown("""
    **📅 Timing Patterns**
    - Monday = highest sales day
    - Saturday = lowest sales day
    - Month-end = spending spike!
    - School holidays boost sales
    - Sales growing year on year 📈
    """)

with col5:
    st.markdown("""
    **🏪 Store Factors**
    - Closer competitor = lower sales
    - Wider assortment = more sales
    - Extended assortment stores win!
    - Store type affects performance
    - 1,115 stores across Germany
    """)

st.divider()

# =============================================
# Model Details — Tabs
# =============================================
st.header("🔬 Model Details")

tab1, tab2, tab3 = st.tabs([
    "📊 Performance",
    "🔧 Methodology",
    "🚀 Future Improvements"
])

with tab1:
    st.markdown("""
    | Method | R² | RMSE |
    |--------|-----|------|
    | NumPy Scratch (Gradient Descent) | 0.1943 | €2,788 |
    | sklearn Linear Regression | 0.1951 | €2,787 |

    **R² = 0.1951** means this baseline linear model explains
    ~20% of sales variation in a complex retail dataset.

    Retail demand involves non-linear interactions between
    promotions, seasonality, store type, and competition
    that linear regression cannot fully capture.
    """)

with tab2:
    st.markdown("""
    **Pipeline:**
    1. Load Rossmann Store Sales (844K rows!)
    2. Merge train + store data
    3. Feature engineering (16 features!)
    4. Date features: Year, Month, IsWeekend...
    5. Encode: StoreType, Assortment
    6. Train/Test Split (80/20, seed=42)
    7. StandardScaler
    8. Linear Regression from NumPy scratch
    9. Compare with sklearn Linear Regression
    10. Both give near-identical results! ✅
    """)

with tab3:
    st.markdown("""
    **This is a BASELINE model.**

    Future improvements being explored:

    - 🌲 Try tree-based models (Random Forest / XGBoost)
    - 📊 Add richer feature engineering
    - 🚀 Deploy with FastAPI
    - 🏆 Extend into advanced ML capstone
    """)

# =============================================
# Footer
# =============================================
st.divider()
st.markdown("""
*Project 09 of 22 | Phase 2: Machine Learning*  
*Prajwal Kondala | IIT KGP → AI/ML Engineer | April 2026*  
*Dataset: Rossmann Store Sales — Kaggle Competition*  
*Baseline model built. Future upgrades may include tree-based models and richer features.*
""")