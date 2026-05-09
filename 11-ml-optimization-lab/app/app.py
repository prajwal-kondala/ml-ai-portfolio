import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

# =============================================
# Page Config
# =============================================
st.set_page_config(
    page_title="ML Optimization Lab",
    page_icon="🧪",
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
        color: #22C55E !important;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #22C55E, #16A34A);
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

    /* Info boxes */
    .winner-badge {
        background: linear-gradient(135deg, #22C55E22, #16A34A11);
        border: 1px solid #22C55E66;
        border-radius: 12px;
        padding: 16px 20px;
        margin: 8px 0;
    }

    .insight-box {
        background-color: #1A1A2E;
        border-left: 4px solid #22C55E;
        border-radius: 0 12px 12px 0;
        padding: 16px 20px;
        margin: 8px 0;
    }
</style>
""", unsafe_allow_html=True)

# =============================================
# Load All Models
# =============================================
@st.cache_resource
def load_all_models():
    base = os.path.dirname(__file__)

    models = {}
    model_files = {
        'Decision Tree'    : 'dt_model.pkl',
        'Random Forest'    : 'rf_model.pkl',
        'Gradient Boosting': 'gb_model.pkl',
        'XGBoost'          : 'xgb_model.pkl',
        'LightGBM'         : 'lgbm_model.pkl',
        'XGBoost (Tuned)'  : 'best_xgb_model.pkl',
    }

    for name, filename in model_files.items():
        path = os.path.join(base, filename)
        with open(path, 'rb') as f:
            models[name] = pickle.load(f)

    feature_path = os.path.join(base, 'feature_names.pkl')
    with open(feature_path, 'rb') as f:
        feature_names = pickle.load(f)

    return models, feature_names

models, feature_names = load_all_models()

# =============================================
# Pre-computed Results (from our exploration!)
# =============================================
results_data = {
    'Model'    : ['Decision Tree', 'Random Forest', 'Gradient Boosting',
                  'XGBoost', 'LightGBM', 'XGBoost (Tuned)'],
    'Recall'   : [0.78, 0.80, 0.66, 0.80, 0.80, 0.81],
    'Precision': [0.47, 0.49, 0.59, 0.50, 0.49, 0.50],
    'F1'       : [0.59, 0.61, 0.62, 0.61, 0.61, 0.62],
    'AUC'      : [0.8179, 0.8364, 0.8407, 0.8390, 0.8382, 0.8409],
    'Accuracy' : [0.71, 0.73, 0.79, 0.73, 0.73, 0.73],
    'Type'     : ['Baseline', 'Bagging', 'Boosting',
                  'Boosting', 'Boosting', 'Tuned 🏆'],
}
results_df = pd.DataFrame(results_data)

# =============================================
# Sidebar Navigation
# =============================================
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 10px 0 20px;'>
        <div style='font-size:36px;'>🧪</div>
        <div style='font-size:18px; font-weight:900;
                    color:#FFFFFF;'>ML Optimization Lab</div>
        <div style='font-size:11px; color:#666;
                    margin-top:4px;'>Project 11 of 22</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    page = st.selectbox(
        "Navigate",
        ["🔬 Model Comparison", "🔮 Live Prediction", "📊 Feature Importance"],
        label_visibility="collapsed"
    )

    st.markdown("---")

    st.markdown("### 🏆 Winner")
    st.markdown("""
    <div class='winner-badge'>
        <div style='font-size:16px; font-weight:800;
                    color:#22C55E;'>XGBoost (Tuned)</div>
        <div style='font-size:12px; color:#aaa;
                    margin-top:4px;'>Recall = 0.81 | AUC = 0.8409</div>
        <div style='font-size:11px; color:#666;
                    margin-top:2px;'>learning_rate=0.05 | max_depth=3</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### 📊 Dataset")
    st.markdown("""
    <div style='font-size:13px; color:#aaa;'>
    IBM Telco Customer Churn<br>
    <b style='color:#fff;'>7,032</b> customers<br>
    <b style='color:#fff;'>30</b> features<br>
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
# PAGE 1 — MODEL COMPARISON
# =============================================
if "Model Comparison" in page:

    st.markdown("""
    <div style='margin-bottom: 24px;'>
        <div style='font-size:12px; color:#22C55E;
                    letter-spacing:3px; text-transform:uppercase;
                    margin-bottom:6px;'>Project 11 — ML Optimization Lab</div>
        <h1 style='font-size:32px; font-weight:900; margin:0;'>
            Which model should we trust<br>with our business decisions?
        </h1>
        <p style='color:#666; margin-top:8px;'>
            5 ensemble models trained and compared on IBM Telco Churn dataset.
            Primary metric: <b style='color:#22C55E;'>Recall</b>
            — missing a churner costs ₹5,000.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Top metrics ──
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Models Compared", "6")
    with col2:
        st.metric("Best Recall", "0.81")
    with col3:
        st.metric("Best AUC", "0.8409")
    with col4:
        st.metric("Training Rows", "5,625")
    with col5:
        st.metric("Features", "30")

    st.markdown("---")

    # ── Metric selector ──
    st.subheader("📊 Complete Model Comparison")

    metric_col, sort_col = st.columns([2, 1])
    with metric_col:
        primary_metric = st.selectbox(
            "Highlight metric",
            ["Recall", "AUC", "F1", "Precision", "Accuracy"],
            help="Select which metric to highlight as primary!"
        )
    with sort_col:
        sort_order = st.selectbox(
            "Sort by",
            ["Best first", "Original order"]
        )

    # Sort dataframe
    display_df = results_df.copy()
    if sort_order == "Best first":
        display_df = display_df.sort_values(
            primary_metric, ascending=False
        ).reset_index(drop=True)

    # Style the dataframe
    def highlight_winner(row):
        if row['Model'] == 'XGBoost (Tuned)':
            return ['background-color: #22C55E22; '
                    'color: #22C55E; font-weight: bold'] * len(row)
        return [''] * len(row)

    styled_df = display_df.style\
        .apply(highlight_winner, axis=1)\
        .format({
            'Recall'   : '{:.2f}',
            'Precision': '{:.2f}',
            'F1'       : '{:.2f}',
            'AUC'      : '{:.4f}',
            'Accuracy' : '{:.2f}',
        })\
        .bar(subset=[primary_metric],
             color='#22C55E44',
             vmin=0, vmax=1)

    st.dataframe(styled_df, use_container_width=True, height=280)

    st.markdown("---")

    # ── Visual comparison ──
    st.subheader("📈 Visual Comparison")

    tab1, tab2 = st.tabs(["Bar Chart", "Radar Chart"])

    with tab1:
        fig = px.bar(
            results_df.sort_values(primary_metric),
            x=primary_metric,
            y='Model',
            orientation='h',
            color=primary_metric,
            color_continuous_scale=['#1A1A2E', '#22C55E'],
            title=f'{primary_metric} Score — All Models',
            text=primary_metric,
        )
        fig.update_traces(texttemplate='%{text:.3f}',
                          textposition='outside')
        fig.update_layout(
            paper_bgcolor='#0D0D1A',
            plot_bgcolor='#0D0D1A',
            font_color='#E0E0E0',
            title_font_size=16,
            showlegend=False,
            height=400,
        )
        fig.update_xaxes(showgrid=True,
                         gridcolor='#2A2A4E', range=[0, 1.1])
        fig.update_yaxes(showgrid=False)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        categories = ['Recall', 'Precision', 'F1', 'AUC', 'Accuracy']
        colors = ['#22C55E', '#6C63FF', '#F59E0B',
                  '#EF4444', '#EC4899', '#00D4FF']

        fig = go.Figure()
        for i, row in results_df.iterrows():
            values = [row[c] for c in categories]
            values += values[:1]
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories + [categories[0]],
                fill='toself',
                name=row['Model'],
                line_color=colors[i],
                opacity=0.6,
            ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True, range=[0, 1],
                    gridcolor='#2A2A4E', color='#666'
                ),
                bgcolor='#0D0D1A',
                angularaxis=dict(color='#aaa')
            ),
            paper_bgcolor='#0D0D1A',
            font_color='#E0E0E0',
            title='Model Comparison — Radar Chart',
            height=500,
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ── Business Impact Calculator ──
    st.subheader("💰 Business Impact Calculator")
    st.markdown(
        "*See the ₹ value of choosing the right model!*"
    )

    biz_col1, biz_col2, biz_col3 = st.columns(3)

    with biz_col1:
        customer_base = st.slider(
            "Customer Base",
            100000, 10000000, 1000000, 100000,
            format="%d"
        )
    with biz_col2:
        churn_rate = st.slider(
            "Churn Rate (%)",
            1, 30, 5
        )
    with biz_col3:
        revenue_per_customer = st.slider(
            "Revenue per Customer (₹)",
            1000, 20000, 5000, 500
        )

    actual_churners = int(customer_base * churn_rate / 100)
    retention_call_cost = 500

    st.markdown("---")

    calc_cols = st.columns(len(results_df))
    for i, (_, row) in enumerate(results_df.iterrows()):
        with calc_cols[i]:
            caught = int(actual_churners * row['Recall'])
            saved  = caught * revenue_per_customer
            cost   = int(actual_churners * 1.5 * retention_call_cost)
            net    = saved - cost
            is_winner = row['Model'] == 'XGBoost (Tuned)'

            color = '#22C55E' if is_winner else '#6C63FF'
            border = f'2px solid {color}' if is_winner else f'1px solid #2A2A4E'

            st.markdown(f"""
            <div style='background:#1A1A2E; border:{border};
                        border-radius:12px; padding:14px;
                        text-align:center;'>
                <div style='font-size:11px; color:{color};
                            font-weight:700; margin-bottom:6px;'>
                    {row['Model']}{'  🏆' if is_winner else ''}
                </div>
                <div style='font-size:11px; color:#666;'>
                    Caught: <b style='color:#fff;'>
                    {caught:,}</b> churners
                </div>
                <div style='font-size:14px; color:{color};
                            font-weight:800; margin-top:6px;'>
                    ₹{net/100000:.1f}L saved
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Key Insights ──
    st.subheader("💡 Key Findings")

    ins1, ins2, ins3 = st.columns(3)

    with ins1:
        st.markdown("""
        <div class='insight-box'>
            <div style='color:#22C55E; font-weight:700;
                        margin-bottom:6px;'>🌲 Bagging vs Boosting</div>
            <div style='font-size:13px; color:#aaa;'>
            Random Forest (bagging) and XGBoost (boosting) both
            achieved Recall=0.80 — similar Recall through completely
            different approaches. Gradient Boosting needed threshold
            adjustment to reach comparable Recall.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with ins2:
        st.markdown("""
        <div class='insight-box'>
            <div style='color:#22C55E; font-weight:700;
                        margin-bottom:6px;'>🔧 Tuning Impact</div>
            <div style='font-size:13px; color:#aaa;'>
            GridSearchCV with Stratified 5-Fold CV improved
            XGBoost Recall from 0.80 → 0.81. At 1M customers
            with 5% churn, this catches 500 more churners —
            potentially saving ₹25 lakhs per month at scale.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with ins3:
        st.markdown("""
        <div class='insight-box'>
            <div style='color:#22C55E; font-weight:700;
                        margin-bottom:6px;'>📊 Feature Consensus</div>
            <div style='font-size:13px; color:#aaa;'>
            Random Forest ranked tenure #1 (importance=0.19).
            XGBoost ranked Contract_Two year #1 (importance=0.24).
            Both agreed on top 3 features — cross-model
            validation confirms what truly matters!
            </div>
        </div>
        """, unsafe_allow_html=True)

# =============================================
# PAGE 2 — LIVE PREDICTION
# =============================================
elif "Live Prediction" in page:

    st.markdown("""
    <div style='margin-bottom: 24px;'>
        <div style='font-size:12px; color:#6C63FF;
                    letter-spacing:3px; text-transform:uppercase;
                    margin-bottom:6px;'>Live Prediction Engine</div>
        <h1 style='font-size:32px; font-weight:900; margin:0;'>
            Is this customer at risk<br>of leaving next month?
        </h1>
        <p style='color:#666; margin-top:8px;'>
            Powered by XGBoost (Tuned) — Recall=0.81 | AUC=0.8409
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📋 Customer Details")

        tenure = st.slider("Tenure (months)", 0, 72, 12)
        monthly_charges = st.slider("Monthly Charges (₹)", 18, 120, 65)
        senior_citizen = st.selectbox("Senior Citizen", ["No", "Yes"])
        partner = st.selectbox("Partner", ["No", "Yes"])
        dependents = st.selectbox("Dependents", ["No", "Yes"])
        phone_service = st.selectbox("Phone Service", ["No", "Yes"])
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
            ["Electronic check", "Mailed check",
             "Bank transfer (automatic)",
             "Credit card (automatic)"]
        )

    with col2:
        st.subheader("🎯 Prediction Results")

        if st.button("🔮 Predict Churn Risk", type="primary"):

            features = {
                'SeniorCitizen'      : 1 if senior_citizen == "Yes" else 0,
                'tenure'             : tenure,
                'MonthlyCharges'     : monthly_charges,
                'TotalCharges'       : tenure * monthly_charges,
                'gender_Male'        : 0,
                'Partner_Yes'        : 1 if partner == "Yes" else 0,
                'Dependents_Yes'     : 1 if dependents == "Yes" else 0,
                'PhoneService_Yes'   : 1 if phone_service == "Yes" else 0,
                'MultipleLines_No phone service':
                    1 if phone_service == "No" else 0,
                'MultipleLines_Yes'  : 0,
                'InternetService_Fiber optic':
                    1 if internet_service == "Fiber optic" else 0,
                'InternetService_No' :
                    1 if internet_service == "No" else 0,
                'OnlineSecurity_No internet service':
                    1 if online_security == "No internet service" else 0,
                'OnlineSecurity_Yes' :
                    1 if online_security == "Yes" else 0,
                'OnlineBackup_No internet service': 0,
                'OnlineBackup_Yes'   : 0,
                'DeviceProtection_No internet service': 0,
                'DeviceProtection_Yes': 0,
                'TechSupport_No internet service':
                    1 if tech_support == "No internet service" else 0,
                'TechSupport_Yes'    :
                    1 if tech_support == "Yes" else 0,
                'StreamingTV_No internet service': 0,
                'StreamingTV_Yes'    : 0,
                'StreamingMovies_No internet service': 0,
                'StreamingMovies_Yes': 0,
                'Contract_One year'  :
                    1 if contract == "One year" else 0,
                'Contract_Two year'  :
                    1 if contract == "Two year" else 0,
                'PaperlessBilling_Yes':
                    1 if paperless_billing == "Yes" else 0,
                'PaymentMethod_Credit card (automatic)':
                    1 if payment_method == "Credit card (automatic)" else 0,
                'PaymentMethod_Electronic check':
                    1 if payment_method == "Electronic check" else 0,
                'PaymentMethod_Mailed check':
                    1 if payment_method == "Mailed check" else 0,
            }

            input_df = pd.DataFrame([features])
            input_df = input_df.reindex(
                columns=feature_names, fill_value=0
            )

            # Get predictions from ALL models!
            threshold = 0.4
            all_probs = {}
            all_preds = {}

            for name, model_obj in models.items():
                prob = model_obj.predict_proba(input_df)[0][1]
                all_probs[name] = prob
                all_preds[name] = 1 if prob >= threshold else 0

            # Best model prediction
            best_prob = all_probs['XGBoost (Tuned)']
            prediction = all_preds['XGBoost (Tuned)']

            # ── Probability display ──
            st.metric("Churn Probability",
                      f"{best_prob:.1%}",
                      help="XGBoost Tuned | Threshold=0.4")
            st.progress(int(best_prob * 100))

            st.markdown("---")

            # ── Risk level ──
            if best_prob >= 0.70:
                st.error("🔴 HIGH RISK — Immediate Action Required!")
                st.markdown("""
                **Recommended Actions:**
                - 📞 Call customer within 24 hours
                - 🎁 Offer 3-month loyalty discount
                - 📋 Review any open service complaints
                - 🔄 Propose annual contract upgrade
                """)
                revenue_risk = "₹5,000"
                net_benefit  = "₹4,500"

            elif best_prob >= 0.40:
                st.warning("🟡 MEDIUM RISK — Monitor Closely")
                st.markdown("""
                **Recommended Actions:**
                - 📧 Send personalized retention email
                - 🎯 Offer relevant add-on services
                - 📊 Schedule check-in call within 2 weeks
                """)
                revenue_risk = "₹2,500"
                net_benefit  = "₹2,000"

            else:
                st.success("🟢 LOW RISK — Customer Likely to Stay")
                st.markdown("""
                **Recommended Actions:**
                - 📱 Include in monthly newsletter
                - ⭐ Enroll in loyalty rewards program
                """)
                revenue_risk = "Low"
                net_benefit  = "₹0"

            # ── Business impact ──
            st.markdown("---")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Revenue at Risk", revenue_risk)
            with c2:
                st.metric("Retention Call Cost", "₹500")
            with c3:
                st.metric("Net Benefit of Action", net_benefit)

            st.markdown("---")

            # ── All models voted ──
            st.subheader("🗳️ How All Models Voted")

            vote_data = []
            for name, prob in all_probs.items():
                vote_data.append({
                    'Model'      : name,
                    'Probability': prob,
                    'Prediction' : '🔴 CHURN' if prob >= 0.4 else '🟢 STAY',
                })
            vote_df = pd.DataFrame(vote_data)

            fig = px.bar(
                vote_df,
                x='Model',
                y='Probability',
                color='Probability',
                color_continuous_scale=['#22C55E', '#EF4444'],
                title='Churn Probability — All Models',
                text='Probability',
            )
            fig.add_hline(
                y=0.4, line_dash="dash",
                line_color="#F59E0B",
                annotation_text="Threshold=0.4",
                annotation_font_color="#F59E0B"
            )
            fig.update_traces(
                texttemplate='%{text:.2f}',
                textposition='outside'
            )
            fig.update_layout(
                paper_bgcolor='#0D0D1A',
                plot_bgcolor='#0D0D1A',
                font_color='#E0E0E0',
                height=350,
                showlegend=False,
            )
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(
                showgrid=True,
                gridcolor='#2A2A4E',
                range=[0, 1.1]
            )
            st.plotly_chart(fig, use_container_width=True)

            churn_votes = sum(1 for p in all_preds.values() if p == 1)
            st.markdown(f"""
            <div class='winner-badge'>
                <b style='color:#22C55E;'>
                {churn_votes} out of {len(all_preds)} models
                predict CHURN</b> at threshold=0.4 🎯
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
                    <b style='color:#22C55E;'>Predict Churn Risk</b>
                    to see results!
                </div>
            </div>
            """, unsafe_allow_html=True)

# =============================================
# PAGE 3 — FEATURE IMPORTANCE
# =============================================
elif "Feature Importance" in page:

    st.markdown("""
    <div style='margin-bottom: 24px;'>
        <div style='font-size:12px; color:#F59E0B;
                    letter-spacing:3px; text-transform:uppercase;
                    margin-bottom:6px;'>Feature Analysis</div>
        <h1 style='font-size:32px; font-weight:900; margin:0;'>
            What drives customer churn?
        </h1>
        <p style='color:#666; margin-top:8px;'>
            Feature importance from Random Forest and XGBoost —
            cross-model consensus reveals true drivers!
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Feature importance data from our exploration!
    rf_importance = {
        'tenure'                          : 0.1908,
        'Contract_Two year'               : 0.1519,
        'InternetService_Fiber optic'     : 0.0877,
        'TotalCharges'                    : 0.0872,
        'PaymentMethod_Electronic check'  : 0.0736,
        'MonthlyCharges'                  : 0.0656,
        'Contract_One year'               : 0.0497,
        'OnlineSecurity_Yes'              : 0.0449,
        'DeviceProtection_No internet service': 0.0340,
        'OnlineSecurity_No internet service'  : 0.0308,
    }

    xgb_importance = {
        'Contract_Two year'              : 0.2388,
        'Contract_One year'              : 0.2005,
        'InternetService_Fiber optic'    : 0.1422,
        'InternetService_No'             : 0.1006,
        'tenure'                         : 0.0432,
        'PaymentMethod_Electronic check' : 0.0384,
        'StreamingMovies_Yes'            : 0.0384,
        'OnlineSecurity_Yes'             : 0.0290,
        'PaperlessBilling_Yes'           : 0.0201,
        'StreamingTV_Yes'                : 0.0174,
    }

    model_choice = st.radio(
        "Select Model",
        ["Random Forest", "XGBoost (Tuned)", "Side by Side"],
        horizontal=True
    )

    if model_choice == "Random Forest":
        rf_df = pd.DataFrame(
            list(rf_importance.items()),
            columns=['Feature', 'Importance']
        ).sort_values('Importance')

        fig = px.bar(
            rf_df, x='Importance', y='Feature',
            orientation='h',
            color='Importance',
            color_continuous_scale=['#1A1A2E', '#22C55E'],
            title='Feature Importance — Random Forest 🌲',
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
            height=500,
            showlegend=False,
        )
        fig.update_xaxes(
            showgrid=True,
            gridcolor='#2A2A4E'
        )
        st.plotly_chart(fig, use_container_width=True)

    elif model_choice == "XGBoost (Tuned)":
        xgb_df = pd.DataFrame(
            list(xgb_importance.items()),
            columns=['Feature', 'Importance']
        ).sort_values('Importance')

        fig = px.bar(
            xgb_df, x='Importance', y='Feature',
            orientation='h',
            color='Importance',
            color_continuous_scale=['#1A1A2E', '#6C63FF'],
            title='Feature Importance — XGBoost ⚡',
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
            height=500,
            showlegend=False,
        )
        fig.update_xaxes(
            showgrid=True,
            gridcolor='#2A2A4E'
        )
        st.plotly_chart(fig, use_container_width=True)

    else:
        col1, col2 = st.columns(2)

        with col1:
            rf_df = pd.DataFrame(
                list(rf_importance.items()),
                columns=['Feature', 'Importance']
            ).sort_values('Importance')

            fig1 = px.bar(
                rf_df, x='Importance', y='Feature',
                orientation='h',
                color='Importance',
                color_continuous_scale=['#1A1A2E', '#22C55E'],
                title='Random Forest 🌲',
                text='Importance',
            )
            fig1.update_traces(
                texttemplate='%{text:.3f}',
                textposition='outside'
            )
            fig1.update_layout(
                paper_bgcolor='#0D0D1A',
                plot_bgcolor='#0D0D1A',
                font_color='#E0E0E0',
                height=500,
                showlegend=False,
            )
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            xgb_df = pd.DataFrame(
                list(xgb_importance.items()),
                columns=['Feature', 'Importance']
            ).sort_values('Importance')

            fig2 = px.bar(
                xgb_df, x='Importance', y='Feature',
                orientation='h',
                color='Importance',
                color_continuous_scale=['#1A1A2E', '#6C63FF'],
                title='XGBoost (Tuned) ⚡',
                text='Importance',
            )
            fig2.update_traces(
                texttemplate='%{text:.3f}',
                textposition='outside'
            )
            fig2.update_layout(
                paper_bgcolor='#0D0D1A',
                plot_bgcolor='#0D0D1A',
                font_color='#E0E0E0',
                height=500,
                showlegend=False,
            )
            st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # ── Consensus insights ──
    st.subheader("🤝 Cross-Model Consensus")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class='insight-box'>
            <div style='color:#22C55E; font-weight:700;
                        margin-bottom:6px;'>
                📄 Contract Type
            </div>
            <div style='font-size:13px; color:#aaa;'>
            Both models agree contract type is critical!
            Two-year contract customers show very low churn (~3%) vs
            43% for month-to-month. Most actionable lever! 🎯
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class='insight-box'>
            <div style='color:#22C55E; font-weight:700;
                        margin-bottom:6px;'>
                ⏱️ Tenure
            </div>
            <div style='font-size:13px; color:#aaa;'>
            RF ranks tenure #1. XGBoost ranks it #5.
            But both confirm: first 10 months = highest
            churn risk! Intervene early! 🎯
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class='insight-box'>
            <div style='color:#22C55E; font-weight:700;
                        margin-bottom:6px;'>
                🌐 Fiber Optic
            </div>
            <div style='font-size:13px; color:#aaa;'>
            Both models rank fiber optic internet in top 3.
            Premium service customers churn more —
            possibly due to high charges or competition! 🎯
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    *Project 11 of 22 | Phase 2: Machine Learning*
    *Prajwal Kondala | IIT KGP → AI/ML Engineer | May 2026*
    *Dataset: IBM Telco Customer Churn — Kaggle*
    """)
