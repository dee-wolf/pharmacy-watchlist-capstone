import openpyxl

import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment


def filter_reporting_month(watchlist, reporting_month):
    reporting_month = pd.to_datetime(reporting_month)
    filtered_watchlist = watchlist[
        pd.to_datetime(watchlist["Month Added to List"]).dt.to_period("M")
        == reporting_month.to_period("M")
    ]
    filtered_watchlist = filtered_watchlist.sort_values(
        by="12 Month Plan Paid",
        ascending=False,
        na_position="last"
    )
    return filtered_watchlist

def report_to_excel(dataframe, filepath):
    edited_report = dataframe[["NPI",
        "Pharmacy Name",
        "Month Added to List",
        "Watch List Reason",
        "Addt'l Details of Watch/Review Findings",
        "12 Month Claim Count",
        "12 Month Plan Paid",
        "Final Status"]]
    edited_report.to_excel(filepath, index=False)
    workbook = load_workbook(filepath)
    worksheet = workbook.active
    worksheet.column_dimensions["A"].width = 20
    worksheet.column_dimensions["B"].width = 50
    worksheet.column_dimensions["C"].width = 25
    worksheet.column_dimensions["D"].width = 30
    worksheet.column_dimensions["E"].width = 50
    worksheet.column_dimensions["F"].width = 25
    worksheet.column_dimensions["G"].width = 25
    worksheet.column_dimensions["H"].width = 30
    for cell in worksheet[1]:
       cell.font = Font(bold=True, color="FFFFFF")
       cell.fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
       cell.alignment = Alignment(horizontal="center", vertical="center")
    for row in worksheet.iter_rows(min_row = 2, min_col = 7, max_col = 7):
        for cell in row:
            cell.number_format = '$#,##0.00'
    for row in worksheet.iter_rows(min_row = 2, min_col = 3, max_col = 3):
        for cell in row:
            cell.number_format = 'yyyy-mm-dd'
    worksheet.freeze_panes = "A2"
    worksheet.auto_filter.ref = worksheet.dimensions
    workbook.save(filepath)


if __name__ == "__main__":
    from src.generators.watchlist import generate_watchlist
    from src.generators.enrollment import generate_enrollment
    from src.processors.claims_processor import (
        load_claims,
        exclude_test_claims,
        aggregate_claims
    )
    from src.processors.watchlist_processor import (
        match_enrollment,
        merge_claims_with_watchlist,
        assign_final_status
    )

    watchlist = generate_watchlist()
    network = load_claims("data/raw/enrolled_pharmacies.xlsx")
    claims = load_claims("data/raw/cognos_claims_minimal.xlsx")

    filtered_claims = exclude_test_claims(claims)
    aggregated_claims = aggregate_claims(filtered_claims)

    enrollment_match = match_enrollment(watchlist, network)
    merged_watchlist = merge_claims_with_watchlist(
        enrollment_match, aggregated_claims
    )
    merged_watchlist = assign_final_status(merged_watchlist)

    reporting_month = "2026-11-01"
    november_report = filter_reporting_month(
        merged_watchlist, reporting_month
    )
    report_to_excel(november_report, "output/pharmacy_watchlist_november_2026.xlsx")

    print("\n--- NOVEMBER 2026 PROCESSED WATCHLIST ---")
    print(
        november_report[
            [
                "NPI",
                "Pharmacy Name",
                "12 Month Claim Count",
                "12 Month Plan Paid",
                "Final Status"
            ]
        ].to_string(index=False)
    )

    print(f"\nRecords in report: {len(november_report)}")
