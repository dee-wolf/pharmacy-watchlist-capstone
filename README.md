# Pharmacy Watchlist Analytics Pipeline

## Overview

The Pharmacy Watchlist Analytics Pipeline is a Python-based data analytics project designed to streamline the monthly process of identifying newly added pharmacies, determining network participation, and analyzing pharmacy claims activity.

The project is modeled after a real-world healthcare analytics workflow and uses entirely synthetic data to demonstrate how Python and pandas can be applied to automate repetitive data preparation, data validation, aggregation, and reporting tasks. The goal is to reduce manual spreadsheet work, improve consistency, and create a more reproducible reporting process.

## Project Objectives

This project aims to:

- Identify pharmacies added to a watchlist during a selected reporting month.
- Determine pharmacy participation by matching pharmacy identifiers against an enrollment directory.
- Prepare pharmacy identifiers and reporting dates for claims extraction.
- Process claims data, apply business rules, and calculate claim counts and total plan-paid amounts.
- Generate structured Excel reports and client-facing PowerPoint presentations.
- Incorporate data validation and quality checks to improve reporting accuracy.

## Technology Stack

- **Python** - Core programming language
- **Pandas** – Data manipulation, merging, and aggregation
- **OpenPyXL** – Excel workbook processing
- **Python-pptx** – PowerPoint report generation
- **Git & GitHub** – Version control and project management

## Current Implementation

The initial synthetic data generation phase is operational.

### Completed

- Configurable synthetic pharmacy enrollment directory generation.
- Monthly pharmacy watchlist generation.
- Synthetic pharmacy names and test identifiers.
- Configurable watchlist reasons and associated review details.
- Weighted random selection of watchlist categories.
- Reproducible data generation using configurable random seeds.
- Excel export of generated datasets.
- Initial data-quality validation, including record counts, NPI uniqueness, and network participation counts.

### In Progress

- Expanded watchlist validation.
- Claims dataset generation.
- Claims processing and aggregation.

## Project Structure

```text
pharmacy-watchlist-capstone/
├── data/
│   ├── raw/
│   └── processed/
├── output/
├── src/
│   ├── generators/
│   └── validators/
├── tests/
├── .gitignore
└── requirements.txt
```

Generated datasets and output files are excluded from version control.

## Sample Outputs

Screenshots of synthetic Excel workbooks will be added here as development progresses.

## Development Roadmap

1. Complete synthetic data generation and validation.
2. Generate synthetic claims-level datasets.
3. Implement claims filtering and business rules.
4. Aggregate claim counts and total plan-paid amounts.
5. Generate formatted Excel reports.
6. Automate PowerPoint presentation generation.
7. Expand automated testing and quality assurance.
