from pptx.util import Inches
from datetime import datetime
from src.reporting.powerpoint_report import create_presentation, add_title_slide, add_review_summary_slide, add_definitions_slide
import pandas as pd


def test_create_presentation_dimensions():
    result = create_presentation()
    assert result.slide_width == Inches(13.333)
    assert result.slide_height == Inches(7.5)

def test_add_title_slide():
    result = create_presentation()
    reporting_month = datetime(2026, 11, 1)
    title = add_title_slide(result, reporting_month)
    assert len(result.slides) == 1
    assert title.shapes[0].text == "Appendix A: New Pharmacies Added to Prime Watchlist - November, 2026"

def test_add_review_summary_slide():
    test_df = pd.DataFrame({
        "NPI": [
            "TEST-000001",
            "TEST-000002",
            "TEST-000003"
        ],
        "Pharmacy Name": [
            "Raven Road Apothecary",
            "Willow Creek Pharmacy",
            "Moonlight Rx"
        ],
        "Final Status": [
            "Participating - Has Claims",
            "Participating - Has Claims",
            "Not Participating"
        ],
        "12 Month Plan Paid": [
            12500.50,
            8500.25,
            float("nan")
        ],
        "12 Month Claim Count": [
            125,
            85,
            float("nan")
        ]
    })
    result = create_presentation()
    reporting_month = datetime(2026, 11, 1)
    summary = add_review_summary_slide(result, test_df, reviewed_count=3, reporting_month=reporting_month)
    assert summary.shapes[0].text == "We reviewed all 3 pharmacies added to the Prime Watch List in November, 2026 for overlap with\nMedi-Cal enrolled pharmacies, 2 unique pharmacies were identified."

def test_add_review_summary_slide_summary_table():
    test_df = pd.DataFrame({
        "NPI": [
            "TEST-000001",
            "TEST-000002",
            "TEST-000003"
        ],
        "Pharmacy Name": [
            "Raven Road Apothecary",
            "Willow Creek Pharmacy",
            "Moonlight Rx"
        ],
        "Final Status": [
            "Participating - Has Claims",
            "Participating - Has Claims",
            "Not Participating"
        ],
        "12 Month Plan Paid": [
            12500.50,
            8500.25,
            float("nan")
        ],
        "12 Month Claim Count": [
            125,
            85,
            float("nan")
        ]
    })
    result = create_presentation()
    reporting_month = datetime(2026, 11, 1)
    summary = add_review_summary_slide(result, test_df, reviewed_count=3, reporting_month=reporting_month)
    table_shape = [shape for shape in summary.shapes if shape.has_table][0]
    table = table_shape.table
    pharmacy_names = [
        table.cell(row, 1).text
        for row in range(1, len(table.rows))
    ]
    assert len(table.rows) == 3
    assert table.cell(1, 1).text == "Raven Road Apothecary"
    assert table.cell(2, 1).text == "Willow Creek Pharmacy"
    assert "Moonlight Rx" not in pharmacy_names

def test_add_review_summary_slide_correct_number_of_pharmacies_in_table():
    test_df = pd.DataFrame({
        "NPI": [
            "TEST-000001",
            "TEST-000002",
            "TEST-000003",
            "TEST-000004",
            "TEST-000005",
            "TEST-000006"
        ],
        "Pharmacy Name": [
            "Raven Road Apothecary",
            "Willow Creek Pharmacy",
            "Moonlight Rx",
            "Blackthorn Pharmacy",
            "Starlight Apothecary",
            "Foxglove Drugstore"
        ],
        "Final Status": [
            "Participating - Has Claims",
            "Participating - Has Claims",
            "Participating - Has Claims",
            "Participating - Has Claims",
            "Participating - Has Claims",
            "Participating - Has Claims"
        ],
        "12 Month Plan Paid": [
            12500.50,
            8500.25,
            7200.00,
            6100.75,
            4300.00,
            3200.50
        ],
        "12 Month Claim Count": [
            125,
            85,
            72,
            61,
            43,
            32
        ]
    })
    result = create_presentation()
    reporting_month = datetime(2026, 11, 1)
    summary = add_review_summary_slide(result, test_df, reviewed_count=6, reporting_month=reporting_month)
    continuation_slide = result.slides[1]
    table_shape = [
        shape for shape in continuation_slide.shapes if shape.has_table
    ][0]
    table = table_shape.table
    assert len(result.slides) == 2
    assert table.cell(1, 1).text == "Foxglove Drugstore"

def test_add_definitions_slide():
    result = create_presentation()
    definitions = add_definitions_slide(result)
    definitions = result.slides[0]
    assert len(result.slides) == 1
    assert definitions.shapes[0].text == "Watch List Reason definitions"
