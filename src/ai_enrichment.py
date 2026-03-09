import pandas as pd
import random

def get_insights_from_llm(text):
    """
    MOCK FUNCTION: Bypasses the Gemini API rate limits for local testing.
    Simulates the LLM's structured JSON output so downstream aggregation works.
    """
    if pd.isna(text) or str(text).strip() == "":
        return {"sentiment": "Neutral", "theme": "Unknown", "confidence": 0.0}

    themes = ["Bug/Issue", "Feature Request", "Pricing/Billing", "Customer Support", "Usability/UX", "General Praise", "Other"]
    sentiments = ["Positive", "Neutral", "Negative"]
    
    return {
        "sentiment": random.choice(sentiments),
        "theme": random.choice(themes),
        "confidence": round(random.uniform(0.75, 0.99), 2)
    }

def enrich_data(df, text_column):
    """
    Applies the MOCK LLM extraction to a specific text column in a DataFrame.
    """
    print(f"Enriching {len(df)} rows using MOCK API for column: '{text_column}'...")
    
    sentiments = []
    themes = []
    confidences = []
    
    for index, row in df.iterrows():
        text = row[text_column]
        insights = get_insights_from_llm(text)
        
        sentiments.append(insights.get("sentiment"))
        themes.append(insights.get("theme"))
        confidences.append(insights.get("confidence"))
        
    df['ai_sentiment'] = sentiments
    df['ai_theme'] = themes
    df['ai_confidence_score'] = confidences
    
    return df