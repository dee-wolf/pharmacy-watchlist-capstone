from src.generate_data import generate_synthetic_data()
from src.processors.claims_processor import exclude_test_claims, aggregate_claims
from src.processors.watchlist_processor import match_enrollment, merge_claims_with_watchlist, assign_final_status
from src.reporting.excel_report import filter_reporting_month, report_to_excel

def main(reporting_month):
    watchlist, enrollment, claims = generate_synthetic_data()
    enrollment_match = match_enrollment(watchlist, enrollment)
