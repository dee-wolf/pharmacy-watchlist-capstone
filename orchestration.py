from src.generate_data import generate_synthetic_data
from src.processors.claims_processor import exclude_test_claims, aggregate_claims
from src.processors.watchlist_processor import match_enrollment, merge_claims_with_watchlist, assign_final_status
from src.reporting.excel_report import filter_reporting_month, report_to_excel
from src.reporting.powerpoint_report import create_presentation, add_title_slide,add_review_summary_slide, add_definitions_slide
from datetime import datetime

def main(reporting_month):
    watchlist, enrollment, claims = generate_synthetic_data()
    enrollment_match = match_enrollment(watchlist, enrollment)
    proper_claims = exclude_test_claims(claims)
    aggregated_claims = aggregate_claims(proper_claims)
    combined = merge_claims_with_watchlist(enrollment_match, aggregated_claims)
    final_watchlist = assign_final_status(combined)
    filtered_report = filter_reporting_month(final_watchlist, reporting_month)
    reporting_month_str = reporting_month.strftime("%Y-%m")
    report_to_excel(filtered_report, f'output/pharmacy_watchlist_{reporting_month_str}.xlsx')
    reviewed_count = len(filtered_report)
    presentation = create_presentation()
    add_title_slide(presentation, reporting_month)
    add_review_summary_slide(presentation, filtered_report, reviewed_count, reporting_month)
    add_definitions_slide(presentation)
    presentation.save(f"output/pharmacy_watchlist_{reporting_month_str}.pptx")
    print(f'pharmacy_watchlist_{reporting_month_str}.xlsx is complete and is located at output/pharmacy_watchlist_{reporting_month_str}.xlsx')
    print(f'pharmacy_watchlist_{reporting_month_str}.pptx is completed and is located at output/pharmacy_watchlist_{reporting_month_str}.pptx')

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Please enter a month in the form of yyyy-mm to run the report.")
        sys.exit()
    reporting_month = sys.argv[1]
    try:
        reporting_month = datetime.strptime(reporting_month, "%Y-%m")
    except ValueError:
        print("Please enter the reporting month in yyyy-mm format.")
        sys.exit()
    main(reporting_month)
