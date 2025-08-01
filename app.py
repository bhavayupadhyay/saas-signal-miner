"""
SaaS Signal Miner - Streamlit Dashboard
Frontend application for displaying and filtering SaaS startup signals
Production-ready for Streamlit Cloud deployment
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time
from main import SaaSSignalMiner
from utils import get_fallback_data, format_startup_data

# Page configuration
st.set_page_config(
    page_title="SaaS Signal Miner",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .startup-card {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        margin-bottom: 1rem;
    }
    .score-high { color: #28a745; font-weight: bold; }
    .score-medium { color: #ffc107; font-weight: bold; }
    .score-low { color: #dc3545; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_startup_data():
    """
    Load startup data with caching to avoid repeated API calls
    """
    try:
        miner = SaaSSignalMiner()
        startups = miner.scan_for_startups()
        return startups
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return format_startup_data(get_fallback_data())

def get_score_color(score):
    """Get color class based on score"""
    if score >= 80:
        return "score-high"
    elif score >= 60:
        return "score-medium"
    else:
        return "score-low"

def create_score_chart(startups_df):
    """Create a score distribution chart"""
    fig = px.histogram(
        startups_df, 
        x='score', 
        nbins=10,
        title="Growth Score Distribution",
        labels={'score': 'Growth Score', 'count': 'Number of Startups'},
        color_discrete_sequence=['#1f77b4']
    )
    fig.update_layout(
        xaxis_title="Growth Score",
        yaxis_title="Number of Startups",
        showlegend=False
    )
    return fig

def create_sector_chart(startups_df):
    """Create a sector distribution chart"""
    sector_counts = startups_df['sector'].value_counts()
    fig = px.pie(
        values=sector_counts.values,
        names=sector_counts.index,
        title="Startups by Sector",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

def create_signal_type_chart(startups_df):
    """Create a signal type distribution chart"""
    signal_counts = startups_df['signal_type'].value_counts()
    fig = px.bar(
        x=signal_counts.index,
        y=signal_counts.values,
        title="Startups by Signal Type",
        labels={'x': 'Signal Type', 'y': 'Number of Startups'},
        color=signal_counts.values,
        color_continuous_scale='viridis'
    )
    fig.update_layout(
        xaxis_title="Signal Type",
        yaxis_title="Number of Startups",
        showlegend=False
    )
    return fig

def main():
    """Main Streamlit application"""
    
    # Header
    st.markdown('<h1 class="main-header">🚀 SaaS Signal Miner</h1>', unsafe_allow_html=True)
    st.markdown("### Discover High-Potential Early-Stage SaaS Startups")
    
    # Sidebar for filters
    st.sidebar.header("🔍 Filters")
    
    # Load data
    with st.spinner("Scanning for SaaS startups..."):
        startups = load_startup_data()
    
    if not startups:
        st.error("No startup data available. Please check your API configuration.")
        return
    
    # Convert to DataFrame for easier manipulation
    startups_df = pd.DataFrame(startups)
    
    # Get unique values for filters
    sectors = ["All"] + sorted(startups_df['sector'].unique().tolist())
    funding_stages = ["All"] + sorted(startups_df['funding_stage'].unique().tolist())
    signal_types = ["All"] + sorted(startups_df['signal_type'].unique().tolist())
    
    # Sidebar filters
    selected_sector = st.sidebar.selectbox("Sector", sectors)
    selected_funding_stage = st.sidebar.selectbox("Funding Stage", funding_stages)
    selected_signal_type = st.sidebar.selectbox("Signal Type", signal_types)
    min_score = st.sidebar.slider("Minimum Growth Score", 0, 100, 0, 5)
    
    # Filter data
    miner = SaaSSignalMiner()
    filtered_startups = miner.filter_startups(
        startups,
        sector=selected_sector if selected_sector != "All" else None,
        funding_stage=selected_funding_stage if selected_funding_stage != "All" else None,
        signal_type=selected_signal_type if selected_signal_type != "All" else None,
        min_score=min_score
    )
    
    filtered_df = pd.DataFrame(filtered_startups)
    
    # Main content area
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Startups", len(filtered_startups))
    
    with col2:
        avg_score = filtered_df['score'].mean() if not filtered_df.empty else 0
        st.metric("Avg Growth Score", f"{avg_score:.1f}")
    
    with col3:
        high_score_count = len(filtered_df[filtered_df['score'] >= 80]) if not filtered_df.empty else 0
        st.metric("High Score (80+)", high_score_count)
    
    with col4:
        st.metric("Last Updated", datetime.now().strftime("%H:%M:%S"))
    
    # Refresh button
    if st.button("🔄 Refresh Data", type="primary"):
        st.cache_data.clear()
        st.rerun()
    
    st.markdown("---")
    
    # Charts section
    if not filtered_df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            score_chart = create_score_chart(filtered_df)
            st.plotly_chart(score_chart, use_container_width=True)
        
        with col2:
            sector_chart = create_sector_chart(filtered_df)
            st.plotly_chart(sector_chart, use_container_width=True)
        
        # Signal type chart
        signal_chart = create_signal_type_chart(filtered_df)
        st.plotly_chart(signal_chart, use_container_width=True)
    
    st.markdown("---")
    
    # Startups table
    st.header("📊 Top SaaS Startups")
    
    if filtered_df.empty:
        st.warning("No startups match the selected filters.")
    else:
        # Display startups in a table format
        for idx, startup in filtered_df.iterrows():
            with st.container():
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"""
                    <div class="startup-card">
                        <h3>{startup['name']}</h3>
                        <p><strong>Description:</strong> {startup['description']}</p>
                        <p><strong>Growth Reason:</strong> {startup['growth_reason']}</p>
                        <p><strong>Sector:</strong> {startup['sector']} | 
                           <strong>Stage:</strong> {startup['funding_stage']} | 
                           <strong>Signal:</strong> {startup['signal_type']}</p>
                        <p><strong>Source:</strong> <a href="{startup['source_link']}" target="_blank">{startup['source_link']}</a></p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    score_class = get_score_color(startup['score'])
                    st.markdown(f"""
                    <div class="metric-card">
                        <h2 class="{score_class}">{startup['score']}</h2>
                        <p>Growth Score</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("---")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🚀 SaaS Signal Miner | Powered by Perplexity API</p>
        <p>Data is refreshed every 5 minutes. Use the refresh button for latest results.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 