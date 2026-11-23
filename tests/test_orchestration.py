from datetime import datetime
from orchestration import main
from unittest.mock import patch, MagicMock

def test_main():
    with patch("orchestration.generate_synthetic_data") as mock_generate:
        with patch("orchestration.match_enrollment") as mock_enrollment:
            with patch("orchestration.exclude_test_claims") as mock_exclude:
                with patch("orchestration.aggregate_claims") as mock_aggregate:
                    with patch("orchestration.merge_claims_with_watchlist") as mock_merge:
                        with patch("orchestration.assign_final_status") as mock_assign:
                            with patch("orchestration.filter_reporting_month") as mock_filter:
                                with patch("orchestration.report_to_excel") as mock_excel:
                                    with patch("orchestration.create_presentation") as mock_create:
                                        with patch("orchestration.add_title_slide") as mock_title:
                                            with patch("orchestration.add_review_summary_slide") as mock_summary:
                                                with patch("orchestration.add_definitions_slide") as mock_definitions:
                                                    reporting_month = datetime(2026, 11, 1)
                                                    mock_generate.return_value = ("watchlist", "enrollment", "claims")
                                                    mock_enrollment.return_value = "enrollment_match"
                                                    mock_exclude.return_value = "proper_claims"
                                                    mock_aggregate.return_value = "aggregated_claims"
                                                    mock_merge.return_value = "combined"
                                                    mock_assign.return_value = "final_watchlist"
                                                    mock_filter.return_value = ["pharmacy"]
                                                    mock_create.return_value = MagicMock()
                                                    main(reporting_month)
                                                    mock_generate.assert_called_once_with()
                                                    mock_enrollment.assert_called_once_with("watchlist", "enrollment")
                                                    mock_exclude.assert_called_once_with("claims")
                                                    mock_aggregate.assert_called_once_with("proper_claims")
                                                    mock_merge.assert_called_once_with("enrollment_match", "aggregated_claims")
                                                    mock_assign.assert_called_once_with("combined")
                                                    mock_filter.assert_called_once_with("final_watchlist", reporting_month)
                                                    mock_excel.assert_called_once_with(["pharmacy"], "output/pharmacy_watchlist_2026-11.xlsx")
                                                    mock_create.assert_called_once_with()
                                                    mock_title.assert_called_once_with(mock_create.return_value, reporting_month)
                                                    mock_summary.assert_called_once_with(mock_create.return_value, ["pharmacy"], 1, reporting_month)
                                                    mock_definitions.assert_called_once_with(mock_create.return_value)
                                                    mock_create.return_value.save.assert_called_once_with("output/pharmacy_watchlist_2026-11.pptx")
