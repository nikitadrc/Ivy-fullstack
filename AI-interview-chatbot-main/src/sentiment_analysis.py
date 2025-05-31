# src/sentiment_analysis.py

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def get_sia():
    """
    Singleton loader for VADER SentimentIntensityAnalyzer.
    Downloads lexicon if needed.
    """
    try:
        nltk.data.find('sentiment/vader_lexicon.zip')
    except LookupError:
        nltk.download('vader_lexicon')
    return SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    """
    Analyze the sentiment of a given text using VADER.

    Args:
        text (str): The text to analyze.

    Returns:
        dict: {
            'compound': float,  # Overall sentiment score [-1, 1]
            'label': str,       # 'Positive', 'Neutral', or 'Negative'
            'pos': float,       # Probability of positive sentiment
            'neu': float,       # Probability of neutral sentiment
            'neg': float        # Probability of negative sentiment
        }
    """
    if not isinstance(text, str) or not text.strip():
        return {
            'compound': 0.0,
            'label': 'Neutral',
            'pos': 0.0,
            'neu': 1.0,
            'neg': 0.0
        }
    sia = get_sia()
    scores = sia.polarity_scores(text)
    compound = scores['compound']
    # Assign a label based on compound score
    if compound >= 0.05:
        label = 'Positive'
    elif compound <= -0.05:
        label = 'Negative'
    else:
        label = 'Neutral'
    return {
        'compound': compound,
        'label': label,
        'pos': scores['pos'],
        'neu': scores['neu'],
        'neg': scores['neg']
    }

# Example usage (for testing/demo)
if __name__ == "__main__":
    test_texts = [
        "I am excited about this opportunity!",
        "I'm not sure if I understand the question.",
        "This process is frustrating and unclear.",
        "",
        None
    ]
    for t in test_texts:
        result = analyze_sentiment(t)
        print(f"Text: {repr(t)}\nSentiment: {result['label']}, Score: {result['compound']}\n")

