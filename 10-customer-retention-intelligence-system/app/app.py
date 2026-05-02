import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
import warnings
warnings.filterwarnings("ignore")

# =============================================
# Page Config
# =============================================
st.set_page_config(
    page_title="Customer Retention Intelligence",
    page_icon="🔮",
    layout="centered"
)

# =============================================
# Load Model — Streamlit Rule 5!
# =============================================
@st.cache_resource
def load_model():
    base = os.path.dirname(__file__)
    model_path   = os.path.join(base, 'model.pkl')
    scaler_path  = os.path.join(base, 'scaler.pkl')
    feature_path = os.path.join(base, 'feature_names.pkl')

    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)
    with open(feature_path, 'rb') as f:
        feature_names = pickle.load(f)

    return model, scaler, feature_names

model, scaler, feature_names = load_model()

# =============================================
# Sidebar — Model Info
# =============================================
with st.sidebar:
    st.header("📊 Model Info")
    st.write("**Model:** Logistic Regression")
    st.write("**Goal:** Maximize Recall (catch churners)")
    st.write("**Threshold:** 0.4")
    st.markdown("---")
    st.markdown("""
    ### 💡 Why Threshold = 0.4?
    Missing a churner = **₹5,000 lost**
    False alarm = **₹500 wasted**

    Lower threshold catches MORE churners
    even at cost of some false alarms!
    10x more expensive to miss a churner! 🎯
    """)
    st.markdown("---")
    st.markdown("""
    ### 📈 Key EDA Findings
    - Month-to-month → **43% churn!**
    - Low tenure → danger zone!
    - High charges → more churn!
    - Two year contract → safest!
    """)

# =============================================
# Header
# =============================================
st.title("🔮 Customer Retention Intelligence")
st.markdown(
    "> **Which customers are at risk of leaving next month?**"
)
st.markdown(
    "*Project 10 of 22 | Prajwal Kondala | IIT KGP → AI/ML Engineer*"
)
st.markdown("---")

# =============================================
# Input Form
# =============================================
st.subheader("📋 Enter Customer Details")

col1, col2 = st.columns(2)

with col1:
    tenure = st.slider(
        "Tenure (months)", 0, 72, 12,
        help="How long has the customer been with us?"
    )
    monthly_charges = st.slider(
        "Monthly Charges ($)", 18, 120, 65,
        help="Customer's current monthly bill"
    )
    senior_citizen = st.selectbox("Senior Citizen", ["No", "Yes"])
    partner = st.selectbox("Partner", ["No", "Yes"])
    dependents = st.selectbox("Dependents", ["No", "Yes"])
    phone_service = st.selectbox("Phone Service", ["No", "Yes"])

with col2:
    contract = st.selectbox(
        "Contract Type",
        ["Month-to-month", "One year", "Two year"],
        help="Month-to-month = highest churn risk!"
    )
    internet_service = st.selectbox(
        "Internet Service", ["DSL", "Fiber optic", "No"]
    )
    online_security = st.selectbox(
        "Online Security",
        ["No", "Yes", "No internet service"]
    )
    tech_support = st.selectbox(
        "Tech Support",
        ["No", "Yes", "No internet service"]
    )
    paperless_billing = st.selectbox(
        "Paperless Billing", ["No", "Yes"]
    )
    payment_method = st.selectbox(
        "Payment Method",
        [
            "Electronic check",
            "Mailed check",
            "Bank transfer (automatic)",
            "Credit card (automatic)"
        ]
    )

# =============================================
# Predict Button
# =============================================
st.markdown("---")

if st.button("🔮 Predict Churn Risk", type="primary"):

    # Build feature dictionary
    features = {
        'SeniorCitizen': 1 if senior_citizen == "Yes" else 0,
        'tenure': tenure,
        'MonthlyCharges': monthly_charges,
        'TotalCharges': tenure * monthly_charges,
        'gender_Male': 0,
        'Partner_Yes': 1 if partner == "Yes" else 0,
        'Dependents_Yes': 1 if dependents == "Yes" else 0,
        'PhoneService_Yes': 1 if phone_service == "Yes" else 0,
        'MultipleLines_No phone service': 1 if phone_service == "No" else 0,
        'MultipleLines_Yes': 0,
        'InternetService_Fiber optic': 1 if internet_service == "Fiber optic" else 0,
        'InternetService_No': 1 if internet_service == "No" else 0,
        'OnlineSecurity_No internet service': 1 if online_security == "No internet service" else 0,
        'OnlineSecurity_Yes': 1 if online_security == "Yes" else 0,
        'OnlineBackup_No internet service': 0,
        'OnlineBackup_Yes': 0,
        'DeviceProtection_No internet service': 0,
        'DeviceProtection_Yes': 0,
        'TechSupport_No internet service': 1 if tech_support == "No internet service" else 0,
        'TechSupport_Yes': 1 if tech_support == "Yes" else 0,
        'StreamingTV_No internet service': 0,
        'StreamingTV_Yes': 0,
        'StreamingMovies_No internet service': 0,
        'StreamingMovies_Yes': 0,
        'Contract_One year': 1 if contract == "One year" else 0,
        'Contract_Two year': 1 if contract == "Two year" else 0,
        'PaperlessBilling_Yes': 1 if paperless_billing == "Yes" else 0,
        'PaymentMethod_Credit card (automatic)': 1 if payment_method == "Credit card (automatic)" else 0,
        'PaymentMethod_Electronic check': 1 if payment_method == "Electronic check" else 0,
        'PaymentMethod_Mailed check': 1 if payment_method == "Mailed check" else 0,
    }

    # CRITICAL — align columns with training order!
    input_df = pd.DataFrame([features])
    input_df = input_df.reindex(columns=feature_names, fill_value=0)

    # Scale
    input_scaled = scaler.transform(input_df)

    # Predict probability
    prob = model.predict_proba(input_scaled)[0][1]

    # Threshold-based prediction (recall-focused!)
    threshold = 0.4
    prediction = 1 if prob >= threshold else 0

    # =============================================
    # Results
    # =============================================
    st.subheader("🎯 Prediction Results")

    # Probability display
    st.metric("Churn Probability", f"{prob:.1%}")
    st.progress(int(prob * 100))

    # Confidence message
    if prob > 0.8:
        st.caption("⚠️ Model is highly confident about churn risk.")
    elif prob < 0.2:
        st.caption("✅ Model is highly confident customer will stay.")

    st.markdown("---")

    # Risk level + recommendation
    if prob >= 0.70:
        st.error("🔴 HIGH RISK — Immediate Action Required!")
        st.markdown("""
        **Recommended Actions:**
        - 📞 Call customer within 24 hours
        - 🎁 Offer 3-month loyalty discount immediately
        - 📋 Review any open service complaints
        - 🔄 Propose annual contract upgrade
        """)
    elif prob >= 0.40:
        st.warning("🟡 MEDIUM RISK — Monitor Closely")
        st.markdown("""
        **Recommended Actions:**
        - 📧 Send personalized retention email this week
        - 🎯 Offer relevant add-on services
        - 📊 Schedule check-in call within 2 weeks
        """)
    else:
        st.success("🟢 LOW RISK — Customer Likely to Stay")
        st.markdown("""
        **Recommended Actions:**
        - 📱 Include in monthly newsletter
        - ⭐ Enroll in loyalty rewards program
        - 📊 Review quarterly — no urgent action needed
        """)

    # Business impact
    st.markdown("---")
    st.subheader("💰 Business Impact")

    if prob >= 0.70:
        revenue_risk = "₹5,000"
    elif prob >= 0.40:
        revenue_risk = "₹2,500"
    else:
        revenue_risk = "Low"

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Revenue at Risk", revenue_risk)
    with col2:
        st.metric("Retention Call Cost", "₹500")
    with col3:
        net = "₹4,500" if prob >= 0.70 else ("₹2,000" if prob >= 0.40 else "₹0")
        st.metric("Net Benefit of Action", net)

# =============================================
# Model Details — Tabs
# =============================================
st.markdown("---")
st.header("🔬 Model Details")

tab1, tab2 = st.tabs(["📊 Performance", "🔧 Methodology"])

with tab1:
    st.markdown("""
    | Method | Recall | Precision | F1 | AUC |
    |--------|--------|-----------|-----|-----|
    | **Logistic Regression** ✅ | **0.80** | 0.49 | 0.61 | **0.835** |
    | Decision Tree | 0.78 | 0.47 | 0.59 | 0.818 |

    **Primary metric: Recall** — catching churners matters most!
    Missing a churner = ₹5,000 lost. False alarm = ₹500 wasted.
    """)

with tab2:
    st.markdown("""
    This model learns from IBM Telco customer data to identify
    customers likely to cancel their subscription. It analyzes
    30 customer attributes including contract type, tenure and
    monthly charges.

    Built using Logistic Regression with a recall-optimized
    threshold of 0.4 — prioritizing catching churners over
    avoiding false alarms. Missing a churner costs ₹5,000
    while a false alarm costs only ₹500.
    """)

# =============================================
# Footer
# =============================================
st.markdown("---")
st.markdown("""
*Project 10 of 22 | Phase 2: Machine Learning*
*Prajwal Kondala | IIT KGP → AI/ML Engineer | May 2026*
*Dataset: IBM Telco Customer Churn — Kaggle*
""")