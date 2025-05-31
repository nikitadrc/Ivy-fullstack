# frontend/components/analytics_dashboard.py

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

def load_interaction_data(data_path="data/interaction_logs.csv"):
    """Load candidate interaction data from CSV"""
    try:
        df = pd.read_csv(data_path, parse_dates=['timestamp'])
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=['candidate_id', 'timestamp', 'question_type', 
                                    'question', 'answer', 'score', 'feedback', 
                                    'sentiment', 'duration_seconds'])

def calculate_kpis(df):
    """Calculate key performance indicators"""
    kpis = {
        'total_candidates': df['candidate_id'].nunique(),
        'avg_score': df['score'].mean(),
        'completion_rate': (df.groupby('candidate_id')['question_type'].count() / 15).mean(),
        'avg_duration': df['duration_seconds'].sum() / 3600 / df['candidate_id'].nunique()
    }
    return kpis

def show_analytics_dashboard():
    """Main function to render the recruiter analytics dashboard"""
    st.title("Recruiter Analytics Dashboard")
    
    # Load data
    df = load_interaction_data()
    
    if df.empty:
        st.warning("No interaction data available yet.")
        return
    
    # Add filters
    st.sidebar.header("Filters")
    date_range = st.sidebar.date_input("Select date range", 
                                      [df['timestamp'].min().date(), 
                                       df['timestamp'].max().date()])
    
    question_type_filter = st.sidebar.multiselect(
        "Question Type",
        options=df['question_type'].unique(),
        default=df['question_type'].unique()
    )
    
    # Apply filters
    filtered_df = df[
        (df['timestamp'].dt.date >= date_range[0]) & 
        (df['timestamp'].dt.date <= date_range[1]) &
        (df['question_type'].isin(question_type_filter))
    ]
    
    # Calculate KPIs
    kpis = calculate_kpis(filtered_df)
    
    # KPI Display
    st.subheader("Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Candidates", kpis['total_candidates'])
    with col2:
        st.metric("Average Score", f"{kpis['avg_score']:.1f}/5")
    with col3:
        st.metric("Completion Rate", f"{kpis['completion_rate']:.0%}")
    with col4:
        st.metric("Avg Time per Candidate", f"{kpis['avg_duration']:.1f} hours")
    
    # Visualization Section
    st.subheader("Performance Analysis")
    
    # Score Distribution
    fig1 = px.histogram(filtered_df, x='score', 
                       title="Score Distribution",
                       labels={'score': 'Score (1-5)'})
    st.plotly_chart(fig1, use_container_width=True)
    
    # Performance Over Time
    time_df = filtered_df.groupby(pd.Grouper(key='timestamp', freq='D'))['score'].mean().reset_index()
    fig2 = px.line(time_df, x='timestamp', y='score', 
                  title="Average Score Trend Over Time")
    st.plotly_chart(fig2, use_container_width=True)
    
    # Question Analysis
    st.subheader("Question Insights")
    
    # Hardest Questions
    question_stats = filtered_df.groupby('question').agg({
        'score': 'mean',
        'candidate_id': 'nunique'
    }).reset_index().rename(columns={'candidate_id': 'attempts'})
    
    hardest_questions = question_stats.sort_values('score').head(5)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("Most Challenging Questions")
        st.dataframe(hardest_questions[['question', 'score', 'attempts']]
                    .set_index('question'),
                    use_container_width=True)
    
    # Sentiment Analysis
    if 'sentiment' in filtered_df.columns:
        with col2:
            sentiment_counts = filtered_df['sentiment'].value_counts().reset_index()
            sentiment_counts.columns = ['sentiment', 'count']
            fig3 = px.pie(sentiment_counts, names='sentiment', values='count',
                         title="Response Sentiment Distribution")
            st.plotly_chart(fig3, use_container_width=True)
    
    # Bottleneck Analysis
    st.subheader("Process Bottlenecks")
    
    # Time per Question Type
    time_analysis = filtered_df.groupby('question_type')['duration_seconds'].mean().reset_index()
    fig4 = px.bar(time_analysis, x='question_type', y='duration_seconds',
                 labels={'duration_seconds': 'Average Time (seconds)'},
                 title="Time Spent per Question Type")
    st.plotly_chart(fig4, use_container_width=True)

if __name__ == "__main__":
    show_analytics_dashboard()
