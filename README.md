# Lightspeed Merchant Feedback Pipeline

This repository contains a data pipeline designed to ingest, clean, enrich, and aggregate multi-channel customer feedback into a unified "Merchant 360" view. 

## Setup Instructions
1. Clone this repository.
2. Install the required dependencies: 
   `pip install pandas google-generativeai python-dotenv matplotlib seaborn`
3. Create a `.env` file in the root directory based on the provided `.env.example`.
4. Configure your `.env` file: 
   * `GEMINI_API_KEY="your_api_key_here"`
   * `NUM_EXAMPLES=15` *(Controls the synthetic dataset scale)*
5. **Generate the synthetic data:** Run `python generate_synthetic_data.py`. This creates the `data/raw/` directory with mock CSVs containing intentional data quality issues.
6. **Run the pipeline:** Execute `python main.py`. This runs the ingestion, cleaning, AI enrichment, aggregation, and **automatically generates visual charts**.

---

## Pipeline Architecture



The pipeline is modularly designed into five distinct phases:
1. **Ingest**: Safely loads raw CSV files.
2. **Clean & Normalize**: Applies deterministic rules for deduplication and date normalization.
3. **AI Enrichment**: Uses Gemini 2.5 Flash to extract `Sentiment`, `Theme`, and a `Confidence Score` from unstructured text.
4. **Aggregate**: Executes a SQL-style join on `merchant_id` to create the unified Merchant 360 table.
5. **Visualize**: Automatically generates PNG charts in `data/visuals/` for stakeholder reporting.

---

## Data Visualization & Insights
The pipeline doesn't just output a CSV; it generates automated reporting to help Product Managers and Support Leads identify trends at a glance.



* **NPS Distribution**: Visualizes the average sentiment across the merchant base.
* **Ticket Health**: Compares total ticket volume against unresolved issues to highlight merchant friction points.
* **Correlation Analysis**: Maps App Store ratings against NPS scores to validate cross-platform customer satisfaction.

---

## AI Governance: Mitigating Hallucinations
As an AI Enablement Specialist, managing LLM reliability is critical. I handled the risk of inaccurate summaries through three technical guardrails:
1. **Strict Output Formatting**: The prompt forces the LLM to return a rigid JSON object with constrained categorical variables.
2. **Confidence Scoring**: The model is instructed to generate a confidence metric (0.0 - 1.0) for every extraction.
3. **Graceful Fallbacks**: The script includes a `try/except` block and a Mock API fallback to maintain pipeline continuity during API rate-limiting or outages.

---

## Extensibility & Scalability
The architecture is designed for "Separation of Concerns." To scale this to an enterprise level:
* **Configuration-Driven**: Transition from hard-coded cleaning scripts to a metadata-driven ingestion layer.
* **Cloud Native**: Deploy the Python modules as Cloud Functions or Airflow DAGs within GCP/BigQuery for processing millions of records.
* **A/B Testing**: Implement side-by-side prompt versioning to refine theme extraction as business contexts evolve.
