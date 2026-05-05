"""
BizPulse Mock Data — simulates federated Karnataka government databases
"""

BUSINESSES = [
    {
        "ubid": "KA-2024-BIZ-001",
        "name": "Ravi Enterprises Pvt Ltd",
        "owner": "Ravi Kumar",
        "city": "Bengaluru",
        "district": "Bengaluru Urban",
        "sector": "Manufacturing",
        "gstin": "29AABCR1234D1Z5",
        "udyam": "UDYAM-KA-01-0012345",
        "municipal_licence": "BBMP/2022/TL/45231",
        "fssai": None,
        "pan": "AABCR1234D",
        "compliance_score": 87,
        "turnover": [42, 51, 48, 63, 71, 68],
        "turnover_months": ["Dec", "Jan", "Feb", "Mar", "Apr", "May"],
        "status": "Active",
        "alerts": [],
        "compliance": [
            {"department": "GST", "status": "compliant", "expires": None, "note": "Filed up to date"},
            {"department": "Udyam", "status": "compliant", "expires": None, "note": "Registered MSME"},
            {"department": "Municipal Licence", "status": "compliant", "expires": "2025-03-15", "note": "Valid"},
            {"department": "FSSAI", "status": "not_applicable", "expires": None, "note": "Not applicable"},
        ],
        "directors": ["Ravi Kumar", "Sunitha Kumar"],
        "address": "Plot 42, KIADB Industrial Area, Bengaluru North, Karnataka 560045",
        "registration_date": "2019-04-12",
        "employees": 48,
    },
    {
        "ubid": "KA-2024-BIZ-002",
        "name": "Meena Textiles",
        "owner": "Meena Sharma",
        "city": "Hubli",
        "district": "Hubli-Dharwad",
        "sector": "Textiles",
        "gstin": "29AABCM5678E1Z3",
        "udyam": "UDYAM-KA-10-0067891",
        "municipal_licence": "HMC/2021/SL/8823",
        "fssai": None,
        "pan": "AABCM5678E",
        "compliance_score": 64,
        "turnover": [28, 31, 29, 35, 38, 34],
        "turnover_months": ["Dec", "Jan", "Feb", "Mar", "Apr", "May"],
        "status": "Action Required",
        "alerts": [
            "Municipal Licence expires in 30 days",
            "GST filing due next week",
        ],
        "compliance": [
            {"department": "GST", "status": "warning", "expires": "2025-05-20", "note": "Filing due next week"},
            {"department": "Udyam", "status": "compliant", "expires": None, "note": "Registered MSME"},
            {"department": "Municipal Licence", "status": "warning", "expires": "2025-06-04", "note": "Expires in 30 days"},
            {"department": "FSSAI", "status": "non_compliant", "expires": None, "note": "Pending — not yet applied"},
        ],
        "directors": ["Meena Sharma"],
        "address": "Door No. 14/A, Textile Nagar, Hubli, Karnataka 580029",
        "registration_date": "2021-08-03",
        "employees": 22,
    },
    {
        "ubid": "KA-2024-BIZ-003",
        "name": "Hubli Foods Co",
        "owner": "Suresh Patil",
        "city": "Hubli",
        "district": "Hubli-Dharwad",
        "sector": "Food & Beverage",
        "gstin": None,
        "udyam": "UDYAM-KA-10-0098234",
        "municipal_licence": "HMC/2023/TL/1102",
        "fssai": None,
        "pan": None,
        "compliance_score": 41,
        "turnover": [18, 22, 19, 24, 41, 43],
        "turnover_months": ["Dec", "Jan", "Feb", "Mar", "Apr", "May"],
        "status": "Non-Compliant",
        "alerts": [
            "GST registration required — turnover crossed Rs.40L",
            "FSSAI licence not found — mandatory for food businesses",
        ],
        "compliance": [
            {"department": "GST", "status": "non_compliant", "expires": None, "note": "Registration required — turnover > Rs.40L"},
            {"department": "Udyam", "status": "compliant", "expires": None, "note": "Registered MSME"},
            {"department": "Municipal Licence", "status": "compliant", "expires": "2025-12-31", "note": "Valid"},
            {"department": "FSSAI", "status": "non_compliant", "expires": None, "note": "Licence not found — mandatory"},
        ],
        "directors": ["Suresh Patil", "Kavitha Patil"],
        "address": "Survey No. 88, Gokul Road, Hubli, Karnataka 580030",
        "registration_date": "2023-01-17",
        "employees": 11,
    },
]

INTELLIGENCE_ALERTS = [
    {
        "id": "ALERT-001",
        "severity": "high",
        "category": "Compliance Anomaly",
        "title": "Sudden drop in GST filings — Textile sector, Dharwad",
        "description": "23% decline in GST filings detected in the Textile sector across Dharwad district this month vs 6-month average. Possible cash-flow distress or evasion pattern.",
        "district": "Dharwad",
        "sector": "Textiles",
        "affected_count": 47,
        "created_at": "2025-05-03",
    },
    {
        "id": "ALERT-002",
        "severity": "medium",
        "category": "Threshold Breach",
        "title": "14 businesses in Hubli crossed Rs.40L turnover threshold",
        "description": "14 businesses have crossed the Rs.40 lakh annual turnover threshold and are now liable for mandatory GST registration. Outreach campaigns recommended.",
        "district": "Hubli-Dharwad",
        "sector": None,
        "affected_count": 14,
        "created_at": "2025-05-02",
    },
    {
        "id": "ALERT-003",
        "severity": "high",
        "category": "Fraud Indicator",
        "title": "Cluster of 6 businesses share same registered address",
        "description": "Six distinct UBIDs share identical registered address at 22B, Industrial Layout, Belagavi. Possible shell entity arrangement — investigation recommended.",
        "district": "Belagavi",
        "sector": None,
        "affected_count": 6,
        "created_at": "2025-05-01",
    },
    {
        "id": "ALERT-004",
        "severity": "low",
        "category": "Data Quality",
        "title": "PAN mismatch detected across 3 UBID records in Mysuru",
        "description": "Entity resolution flagged 3 businesses in Mysuru where PAN numbers differ between GST portal and Udyam registry. Data reconciliation required.",
        "district": "Mysuru",
        "sector": None,
        "affected_count": 3,
        "created_at": "2025-04-30",
    },
]

PLATFORM_STATS = {
    "total_businesses": 473291,
    "unified_today": 1847,
    "compliance_rate": 94.2,
    "active_alerts": 4,
    "districts_active": 31,
    "sectors_monitored": 18,
    "ubids_issued": 473291,
    "departments_integrated": 4,
}

SECTOR_ANALYTICS = [
    {"district": "Bengaluru Urban", "sector": "IT/Software", "compliance_rate": 98.4, "total": 42100},
    {"district": "Bengaluru Urban", "sector": "Manufacturing", "compliance_rate": 91.2, "total": 18400},
    {"district": "Mysuru", "sector": "Tourism", "compliance_rate": 87.6, "total": 9200},
    {"district": "Hubli-Dharwad", "sector": "Textiles", "compliance_rate": 74.3, "total": 12800},
    {"district": "Hubli-Dharwad", "sector": "Food & Beverage", "compliance_rate": 69.1, "total": 8300},
    {"district": "Belagavi", "sector": "Manufacturing", "compliance_rate": 82.5, "total": 11200},
    {"district": "Mangaluru", "sector": "Trade & Commerce", "compliance_rate": 89.7, "total": 14600},
    {"district": "Shivamogga", "sector": "Agriculture Processing", "compliance_rate": 71.8, "total": 6400},
    {"district": "Kalaburagi", "sector": "Mining", "compliance_rate": 63.4, "total": 4200},
    {"district": "Ballari", "sector": "Mining", "compliance_rate": 67.8, "total": 5800},
]

# Raw fragmented records simulating 4 separate government databases
FRAGMENTED_RECORDS = {
    "GST Portal": [
        {"raw_name": "Ravi Enterprises Pvt Ltd", "pan": "AABCR1234D", "address": "Plot 42, KIADB Industrial Area, Bengaluru", "gstin": "29AABCR1234D1Z5"},
        {"raw_name": "Meena Textiles", "pan": "AABCM5678E", "address": "14/A, Textile Nagar, Hubli", "gstin": "29AABCM5678E1Z3"},
        {"raw_name": "Hubli Foods Co", "pan": None, "address": "Survey 88, Gokul Road, Hubli", "gstin": None},
    ],
    "Udyam Registry": [
        {"raw_name": "Ravi Enterprises Private Limited", "pan": "AABCR1234D", "address": "Plot 42, KIADB Indl Area, Blr North", "udyam": "UDYAM-KA-01-0012345"},
        {"raw_name": "M. Textiles", "pan": "AABCM5678E", "address": "Door 14A, Hubli 580029", "udyam": "UDYAM-KA-10-0067891"},
        {"raw_name": "Hubli Food Company", "pan": None, "address": "Gokul Road, Hubli, KA 580030", "udyam": "UDYAM-KA-10-0098234"},
    ],
    "Municipal Database": [
        {"raw_name": "RAVI ENT PVT LTD", "pan": None, "address": "42, Bangalore Industrial Estate", "licence": "BBMP/2022/TL/45231"},
        {"raw_name": "Meena Textile Works", "pan": None, "address": "Textile Nagar Hubli Karnataka", "licence": "HMC/2021/SL/8823"},
        {"raw_name": "HublifoOds", "pan": None, "address": "88, Gokul Rd, Hubli", "licence": "HMC/2023/TL/1102"},
    ],
    "FSSAI Registry": [
        {"raw_name": "Hubli Foods Pvt", "pan": None, "address": "Survey No 88 Gokul Road", "fssai": None},
    ],
}

# Karnataka districts for anomaly detection time series
DISTRICTS = [
    "Bengaluru Urban", "Mysuru", "Hubli-Dharwad", "Belagavi",
    "Mangaluru", "Shivamogga", "Kalaburagi", "Ballari",
    "Davangere", "Bidar",
]

COMPLIANCE_DEADLINES = [
    {"business": "Meena Textiles (KA-2024-BIZ-002)", "event": "Municipal Licence Renewal", "due": "2025-06-04", "urgency": "high"},
    {"business": "Meena Textiles (KA-2024-BIZ-002)", "event": "GST Monthly Filing", "due": "2025-05-20", "urgency": "high"},
    {"business": "Hubli Foods Co (KA-2024-BIZ-003)", "event": "GST Registration Required", "due": "2025-05-15", "urgency": "critical"},
    {"business": "Hubli Foods Co (KA-2024-BIZ-003)", "event": "FSSAI Licence Application", "due": "2025-05-30", "urgency": "high"},
    {"business": "Ravi Enterprises (KA-2024-BIZ-001)", "event": "Annual MSME Return", "due": "2025-07-31", "urgency": "low"},
    {"business": "Ravi Enterprises (KA-2024-BIZ-001)", "event": "GST Quarterly Filing", "due": "2025-07-25", "urgency": "low"},
]
