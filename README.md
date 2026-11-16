# Pharmacy Watchlist Analytics Pipeline

## Overview

The Pharmacy Watchlist Analytics Pipeline is a Python-based data analytics project designed to streamline the monthly process of identifying newly added pharmacies, determining network participation, and analyzing pharmacy claims activity.

The project is modeled after a real-world healthcare analytics workflow and uses entirely synthetic data to demonstrate how Python and pandas can be applied to automate repetitive data preparation, data validation, aggregation, and reporting tasks.

The goal is to reduce manual spreadsheet work, improve consistency, and create a more reproducible reporting process.

## Project Objectives

This project aims to:

- Identify pharmacies added to a watchlist during a selected reporting month.
- Determine pharmacy participation by matching pharmacy identifiers against an enrollment directory.
- Prepare pharmacy identifiers and reporting dates for claims extraction.
- Process claims data, apply business rules, and calculate claim counts and total plan-paid amounts.
- Generate structured Excel reports and client-facing PowerPoint presentations.
- Incorporate data validation and quality checks to improve reporting accuracy.

## Technology Stack

- **Python** – Core programming language
- **Pandas** – Data manipulation, merging, and aggregation
- **OpenPyXL** – Excel workbook processing and formatting
- **Python-pptx** – PowerPoint report generation
- **Git & GitHub** – Version control and project management

## Current Capabilities

### Synthetic Data Generation

- Configurable synthetic pharmacy enrollment directory generation.
- Monthly pharmacy watchlist generation.
- Synthetic pharmacy names and test identifiers.
- Configurable watchlist reasons and associated review details.
- Weighted random selection of watchlist categories.
- Reproducible data generation using configurable random seeds.
- Excel export of generated datasets.
- Initial data-quality validation, including record counts, NPI uniqueness, and network participation counts.

### Claims Processing and Analytics

- Loading synthetic Cognos claims exports from Excel.
- Identifying and excluding `SB393 TEST` claims using normalized member names.
- Aggregating eligible claims by Pharmacy Name and Pharmacy NPI.
- Calculating claim counts and total plan-paid amounts.
- Sorting pharmacy results by total plan-paid amount in descending order.
- Reconciling aggregated claim counts against source claim records.
- Reconciling aggregated financial totals against source claim amounts.
- Matching watchlist pharmacies against the Medi-Cal enrollment directory.
- Preserving all watchlist pharmacies through left joins, including pharmacies without claims activity.
- Identifying participating pharmacies with no eligible claims.
- Assigning final pharmacy statuses based on enrollment and claims results.
- Preserving blank claim metrics for nonparticipating pharmacies while assigning zero metrics to participating pharmacies with no eligible claims.

### Excel Reporting

- Filtering the processed watchlist to pharmacies added during the selected reporting month.
- Sorting the final report by 12-month Plan Paid in descending order.
- Positioning nonparticipating pharmacies at the bottom of the report.
- Selecting client-facing report columns while excluding internal processing fields.
- Exporting the final reporting dataset to Excel.
- Applying custom column widths and styled headers.
- Formatting Plan Paid values as currency.
- Formatting reporting dates for readability.
- Freezing the header row for easier navigation.
- Enabling column filters across the reporting dataset.

## Current Processing Workflow

The project currently implements the following workflow:

1. **Generate Synthetic Data:** Create fictional pharmacy watchlists, enrollment directories, member names, and claims records.
2. **Load Claims Data:** Import the synthetic Cognos claims export into pandas.
3. **Exclude Test Claims:** Normalize member names and remove records identified as `SB393 TEST`.
4. **Aggregate Claims:** Group eligible claims by Pharmacy Name and Pharmacy NPI, calculating claim counts and total plan-paid amounts.
5. **Reconcile Results:** Validate that aggregated claim counts and financial totals match the filtered source claims.
6. **Match Enrollment:** Compare pharmacy NPIs against the Medi-Cal enrollment directory.
7. **Merge Results:** Use left joins to preserve all pharmacies in the original watchlist, including pharmacies without matching claims records.
8. **Assign Final Status:** Distinguish between nonparticipating pharmacies, participating pharmacies with claims, and participating pharmacies without eligible claims.
9. **Filter Reporting Month:** Identify pharmacies added during the selected reporting month.
10. **Generate Excel Report:** Export a client-facing workbook with formatted columns, currency values, date formatting, filters, and a frozen header row.

The initial workflow retains manual Cognos report extraction. Python handles the downstream data processing and analysis.

## Project Structure

```text
pharmacy-watchlist-capstone/
│
├── data/
│   ├── raw/                     # Generated synthetic source datasets
│   └── processed/               # Intermediate datasets
│
├── docs/
│   └── screenshots/             # README screenshots and sample outputs
│       ├── monthly_watchlist.png
│       ├── enrolled_pharmacies.png
│       ├── watchlist_validation.png
│       ├── claims_output.png
│       └── processed_watchlist.png
│
├── output/                      # Final reporting deliverables
│
├── src/
│   ├── generators/
│   │   ├── __init__.py
│   │   ├── claims.py
│   │   ├── enrollment.py
│   │   ├── member_names.py
│   │   ├── name_parts.py
│   │   ├── watchlist.py
│   │   └── watchlist_reasons.py
│   │
│   ├── processors/
│   │   ├── __init__.py
│   │   ├── claims_processor.py
│   │   └── watchlist_processor.py
│   │
│   ├── reporting/
│   │   ├── __init__.py
│   │   └── excel_report.py
│   │   └── powerpoint_report.py
│   │
│   ├── validators/
│   │   ├── __init__.py
│   │   └── watchlist_validator.py
│   │
│   └── generate_data.py
│
├── tests/
│
├── demo.py                      #Runs the project demostration         
├── .gitignore
├── README.md
└── requirements.txt
```

### Directory Descriptions

- **data/raw/** – Synthetic source datasets used to simulate monthly reporting inputs.
- **data/processed/** – Intermediate datasets generated during processing.
- **docs/screenshots/** – Visual examples of synthetic data and project outputs.
- **output/** – Final reporting deliverables.
- **src/generators/** – Modules responsible for generating synthetic source data.
- **src/processors/** – Modules responsible for loading, filtering, merging, and aggregating datasets.
- **src/reporting/** – Modules responsible for generating and formatting reporting deliverables.
- **src/validators/** – Data validation functions.
- **tests/** – Project testing and quality assurance.
- **demo.py** – Demostrates the end-to-end pharmacy watchlist analytics workflow.

Generated datasets and output files are excluded from version control to keep the repository focused on source code, documentation, and reproducible workflows.

## Sample Outputs

### Monthly Pharmacy Watchlist

![Synthetic monthly pharmacy watchlist](docs/screenshots/monthly_watchlist.png)

### Pharmacy Enrollment Directory

![Synthetic pharmacy enrollment directory](docs/screenshots/enrolled_pharmacies.png)

### Watchlist Validation Results

![Successful watchlist validation](docs/screenshots/watchlist_validation.png)

### Synthetic Claims Output

The generated Cognos-style claims export contains synthetic member names, pharmacy names, pharmacy NPIs, and total paid amounts.

![Synthetic Claims Data](docs/screenshots/claims_data.png)

### Processed Pharmacy Watchlist Report

The final Excel report contains pharmacies added during the selected reporting month, with enrollment and claims results, claim counts, and total plan-paid amounts.

The workbook includes formatted headers, currency formatting, date formatting, column filters, and a frozen header row.

![Formatted pharmacy watchlist report](docs/screenshots/processed_watchlist.png)

## Upcoming Development

1. Implement dynamic reporting-month selection to eliminate hardcoded reporting dates.
2. Expand automated testing and quality assurance.
3. Develop automated PowerPoint presentation generation.
4. Improve processing documentation and reporting reproducibility.
5. Explore further automation of the monthly reporting workflow.

## Data Privacy

This project uses entirely synthetic data. No real pharmacy identifiers, member information, claims records, or protected health information are used.

The project is intended for educational and portfolio demonstration purposes.
