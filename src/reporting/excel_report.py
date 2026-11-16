import pandas as pd
import sys
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
from datetime import datetime
from time import strftime


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

column_widths = {
    "A": 20,
    "B": 50,
    "C": 30,
    "D": 30,
    "E": 50,
    "F": 25,
    "G": 25,
    "H": 50
}

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
    for column, width in column_widths.items():
        worksheet.column_dimensions[column].width = width
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
    if len(sys.argv) < 2:
        print("Please enter a month in the form of yyyy-mm to run the report.")
        sys.exit()
    reporting_month = sys.argv[1]
    try:
        reporting_month = datetime.strptime(reporting_month, "%Y-%m")
    except ValueError:
        print("Please enter the reporting month in yyyy-mm format.")
        sys.exit()
    reporting_month_str = reporting_month.strftime("%Y-%m")
    watchlist = generate_watchlist(reporting_month=reporting_month_str)
    network = load_claims("data/raw/enrolled_pharmacies.xlsx")
    claims = load_claims("data/raw/cognos_claims_minimal.xlsx")

    filtered_claims = exclude_test_claims(claims)
    aggregated_claims = aggregate_claims(filtered_claims)

    enrollment_match = match_enrollment(watchlist, network)
    merged_watchlist = merge_claims_with_watchlist(
        enrollment_match, aggregated_claims
    )
    merged_watchlist = assign_final_status(merged_watchlist)
    monthly_report = filter_reporting_month(
        merged_watchlist, reporting_month
    )
    report_to_excel(monthly_report, f"output/pharmacy_watchlist_{reporting_month_str}.xlsx")

    print(f"\n--- {reporting_month_str} PROCESSED WATCHLIST ---")
    print(
        monthly_report[
            [
                "NPI",
                "Pharmacy Name",
                "12 Month Claim Count",
                "12 Month Plan Paid",
                "Final Status"
            ]
        ].to_string(index=False)
    )

    print(f"\nRecords in report: {len(monthly_report)}")
