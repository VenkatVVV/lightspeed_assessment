import pandas as pd

def build_merchant_360(reviews_df, tickets_df, nps_df):
    """
    Aggregates the three cleaned and AI-enriched datasets into a single 
    unified Merchant 360 view, matching records using the shared 'merchant_id'.
    """
    print("Aggregating data into a unified Merchant 360 dataset...")
    
    # 1. Aggregate App Reviews
    if not reviews_df.empty:
        reviews_agg = reviews_df.groupby('merchant_id').agg(
            avg_app_rating=('rating', 'mean'),
            review_count=('rating', 'count'),
            # Get the most frequent AI theme for reviews using a lambda function
            top_review_theme=('ai_theme', lambda x: x.mode()[0] if not x.mode().empty else 'None')
        ).reset_index()
    else:
        reviews_agg = pd.DataFrame(columns=['merchant_id', 'avg_app_rating', 'review_count', 'top_review_theme'])

    # 2. Aggregate Support Tickets
    if not tickets_df.empty:
        tickets_agg = tickets_df.groupby('merchant_id').agg(
            ticket_count=('ticket_id', 'count'),
            # Count how many tickets are NOT 'Resolved'
            unresolved_tickets=('resolution', lambda x: (x.str.lower() != 'resolved').sum()),
            top_ticket_theme=('ai_theme', lambda x: x.mode()[0] if not x.mode().empty else 'None')
        ).reset_index()
    else:
        tickets_agg = pd.DataFrame(columns=['merchant_id', 'ticket_count', 'unresolved_tickets', 'top_ticket_theme'])

    # 3. Aggregate NPS Surveys
    if not nps_df.empty:
        nps_agg = nps_df.groupby('merchant_id').agg(
            avg_nps_score=('score', 'mean'),
            nps_response_count=('score', 'count'),
            # Get the most frequent AI sentiment
            top_nps_sentiment=('ai_sentiment', lambda x: x.mode()[0] if not x.mode().empty else 'None')
        ).reset_index()
    else:
        nps_agg = pd.DataFrame(columns=['merchant_id', 'avg_nps_score', 'nps_response_count', 'top_nps_sentiment'])

    # 4. Create a master list of all unique merchant IDs across all datasets
    all_merchants = pd.concat([
        reviews_df['merchant_id'], 
        tickets_df['merchant_id'], 
        nps_df['merchant_id']
    ]).drop_duplicates().to_frame('merchant_id')

    # 5. Iteratively left-join the aggregated metrics onto the master list
    unified_df = all_merchants.merge(reviews_agg, on='merchant_id', how='left')
    unified_df = unified_df.merge(tickets_agg, on='merchant_id', how='left')
    unified_df = unified_df.merge(nps_agg, on='merchant_id', how='left')

    # 6. Fill NaN values for count columns with 0
    counts_cols = ['review_count', 'ticket_count', 'unresolved_tickets', 'nps_response_count']
    unified_df[counts_cols] = unified_df[counts_cols].fillna(0)
    
    # Optional: Round the averages for cleaner presentation
    unified_df['avg_app_rating'] = unified_df['avg_app_rating'].round(2)
    unified_df['avg_nps_score'] = unified_df['avg_nps_score'].round(2)

    return unified_df