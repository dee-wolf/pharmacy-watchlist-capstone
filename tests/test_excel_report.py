import pandas as pd
import pytest
from src.reporting.excel_report import filter_reporting_month, report_to_excel
from openpyxl import load_workbook

def test_filter_reporting_month():
    test_df = pd.DataFrame({
        "Pharmacy Name": [
            "Pharmacy A",
            "Pharmacy B",
            "Pharmacy C"
        ],
        "Month Added to List": [
            "November 1, 2026",
            "November 23, 2026",
            "October 31, 2026"
        ],
        "12 Month Plan Paid": [
            100,
            200,
            50
        ]
    })
    result = filter_reporting_month(test_df, "2026-11")
    assert result["Pharmacy Name"].to_list() == ["Pharmacy B", "Pharmacy A"]

def test_filter_reporting_month_descending_order():
    test_df = pd.DataFrame({
        "Pharmacy Name": [
            "Pharmacy A",
            "Pharmacy B",
            "Pharmacy C"
        ],
        "Month Added to List": [
            "November 1, 2026",
            "November 23, 2026",
            "November 16, 2026"
        ],
        "12 Month Plan Paid": [
            100,
            200,
            350
        ]
    })
    result = filter_reporting_month(test_df, "2026-11")
    assert result["Pharmacy Name"].to_list() == ["Pharmacy C", "Pharmacy B", "Pharmacy A"]

def test_report_to_excel(tmp_path):
    test_df = pd.DataFrame({
        "NPI": ["TEST-000001"],
        "Pharmacy Name": ["Raven Road Apothecary"],
        "Month Added to List": ["November 1, 2026"],
        "Watch List Reason": ["Industry Alert"],
        "Addt'l Details of Watch/Review Findings": ["Synthetic test pharmacy"],
        "12 Month Claim Count": [125],
        "12 Month Plan Paid": [12500.50],
        "Final Status": ["Participating - Has Claims"]
    })
    (tmp_path / "data" / "output").mkdir(parents=True)
    output_file = tmp_path / "data" / "output" / "test_pharmacy_watchlist.xlsx"
    report_to_excel(test_df, output_file)
    assert output_file.exists()

def test_report_to_excel_correct_headers(tmp_path):
    test_df = pd.DataFrame({
        "NPI": ["TEST-000001"],
        "Pharmacy Name": ["Raven Road Apothecary"],
        "Month Added to List": ["November 1, 2026"],
        "Watch List Reason": ["Industry Alert"],
        "Addt'l Details of Watch/Review Findings": ["Synthetic test pharmacy"],
        "12 Month Claim Count": [125],
        "12 Month Plan Paid": [12500.50],
        "Final Status": ["Participating - Has Claims"]
    })
    (tmp_path / "data" / "output").mkdir(parents=True)
    output_file = tmp_path / "data" / "output" / "test_pharmacy_watchlist.xlsx"
    report_to_excel(test_df, output_file)
    workbook = load_workbook(output_file)
    worksheet = workbook.active
    headers = [cell.value for cell in worksheet[1]]
    assert headers == ["NPI", "Pharmacy Name", "Month Added to List", "Watch List Reason", "Addt'l Details of Watch/Review Findings", "12 Month Claim Count", "12 Month Plan Paid", "Final Status"]
    assert worksheet["A2"].value == "TEST-000001"
    assert worksheet["B2"].value == "Raven Road Apothecary"

def test_report_to_excel_correct_format_for_plan_paid(tmp_path):
    test_df = pd.DataFrame({
        "NPI": ["TEST-000001"],
        "Pharmacy Name": ["Raven Road Apothecary"],
        "Month Added to List": ["November 1, 2026"],
        "Watch List Reason": ["Industry Alert"],
        "Addt'l Details of Watch/Review Findings": ["Synthetic test pharmacy"],
        "12 Month Claim Count": [125],
        "12 Month Plan Paid": [12500.50],
        "Final Status": ["Participating - Has Claims"]
    })
    (tmp_path / "data" / "output").mkdir(parents=True)
    output_file = tmp_path / "data" / "output" / "test_pharmacy_watchlist.xlsx"
    report_to_excel(test_df, output_file)
    workbook = load_workbook(output_file)
    worksheet = workbook.active
    assert worksheet["G2"].number_format == "$#,##0.00"

def test_report_to_excel_correct_format_for_month_added(tmp_path):
    test_df = pd.DataFrame({
        "NPI": ["TEST-000001"],
        "Pharmacy Name": ["Raven Road Apothecary"],
        "Month Added to List": ["November 1, 2026"],
        "Watch List Reason": ["Industry Alert"],
        "Addt'l Details of Watch/Review Findings": ["Synthetic test pharmacy"],
        "12 Month Claim Count": [125],
        "12 Month Plan Paid": [12500.50],
        "Final Status": ["Participating - Has Claims"]
    })
    (tmp_path / "data" / "output").mkdir(parents=True)
    output_file = tmp_path / "data" / "output" / "test_pharmacy_watchlist.xlsx"
    report_to_excel(test_df, output_file)
    workbook = load_workbook(output_file)
    worksheet = workbook.active
    assert worksheet["C2"].number_format == "yyyy-mm-dd"

def test_report_to_excel_freeze_panes(tmp_path):
    test_df = pd.DataFrame({
        "NPI": ["TEST-000001"],
        "Pharmacy Name": ["Raven Road Apothecary"],
        "Month Added to List": ["November 1, 2026"],
        "Watch List Reason": ["Industry Alert"],
        "Addt'l Details of Watch/Review Findings": ["Synthetic test pharmacy"],
        "12 Month Claim Count": [125],
        "12 Month Plan Paid": [12500.50],
        "Final Status": ["Participating - Has Claims"]
    })
    (tmp_path / "data" / "output").mkdir(parents=True)
    output_file = tmp_path / "data" / "output" / "test_pharmacy_watchlist.xlsx"
    report_to_excel(test_df, output_file)
    workbook = load_workbook(output_file)
    worksheet = workbook.active
    assert worksheet.freeze_panes == "A2"

def test_report_to_excel_auto_filter(tmp_path):
    test_df = pd.DataFrame({
        "NPI": ["TEST-000001"],
        "Pharmacy Name": ["Raven Road Apothecary"],
        "Month Added to List": ["November 1, 2026"],
        "Watch List Reason": ["Industry Alert"],
        "Addt'l Details of Watch/Review Findings": ["Synthetic test pharmacy"],
        "12 Month Claim Count": [125],
        "12 Month Plan Paid": [12500.50],
        "Final Status": ["Participating - Has Claims"]
    })
    (tmp_path / "data" / "output").mkdir(parents=True)
    output_file = tmp_path / "data" / "output" / "test_pharmacy_watchlist.xlsx"
    report_to_excel(test_df, output_file)
    workbook = load_workbook(output_file)
    worksheet = workbook.active
    assert worksheet.auto_filter.ref == "A1:H2"
