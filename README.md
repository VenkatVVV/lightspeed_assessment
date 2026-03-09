# Lightspeed Merchant Feedback Pipeline

This repository contains a data pipeline designed to ingest, clean, enrich, and aggregate multi-channel customer feedback into a unified "Merchant 360" view. 

## Setup Instructions
1. Clone this repository.
2. Install the required dependencies: `pip install -r requirements.txt` (requires `pandas`, `google-generativeai`, `python-dotenv`).
3. Create a `.env` file in the root directory based on the provided `.env.example`.
4. Add your API key and configure the dataset size in your `.env` file: 
   * `GEMINI_API_KEY="your_api_key_here"`
   * `NUM_EXAMPLES=15` *(Controls how many synthetic rows are generated per source)*
5. **Generate the synthetic data:** Run `python generate_synthetic_data.py`. This will automatically create the `data/raw/` directory and populate it with mock CSV datasets containing intentional data quality issues scaled to your `NUM_EXAMPLES` parameter.
6. **Run the pipeline:** Execute `python main.py` to run the end-to-end ingestion, cleaning, AI enrichment, and aggregation process. The final dataset will be exported to `data/processed/merchant_360.csv`.

---

## Pipeline Architecture



The pipeline is modularly designed into four distinct phases to ensure scalability and ease of debugging:
1. **Ingest (`src/ingest.py`)**: Safely loads raw CSV files with error handling for missing files.
2. **Clean & Normalize (`src/clean.py`)**: Applies deterministic rules to handle data quality issues (deduplication, date normalization, null handling).
3. **AI Enrichment (`src/ai_enrichment.py`)**: Passes unstructured text to the Gemini API to extract `Sentiment`, `Theme`, and a `Confidence Score`. *(Note: Contains a mock fallback to handle free-tier API rate limits).*
4. **Aggregate (`src/aggregate.py`)**: Merges the enriched datasets using a shared `merchant_id` via a SQL-style outer join to create a unified view.

---

## Data Sources & Assumptions
For this assessment, I created a script (`generate_synthetic_data.py`) that generates three synthetic datasets (`app_reviews.csv`, `support_tickets.csv`, `nps_surveys.csv`) mimicking real-world "dirty" data. 
* **Assumption 1**: `merchant_id` serves as the primary key across all systems.
* **Assumption 2**: External system syncs are imperfect. The data contains duplicate records, missing IDs, and varying date formats (ISO, MM/DD/YYYY) that must be reconciled prior to AI analysis.

---

## Automation vs. AI: 
I utilized a "Path of Least Resistance" approach, strictly separating deterministic data transformations from probabilistic AI tasks.

* **Where I used Automation (Pandas)**: Data cleansing, deduplication, date normalization, and table joins. Code is cheaper, faster, and 100% deterministic for these tasks. Using an LLM to join tables or format dates introduces unnecessary latency and risk.
* **Where I used AI (Gemini 2.5 Flash)**: Unstructured text analysis. I leveraged the LLM specifically to read `review_text` and `support_descriptions` to categorize Sentiment and extract Themes—tasks that would otherwise require complex, brittle regex or manual human review.

---

## Handling Data Quality & Anomalies
Anticipating messy data, the `clean.py` module includes specific mitigations:
* **Null Handling**: Rows missing a `merchant_id` in App Reviews are explicitly dropped and logged, as they cannot be tied back to the unified merchant view.
* **Format Coercion**: Used `pd.to_datetime(errors='coerce')` and `pd.to_numeric(errors='coerce')` to gracefully handle completely mangled string inputs without crashing the pipeline.
* **Deduplication**: Applied strict `.drop_duplicates()` on support tickets to account for potential double-firing from external CRM webhooks.

---

## AI Governance: Mitigating Hallucinations
As an AI Enablement Specialist, managing LLM reliability is critical. I handled the risk of inaccurate summaries and hallucinations through three technical guardrails:
1. **Strict Output Formatting**: The prompt engineered in `ai_enrichment.py` forces the LLM to return only a JSON object with constrained categorical variables (e.g., Sentiment must be exactly Positive, Neutral, or Negative).
2. **Confidence Scoring**: The prompt instructs the model to generate a confidence score (0.0 - 1.0) for its extraction.
3. **Graceful Fallbacks**: The Python script wraps the API call in a `try/except` block. If the model hallucinates a non-JSON response or times out, the pipeline catches the error and defaults the row to `{"sentiment": "Error", "theme": "Error", "confidence": 0.0}` to prevent pipeline failure and flag the row for human-in-the-loop review.

---

## Extensibility
The pipeline is designed for high extensibility. If Lightspeed acquires a new company and needs to integrate their distinct CRM data:
1. We add a `clean_new_crm()` function to `src/clean.py`.
2. We pass the text column through the existing `enrich_data()` function.
3. We add a single `merge` statement in `src/aggregate.py`. 
No core AI or architectural logic needs to be rewritten.