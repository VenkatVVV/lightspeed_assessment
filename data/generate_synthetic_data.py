import pandas as pd
import random
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import uuid

# 1. Create the target directory if it doesn't exist
output_dir = 'data/raw'
os.makedirs(output_dir, exist_ok=True)

load_dotenv()
try:
    n = int(os.getenv("NUM_EXAMPLES", 15))
except ValueError:
    n = 15

# Set a shared pool of Merchant IDs to ensure overlap across datasets
shared_merchants = ['MERCH-001', 'MERCH-002', 'MERCH-003', 'MERCH-004', 'MERCH-005']

# Helper to generate random dates
def random_date(start_days_ago=30):
    return datetime.now() - timedelta(days=random.randint(0, start_days_ago))

# ---------------------------------------------------------
# 1. App Store Reviews 
# ---------------------------------------------------------
app_reviews = []
for _ in range(n):
    m_id = random.choice(shared_merchants) if random.random() > 0.2 else None
    app_reviews.append({
        'merchant_id': m_id,
        'rating': random.randint(1, 5),
        'review_text': random.choice([
            "Love the new POS interface, super fast!",
            "App keeps crashing when I try to sync inventory.",
            "Great support team, but the analytics dashboard is confusing.",
            "Payment terminal disconnects randomly.",
            "Works perfectly for my retail shop."
        ]),
        'date': random_date().strftime('%Y-%m-%d'), 
        'platform': random.choice(['iOS', 'android', 'IOS ', ' Android']) 
    })

# ---------------------------------------------------------
# 2. Support Tickets 
# ---------------------------------------------------------
support_tickets = []
for _ in range(n):
    support_tickets.append({
        'merchant_id': random.choice(shared_merchants),
        'ticket_id': f"TCK-{uuid.uuid4().hex[:6].upper()}",
        'category': random.choice(['Billing', 'hardware', 'Sync', 'LOGIN']),
        'description': random.choice([
            "Can't log into the back office.",
            "Need help setting up my eCom store.",
            "Card reader isn't pairing with the iPad.",
            "Double charged for my monthly subscription.",
            "How do I export my sales tax report?"
        ]),
        'resolution': random.choice(['Resolved', 'Pending', 'Escalated']),
        'created_at': random_date().strftime('%m/%d/%Y') 
    })
support_tickets.append(support_tickets[0]) # Inject duplicate

# ---------------------------------------------------------
# 3. NPS Surveys 
# ---------------------------------------------------------
nps_surveys = []
for _ in range(n):
    nps_surveys.append({
        'merchant_id': random.choice(shared_merchants),
        'score': random.choice([random.randint(0, 10), str(random.randint(0, 10))]), 
        'feedback_text': random.choice([
            "The offline mode saved us during a power outage.",
            "I wish the loyalty program features were more robust.",
            "Setup was a breeze, highly recommend.",
            "Still waiting on a feature request from 6 months ago.",
            "Solid system, no complaints."
        ]),
        'survey_date': random_date().isoformat(), 
        'product_area': random.choice(['Payments', 'eCom', 'POS', 'Loyalty'])
    })

# ---------------------------------------------------------
# Export directly to data/raw/
# ---------------------------------------------------------
pd.DataFrame(app_reviews).to_csv(f'{output_dir}/app_reviews.csv', index=False)
pd.DataFrame(support_tickets).to_csv(f'{output_dir}/support_tickets.csv', index=False)
pd.DataFrame(nps_surveys).to_csv(f'{output_dir}/nps_surveys.csv', index=False)

print(f"Synthetic 'dirty' datasets generated successfully in the '{output_dir}' directory.")