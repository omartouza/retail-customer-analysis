# Retail Customer Analysis

End-to-end customer analytics on the **UCI Online Retail II** dataset (1M+ transactions, 5,852 customers, 43 countries). The project moves from raw data to a published interactive dashboard, answering four business questions:

- Who are our customers, and which segments drive revenue?
- How well are we retaining first-time buyers?
- Which customers are most valuable looking forward, and how confident are we?
- Which products get bought together — and what should we bundle?

**🔗 Interactive dashboard (Tableau Public):** [Retail Customer Analysis dashboard](https://public.tableau.com/app/profile/touzani.omar/viz/retail_customer_analysis_17810347677650/d_sales)

---

## Headline findings

- **£20M revenue across 39,516 orders.** 86% from the UK; meaningful long tail across 42 other countries.
- **1 in 5 first-time buyers returns the next month.** Retention stabilises around 15% long-run — the analysis isolates this from a Dec 2009 cohort artifact reflecting a pre-existing customer base.
- **The top two segments (Champions + Loyal Customers) drive ~79% of revenue from ~34% of the base.** Classic Pareto concentration.
- **Champions are predicted to be worth ~£5,244 each over the next 12 months — 24× a Hibernating customer.** The BG/NBD + Gamma-Gamma model was validated against a held-out period (+8% holdout error).
- **The Regency tea range dominates product affinity.** The cakestand + rose teacup + green teacup combination is bought together at **15× the rate chance would predict.** 242 association rules surfaced; 42 are "strong" (≥50% confidence).

---

## Methodology

Eight phases, each with a documented notebook and a one-page stakeholder PDF report.

| Phase | Notebook | Output |
|---|---|---|
| 1. Exploration | `01_eda.ipynb` | Dataset shape, quality issues, scope decisions |
| 2. Cleaning + DB load | `02_data_cleaning.ipynb` | `transactions_clean`, `customers_clean`, `returns` (94% retention) |
| 3. Cohort retention | `03_cohort_analysis.ipynb` | Monthly cohort matrix, retention curve |
| 4. RFM segmentation | `04_rfm_segmentation.ipynb` | 10 named segments, customer-revenue concentration |
| 5. CLV prediction | `05_clv_modeling.ipynb` | BG/NBD + Gamma-Gamma, 12-month forward CLV per customer |
| 6. Market basket | `06_market_basket.ipynb` | Apriori (cross-checked with FP-Growth), 242 association rules |
| 7. Dashboard | Tableau Public | 5-page interactive dashboard with navigation |
| 8. Packaging | This repo | Reproducible end-to-end pipeline |

**Per-phase PDF reports** are in `Reports/` — one page each, plain-language summary plus a key visual. These are the artifacts a non-technical stakeholder would actually read.

---

## What this project demonstrates

- **End-to-end data work** — ingestion → cleaning → multiple modelling approaches → communication via dashboard and reports.
- **Methodological rigor** — every classification/CLV model evaluated systematically (confusion matrix → per-class recall → AUC-ROC), not by a single headline metric. Apriori cross-checked with FP-Growth to confirm pattern stability. CLV reliability bounded by frequency to avoid single-purchase phantoms.
- **Analytical honesty** — Dec 2009 cohort artifact identified and excluded from headline retention figures, with the caveat documented in both notebook and dashboard. AOV reported as the genuine skewed mean rather than a cherry-picked subset.
- **Clear communication** — the same findings expressed at three levels: notebook (technical), one-page PDF (stakeholder), interactive dashboard (executive).

---

## Tech stack

- **Python 3.11** — pandas, numpy, matplotlib, sqlalchemy, lifetimes, mlxtend, reportlab
- **PostgreSQL** — source-of-truth tables for all downstream analyses
- **Tableau Public** — final interactive dashboard
- **Git / GitHub** — version control

---

## Project structure

```
retail-customer-analysis/
├── README.md
├── requirements.txt
├── .gitignore
│
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_cohort_analysis.ipynb
│   ├── 04_rfm_segmentation.ipynb
│   ├── 05_clv_modeling.ipynb
│   ├── 06_market_basket.ipynb
│   └── generate_tableau_extracts.py
│
├── Reports/
│   ├── 01_EDA_report.pdf
│   ├── 02_data_cleaning_report.pdf
│   ├── 03_cohort_analysis_report.pdf
│   ├── 04_RFM_segmentation_report.pdf
│   ├── 05_CLV_report.pdf
│   └── 06_market_basket_report.pdf
│
├── dashboard/
│   └── tableau_data/        # CSV extracts feeding the Tableau workbook
│
├── data/                    # gitignored — see "Reproducing" below
│   ├── raw/
│   └── processed/
│
└── sql/
```

---

## Reproducing the analysis

The raw dataset is gitignored (~44 MB). To reproduce locally:

**1. Download the data**

Get `online_retail_II.xlsx` from the [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/502/online+retail+ii) and place it in `data/raw/`.

**2. Set up PostgreSQL**

The notebooks use a local PostgreSQL database called `retail_db` with trust authentication (no password). On Mac:

```bash
brew install postgresql@16
brew services start postgresql@16
createdb retail_db
```

**3. Install Python dependencies**

```bash
pip install -r requirements.txt
```

**4. Run the notebooks in order**

```bash
cd notebooks/
jupyter notebook
```

Execute `01_eda.ipynb` through `06_market_basket.ipynb` sequentially. Each phase reads from the previous phase's database tables.

**5. Refresh Tableau extracts (optional)**

```bash
cd notebooks/
python generate_tableau_extracts.py
```

This regenerates the five CSVs in `dashboard/tableau_data/` that feed the Tableau workbook.

---

## Author

**Omar Touzani** — data analyst building toward remote analytics roles.

- GitHub: [omartouza](https://github.com/omartouza)
- Tableau Public: [touzani.omar](https://public.tableau.com/app/profile/touzani.omar)

---

## License

Code: MIT. Dataset: UCI Online Retail II — see [original license](https://archive.ics.uci.edu/dataset/502/online+retail+ii).
