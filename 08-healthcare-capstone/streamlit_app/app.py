import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="Healthcare Analytics Dashboard",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Heart Disease Analytics Dashboard")
st.markdown("""
**Prajwal Kondala | IIT Kharagpur | DS/AI Portfolio — Project 08**

*Analysis of Cleveland Heart Disease Dataset (302 patients, 1988)*
""")

@st.cache_data
def load_data():
    df = pd.read_csv("08-healthcare-capstone/streamlit_app/heart_disease_cleaned.csv")
    categorical_cols = ["sex", "cp", "fbs", "restecg",
                        "exang", "slope", "ca", "thal", "target"]
    for col in categorical_cols:
        df[col] = df[col].astype("category")
    df["age_group"] = pd.cut(df["age"], bins=[0,40,50,60,100],
        labels=["Young (<40)","Middle (40-50)",
                "Senior (50-60)","Elderly (60+)"])
    conditions = [df["chol"]<200,
                  (df["chol"]>=200)&(df["chol"]<240),
                  df["chol"]>=240]
    df["chol_risk"] = np.select(conditions,
        ["Normal","Borderline High","High Risk"])
    df["high_hr"] = np.where(df["thalach"] > 150, 1, 0)
    df["oldpeak_log"] = np.log1p(df["oldpeak"])
    return df

df = load_data()

# Sidebar
st.sidebar.title("🔍 Filters")
st.sidebar.markdown("---")

age_range = st.sidebar.slider(
    "Age Range",
    int(df["age"].min()),
    int(df["age"].max()),
    (int(df["age"].min()), int(df["age"].max()))
)

gender_options = st.sidebar.multiselect(
    "Gender",
    options=[0, 1],
    default=[0, 1],
    format_func=lambda x: "Male" if x == 1 else "Female"
)

target_options = st.sidebar.multiselect(
    "Disease Status",
    options=[0, 1],
    default=[0, 1],
    format_func=lambda x: "Disease" if x == 1 else "No Disease"
)

# Filter
filtered_df = df[
    (df["age"].between(age_range[0], age_range[1])) &
    (df["sex"].astype(int).isin(gender_options)) &
    (df["target"].astype(int).isin(target_options))
]

# KPI Metrics
st.markdown("### 📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Patients", len(filtered_df))
with col2:
    disease_rate = (filtered_df["target"].astype(int)==1).mean()*100
    st.metric("Disease Rate", f"{disease_rate:.1f}%")
with col3:
    st.metric("Avg Age", f"{filtered_df['age'].mean():.1f} yrs")
with col4:
    st.metric("Avg Cholesterol", f"{filtered_df['chol'].mean():.0f} mg/dl")

st.divider()

# Row 1
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📈 Age Distribution by Disease Status")
    fig1 = px.histogram(
        filtered_df, x="age", color="target",
        nbins=20, barmode="overlay", opacity=0.7,
        color_discrete_map={0:"steelblue", 1:"crimson"},
        labels={"target":"Heart Disease","age":"Age (years)"}
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("### 💔 Chest Pain Type vs Disease")
    cp_data = filtered_df.groupby(
        ["cp","target"], observed=True
    ).size().reset_index(name="count")
    fig2 = px.bar(
        cp_data, x="cp", y="count", color="target",
        barmode="group",
        color_discrete_map={0:"steelblue", 1:"crimson"},
        labels={"cp":"Chest Pain Type (0-3)",
                "target":"Heart Disease"}
    )
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# Row 2
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🫀 Age vs Max Heart Rate")
    fig3 = px.scatter(
        filtered_df, x="age", y="thalach",
        color="target", size="chol",
        color_discrete_map={0:"steelblue", 1:"crimson"},
        labels={"age":"Age (years)",
                "thalach":"Max Heart Rate (bpm)",
                "target":"Heart Disease"},
        height=400
    )
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.markdown("### 🧪 Cholesterol Distribution")
    fig4 = px.histogram(
        filtered_df, x="chol", color="target",
        nbins=25, barmode="overlay", opacity=0.7,
        color_discrete_map={0:"steelblue", 1:"crimson"},
        labels={"chol":"Cholesterol (mg/dl)",
                "target":"Heart Disease"},
        height=400
    )
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

# Hypothesis Results
st.markdown("### 📋 Statistical Hypothesis Test Results")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **Test 1: Age vs Disease**
    - Test: Independent t-test
    - p-value: **0.0001**
    - Result: ✅ SIGNIFICANT
    - Disease: 52.59 vs 56.60 yrs
    """)

with col2:
    st.markdown("""
    **Test 2: Gender vs Disease**
    - Test: Chi-square test
    - p-value: **0.0000**
    - Result: ✅ SIGNIFICANT
    - Females: 75% vs Males: 44.7%
    """)

with col3:
    st.markdown("""
    **Test 3: Heart Rate vs Disease**
    - Test: Independent t-test
    - p-value: **0.0000**
    - Result: ✅ SIGNIFICANT
    - Disease: 158 vs 139 bpm
    """)

st.divider()

# Key Insights
st.markdown("### 💡 Key Insights")
st.info("""
**Counterintuitive Findings:**

1. 🔴 Younger patients show higher disease rate — Middle age (40-50): 69.7%!
2. 🔴 Females show higher disease rate (75% vs 44.7%) — selection bias!
3. 🔴 High cholesterol does NOT mean more disease!
4. ✅ Max heart rate is strongest predictor (t=8.01, p≈0.0000)!
5. ✅ Non-anginal chest pain (cp=2) most associated with disease!
""")

st.divider()

if st.checkbox("📄 Show Raw Data"):
    st.dataframe(filtered_df, use_container_width=True)

st.markdown("---")
st.markdown("""
*Project 08 — Healthcare Data Analytics Pipeline*
*Prajwal Kondala | IIT Kharagpur | April 2026*
*IIT KGP → AI/ML Engineer 🎯*
""")
