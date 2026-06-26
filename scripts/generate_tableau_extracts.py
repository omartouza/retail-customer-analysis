import pandas as pd
import getpass, os
from pathlib import Path
from sqlalchemy import create_engine

username = getpass.getuser()
engine = create_engine(f'postgresql+psycopg2://{username}@localhost:5432/retail_db', future=True)

# Output folder for Tableau inputs (under dashboard/). Anchor to this script's
# own location so it runs from any working directory; scripts/ sits one level
# below the repo root.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUT = str(PROJECT_ROOT / 'dashboard' / 'tableau_data')
os.makedirs(OUT, exist_ok=True)

# 1. Customer-level file: RFM segments + CLV predictions joined into one table.
#    We pull only the non-overlapping CLV columns (RFM already has recency/frequency/monetary,
#    defined differently — so we keep RFM's and add CLV's forward-looking fields).
rfm = pd.read_sql('SELECT * FROM rfm_segments', engine)
clv = pd.read_sql('SELECT customer_id, predicted_purchases_90d, prob_alive, '
                  'exp_avg_value, clv_12m FROM clv_predictions', engine)
customers = rfm.merge(clv, on='customer_id', how='left')
customers.to_csv(f'{OUT}/customers_dashboard.csv', index=False)
print(f'customers_dashboard.csv: {len(customers):,} rows')

# 2. Market basket rules (already small and dashboard-ready)
rules = pd.read_sql('SELECT * FROM market_basket_rules', engine)
rules.to_csv(f'{OUT}/basket_rules.csv', index=False)
print(f'basket_rules.csv: {len(rules):,} rows')

# 3. Sales summaries — aggregate the big transactions table so Tableau stays fast
tx = pd.read_sql('SELECT invoice, invoicedate, revenue, country, region '
                 'FROM transactions_clean', engine)
tx['invoicedate'] = pd.to_datetime(tx['invoicedate'])
tx['month'] = tx['invoicedate'].dt.to_period('M').astype(str)

monthly = (tx.groupby('month')
             .agg(revenue=('revenue', 'sum'), orders=('invoice', 'nunique'))
             .reset_index())
monthly.to_csv(f'{OUT}/sales_monthly.csv', index=False)
print(f'sales_monthly.csv: {len(monthly):,} rows')

country = (tx.groupby(['country', 'region'])
             .agg(revenue=('revenue', 'sum'), orders=('invoice', 'nunique'))
             .reset_index()
             .sort_values('revenue', ascending=False))
country.to_csv(f'{OUT}/sales_by_country.csv', index=False)
print(f'sales_by_country.csv: {len(country):,} rows')

# 4. Cohort retention — recompute from customers_clean, long format for a Tableau heatmap
cc = pd.read_sql('SELECT customer_id, invoicedate FROM customers_clean', engine)
cc['invoicedate'] = pd.to_datetime(cc['invoicedate'])
cc['invoice_month'] = cc['invoicedate'].dt.to_period('M')
cc['cohort_month'] = cc.groupby('customer_id')['invoicedate'].transform('min').dt.to_period('M')
cc['cohort_index'] = ((cc['invoice_month'].dt.year  - cc['cohort_month'].dt.year) * 12 +
                      (cc['invoice_month'].dt.month - cc['cohort_month'].dt.month))

cohort = (cc.groupby(['cohort_month', 'cohort_index'])['customer_id']
            .nunique().reset_index(name='customers'))
sizes = (cohort[cohort['cohort_index'] == 0][['cohort_month', 'customers']]
         .rename(columns={'customers': 'cohort_size'}))
cohort = cohort.merge(sizes, on='cohort_month')
cohort['retention_rate'] = cohort['customers'] / cohort['cohort_size']
cohort['cohort_month'] = cohort['cohort_month'].astype(str)
cohort.to_csv(f'{OUT}/cohort_retention.csv', index=False)
print(f'cohort_retention.csv: {len(cohort):,} rows')

print('\nAll extracts written to', OUT)