import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
import plotly.graph_objects as go
import plotly.express as px
import warnings
warnings.filterwarnings("ignore")

# =============================================
# Page Config
# =============================================
st.set_page_config(
    page_title="AI Prediction Dashboard",
    page_icon="🔵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================
# Custom CSS — Dark Professional Theme
# =============================================
st.markdown("""
<style>
    /* Dark background */
    .stApp {
        background-color: #0D0D1A;
        color: #E0E0E0;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #111128;
        border-right: 1px solid #2A2A4E;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background-color: #1A1A2E;
        border: 1px solid #2A2A4E;
        border-radius: 12px;
        padding: 16px;
    }

    /* Headers */
    h1, h2, h3 {
        color: #FFFFFF !important;
    }

    /* Divider */
    hr {
        border-color: #2A2A4E;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #1A1A2E;
        border-radius: 10px;
    }

    .stTabs [data-baseweb="tab"] {
        color: #888;
    }

    .stTabs [aria-selected="true"] {
        color: #3B82F6 !important;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #3B82F6, #2563EB);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 700;
        padding: 12px 24px;
    }

    /* Selectbox */
    .stSelectbox > div {
        background-color: #1A1A2E;
        border: 1px solid #2A2A4E;
        border-radius: 8px;
    }

    /* Dataframe */
    [data-testid="stDataFrame"] {
        background-color: #1A1A2E;
        border-radius: 12px;
    }

    /* Custom boxes */
    .model-card {
        background: linear-gradient(135deg, #3B82F622, #3B82F608);
        border: 1px solid #3B82F666;
        border-radius: 16px;
        padding: 20px 24px;
        margin: 8px 0;
    }

    .insight-box {
        background-color: #1A1A2E;
        border-left: 4px solid #3B82F6;
        border-radius: 0 12px 12px 0;
        padding: 16px 20px;
        margin: 8px 0;
    }

    .risk-high {
        background: linear-gradient(135deg, #EF444422, #EF444408);
        border: 1px solid #EF444466;
        border-radius: 16px;
        padding: 20px 24px;
        margin: 8px 0;
    }

    .risk-medium {
        background: linear-gradient(135deg, #F59E0B22, #F59E0B08);
        border: 1px solid #F59E0B66;
        border-radius: 16px;
        padding: 20px 24px;
        margin: 8px 0;
    }

    .risk-low {
        background: linear-gradient(135deg, #22C55E22, #22C55E08);
        border: 1px solid #22C55E66;
        border-radius: 16px;
        padding: 20px 24px;
        margin: 8px 0;
    }

    .explanation-box {
        background-color: #1A1A2E;
        border: 1px solid #3B82F644;
        border-radius: 12px;
        padding: 16px 20px;
        margin: 8px 0;
    }

    .feature-pill {
        display: inline-block;
        background: #3B82F622;
        border: 1px solid #3B82F666;
        border-radius: 20px;
        padding: 4px 12px;
        font-size: 12px;
        color: #93C5FD;
        margin: 3px;
    }
</style>
""", unsafe_allow_html=True)

# =============================================
# Load Model
# =============================================
@st.cache_resource
def load_model():
    base = os.path.dirname(__file__)
    model_path   = os.path.join(base, 'engineered_model.pkl')
    feature_path = os.path.join(base, 'engineered_features.pkl')

    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    with open(feature_path, 'rb') as f:
        feature_names = pickle.load(f)

    return model, feature_names

model, feature_names = load_model()

# =============================================
# Pre-computed Results (from our notebooks!)
# =============================================
MEDIAN_MONTHLY_CHARGES = 70.35

feature_importance_data = {
    'ContractRiskScore'       : 0.3098,
    'FiberAndMonthly'         : 0.1132,
    'FiberAndNoSecurity'      : 0.0747,
    'ChargesPerTenure'        : 0.0697,
    'StreamingMovies_Yes'     : 0.0510,
    'Contract_One year'       : 0.0420,
    'InternetService_Fiber optic': 0.0380,
    'tenure'                  : 0.0310,
    'MonthlyCharges'          : 0.0290,
    'TotalToMonthly'          : 0.0210,
}

# =============================================
# Sidebar Navigation
# =============================================
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 10px 0 20px;'>
        <div style='font-size:36px;'>🔵</div>
        <div style='font-size:18px; font-weight:900;
                    color:#FFFFFF;'>AI Prediction Dashboard</div>
        <div style='font-size:11px; color:#666;
                    margin-top:4px;'>Project 13 of 22</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    page = st.selectbox(
        "Navigate",
        ["🏠 Home", "🔮 Live Prediction", "📊 Model Insights", "💰 Business Impact"],
        label_visibility="collapsed"
    )

    st.markdown("---")

    st.markdown("""
    <div class='model-card'>
        <div style='font-size:12px; color:#3B82F6;
                    letter-spacing:2px; text-transform:uppercase;
                    margin-bottom:6px;'>Powering This App</div>
        <div style='font-size:16px; font-weight:800;
                    color:#FFFFFF;'>XGBoost (Engineered)</div>
        <div style='font-size:12px; color:#aaa; margin-top:6px;'>
            Recall = 0.8128<br>
            AUC = 0.8414<br>
            Features = 45
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""
    <div style='font-size:13px; color:#aaa;'>
        <b style='color:#fff;'>Dataset</b><br>
        IBM Telco Customer Churn<br>
        <b style='color:#fff;'>7,032</b> customers<br>
        <b style='color:#fff;'>45</b> features (13 engineered!)<br>
        <b style='color:#fff;'>26.6%</b> churn rate
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""
    <div style='font-size:11px; color:#444; text-align:center;'>
    Prajwal Kondala<br>
    IIT KGP → AI/ML Engineer<br>
    May 2026
    </div>
    """, unsafe_allow_html=True)

# =============================================
# PAGE 1 — HOME
# =============================================
if "Home" in page:

    st.markdown("""
    <div style='margin-bottom: 24px;'>
        <div style='font-size:12px; color:#3B82F6;
                    letter-spacing:3px; text-transform:uppercase;
                    margin-bottom:6px;'>Project 13 — AI Prediction Dashboard</div>
        <h1 style='font-size:32px; font-weight:900; margin:0;'>
            How can non-technical users<br>interact with our ML model?
        </h1>
        <p style='color:#666; margin-top:8px;'>
            The product moment — notebook → real usable application.
            Enter customer details and get instant churn predictions
            with plain-language explanations.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Top metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Model", "XGBoost")
    with col2:
        st.metric("Recall", "0.8128")
    with col3:
        st.metric("AUC", "0.8414")
    with col4:
        st.metric("Features", "45")
    with col5:
        st.metric("Engineered", "13")

    st.markdown("---")

    # What this app does
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("🎯 What This App Does")
        st.markdown("""
        <div class='insight-box'>
            <div style='font-size:13px; color:#aaa; line-height:1.8;'>
            This app takes the best ML model from Projects 11 and 12
            and makes it accessible to <b style='color:#fff;'>anyone</b>
            — no Colab, no code, no technical knowledge required.<br><br>
            Enter customer details → get churn probability →
            understand WHY → take the right business action.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class='insight-box' style='margin-top:12px;'>
            <div style='color:#3B82F6; font-weight:700; margin-bottom:6px;'>
                🔬 Model Journey
            </div>
            <div style='font-size:13px; color:#aaa; line-height:1.8;'>
            <b style='color:#fff;'>Project 11</b> → trained 6 models, XGBoost won<br>
            <b style='color:#fff;'>Project 12</b> → engineered 13 new features, scores improved<br>
            <b style='color:#fff;'>Project 13</b> → best model → real product → live!
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.subheader("📊 Model Performance")

        perf_data = {
            'Metric'    : ['Recall', 'Precision', 'F1 Score', 'AUC'],
            'Baseline'  : [0.8102, 0.4959, 0.6152, 0.8409],
            'Engineered': [0.8128, 0.5008, 0.6198, 0.8414],
        }
        perf_df = pd.DataFrame(perf_data)

        fig = go.Figure()

        fig.add_trace(go.Bar(
            name='Baseline (30 features)',
            x=perf_df['Metric'],
            y=perf_df['Baseline'],
            marker_color='#2A2A4E',
            text=perf_df['Baseline'],
            texttemplate='%{text:.4f}',
            textposition='outside',
        ))

        fig.add_trace(go.Bar(
            name='Engineered (45 features) 🏆',
            x=perf_df['Metric'],
            y=perf_df['Engineered'],
            marker_color='#3B82F6',
            text=perf_df['Engineered'],
            texttemplate='%{text:.4f}',
            textposition='outside',
        ))

        fig.update_layout(
            barmode='group',
            paper_bgcolor='#0D0D1A',
            plot_bgcolor='#0D0D1A',
            font_color='#E0E0E0',
            height=320,
            legend=dict(
                bgcolor='#1A1A2E',
                bordercolor='#2A2A4E',
            ),
            yaxis=dict(
                range=[0, 1.1],
                showgrid=True,
                gridcolor='#2A2A4E',
            ),
            xaxis=dict(showgrid=False),
            margin=dict(t=20, b=20),
        )

        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Key EDA findings
    st.subheader("💡 Key Findings from the Data")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class='insight-box'>
            <div style='color:#3B82F6; font-weight:700; margin-bottom:6px;'>
                📄 Contract Type
            </div>
            <div style='font-size:13px; color:#aaa;'>
            Month-to-month → <b style='color:#fff;'>42.7% churn</b><br>
            Two year → <b style='color:#fff;'>2.8% churn</b><br>
            Roughly 15x difference in churn rate!
            ContractRiskScore is the #1 feature at importance 0.31.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class='insight-box'>
            <div style='color:#3B82F6; font-weight:700; margin-bottom:6px;'>
                ⏱️ Tenure Effect
            </div>
            <div style='font-size:13px; color:#aaa;'>
            New customers (0–6m) → <b style='color:#fff;'>53.3% churn</b><br>
            Loyal customers (24m+) → <b style='color:#fff;'>14.0% churn</b><br>
            First 6 months = most critical retention window!
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class='insight-box'>
            <div style='color:#3B82F6; font-weight:700; margin-bottom:6px;'>
                💸 Price Shock
            </div>
            <div style='font-size:13px; color:#aaa;'>
            New customer + high charges →
            <b style='color:#fff;'>73.6% churn rate!</b><br>
            527 customers in this danger profile.
            PriceShockFeature was designed to capture this pattern.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    *Project 13 of 22 | Phase 2: Machine Learning*
    *Prajwal Kondala | IIT KGP → AI/ML Engineer | May 2026*
    """)

# =============================================
# PAGE 2 — LIVE PREDICTION
# =============================================
elif "Live Prediction" in page:

    st.markdown("""
    <div style='margin-bottom: 24px;'>
        <div style='font-size:12px; color:#3B82F6;
                    letter-spacing:3px; text-transform:uppercase;
                    margin-bottom:6px;'>Live Prediction Engine</div>
        <h1 style='font-size:32px; font-weight:900; margin:0;'>
            What is this customer's churn risk?
        </h1>
        <p style='color:#666; margin-top:8px;'>
            Enter customer details below.
            Model predicts churn probability with plain-language explanation.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Inputs ──
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**📋 Customer Profile**")

        tenure = st.slider("Tenure (months)", 0, 72, 12)
        monthly_charges = st.slider("Monthly Charges (₹)", 18, 120, 65)
        senior_citizen = st.selectbox("Senior Citizen", ["No", "Yes"])
        partner = st.selectbox("Partner", ["No", "Yes"])
        dependents = st.selectbox("Dependents", ["No", "Yes"])
        phone_service = st.selectbox("Phone Service", ["No", "Yes"])
        multiple_lines = st.selectbox(
            "Multiple Lines",
            ["No", "Yes", "No phone service"]
        )

    with col2:
        st.markdown("**📋 Service & Contract**")

        contract = st.selectbox(
            "Contract Type",
            ["Month-to-month", "One year", "Two year"]
        )
        internet_service = st.selectbox(
            "Internet Service", ["DSL", "Fiber optic", "No"]
        )
        online_security = st.selectbox(
            "Online Security", ["No", "Yes", "No internet service"]
        )
        online_backup = st.selectbox(
            "Online Backup", ["No", "Yes", "No internet service"]
        )
        device_protection = st.selectbox(
            "Device Protection", ["No", "Yes", "No internet service"]
        )
        tech_support = st.selectbox(
            "Tech Support", ["No", "Yes", "No internet service"]
        )
        streaming_tv = st.selectbox(
            "Streaming TV", ["No", "Yes", "No internet service"]
        )
        streaming_movies = st.selectbox(
            "Streaming Movies", ["No", "Yes", "No internet service"]
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

    st.markdown("---")

    if st.button("🔮 Predict Churn Risk", type="primary"):

        # ── Compute raw features ──
        total_charges = tenure * monthly_charges
        service_count = sum([
            1 if online_security == "Yes" else 0,
            1 if online_backup == "Yes" else 0,
            1 if device_protection == "Yes" else 0,
            1 if tech_support == "Yes" else 0,
            1 if streaming_tv == "Yes" else 0,
            1 if streaming_movies == "Yes" else 0,
            1 if multiple_lines == "Yes" else 0,
        ])

        # ── Compute all 13 engineered features ──
        charges_per_tenure   = monthly_charges / (tenure + 1)
        total_to_monthly     = total_charges / (monthly_charges + 1)
        is_new_customer      = 1 if tenure <= 6 else 0
        is_long_term         = 1 if tenure >= 24 else 0
        is_auto_payment      = 1 if payment_method in [
            "Bank transfer (automatic)", "Credit card (automatic)"
        ] else 0
        fiber_and_monthly    = 1 if (
            internet_service == "Fiber optic" and
            contract == "Month-to-month"
        ) else 0
        fiber_and_no_sec     = 1 if (
            internet_service == "Fiber optic" and
            online_security == "No"
        ) else 0
        new_and_monthly      = 1 if (
            tenure <= 6 and contract == "Month-to-month"
        ) else 0

        contract_risk = {
            "Month-to-month": 3,
            "One year"      : 2,
            "Two year"      : 1
        }[contract]

        lifetime_value  = monthly_charges * tenure
        price_shock     = 1 if (
            monthly_charges > MEDIAN_MONTHLY_CHARGES and tenure <= 6
        ) else 0

        tenure_group_early = 1 if 6 < tenure <= 12 else 0
        tenure_group_mid   = 1 if 12 < tenure <= 24 else 0
        tenure_group_loyal = 1 if tenure > 24 else 0

        # ── Build feature dict ──
        features = {
            'SeniorCitizen'                       : 1 if senior_citizen == "Yes" else 0,
            'tenure'                              : tenure,
            'MonthlyCharges'                      : monthly_charges,
            'TotalCharges'                        : total_charges,
            'ChargesPerTenure'                    : charges_per_tenure,
            'TotalToMonthly'                      : total_to_monthly,
            'IsNewCustomer'                       : is_new_customer,
            'IsLongTermCustomer'                  : is_long_term,
            'IsAutoPayment'                       : is_auto_payment,
            'ServiceCount'                        : service_count,
            'FiberAndMonthly'                     : fiber_and_monthly,
            'FiberAndNoSecurity'                  : fiber_and_no_sec,
            'NewAndMonthly'                       : new_and_monthly,
            'ContractRiskScore'                   : contract_risk,
            'LifetimeValueApprox'                 : lifetime_value,
            'PriceShockFeature'                   : price_shock,
            'gender_Male'                         : 0,
            'Partner_Yes'                         : 1 if partner == "Yes" else 0,
            'Dependents_Yes'                      : 1 if dependents == "Yes" else 0,
            'PhoneService_Yes'                    : 1 if phone_service == "Yes" else 0,
            'MultipleLines_No phone service'      : 1 if multiple_lines == "No phone service" else 0,
            'MultipleLines_Yes'                   : 1 if multiple_lines == "Yes" else 0,
            'InternetService_Fiber optic'         : 1 if internet_service == "Fiber optic" else 0,
            'InternetService_No'                  : 1 if internet_service == "No" else 0,
            'OnlineSecurity_No internet service'  : 1 if online_security == "No internet service" else 0,
            'OnlineSecurity_Yes'                  : 1 if online_security == "Yes" else 0,
            'OnlineBackup_No internet service'    : 1 if online_backup == "No internet service" else 0,
            'OnlineBackup_Yes'                    : 1 if online_backup == "Yes" else 0,
            'DeviceProtection_No internet service': 1 if device_protection == "No internet service" else 0,
            'DeviceProtection_Yes'                : 1 if device_protection == "Yes" else 0,
            'TechSupport_No internet service'     : 1 if tech_support == "No internet service" else 0,
            'TechSupport_Yes'                     : 1 if tech_support == "Yes" else 0,
            'StreamingTV_No internet service'     : 1 if streaming_tv == "No internet service" else 0,
            'StreamingTV_Yes'                     : 1 if streaming_tv == "Yes" else 0,
            'StreamingMovies_No internet service' : 1 if streaming_movies == "No internet service" else 0,
            'StreamingMovies_Yes'                 : 1 if streaming_movies == "Yes" else 0,
            'Contract_One year'                   : 1 if contract == "One year" else 0,
            'Contract_Two year'                   : 1 if contract == "Two year" else 0,
            'PaperlessBilling_Yes'                : 1 if paperless_billing == "Yes" else 0,
            'PaymentMethod_Credit card (automatic)': 1 if payment_method == "Credit card (automatic)" else 0,
            'PaymentMethod_Electronic check'      : 1 if payment_method == "Electronic check" else 0,
            'PaymentMethod_Mailed check'          : 1 if payment_method == "Mailed check" else 0,
            'TenureGroup_Early'                   : tenure_group_early,
            'TenureGroup_Mid'                     : tenure_group_mid,
            'TenureGroup_Loyal'                   : tenure_group_loyal,
        }

        # ── Align columns — CRITICAL ──
        input_df = pd.DataFrame([features])
        input_df = input_df.reindex(columns=feature_names, fill_value=0)

        # ── Predict ──
        prob = model.predict_proba(input_df)[0][1]

        # ── Results layout ──
        res_col1, res_col2 = st.columns([1, 1])

        with res_col1:
            st.subheader("🎯 Prediction Result")

            # Gauge chart
            if prob >= 0.70:
                gauge_color = "#EF4444"
            elif prob >= 0.40:
                gauge_color = "#F59E0B"
            else:
                gauge_color = "#22C55E"

            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=round(prob * 100, 1),
                number={
                    'suffix': '%',
                    'font'  : {'size': 48, 'color': gauge_color}
                },
                gauge={
                    'axis': {
                        'range'    : [0, 100],
                        'tickcolor': '#444',
                        'tickfont' : {'color': '#888'},
                    },
                    'bar': {'color': gauge_color},
                    'bgcolor': '#1A1A2E',
                    'bordercolor': '#2A2A4E',
                    'steps': [
                        {'range': [0, 40],  'color': '#22C55E22'},
                        {'range': [40, 70], 'color': '#F59E0B22'},
                        {'range': [70, 100],'color': '#EF444422'},
                    ],
                    'threshold': {
                        'line' : {'color': gauge_color, 'width': 4},
                        'thickness': 0.75,
                        'value': round(prob * 100, 1),
                    }
                },
                title={
                    'text': 'Churn Probability',
                    'font': {'color': '#888', 'size': 14}
                }
            ))

            fig_gauge.update_layout(
                paper_bgcolor='#0D0D1A',
                font_color='#E0E0E0',
                height=280,
                margin=dict(t=40, b=20, l=20, r=20),
            )

            st.plotly_chart(fig_gauge, use_container_width=True)

            # Risk badge
            if prob >= 0.70:
                st.markdown("""
                <div class='risk-high'>
                    <div style='font-size:20px; font-weight:900;
                                color:#EF4444;'>🔴 HIGH RISK</div>
                    <div style='font-size:13px; color:#aaa;
                                margin-top:4px;'>
                        Customer may benefit from proactive retention outreach.
                    </div>
                </div>
                """, unsafe_allow_html=True)
            elif prob >= 0.40:
                st.markdown("""
                <div class='risk-medium'>
                    <div style='font-size:20px; font-weight:900;
                                color:#F59E0B;'>🟡 MEDIUM RISK</div>
                    <div style='font-size:13px; color:#aaa;
                                margin-top:4px;'>
                        Monitor closely — act this week.
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class='risk-low'>
                    <div style='font-size:20px; font-weight:900;
                                color:#22C55E;'>🟢 LOW RISK</div>
                    <div style='font-size:13px; color:#aaa;
                                margin-top:4px;'>
                        Current profile indicates relatively lower churn risk.
                    </div>
                </div>
                """, unsafe_allow_html=True)

        with res_col2:
            st.subheader("🧠 Why This Prediction?")

            # ── Natural language explanation engine ──
            risk_factors  = []
            safe_factors  = []

            if contract_risk == 3:
                risk_factors.append("Month-to-month contract (biggest churn driver — importance 0.31)")
            elif contract_risk == 2:
                risk_factors.append("One-year contract (moderate commitment level)")
            else:
                safe_factors.append("Two-year contract (strong loyalty signal)")

            if is_new_customer:
                risk_factors.append(f"New customer — only {tenure} month(s) tenure (first 6 months = highest risk window)")
            elif is_long_term:
                safe_factors.append(f"Long-term customer — {tenure} months tenure (loyalty established)")

            if fiber_and_monthly:
                risk_factors.append("Fiber optic + month-to-month combination (highest risk profile)")

            if price_shock:
                risk_factors.append(f"Price shock risk — high charges (₹{monthly_charges}) with very low tenure ({tenure}m)")

            if fiber_and_no_sec:
                risk_factors.append("Fiber optic with no online security (vulnerability risk signal)")

            if new_and_monthly:
                risk_factors.append("New customer on month-to-month contract (double risk flag)")

            if is_auto_payment:
                safe_factors.append("Auto-payment method (loyalty and commitment signal)")

            if service_count >= 4:
                safe_factors.append(f"High service engagement — {service_count} active services (switching costs high)")
            elif service_count <= 1:
                risk_factors.append(f"Low service engagement — only {service_count} active service(s)")

            if monthly_charges > 80:
                risk_factors.append(f"High monthly charges (₹{monthly_charges}) — above comfort zone")
            elif monthly_charges < 40:
                safe_factors.append(f"Low monthly charges (₹{monthly_charges}) — price satisfaction likely")

            # Display explanation
            if risk_factors:
                st.markdown("""
                <div class='explanation-box'>
                    <div style='color:#EF4444; font-weight:700;
                                font-size:13px; margin-bottom:10px;
                                letter-spacing:1px; text-transform:uppercase;'>
                        ⚠️ Risk Factors Detected
                    </div>
                """, unsafe_allow_html=True)
                for i, factor in enumerate(risk_factors, 1):
                    st.markdown(f"""
                    <div style='font-size:13px; color:#E0E0E0;
                                padding:6px 0; border-bottom:1px solid #2A2A4E;
                                line-height:1.5;'>
                        <span style='color:#EF4444; font-weight:700;'>{i}.</span>
                        {factor}
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            if safe_factors:
                st.markdown("""
                <div class='explanation-box' style='margin-top:10px;'>
                    <div style='color:#22C55E; font-weight:700;
                                font-size:13px; margin-bottom:10px;
                                letter-spacing:1px; text-transform:uppercase;'>
                        ✅ Positive Signals
                    </div>
                """, unsafe_allow_html=True)
                for i, factor in enumerate(safe_factors, 1):
                    st.markdown(f"""
                    <div style='font-size:13px; color:#E0E0E0;
                                padding:6px 0; border-bottom:1px solid #2A2A4E;
                                line-height:1.5;'>
                        <span style='color:#22C55E; font-weight:700;'>{i}.</span>
                        {factor}
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

        # ── Business Recommendation ──
        st.markdown("---")
        st.subheader("💼 Business Recommendation")

        if prob >= 0.70:
            st.markdown("""
            <div class='risk-high'>
                <div style='font-size:15px; font-weight:700;
                            color:#EF4444; margin-bottom:10px;'>
                    Immediate Intervention Required
                </div>
                <div style='font-size:13px; color:#E0E0E0; line-height:1.8;'>
                📞 Call customer within 24 hours<br>
                🎁 Offer 3-month loyalty discount immediately<br>
                📋 Review any open service complaints<br>
                🔄 Propose annual or two-year contract upgrade<br>
                ⚡ If fiber optic — check if charges are competitive
                </div>
            </div>
            """, unsafe_allow_html=True)
        elif prob >= 0.40:
            st.markdown("""
            <div class='risk-medium'>
                <div style='font-size:15px; font-weight:700;
                            color:#F59E0B; margin-bottom:10px;'>
                    Proactive Retention — Act This Week
                </div>
                <div style='font-size:13px; color:#E0E0E0; line-height:1.8;'>
                📧 Send personalized retention email this week<br>
                🎯 Offer relevant add-on services to increase engagement<br>
                📊 Schedule check-in call within 2 weeks<br>
                🔄 Present one-year contract upgrade with incentive
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class='risk-low'>
                <div style='font-size:15px; font-weight:700;
                            color:#22C55E; margin-bottom:10px;'>
                    Loyalty Nurture — No Urgent Action
                </div>
                <div style='font-size:13px; color:#E0E0E0; line-height:1.8;'>
                📱 Include in monthly loyalty newsletter<br>
                ⭐ Enroll in rewards program if not already<br>
                📊 Review quarterly — no urgent action needed<br>
                🎁 Occasional appreciation offer to maintain satisfaction
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("""
        *Project 13 of 22 | Phase 2: Machine Learning*
        *Prajwal Kondala | IIT KGP → AI/ML Engineer | May 2026*
        """)

# =============================================
# PAGE 3 — MODEL INSIGHTS
# =============================================
elif "Model Insights" in page:

    st.markdown("""
    <div style='margin-bottom: 24px;'>
        <div style='font-size:12px; color:#3B82F6;
                    letter-spacing:3px; text-transform:uppercase;
                    margin-bottom:6px;'>Model Insights</div>
        <h1 style='font-size:32px; font-weight:900; margin:0;'>
            What drives customer churn?
        </h1>
        <p style='color:#666; margin-top:8px;'>
            Feature importance from engineered XGBoost model.
            ContractRiskScore — built from business understanding — emerged as #1 at 0.31.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Feature importance chart
    fi_df = pd.DataFrame(
        list(feature_importance_data.items()),
        columns=['Feature', 'Importance']
    ).sort_values('Importance')

    fig_fi = px.bar(
        fi_df,
        x='Importance',
        y='Feature',
        orientation='h',
        color='Importance',
        color_continuous_scale=['#1A1A2E', '#3B82F6'],
        text='Importance',
        title='Top 10 Features — XGBoost Engineered Model',
    )
    fig_fi.update_traces(
        texttemplate='%{text:.4f}',
        textposition='outside'
    )
    fig_fi.update_layout(
        paper_bgcolor='#0D0D1A',
        plot_bgcolor='#0D0D1A',
        font_color='#E0E0E0',
        height=480,
        showlegend=False,
        xaxis=dict(showgrid=True, gridcolor='#2A2A4E'),
        yaxis=dict(showgrid=False),
        margin=dict(t=50, b=20),
    )
    st.plotly_chart(fig_fi, use_container_width=True)

    st.markdown("---")

    # Feature stories
    st.subheader("📖 Feature Stories — What Each Signal Means")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class='insight-box'>
            <div style='color:#3B82F6; font-weight:700; margin-bottom:6px;'>
                🏆 ContractRiskScore (0.31)
            </div>
            <div style='font-size:13px; color:#aaa; line-height:1.6;'>
            Engineered feature combining contract commitment into one signal.
            Month-to-month→3, One year→2, Two year→1.<br><br>
            <b style='color:#fff;'>Why it matters:</b> Two raw contract columns
            consolidated into one powerful signal. The model learned commitment
            = loyalty. Built from business understanding, not just math.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class='insight-box'>
            <div style='color:#3B82F6; font-weight:700; margin-bottom:6px;'>
                ⚡ FiberAndMonthly (0.11)
            </div>
            <div style='font-size:13px; color:#aaa; line-height:1.6;'>
            Interaction feature — fiber optic internet AND month-to-month contract.<br><br>
            <b style='color:#fff;'>Why it matters:</b> Neither feature alone captures
            this risk fully. Premium service with zero commitment
            emerged as one of the strongest churn-risk profiles.
            Combination reveals what individual features hide.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class='insight-box'>
            <div style='color:#3B82F6; font-weight:700; margin-bottom:6px;'>
                💰 ChargesPerTenure (0.07)
            </div>
            <div style='font-size:13px; color:#aaa; line-height:1.6;'>
            Ratio feature — MonthlyCharges / (tenure + 1).<br><br>
            <b style='color:#fff;'>Why it matters:</b> A new customer paying ₹90/month
            looks identical to a loyal 5-year customer paying ₹90/month on raw data.
            The ratio exposes the difference — new + high charges = danger signal.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # What XGBoost ignored
    st.subheader("🔍 What XGBoost Ignored — and Why")
    st.markdown("""
    <div class='explanation-box'>
        <div style='font-size:13px; color:#aaa; line-height:1.8;'>
        <b style='color:#fff;'>Zero-importance features:</b>
        IsAutoPayment, IsNewCustomer, IsLongTermCustomer, TenureGroup groups, PriceShockFeature<br><br>
        <b style='color:#fff;'>Why?</b> XGBoost already captures these patterns from tenure,
        contract, and payment columns directly. A feature can have strong business signal
        (PriceShockFeature shows 73.6% churn rate!) but still be <b style='color:#EF4444;'>redundant</b>
        if the model already learns that pattern through other features.<br><br>
        Key lesson: a zero-importance feature is not a failed feature —
        it means the model found a more efficient path to the same information.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    *Project 13 of 22 | Phase 2: Machine Learning*
    *Prajwal Kondala | IIT KGP → AI/ML Engineer | May 2026*
    """)

# =============================================
# PAGE 4 — BUSINESS IMPACT
# =============================================
elif "Business Impact" in page:

    st.markdown("""
    <div style='margin-bottom: 24px;'>
        <div style='font-size:12px; color:#3B82F6;
                    letter-spacing:3px; text-transform:uppercase;
                    margin-bottom:6px;'>Business Impact Calculator</div>
        <h1 style='font-size:32px; font-weight:900; margin:0;'>
            How much does this model save?
        </h1>
        <p style='color:#666; margin-top:8px;'>
            Translate Recall=0.8128 into real business value.
            Adjust the sliders to see impact at your scale.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Sliders
    col1, col2 = st.columns(2)

    with col1:
        total_customers  = st.slider(
            "Total Customers", 10000, 10000000, 1000000, step=10000,
            format="%d"
        )
        churn_rate = st.slider(
            "Monthly Churn Rate (%)", 1, 30, 5
        )

    with col2:
        cost_per_churner = st.slider(
            "Revenue Lost per Churner (₹)", 1000, 20000, 5000, step=500
        )
        retention_cost = st.slider(
            "Retention Outreach Cost (₹)", 100, 2000, 500, step=100
        )

    st.markdown("---")

    # ── Calculations ──
    actual_churners = int(total_customers * churn_rate / 100)

    # With model
    churners_caught   = int(actual_churners * 0.8128)
    total_flagged     = int(churners_caught / 0.5008) if churners_caught > 0 else 0
    false_alarms      = total_flagged - churners_caught
    revenue_protected = churners_caught * cost_per_churner
    outreach_cost     = total_flagged * retention_cost
    net_benefit       = revenue_protected - outreach_cost

    # Without model
    revenue_lost_no_model = actual_churners * cost_per_churner

    # ── Display results ──
    st.subheader("📊 At Your Scale")

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Actual Churners/Month", f"{actual_churners:,}")
    with m2:
        st.metric("Churners Caught (Recall=0.81)", f"{churners_caught:,}")
    with m3:
        st.metric("False Alarms", f"{false_alarms:,}")
    with m4:
        st.metric("Total Outreach Needed", f"{total_flagged:,}")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("💰 Financial Impact")

        fin_data = {
            'Item'  : ['Revenue Protected', 'Outreach Cost', 'Net Benefit'],
            'Amount': [revenue_protected, -outreach_cost, net_benefit],
        }
        fin_df = pd.DataFrame(fin_data)

        colors = [
            '#22C55E' if v >= 0 else '#EF4444'
            for v in fin_df['Amount']
        ]

        fig_fin = go.Figure(go.Bar(
            x=fin_df['Item'],
            y=fin_df['Amount'],
            marker_color=colors,
            text=[f"₹{abs(v)/1e7:.1f} Cr" for v in fin_df['Amount']],
            textposition='outside',
            textfont={'color': '#E0E0E0'},
        ))
        fig_fin.update_layout(
            paper_bgcolor='#0D0D1A',
            plot_bgcolor='#0D0D1A',
            font_color='#E0E0E0',
            height=320,
            showlegend=False,
            yaxis=dict(showgrid=True, gridcolor='#2A2A4E'),
            xaxis=dict(showgrid=False),
            margin=dict(t=40, b=20),
        )
        st.plotly_chart(fig_fin, use_container_width=True)

    with col2:
        st.subheader("📈 Model vs No Model")

        comp_data = {
            'Scenario'     : ['No Model', 'With This Model'],
            'Revenue Saved': [0, net_benefit],
        }
        comp_df = pd.DataFrame(comp_data)

        fig_comp = go.Figure(go.Bar(
            x=comp_df['Scenario'],
            y=comp_df['Revenue Saved'],
            marker_color=['#2A2A4E', '#3B82F6'],
            text=[f"₹{v/1e7:.1f} Cr" for v in comp_df['Revenue Saved']],
            textposition='outside',
            textfont={'color': '#E0E0E0'},
        ))
        fig_comp.update_layout(
            paper_bgcolor='#0D0D1A',
            plot_bgcolor='#0D0D1A',
            font_color='#E0E0E0',
            height=320,
            showlegend=False,
            yaxis=dict(showgrid=True, gridcolor='#2A2A4E'),
            xaxis=dict(showgrid=False),
            margin=dict(t=40, b=20),
        )
        st.plotly_chart(fig_comp, use_container_width=True)

    # Summary box
    st.markdown("---")
    st.markdown(f"""
    <div class='model-card'>
        <div style='font-size:12px; color:#3B82F6;
                    letter-spacing:2px; text-transform:uppercase;
                    margin-bottom:10px;'>Summary at {total_customers:,} Customers</div>
        <div style='font-size:13px; color:#aaa; line-height:2.0;'>
        Monthly churners: <b style='color:#fff;'>{actual_churners:,}</b><br>
        Churners our model catches: <b style='color:#22C55E;'>{churners_caught:,}</b>
        (Recall = 0.8128)<br>
        Revenue protected: <b style='color:#22C55E;'>₹{revenue_protected/1e7:.1f} Cr/month</b><br>
        Outreach cost: <b style='color:#F59E0B;'>₹{outreach_cost/1e7:.1f} Cr/month</b><br>
        Net benefit: <b style='color:#3B82F6; font-size:16px;'>
        ₹{net_benefit/1e7:.1f} Cr/month</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    *Project 13 of 22 | Phase 2: Machine Learning*
    *Prajwal Kondala | IIT KGP → AI/ML Engineer | May 2026*
    *Model: XGBoost Engineered | Recall=0.8128 | Precision=0.5008*
    """)
