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

## Data & Privacy

All datasets used in this project are synthetically generated and contain no real patient, pharmacy, member, or claims information. Pharmacy identifiers are fictional test values and are not actual National Provider Identifiers (NPIs).

The project is intended for educational and portfolio demonstration purposes and does not process production healthcare data or protected health information (PHI).

## Project Status

**In Development**

The initial phase focuses on building a reproducible synthetic data generator. Subsequent development will implement the watchlist processing, network matching, claims analysis, validation, and automated reporting components.
