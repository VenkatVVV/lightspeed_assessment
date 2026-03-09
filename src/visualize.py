import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def generate_charts(input_csv):
    """
    Reads the final aggregated dataset and generates charts for 
    numerical analysis and trend distribution.
    """
    if not os.path.exists(input_csv):
        print(f"Error: {input_csv} not found. Run the pipeline first.")
        return

    # Load the data
    df = pd.read_csv(input_csv)
    
    # Set the visual style
    sns.set_theme(style="whitegrid")
    output_dir = 'data/visuals'
    os.makedirs(output_dir, exist_ok=True)

    # 1. Merchant NPS Scores (Bar Chart)
    plt.figure(figsize=(10, 6))
    sns.barplot(x='merchant_id', y='avg_nps_score', data=df, palette='viridis')
    plt.title('Average NPS Score by Merchant', fontsize=15)
    plt.ylabel('NPS Score (0-10)')
    plt.xlabel('Merchant ID')
    plt.ylim(0, 10)
    plt.savefig(f'{output_dir}/nps_scores.png')
    print(f"Generated: {output_dir}/nps_scores.png")

    # 2. Support Ticket Volume vs. Unresolved (Grouped Bar)
    plt.figure(figsize=(10, 6))
    df_melted = df.melt(id_vars='merchant_id', value_vars=['ticket_count', 'unresolved_tickets'], 
                        var_name='Ticket Status', value_name='Count')
    sns.barplot(x='merchant_id', y='Count', hue='Ticket Status', data=df_melted)
    plt.title('Support Ticket Distribution', fontsize=15)
    plt.savefig(f'{output_dir}/ticket_distribution.png')
    print(f"Generated: {output_dir}/ticket_distribution.png")

    # 3. Sentiment vs. Rating Correlation (Scatter)
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x='avg_app_rating', y='avg_nps_score', size='review_count', 
                    hue='top_nps_sentiment', data=df, sizes=(100, 500), alpha=0.7)
    plt.title('App Rating vs. NPS Score Correlation', fontsize=15)
    plt.savefig(f'{output_dir}/rating_correlation.png')
    print(f"Generated: {output_dir}/rating_correlation.png")

if __name__ == "__main__":
    # If running as a standalone script for testing
    generate_charts('data/processed/merchant_360.csv')