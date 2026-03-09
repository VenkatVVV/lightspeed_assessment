import os
import pandas as pd
from src.ingest import load_data
from src.clean import clean_app_reviews, clean_support_tickets, clean_nps_surveys
from src.ai_enrichment import enrich_data
from src.aggregate import build_merchant_360
from src.visualize import generate_charts

def run_pipeline():
    print("=== Starting Lightspeed Feedback Pipeline ===\n")

    # Ensure the data directories exist
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)

    # ---------------------------------------------------------
    # Step 1: Data Ingestion
    # ---------------------------------------------------------
    print("--- Step 1: Data Ingestion ---")
    # Assuming you placed the generated synthetic CSVs in the data/raw folder
    raw_reviews = load_data('data/raw/app_reviews.csv')
    raw_tickets = load_data('data/raw/support_tickets.csv')
    raw_nps = load_data('data/raw/nps_surveys.csv')
    print("\n")

    # ---------------------------------------------------------
    # Step 2: Data Cleaning & Normalization
    # ---------------------------------------------------------
    print("--- Step 2: Data Cleaning & Normalization ---")
    clean_reviews = clean_app_reviews(raw_reviews)
    clean_tickets = clean_support_tickets(raw_tickets)
    clean_nps = clean_nps_surveys(raw_nps)

    clean_reviews.to_csv('data/processed/clean_reviews.csv', index=False)
    clean_tickets.to_csv('data/processed/clean_tickets.csv', index=False)
    clean_nps.to_csv('data/processed/clean_nps.csv', index=False)
    print("\n")

    # ---------------------------------------------------------
    # Step 3: AI Enrichment (Sentiment & Theme Extraction)
    # ---------------------------------------------------------
    print("--- Step 3: AI Enrichment (Gemini API) ---")
    # We pass the specific text column we want the LLM to analyze for each dataset
    enriched_reviews = enrich_data(clean_reviews, 'review_text')
    enriched_tickets = enrich_data(clean_tickets, 'description')
    enriched_nps = enrich_data(clean_nps, 'feedback_text')
    print("\n")

    # ---------------------------------------------------------
    # Step 4: Aggregation (The Merchant 360 View)
    # ---------------------------------------------------------
    print("--- Step 4: Aggregation ---")
    merchant_360_df = build_merchant_360(enriched_reviews, enriched_tickets, enriched_nps)
    
    # ---------------------------------------------------------
    # Step 5: Export
    # ---------------------------------------------------------
    output_path = 'data/processed/merchant_360.csv'
    merchant_360_df.to_csv(output_path, index=False)
    print(f"\n=== Pipeline Complete! Unified dataset saved to {output_path} ===")

    generate_charts('data/processed/merchant_360.csv')
    
    # Display a quick preview in the terminal for the reviewer
    print("\nPreview of Final Merchant 360 Dataset:")
    print(merchant_360_df.head(3))

if __name__ == "__main__":
    run_pipeline()