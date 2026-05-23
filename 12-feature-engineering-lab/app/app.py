import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
import plotly.express as px
import plotly.graph_objects as go
import warnings
warnings.filterwarnings("ignore")

# =============================================
# Page Config
# =============================================
st.set_page_config(
    page_title="Feature Engineering Lab",
    page_icon="⚗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================
# Custom CSS — Gold Dark Theme
# =============================================
st.markdown("""
<style>
    .stApp {
        background-color: #0D0D1A;
        color: #E0E0E0;
    }
    [data-testid="stSidebar"] {
        background-color: #111128;
        border-right: 1px solid #2A2A3E;
    }
    [data-testid="stMetric"] {
        background-color: #1A1A2E;
        border: 1px solid #2A2A4E;
        border-radius: 12px;
        padding: 16px;
    }
    h1, h2, h3 {
        color: #FFFFFF !important;
    }
    hr {
        border-color: #2A2A4E;
    }
    .stTabs [data-baseweb="tab-list"] {
        background-color: #1A1A2E;
        border-radius: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #888;
    }
    .stTabs [aria-selected="true"] {
        color: #F59E0B !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #F59E0B, #D97706);
        color: #0D0D1A;
        border: none;
        border-radius: 10px;
        font-weight: 700;
        padding: 12px 24px;
    }
    .stSelectbox > div {
        background-color: #1A1A2E;
        border: 1px solid #2A2A4E;
        border-radius: 8px;
    }
    .proof-badge {
        background: linear-gradient(135deg, #F59E0B22, #D9770622);
        border: 1px solid #F59E0B66;
        border-radius: 12px;
        padding: 16px 20px;
        margin: 8px 0;
    }
    .insight-box {
        background-color: #1A1A2E;
        border-left: 4px solid #F59E0B;
        border-radius: 0 12px 12px 0;
        padding: 16px 20px;
        margin: 8px 0;
    }
    .feature-card {
        background-color: #1A1A2E;
        border: 1px solid #2A2A4E;
        border-radius: 12px;
        padding: 16px 20px;
        margin: 8px 0;
    }
</style>
""", unsafe_allow_html=True)

# =============================================
# Load Models + Features
# =============================================
@st.cache_resource
def load_models():
    base = os.path.dirname(__file__)
    with open(os.path.join(base, 'baseline_model.pkl'), 'rb') as f:
        baseline_model = pickle.load(f)
    with open(os.path.join(base, 'engineered_model.pkl'), 'rb') as f:
        engineered_model = pickle.load(f)
    with open(os.path.join(base, 'baseline_features.pkl'), 'rb') as f:
        baseline_features = pickle.load(f)
    with open(os.path.join(base, 'engineered_features.pkl'), 'rb') as f:
        engineered_features = pickle.load(f)
    return baseline_model, engineered_model, baseline_features, engineered_features

baseline_model, engineered_model, baseline_features, engineered_features = load_models()

# =============================================
# Pre-computed Results
# =============================================
results_data = {
    'Metric'     : ['Recall', 'Precision', 'F1', 'AUC'],
    'Baseline'   : [0.8102, 0.4959, 0.6152, 0.8409],
    'Engineered' : [0.8128, 0.5008, 0.6198, 0.8414],
}
results_df = pd.DataFrame(results_data)
results_df['Improvement'] = (
    results_df['Engineered'] - results_df['Baseline']
).round(4)

# =============================================
# Sidebar
# =============================================
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 10px 0 20px;'>
        <div style='font-size:36px;'>⚗️</div>
        <div style='font-size:18px; font-weight:900;
                    color:#FFFFFF;'>Feature Engineering Lab</div>
        <div style='font-size:11px; color:#666;
                    margin-top:4px;'>Project 12 of 22</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    page = st.selectbox(
        "Navigate",
        ["📊 The Proof", "🔍 Feature Story",
         "🔮 Live Prediction", "💡 Business Insights"],
        label_visibility="collapsed"
    )

    st.markdown("---")

    st.markdown("### 🏆 The Gold Lesson")
    st.markdown("""
    <div class='proof-badge'>
        <div style='font-size:14px; font-weight:800;
                    color:#F59E0B;'>Better Features > Better Models</div>
        <div style='font-size:12px; color:#aaa;
                    margin-top:6px;'>Same XGBoost. Same params.</div>
        <div style='font-size:12px; color:#aaa;'>
                    Better data → better results!</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### 📊 Dataset")
    st.markdown("""
    <div style='font-size:13px; color:#aaa;'>
    IBM Telco Customer Churn<br>
    <b style='color:#fff;'>7,032</b> customers<br>
    <b style='color:#fff;'>30</b> baseline features<br>
    <b style='color:#fff;'>45</b> engineered features<br>
    <b style='color:#fff;'>13</b> new features created
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
# PAGE 1 — THE PROOF
# =============================================
if "The Proof" in page:

    st.markdown("""
    <div style='margin-bottom: 24px;'>
        <div style='font-size:12px; color:#F59E0B;
                    letter-spacing:3px; text-transform:uppercase;
                    margin-bottom:6px;'>Project 12 — Feature Engineering Lab</div>
        <h1 style='font-size:32px; font-weight:900; margin:0;'>
            Can better features beat<br>a better model?
        </h1>
        <p style='color:#666; margin-top:8px;'>
            Same XGBoost. Same hyperparameters. Same dataset.
            Only the features changed.
            <b style='color:#F59E0B;'>Here's what happened.</b>
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Baseline Features", "30")
    with col2:
        st.metric("Engineered Features", "45")
    with col3:
        st.metric("New Features Created", "13")
    with col4:
        st.metric("Recall Improvement", "+0.27%")

    st.markdown("---")

    # Comparison table
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.subheader("📊 Score Comparison")

        for _, row in results_df.iterrows():
            color = "#F59E0B" if row['Improvement'] > 0 else "#EF4444"
            arrow = "▲" if row['Improvement'] > 0 else "▼"
            st.markdown(f"""
            <div class='feature-card'>
                <div style='display:flex; justify-content:space-between;
                            align-items:center;'>
                    <div style='font-size:14px; color:#aaa;
                                font-weight:600;'>{row['Metric']}</div>
                    <div style='font-size:12px; color:{color};
                                font-weight:700;'>{arrow} {abs(row['Improvement']):.4f}</div>
                </div>
                <div style='display:flex; justify-content:space-between;
                            margin-top:8px;'>
                    <div style='text-align:center;'>
                        <div style='font-size:11px; color:#555;'>Baseline</div>
                        <div style='font-size:20px; font-weight:800;
                                    color:#888;'>{row['Baseline']:.4f}</div>
                    </div>
                    <div style='font-size:20px; color:#333; 
                                align-self:center;'>→</div>
                    <div style='text-align:center;'>
                        <div style='font-size:11px; color:#F59E0B;'>Engineered</div>
                        <div style='font-size:20px; font-weight:800;
                                    color:#F59E0B;'>{row['Engineered']:.4f}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col_right:
        st.subheader("📈 Visual Comparison")

        metrics = results_df['Metric'].tolist()
        baseline_vals = results_df['Baseline'].tolist()
        engineered_vals = results_df['Engineered'].tolist()

        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Baseline',
            x=metrics,
            y=baseline_vals,
            marker_color='#2A2A4E',
            text=[f'{v:.4f}' for v in baseline_vals],
            textposition='outside',
            textfont=dict(color='#888', size=11)
        ))
        fig.add_trace(go.Bar(
            name='Engineered',
            x=metrics,
            y=engineered_vals,
            marker_color='#F59E0B',
            text=[f'{v:.4f}' for v in engineered_vals],
            textposition='outside',
            textfont=dict(color='#F59E0B', size=11)
        ))
        fig.update_layout(
            barmode='group',
            paper_bgcolor='#0D0D1A',
            plot_bgcolor='#0D0D1A',
            font_color='#E0E0E0',
            height=400,
            legend=dict(
                bgcolor='#1A1A2E',
                bordercolor='#2A2A4E'
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='#2A2A4E',
                range=[0, 1.05]
            ),
            xaxis=dict(showgrid=False),
            margin=dict(t=20)
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    st.markdown("""
    <div class='proof-badge'>
        <div style='font-size:15px; font-weight:800; color:#F59E0B;
                    margin-bottom:8px;'>🏆 The Verdict</div>
        <div style='font-size:14px; color:#ccc; line-height:1.8;'>
        All 4 metrics improved modestly but consistently with engineered features — same XGBoost, same hyperparameters.<br>
        <b style='color:#F59E0B;'>ContractRiskScore</b> became the single most important feature
        at importance 0.31 — created from domain knowledge, not raw data!<br>
        This is the gold lesson of ML: <b style='color:#F59E0B;'>Better features can outperform algorithm changes alone.</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

# =============================================
# PAGE 2 — FEATURE STORY
# =============================================
elif "Feature Story" in page:

    st.markdown("""
    <div style='margin-bottom: 24px;'>
        <div style='font-size:12px; color:#F59E0B;
                    letter-spacing:3px; text-transform:uppercase;
                    margin-bottom:6px;'>Feature Analysis</div>
        <h1 style='font-size:32px; font-weight:900; margin:0;'>
            What changed when we engineered features?
        </h1>
        <p style='color:#666; margin-top:8px;'>
            Before vs After — see exactly which new features
            XGBoost found valuable and which were redundant.
        </p>
    </div>
    """, unsafe_allow_html=True)

    view = st.radio(
        "Select View",
        ["Before Engineering", "After Engineering", "Side by Side"],
        horizontal=True
    )

    # Baseline importance
    baseline_imp = {
        'Contract_One year'                   : 0.2609,
        'Contract_Two year'                   : 0.2457,
        'InternetService_Fiber optic'         : 0.0943,
        'InternetService_No'                  : 0.0797,
        'tenure'                              : 0.0490,
        'StreamingMovies_Yes'                 : 0.0440,
        'PaymentMethod_Electronic check'      : 0.0380,
        'OnlineSecurity_Yes'                  : 0.0310,
        'PaperlessBilling_Yes'                : 0.0280,
        'StreamingTV_Yes'                     : 0.0250,
    }

    # Engineered importance
    engineered_imp = {
        'ContractRiskScore'                   : 0.3098,
        'FiberAndMonthly'                     : 0.1132,
        'FiberAndNoSecurity'                  : 0.0747,
        'ChargesPerTenure'                    : 0.0697,
        'StreamingMovies_Yes'                 : 0.0510,
        'PaymentMethod_Electronic check'      : 0.0420,
        'PaperlessBilling_Yes'                : 0.0380,
        'InternetService_No'                  : 0.0320,
        'MonthlyCharges'                      : 0.0290,
        'InternetService_Fiber optic'         : 0.0180,
    }

    def make_chart(data, title, color):
        df_imp = pd.DataFrame(
            list(data.items()),
            columns=['Feature', 'Importance']
        ).sort_values('Importance')

        fig = px.bar(
            df_imp, x='Importance', y='Feature',
            orientation='h',
            color='Importance',
            color_continuous_scale=['#1A1A2E', color],
            title=title,
            text='Importance',
        )
        fig.update_traces(
            texttemplate='%{text:.4f}',
            textposition='outside'
        )
        fig.update_layout(
            paper_bgcolor='#0D0D1A',
            plot_bgcolor='#0D0D1A',
            font_color='#E0E0E0',
            height=480,
            showlegend=False,
            margin=dict(t=40)
        )
        fig.update_xaxes(showgrid=True, gridcolor='#2A2A4E')
        fig.update_yaxes(showgrid=False)
        return fig

    if view == "Before Engineering":
        st.plotly_chart(
            make_chart(baseline_imp,
                      'Before Engineering — Top 10 Features (Raw Only)',
                      '#22C55E'),
            use_container_width=True
        )
        st.markdown("""
        <div class='insight-box'>
            <div style='color:#F59E0B; font-weight:700; margin-bottom:6px;'>
                📌 What you see here
            </div>
            <div style='font-size:13px; color:#aaa;'>
            Contract type is split across TWO separate columns —
            Contract_One year and Contract_Two year — each competing
            for importance. The signal is scattered!
            Raw tenure sits at rank 5 with only 0.049 importance.
            </div>
        </div>
        """, unsafe_allow_html=True)

    elif view == "After Engineering":
        st.plotly_chart(
            make_chart(engineered_imp,
                      'After Engineering — Top 10 Features (With New Features)',
                      '#F59E0B'),
            use_container_width=True
        )
        st.markdown("""
        <div class='insight-box'>
            <div style='color:#F59E0B; font-weight:700; margin-bottom:6px;'>
                📌 What changed
            </div>
            <div style='font-size:13px; color:#aaa;'>
            ContractRiskScore consolidated both contract columns into
            ONE powerful feature — importance 0.31, dominating everything!
            FiberAndMonthly captured the riskiest customer segment directly.
            Raw contract columns disappeared from top 10 entirely!
            </div>
        </div>
        """, unsafe_allow_html=True)

    else:
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(
                make_chart(baseline_imp, 'Before Engineering 🟢', '#22C55E'),
                use_container_width=True
            )
        with col2:
            st.plotly_chart(
                make_chart(engineered_imp, 'After Engineering 🟡', '#F59E0B'),
                use_container_width=True
            )

    st.markdown("---")

    st.subheader("🔍 Engineered Features — What XGBoost Said")

    eng_results = [
        ("ContractRiskScore", "0.3098", "✅ High", "#F59E0B",
         "Consolidated contract type into ordinal risk score. Became #1 feature!"),
        ("FiberAndMonthly", "0.1132", "✅ High", "#F59E0B",
         "Fiber optic + month-to-month = one of the strongest churn-risk combinations. XGBoost assigned high importance to it."),
        ("FiberAndNoSecurity", "0.0747", "✅ Good", "#22C55E",
         "Expensive service + no protection = vulnerable customer profile."),
        ("ChargesPerTenure", "0.0697", "✅ Good", "#22C55E",
         "New customer paying high charges revealed as high risk signal."),
        ("LifetimeValueApprox", "0.0135", "⚠️ Low", "#888",
         "Some signal but overlaps with tenure and MonthlyCharges."),
        ("ServiceCount", "0.0124", "⚠️ Low", "#888",
         "Mild signal — XGBoost already handles individual services."),
        ("IsAutoPayment", "0.0070", "⚠️ Low", "#888",
         "Weak — PaymentMethod column already covers this information."),
        ("PriceShockFeature", "0.0000", "❌ Redundant", "#EF4444",
         "73.6% churn rate but redundant — ContractRiskScore + ChargesPerTenure already capture this!"),
        ("IsNewCustomer", "0.0000", "❌ Redundant", "#EF4444",
         "tenure already present — IsNewCustomer adds no new information for XGBoost."),
        ("IsLongTermCustomer", "0.0000", "❌ Redundant", "#EF4444",
         "Same reason — tenure covers this. Tree models don't need this hint!"),
    ]

    for feat, imp, status, color, explanation in eng_results:
        st.markdown(f"""
        <div class='feature-card' style='margin-bottom:8px;'>
            <div style='display:flex; justify-content:space-between;
                        align-items:center; margin-bottom:6px;'>
                <div style='font-size:14px; font-weight:700;
                            color:#fff;'>{feat}</div>
                <div style='display:flex; gap:12px; align-items:center;'>
                    <div style='font-size:13px; color:#F59E0B;'>
                        importance: {imp}</div>
                    <div style='font-size:12px; color:{color};
                                font-weight:700;'>{status}</div>
                </div>
            </div>
            <div style='font-size:13px; color:#888;'>{explanation}</div>
        </div>
        """, unsafe_allow_html=True)

# =============================================
# PAGE 3 — LIVE PREDICTION
# =============================================
elif "Live Prediction" in page:

    st.markdown("""
    <div style='margin-bottom: 24px;'>
        <div style='font-size:12px; color:#F59E0B;
                    letter-spacing:3px; text-transform:uppercase;
                    margin-bottom:6px;'>Live Prediction Engine</div>
        <h1 style='font-size:32px; font-weight:900; margin:0;'>
            Same customer — two models.<br>Which wins?
        </h1>
        <p style='color:#666; margin-top:8px;'>
            Enter customer details and watch baseline vs engineered
            model predictions side by side!
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_input, col_output = st.columns([1, 1])

    with col_input:
        st.subheader("👤 Customer Details")

        tenure = st.slider("Tenure (months)", 0, 72, 6)
        monthly_charges = st.slider("Monthly Charges (₹)", 18, 120, 75)
        total_charges = float(monthly_charges * tenure * np.random.uniform(0.9, 1.1))

        contract = st.selectbox(
            "Contract Type",
            ['Month-to-month', 'One year', 'Two year']
        )
        internet_service = st.selectbox(
            "Internet Service",
            ['DSL', 'Fiber optic', 'No']
        )
        payment_method = st.selectbox(
            "Payment Method",
            ['Electronic check', 'Mailed check',
             'Bank transfer (automatic)', 'Credit card (automatic)']
        )
        online_security = st.selectbox(
            "Online Security", ['No', 'Yes', 'No internet service']
        )

        senior = st.selectbox(
            "Senior Citizen", [0, 1],
            format_func=lambda x: 'Yes' if x == 1 else 'No'
        )

        predict_btn = st.button("🔮 Predict Churn Risk")

    with col_output:
        st.subheader("📊 Model Predictions")

        if predict_btn:
            # ── Build baseline input ──
            base_input = {f: 0 for f in baseline_features}
            base_input['tenure'] = tenure
            base_input['MonthlyCharges'] = monthly_charges
            base_input['TotalCharges'] = float(total_charges)
            base_input['SeniorCitizen'] = senior

            if contract == 'One year':
                base_input['Contract_One year'] = 1
            elif contract == 'Two year':
                base_input['Contract_Two year'] = 1
            if internet_service == 'Fiber optic':
                base_input['InternetService_Fiber optic'] = 1
            elif internet_service == 'No':
                base_input['InternetService_No'] = 1
            if payment_method == 'Electronic check':
                base_input['PaymentMethod_Electronic check'] = 1
            elif payment_method == 'Mailed check':
                base_input['PaymentMethod_Mailed check'] = 1
            elif payment_method == 'Credit card (automatic)':
                base_input['PaymentMethod_Credit card (automatic)'] = 1
            if online_security == 'Yes':
                base_input['OnlineSecurity_Yes'] = 1
            elif online_security == 'No internet service':
                base_input['OnlineSecurity_No internet service'] = 1

            base_df = pd.DataFrame([base_input])
            base_prob = baseline_model.predict_proba(base_df)[0][1]

            # ── Build engineered input ──
            eng_input = {f: 0 for f in engineered_features}

            # Copy base features
            for k, v in base_input.items():
                if k in eng_input:
                    eng_input[k] = v

            # Add engineered features
            eng_input['ChargesPerTenure'] = monthly_charges / (tenure + 1)
            eng_input['TotalToMonthly'] = total_charges / (monthly_charges + 1)
            eng_input['IsNewCustomer'] = 1 if tenure <= 6 else 0
            eng_input['IsLongTermCustomer'] = 1 if tenure >= 24 else 0
            eng_input['IsAutoPayment'] = 1 if payment_method in [
                'Credit card (automatic)', 'Bank transfer (automatic)'] else 0
            eng_input['FiberAndMonthly'] = 1 if (
                internet_service == 'Fiber optic' and
                contract == 'Month-to-month') else 0
            eng_input['FiberAndNoSecurity'] = 1 if (
                internet_service == 'Fiber optic' and
                online_security == 'No') else 0
            eng_input['NewAndMonthly'] = 1 if (
                tenure <= 6 and contract == 'Month-to-month') else 0
            contract_risk_map = {
                'Month-to-month': 3, 'One year': 2, 'Two year': 1
            }
            eng_input['ContractRiskScore'] = contract_risk_map[contract]
            eng_input['LifetimeValueApprox'] = monthly_charges * tenure
            median_charges = 70.35
            eng_input['PriceShockFeature'] = 1 if (
                monthly_charges > median_charges and tenure <= 6) else 0

            eng_df = pd.DataFrame([eng_input])
            eng_prob = engineered_model.predict_proba(eng_df)[0][1]

            # ── Display results ──
            b_color = "#EF4444" if base_prob >= 0.4 else "#22C55E"
            e_color = "#EF4444" if eng_prob >= 0.4 else "#22C55E"
            b_label = "⚠️ HIGH RISK" if base_prob >= 0.4 else "✅ LOW RISK"
            e_label = "⚠️ HIGH RISK" if eng_prob >= 0.4 else "✅ LOW RISK"

            st.markdown(f"""
            <div style='display:grid; grid-template-columns:1fr 1fr;
                        gap:12px; margin-bottom:16px;'>
                <div class='feature-card' style='text-align:center;'>
                    <div style='font-size:11px; color:#888;
                                letter-spacing:2px; text-transform:uppercase;
                                margin-bottom:8px;'>Baseline Model</div>
                    <div style='font-size:42px; font-weight:900;
                                color:{b_color};'>{base_prob:.1%}</div>
                    <div style='font-size:13px; font-weight:700;
                                color:{b_color}; margin-top:4px;'>{b_label}</div>
                    <div style='font-size:11px; color:#555;
                                margin-top:6px;'>30 raw features</div>
                </div>
                <div class='feature-card' style='text-align:center;
                            border-color:#F59E0B44;'>
                    <div style='font-size:11px; color:#F59E0B;
                                letter-spacing:2px; text-transform:uppercase;
                                margin-bottom:8px;'>Engineered Model</div>
                    <div style='font-size:42px; font-weight:900;
                                color:{e_color};'>{eng_prob:.1%}</div>
                    <div style='font-size:13px; font-weight:700;
                                color:{e_color}; margin-top:4px;'>{e_label}</div>
                    <div style='font-size:11px; color:#555;
                                margin-top:6px;'>45 engineered features</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Risk factors
            risk_factors = []
            if contract == 'Month-to-month':
                risk_factors.append("📄 Month-to-month contract — 42.7% avg churn rate!")
            if tenure <= 6:
                risk_factors.append("🆕 New customer — danger zone (first 6 months)!")
            if internet_service == 'Fiber optic' and contract == 'Month-to-month':
                risk_factors.append("⚡ Fiber + month-to-month contract emerged as one of the strongest churn-risk combinations.")
            if monthly_charges > 70.35 and tenure <= 6:
                risk_factors.append("💸 Price shock — high charges before loyalty forms!")

            if risk_factors:
                st.markdown("**⚠️ Risk Factors Detected:**")
                for rf in risk_factors:
                    st.markdown(f"""
                    <div class='insight-box' style='padding:10px 16px;'>
                        <div style='font-size:13px; color:#ccc;'>{rf}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class='insight-box' style='border-color:#22C55E;'>
                    <div style='font-size:13px; color:#22C55E;'>
                    ✅ Low risk profile — long tenure, committed contract,
                    stable payment method!
                    </div>
                </div>
                """, unsafe_allow_html=True)

        else:
            st.markdown("""
            <div style='background:#1A1A2E; border:1px solid #2A2A4E;
                        border-radius:16px; padding:40px;
                        text-align:center; margin-top:20px;'>
                <div style='font-size:48px; margin-bottom:16px;'>🔮</div>
                <div style='color:#666; font-size:14px;'>
                    Fill in customer details and click<br>
                    <b style='color:#F59E0B;'>Predict Churn Risk</b>
                    to see both models side by side!
                </div>
            </div>
            """, unsafe_allow_html=True)

# =============================================
# PAGE 4 — BUSINESS INSIGHTS
# =============================================
elif "Business Insights" in page:

    st.markdown("""
    <div style='margin-bottom: 24px;'>
        <div style='font-size:12px; color:#F59E0B;
                    letter-spacing:3px; text-transform:uppercase;
                    margin-bottom:6px;'>Business Intelligence</div>
        <h1 style='font-size:32px; font-weight:900; margin:0;'>
            What do the engineered features<br>tell us about customers?
        </h1>
        <p style='color:#666; margin-top:8px;'>
            Each engineered feature revealed a hidden pattern
            in the data — with real business implications!
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Key metrics
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("PriceShock Churn Rate", "73.6%", "+50.8% vs avg")
    with c2:
        st.metric("New Customer Churn", "53.3%", "vs 14% loyal")
    with c3:
        st.metric("Month-to-month Churn", "42.7%", "vs 2.8% 2yr")
    with c4:
        st.metric("Avg Lifetime Value Gap", "₹1,023", "churners vs loyals")

    st.markdown("---")

    # Insight 1
    st.markdown("""
    <div class='insight-box'>
        <div style='color:#F59E0B; font-weight:700; font-size:15px;
                    margin-bottom:8px;'>
            📄 ContractRiskScore — The Commitment Signal
        </div>
        <div style='font-size:13px; color:#ccc; line-height:1.8;'>
        Converting contract type into an ordinal risk score
        (Month-to-month=3, One year=2, Two year=1) revealed a strong monotonic relationship with churn:<br>
        <b style='color:#F59E0B;'>Risk 3 → 42.7% churn</b> vs
        <b style='color:#22C55E;'>Risk 1 → 2.8% churn</b> — roughly a 15x difference in churn rate.<br>
        This became the single most important feature at importance 0.31.
        <b>Action: Push customers toward annual contracts from day 1!</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Insight 2
    st.markdown("""
    <div class='insight-box'>
        <div style='color:#F59E0B; font-weight:700; font-size:15px;
                    margin-bottom:8px;'>
            💸 PriceShockFeature — The Hidden Danger Zone
        </div>
        <div style='font-size:13px; color:#ccc; line-height:1.8;'>
        New customers (tenure ≤ 6) paying above median charges (₹70+)
        show a <b style='color:#EF4444;'>73.6% churn rate</b> —
        vs 22.8% for everyone else!<br>
        Only 527 customers hit this condition — approximately 3 out of 4 customers in this segment churned.<br>
        <b>Action: Target these 527 customers immediately with
        retention offers and contract incentives!</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Insight 3
    st.markdown("""
    <div class='insight-box'>
        <div style='color:#F59E0B; font-weight:700; font-size:15px;
                    margin-bottom:8px;'>
            ⏱️ TenureGroup — The Loyalty Curve
        </div>
        <div style='font-size:13px; color:#ccc; line-height:1.8;'>
        Binning tenure into groups revealed the loyalty curve clearly:<br>
        <b style='color:#EF4444;'>New (0-6m): 53.3%</b> →
        <b>Early (6-12m): 35.9%</b> →
        <b>Mid (12-24m): 28.7%</b> →
        <b style='color:#22C55E;'>Loyal (24m+): 14.0%</b><br>
        Every month a customer stays, churn risk drops!
        <b>Action: Survival window is first 6 months — intervene early!</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Insight 4
    st.markdown("""
    <div class='insight-box'>
        <div style='color:#F59E0B; font-weight:700; font-size:15px;
                    margin-bottom:8px;'>
            💰 LifetimeValueApprox — Loyal vs Risky Customers
        </div>
        <div style='font-size:13px; color:#ccc; line-height:1.8;'>
        Approximating lifetime value (MonthlyCharges × tenure) revealed:<br>
        <b style='color:#22C55E;'>Non-churners avg: ₹2,555</b> vs
        <b style='color:#EF4444;'>Churners avg: ₹1,532</b> — a 1.7x gap!<br>
        Churners leave before accumulating value for the business.<br>
        <b>Action: High-value customers (₹2,500+) need proactive
        retention — they are worth protecting!</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""
    <div class='proof-badge'>
        <div style='font-size:15px; font-weight:800; color:#F59E0B;
                    margin-bottom:8px;'>🎯 Final Insight</div>
        <div style='font-size:14px; color:#ccc; line-height:1.8;'>
        Feature engineering is not just a technical step —
        it is <b style='color:#F59E0B;'>business understanding translated into math!</b><br>
        ContractRiskScore didn't come from a formula —
        it came from understanding that commitment = loyalty.<br>
        PriceShockFeature didn't come from statistics —
        it came from knowing that high prices hurt most
        before loyalty forms.<br><br>
        <b style='color:#F59E0B;'>The best features are behaviorally meaningful,
        not just mathematically creative!</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    *Project 12 of 22 | Phase 2: Machine Learning*
    *Prajwal Kondala | IIT KGP → AI/ML Engineer | May 2026*
    *Dataset: IBM Telco Customer Churn — Kaggle*
    """)
