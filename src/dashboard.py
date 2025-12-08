import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go
import os

# Configuration
API_URL = "http://localhost:8000"

# Page config with custom theme
st.set_page_config(
    page_title="Saylani Health Desk Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🏥"
)

# Custom CSS for high-contrast professional theme
st.markdown("""
<style>
    /* Main background - Very Dark Navy */
    .main {
        background-color: #0A1929;
    }
    
    /* Metric cards - Dark Slate Blue containers */
    .stMetric {
        background-color: #14344F !important;
        padding: 20px !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5) !important;
        border: 1px solid rgba(79, 159, 253, 0.2) !important;
    }
    
    /* Metric labels - Very Light Blue-Grey */
    .stMetric label {
        color: #E0E7FF !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Metric values - Very Light Blue-Grey */
    .stMetric [data-testid="stMetricValue"] {
        color: #E0E7FF !important;
        font-size: 32px !important;
        font-weight: 700 !important;
    }
    
    /* Metric delta - Vibrant Azure */
    .stMetric [data-testid="stMetricDelta"] {
        color: #4F9FFD !important;
    }
    
    /* Headers - Very Light Blue-Grey */
    h1 {
        color: #E0E7FF !important;
        font-weight: 700 !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    h2, h3 {
        color: #E0E7FF !important;
        font-weight: 600 !important;
    }
    
    /* Sidebar - Dark Slate Blue */
    .css-1d391kg, [data-testid="stSidebar"] {
        background-color: #14344F !important;
        border-right: 1px solid rgba(79, 159, 253, 0.2);
    }
    
    .css-1d391kg p, [data-testid="stSidebar"] p {
        color: #E0E7FF !important;
    }
    
    .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3,
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #E0E7FF !important;
    }
    
    /* Context and answer boxes */
    .context-box {
        background-color: #14344F !important;
        padding: 15px !important;
        border-radius: 8px !important;
        border-left: 4px solid #4F9FFD !important;
        margin: 10px 0 !important;
        color: #E0E7FF !important;
    }
    
    .answer-box {
        background-color: #14344F !important;
        padding: 20px !important;
        border-radius: 10px !important;
        border-left: 4px solid #4F9FFD !important;
        margin: 15px 0 !important;
        font-size: 16px !important;
        line-height: 1.6 !important;
        color: #E0E7FF !important;
    }
    
    .answer-box h4 {
        color: #4F9FFD !important;
    }
    
    /* Input fields */
    .stTextInput input {
        background-color: #14344F !important;
        color: #E0E7FF !important;
        border: 2px solid #4F9FFD !important;
    }
    
    .stTextInput input::placeholder {
        color: #9AA5B1 !important;
    }
    
    /* Buttons - Vibrant Azure */
    .stButton button {
        background-color: #4F9FFD !important;
        color: #0A1929 !important;
        font-weight: 600 !important;
        border: none !important;
        padding: 10px 24px !important;
        border-radius: 6px !important;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        background-color: #6BB0FF !important;
        box-shadow: 0 4px 12px rgba(79, 159, 253, 0.4);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #14344F !important;
        color: #E0E7FF !important;
        font-weight: 600 !important;
        border: 1px solid rgba(79, 159, 253, 0.2);
    }
    
    /* Selectbox */
    .stSelectbox label {
        color: #E0E7FF !important;
        font-weight: 600 !important;
    }
    
    .stSelectbox div[data-baseweb="select"] {
        background-color: #14344F !important;
        border-color: #4F9FFD !important;
    }
    
    /* Info/Warning boxes */
    .stAlert {
        border-radius: 10px !important;
        background-color: #14344F !important;
        color: #E0E7FF !important;
        border: 1px solid rgba(79, 159, 253, 0.3);
    }
    
    /* Plotly charts background - Dark Slate Blue */
    .js-plotly-plot {
        background-color: #14344F !important;
        border-radius: 10px !important;
        padding: 10px !important;
        border: 1px solid rgba(79, 159, 253, 0.2);
    }
    
    /* Plotly chart paper background */
    .plot-container {
        background-color: #14344F !important;
    }
    
    /* Divider */
    hr {
        border-color: rgba(79, 159, 253, 0.2) !important;
    }
    
    /* Markdown text */
    .stMarkdown {
        color: #E0E7FF !important;
    }
    
    /* Code blocks */
    code {
        background-color: #14344F !important;
        color: #4F9FFD !important;
        border: 1px solid rgba(79, 159, 253, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# Title with high-contrast theme
st.markdown("""
<h1 style='text-align: center; color: #E0E7FF; font-size: 3em; font-weight: 700; margin-bottom: 30px; text-shadow: 0 2px 4px rgba(0,0,0,0.3);'>
🏥 Saylani Medical Help Desk Analytics
</h1>
""", unsafe_allow_html=True)

# Sidebar with enhanced styling
st.sidebar.markdown("### 🎛️ Control Panel")
st.sidebar.markdown("---")

branch_filter = st.sidebar.selectbox(
    "🏢 Select Branch",
    ["All", "B001", "B002", "B003", "B004"],
    help="Filter data by specific branch"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Quick Stats")

# Load Data
@st.cache_data
def load_data():
    if os.path.exists("data/cleaned/patients.csv"):
        return pd.read_csv("data/cleaned/patients.csv")
    return None

df = load_data()

if df is not None and len(df) > 0:
    # Sidebar quick stats
    st.sidebar.metric("📋 Total Records", len(df))
    st.sidebar.metric("🏥 Branches", df['branch_id'].nunique() if 'branch_id' in df.columns else 0)
    
    if branch_filter != "All":
        df = df[df['branch_id'] == branch_filter]
    
    if len(df) == 0:
        st.warning(f"⚠️ No data available for branch {branch_filter}. Please select a different branch.")
    else:
        # Summary Metrics with enhanced styling
        st.markdown("### 📊 Key Performance Indicators")
        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
        
        with metric_col1:
            st.metric(
                "👥 Total Patients",
                f"{len(df):,}",
                delta=None,
                help="Total number of patient visits"
            )
        
        with metric_col2:
            unique_doctors = df['doctor_id'].nunique() if 'doctor_id' in df.columns else 0
            st.metric(
                "👨‍⚕️ Active Doctors",
                unique_doctors,
                help="Number of doctors serving patients"
            )
        
        with metric_col3:
            unique_diseases = df['cleaned_disease_name'].nunique() if 'cleaned_disease_name' in df.columns else 0
            st.metric(
                "🦠 Disease Types",
                unique_diseases,
                help="Unique diseases being treated"
            )
        
        with metric_col4:
            unique_areas = df['area'].nunique() if 'area' in df.columns else 0
            st.metric(
                "🗺️ Areas Served",
                unique_areas,
                help="Geographic coverage"
            )
        
        st.markdown("---")
        
        # Top Diseases with Plotly
        st.markdown("### 🦠 Top 10 Diseases")
        if 'cleaned_disease_name' in df.columns and len(df) > 0:
            disease_counts = df['cleaned_disease_name'].value_counts().head(10)
            if len(disease_counts) > 0:
                fig = px.bar(
                    x=disease_counts.values,
                    y=disease_counts.index,
                    orientation='h',
                    labels={'x': 'Number of Cases', 'y': 'Disease'},
                    color=disease_counts.values,
                    color_continuous_scale='Viridis',
                    title="Most Common Diseases"
                )
                fig.update_layout(
                    height=400,
                    showlegend=False,
                    plot_bgcolor='#14344F',
                    paper_bgcolor='#14344F',
                    font=dict(size=12, color='#E0E7FF'),
                    xaxis=dict(gridcolor='rgba(224, 231, 255, 0.1)', color='#9AA5B1', title_font=dict(color='#E0E7FF')),
                    yaxis=dict(categoryorder='total ascending', gridcolor='rgba(224, 231, 255, 0.1)', color='#9AA5B1', title_font=dict(color='#E0E7FF'))
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("📊 No disease data available.")
        else:
            st.info("📊 Disease data not available.")
        
        st.markdown("---")
        
        # Two column layout for charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📈 Patient Visits Over Time")
            if 'visit_timestamp' in df.columns and len(df) > 0:
                df_copy = df.copy()
                df_copy['visit_timestamp'] = pd.to_datetime(df_copy['visit_timestamp'], errors='coerce')
                df_copy = df_copy.dropna(subset=['visit_timestamp'])
                
                if len(df_copy) > 0:
                    daily_counts = df_copy.set_index('visit_timestamp').resample('D').size().reset_index()
                    daily_counts.columns = ['Date', 'Visits']
                    
                    if len(daily_counts) > 0 and daily_counts['Visits'].sum() > 0:
                        fig = px.line(
                            daily_counts,
                            x='Date',
                            y='Visits',
                            markers=True,
                            color_discrete_sequence=['#3b82f6']
                        )
                        fig.update_traces(
                            line=dict(width=3),
                            marker=dict(size=8)
                        )
                        fig.update_layout(
                            height=350,
                            plot_bgcolor='#14344F',
                            paper_bgcolor='#14344F',
                            xaxis_title="Date",
                            yaxis_title="Number of Visits",
                            hovermode='x unified',
                            font=dict(color='#E0E7FF'),
                            xaxis=dict(gridcolor='rgba(224, 231, 255, 0.1)', color='#9AA5B1', title_font=dict(color='#E0E7FF')),
                            yaxis=dict(gridcolor='rgba(224, 231, 255, 0.1)', color='#9AA5B1', title_font=dict(color='#E0E7FF'))
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("📊 No time-series data available.")
                else:
                    st.info("📊 No valid timestamp data available.")
            else:
                st.info("📊 Timestamp data not available.")
        
        with col2:
            st.markdown("### 👨‍⚕️ Top 10 Busiest Doctors")
            if 'doctor_id' in df.columns and len(df) > 0:
                doctor_counts = df['doctor_id'].value_counts().head(10)
                if len(doctor_counts) > 0:
                    fig = px.bar(
                        x=doctor_counts.index,
                        y=doctor_counts.values,
                        labels={'x': 'Doctor ID', 'y': 'Patient Count'},
                        color=doctor_counts.values,
                        color_continuous_scale='Plasma'
                    )
                    fig.update_layout(
                        height=350,
                        showlegend=False,
                        plot_bgcolor='#14344F',
                        paper_bgcolor='#14344F',
                        xaxis_title="Doctor ID",
                        yaxis_title="Number of Patients",
                        font=dict(color='#E0E7FF'),
                        xaxis=dict(gridcolor='rgba(224, 231, 255, 0.1)', color='#9AA5B1', title_font=dict(color='#E0E7FF')),
                        yaxis=dict(gridcolor='rgba(224, 231, 255, 0.1)', color='#9AA5B1', title_font=dict(color='#E0E7FF'))
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("📊 No doctor workload data available.")
            else:
                st.info("📊 Doctor data not available.")
        
        # Geographic Distribution
        st.markdown("### 🗺️ Geographic Distribution")
        if 'area' in df.columns and len(df) > 0:
            area_counts = df['area'].value_counts().head(15)
            if len(area_counts) > 0:
                fig = go.Figure(data=[
                    go.Bar(
                        x=area_counts.index,
                        y=area_counts.values,
                        marker=dict(
                            color=area_counts.values,
                            colorscale='Turbo',
                            showscale=True,
                            colorbar=dict(title="Patients")
                        ),
                        text=area_counts.values,
                        textposition='outside'
                    )
                ])
                fig.update_layout(
                    height=400,
                    plot_bgcolor='#14344F',
                    paper_bgcolor='#14344F',
                    xaxis_title="Area",
                    yaxis_title="Number of Patients",
                    xaxis_tickangle=-45,
                    font=dict(color='#E0E7FF'),
                    xaxis=dict(gridcolor='rgba(224, 231, 255, 0.1)', color='#9AA5B1', title_font=dict(color='#E0E7FF')),
                    yaxis=dict(gridcolor='rgba(224, 231, 255, 0.1)', color='#9AA5B1', title_font=dict(color='#E0E7FF'))
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("📊 No area distribution data available.")
        else:
            st.info("📊 Area data not available.")
    
    # AI Assistant Section with enhanced UI
    st.markdown("---")
    st.markdown("### 🤖 AI Medical Assistant")
    st.markdown("Ask questions about doctors, diseases, schedules, and more!")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        query = st.text_input(
            "💬 Your Question:",
            placeholder="e.g., Explain the disease trends graph, Who is the busiest doctor?, What are the top diseases?",
            help="Ask about doctors, diseases, or ask for an explanation of the analytics graphs shown above."
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        ask_button = st.button("🔍 Ask AI", type="primary", use_container_width=True)
    
    if ask_button and query:
        with st.spinner("🔄 Thinking..."):
            try:
                response = requests.post(f"{API_URL}/chat/query", json={"query": query}, timeout=30)
                if response.status_code == 200:
                    data = response.json()
                    
                    # Display answer in a styled box
                    st.markdown(f"""
                    <div class="answer-box">
                        <h4 style="color: #059669; margin-top: 0;">💡 Answer:</h4>
                        <p style="margin-bottom: 0;">{data['answer']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display context info
                    if data.get('context_used'):
                        st.info(f"📚 Source: {data['context_used']}")
                    elif data.get('contexts'):
                        # Fallback for old format if needed
                        st.markdown("#### 📚 Knowledge Base Sources")
                        for i, ctx in enumerate(data['contexts'], 1):
                            with st.expander(f"📄 Source {i}: {ctx.get('source', 'Unknown')}"):
                                st.markdown(f"**Content:** {ctx['content']}")
                    else:
                        st.info("No specific context sources returned.")
                        
                else:
                    st.error(f"❌ API Error: Status code {response.status_code}")
                        

                    st.info("💡 Make sure the API server is running: `python -m src.app`")
            except requests.exceptions.Timeout:
                st.error("⏱️ Request timed out. The server might be busy.")
            except requests.exceptions.ConnectionError:
                st.error("🔌 Cannot connect to API server.")
                st.info("💡 Start the server with: `python -m src.app`")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    elif ask_button:
        st.warning("⚠️ Please enter a question first!")

else:
    st.error("❌ Data not found!")
    st.info("💡 Please run the data cleaning script first: `python src/clean_data.py`")
    
    with st.expander("🔧 Setup Instructions"):
        st.code("""
# Step 1: Clean the data
python src/clean_data.py

# Step 2: Create knowledge base
python src/create_kb.py

# Step 3: Build RAG index
python src/rag.py

# Step 4: Start API server
python -m src.app

# Step 5: Refresh this dashboard
        """, language="bash")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #9AA5B1; padding: 20px;'>
    <p><strong style='color: #E0E7FF;'>Saylani Medical Help Desk System v1.2</strong></p>
    <p>Developed by <strong>Muhammad Hanzala</strong> from Saylani Health Management Team-AI || Powered by FastAPI & Streamlit.</p>
</div>
""", unsafe_allow_html=True)
