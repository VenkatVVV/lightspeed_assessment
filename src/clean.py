import pandas as pd

def normalize_date(date_series):
    return pd.to_datetime(date_series, errors='coerce').dt.strftime('%Y-%m-%d')

def clean_app_reviews(df):
    print("Cleaning App Store Reviews...")
    initial_count = len(df)
    df_clean = df.dropna(subset=['merchant_id']).copy()
    dropped_count = initial_count - len(df_clean)
    if dropped_count > 0:
        print(f"  -> Dropped {dropped_count} rows with missing 'merchant_id'")

    df_clean['date'] = normalize_date(df_clean['date'])
    df_clean['platform'] = df_clean['platform'].astype(str).str.strip().str.lower()
    return df_clean

def clean_support_tickets(df):
    print("Cleaning Support Tickets...")
    initial_count = len(df)
    df_clean = df.drop_duplicates().copy()
    dup_count = initial_count - len(df_clean)
    if dup_count > 0:
        print(f"  -> Removed {dup_count} duplicate rows")

    df_clean = df_clean.dropna(subset=['merchant_id'])
    df_clean['created_at'] = normalize_date(df_clean['created_at'])
    df_clean['category'] = df_clean['category'].astype(str).str.strip().str.title()
    return df_clean

def clean_nps_surveys(df):
    print("Cleaning NPS Surveys...")
    df_clean = df.dropna(subset=['merchant_id']).copy()
    df_clean['survey_date'] = normalize_date(df_clean['survey_date'])
    df_clean['score'] = pd.to_numeric(df_clean['score'], errors='coerce')
    return df_clean