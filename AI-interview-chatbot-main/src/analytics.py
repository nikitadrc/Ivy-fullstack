# src/analytics.py

import pandas as pd
from datetime import datetime

def load_interaction_data(data_path="data/interaction_logs.csv"):
    """
    Load candidate interaction data from CSV.
    Returns a pandas DataFrame.
    """
    try:
        df = pd.read_csv(data_path, parse_dates=['timestamp'])
        return df
    except FileNotFoundError:
        # Return empty DataFrame with expected columns if file doesn't exist
        columns = ['candidate_id', 'timestamp', 'question_type', 
                   'question', 'answer', 'score', 'feedback', 
                   'sentiment', 'duration_seconds']
        return pd.DataFrame(columns=columns)

def get_kpis(df):
    """
    Calculate key performance indicators from the DataFrame.
    Returns a dictionary of KPIs.
    """
    if df.empty:
        return {
            'total_candidates': 0,
            'avg_score': 0,
            'completion_rate': 0,
            'avg_duration': 0
        }
    total_candidates = df['candidate_id'].nunique()
    avg_score = df['score'].mean() if 'score' in df else 0
    # Assuming each candidate should answer the same number of questions
    questions_per_candidate = df.groupby('candidate_id')['question'].count()
    expected_questions = questions_per_candidate.max() if not questions_per_candidate.empty else 1
    completion_rate = (questions_per_candidate / expected_questions).mean() if expected_questions else 0
    avg_duration = df.groupby('candidate_id')['duration_seconds'].sum().mean() / 60 if 'duration_seconds' in df else 0
    return {
        'total_candidates': total_candidates,
        'avg_score': round(avg_score, 2),
        'completion_rate': round(completion_rate * 100, 1),  # as percentage
        'avg_duration': round(avg_duration, 1)  # in minutes
    }

def score_distribution(df):
    """
    Return a Series representing the distribution of scores.
    """
    if 'score' in df:
        return df['score'].dropna()
    return pd.Series([])

def average_score_over_time(df):
    """
    Return a DataFrame with average score per day.
    """
    if df.empty or 'timestamp' not in df or 'score' not in df:
        return pd.DataFrame()
    df = df.dropna(subset=['timestamp', 'score'])
    df['date'] = df['timestamp'].dt.date
    return df.groupby('date')['score'].mean().reset_index()

def hardest_questions(df, top_n=5):
    """
    Return the top N hardest questions (lowest average score).
    """
    if df.empty or 'question' not in df or 'score' not in df:
        return pd.DataFrame()
    q_stats = df.groupby('question').agg(
        avg_score=('score', 'mean'),
        attempts=('candidate_id', 'nunique')
    ).reset_index()
    return q_stats.sort_values('avg_score').head(top_n)

def sentiment_distribution(df):
    """
    Return a Series with sentiment counts.
    """
    if 'sentiment' in df:
        return df['sentiment'].value_counts()
    return pd.Series([])

def time_per_question_type(df):
    """
    Return a DataFrame with average time spent per question type.
    """
    if 'question_type' in df and 'duration_seconds' in df:
        return df.groupby('question_type')['duration_seconds'].mean().reset_index()
    return pd.DataFrame()

# Example usage (for testing/demo)
if __name__ == "__main__":
    df = load_interaction_data()
    print("KPIs:", get_kpis(df))
    print("Score Distribution:\n", score_distribution(df).value_counts())
    print("Average Score Over Time:\n", average_score_over_time(df))
    print("Hardest Questions:\n", hardest_questions(df))
    print("Sentiment Distribution:\n", sentiment_distribution(df))
    print("Time per Question Type:\n", time_per_question_type(df))
