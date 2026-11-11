watchlist_reasons = {
    "NETWORK TERMINATION": [
        "CC: Common Control",
        "CC: Invoice Shortages",
        "CC: Missing Documentation",
        "CC: No Response"],
    "FWA TRIAGE" : [
        "Billing for Services not Rendered",
        "Invoice Shortages",
        "FWA Concerns - FWA Analysis",
        "FWA Analytics - Indictment"
    ],
    "FWA ISSUE": [
        "FWA Concerns",
        "Pharmacy was associated with Kickback Scheme",
        "Not Contracted",
        "Terminated"
    ],
    "INDUSTRY ALERT": [
        "N/A",
        "CC: Invoice Shortages",
        "Proactive Monitoring",
        "CMS Fraud Alert"
    ],
    "NETWORK DENIAL": [
        "CC: No Response",
        "CC: Not eligible until 2027",
        "Uphold Denial due to not meeting criteria",
        "CC: Outstanding Balance"
    ]
}

reason_weights = {
    "NETWORK DENIAL": 0.45,
    "NETWORK TERMINATION": 0.40,
    "FWA TRIAGE": 0.10,
    "FWA ISSUE": 0.075,
    "INDUSTRY ALERT": 0.025
}
