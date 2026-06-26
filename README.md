# Retail Customer Analysis

End-to-end customer analytics on the **UCI Online Retail II** dataset (1M+ transactions, 5,852 customers, 43 countries). The project moves from raw data to a published interactive dashboard, answering four business questions:

- Who are our customers, and which segments drive revenue?
- How well are we retaining first-time buyers?
- Which customers are most valuable looking forward, and how confident are we?
- Which products get bought together — and what should we bundle?

**🔗 Interactive dashboard (Tableau Public):** [Retail Customer Analysis dashboard](https://public.tableau.com/app/profile/touzani.omar/viz/retail_customer_analysis_17810347677650/d_sales)

---

## Headline findings

- **£20M revenue across 39,516 orders.** 86% from the UK; a long tail across the other 42 of 43 countries.
- **1 in 5 first-time buyers returns the next month.** Retention stabilises around 15% long-run — the analysis isolates this from a Dec 2009 cohort artifact reflecting a pre-existing customer base.
- **The top two segments (Champions + Loyal Customers) drive ~79% of revenue from ~34% of the base.** Classic Pareto concentration.
- **Champions are predicted to be worth ~£5,244 each over the next 12 months — 24× a Hibernating customer.** The BG/NBD + Gamma-Gamma model was validated against a held-out period (+8% holdout error).
- **The Regency tea range dominates product affinity.** The cakestand + rose teacup + green teacup combination is bought together at **15× the rate chance would predict.** 242 association rules surfaced; 42 are "strong" (≥50% confidence).

---

## Methodology

Six analytical phases, each with a documented notebook and a one-page stakeholder PDF report, plus a published Tableau dashboard and this reproducibility packaging.

| Phase | Notebook | Output |
|---|---|---|
| 1. Exploration | `01_eda.ipynb` | Dataset shape, quality issues, scope decisions |
| 2. Cleaning + DB load | `02_data_cleaning.ipynb` | `transactions_clean`, `customers_clean`, `returns` (94% of rows retained) |
| 3. Cohort retention | `03_cohort_analysis.ipynb` | Monthly cohort matrix, retention curve |
| 4. RFM segmentation | `04_rfm_segmentation.ipynb` | 10 named segments, customer-revenue concentration |
| 5. CLV prediction | `05_clv_modeling.ipynb` | BG/NBD + Gamma-Gamma, 12-month forward CLV per customer |
| 6. Market basket | `06_market_basket.ipynb` | Apriori (cross-checked with FP-Growth), 242 association rules |
| 7. Dashboard | Tableau Public | 5-page interactive dashboard with navigation |
| 8. Packaging | This repo | Reproducible pipeline: portable paths, pinned deps, checksums, CI |

**Per-phase PDF reports** are in `Reports/` — one page each, plain-language summary plus a key visual. These are the artifacts a non-technical stakeholder would actually read.

---

## What this project demonstrates

- **End-to-end data work** — ingestion → cleaning → multiple modelling approaches → communication via dashboard and reports.
- **Methodological rigor** — CLV validated against a held-out period rather than trusted blindly, and its reliability bounded by purchase frequency to avoid single-purchase phantoms. Apriori cross-checked with FP-Growth (identical itemsets) to confirm the patterns are algorithm-independent, not artifacts.
- **Analytical honesty** — Dec 2009 cohort artifact identified and excluded from headline retention figures, with the caveat documented in both notebook and dashboard. AOV reported as the genuine skewed mean rather than a cherry-picked subset.
- **Clear communication** — the same findings expressed at three levels: notebook (technical), one-page PDF (stakeholder), interactive dashboard (executive).

---

## Tech stack

- **Python 3.11** — pandas, numpy, matplotlib, seaborn, sqlalchemy, lifetimes, mlxtend (the PDF reports were generated with reportlab, which isn't needed to reproduce the analysis)
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
│   └── 06_market_basket.ipynb
│
├── Reports/
│   ├── 01_EDA_report.pdf
│   ├── 02_data_cleaning_report.pdf
│   ├── 03_cohort_analysis_report.pdf
│   ├── 04_RFM_segmentation_report.pdf
│   ├── 05_CLV_report.pdf
│   └── 06_market_basket_report.pdf
│
├── scripts/
│   └── generate_tableau_extracts.py   # Rebuilds the dashboard CSVs from PostgreSQL
│
├── dashboard/
│   └── tableau_data/        # CSV extracts feeding the Tableau workbook
│
└── data/                    # gitignored — see "Reproducing" below
    ├── raw/
    └── processed/
```

---

## Reproducing the analysis

The raw dataset is gitignored (~44 MB). To reproduce locally:

**1. Download the data**

Get `online_retail_II.xlsx` from the [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/502/online+retail+ii) and place it in `data/raw/`.

Phases 1 and 2 print a SHA-256 checksum for the raw file before processing. If yours differs, you have a different version of the data and results may differ:

| File | SHA-256 (first 12) |
|------|--------------------|
| online_retail_II.xlsx | `bcbe73b35f5b` |

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

> `openpyxl` is required to read the `.xlsx` source, and the CLV phase pins `lifetimes==0.11.3` with its `scipy` dependency (runs on Python 3.11). There is no randomness to seed anywhere in the project: RFM uses `qcut` on ranked values, CLV uses fixed-penalizer maximum-likelihood fits, and the market basket uses Apriori (cross-checked against FP-Growth, identical itemsets).

**4. Run the notebooks in order**

Run `notebooks/01_eda.ipynb` through `06_market_basket.ipynb` in order, each from inside the repository. Phase 2 loads the cleaned tables into PostgreSQL; Phases 3–6 read from them.

**5. Refresh Tableau extracts (optional)**

```bash
python scripts/generate_tableau_extracts.py
```

This regenerates the five CSVs in `dashboard/tableau_data/` (customers, basket rules, monthly sales, sales by country, cohort retention) that feed the Tableau workbook. It reads from `retail_db`, so it needs steps 2–4 done first.

---

## Author

**Omar Touzani** — data analyst building toward remote analytics roles.

- GitHub: [omartouza](https://github.com/omartouza)
- Tableau Public: [touzani.omar](https://public.tableau.com/app/profile/touzani.omar)

---

## License

Code: MIT. Dataset: UCI Online Retail II — see [original license](https://archive.ics.uci.edu/dataset/502/online+retail+ii).
