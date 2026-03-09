import os
import json
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv
import time

# Load environment variables (API Key)
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize the Gemini model
# We use gemini-2.5-flash as it's fast and cost-effective for bulk text processing
model = genai.GenerativeModel('gemini-2.5-flash')

def get_insights_from_llm(text):
    """
    Passes unstructured text to Gemini to extract Sentiment and Theme.
    Enforces a strict JSON output.
    """
    if pd.isna(text) or str(text).strip() == "":
        return {"sentiment": "Neutral", "theme": "Unknown", "confidence": 0.0}

    prompt = f"""
    You are an expert customer success analyst. Analyze the following customer feedback.
    
    Feedback: "{text}"
    
    Extract the following information and return ONLY a valid JSON object:
    1. "sentiment": Categorize as "Positive", "Neutral", or "Negative".
    2. "theme": Categorize into ONE of the following themes: "Bug/Issue", "Feature Request", "Pricing/Billing", "Customer Support", "Usability/UX", "General Praise", or "Other".
    3. "confidence": A score between 0.0 and 1.0 indicating your confidence in this assessment.
    
    JSON format:
    {{
        "sentiment": "...",
        "theme": "...",
        "confidence": ...
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        # Clean the response text to ensure it's valid JSON (removing markdown blocks if present)
        response_text = response.text.replace('```json\n', '').replace('\n```', '').strip()
        return json.loads(response_text)
    except Exception as e:
        print(f"Error processing text: {text[:30]}... - {e}")
        # Fallback for errors or hallucinations to maintain data pipeline integrity
        return {"sentiment": "Error", "theme": "Error", "confidence": 0.0}

def enrich_data(df, text_column):
    """
    Applies the LLM extraction to a specific text column in a DataFrame.
    """
    print(f"Enriching {len(df)} rows using column: '{text_column}'...")
    
    # Initialize lists to store the new data
    sentiments = []
    themes = []
    confidences = []
    
    for index, row in df.iterrows():
        text = row[text_column]
        insights = get_insights_from_llm(text)
        
        sentiments.append(insights.get("sentiment"))
        themes.append(insights.get("theme"))
        confidences.append(insights.get("confidence"))

        time.sleep(4.1)
        
    # Append the new columns to the dataframe
    df['ai_sentiment'] = sentiments
    df['ai_theme'] = themes
    df['ai_confidence_score'] = confidences
    
    return df