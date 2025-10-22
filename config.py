import pandas as pd

DEFAULT_PRODUCTS = {
    "Fire Damper": {
        "FD-MB-3V": [
            {"width": 300, "height": 300, "c_factor": 1.1152},
            {"width": 600, "height": 600, "c_factor": 0.7186},
            {"width": 900, "height": 900, "c_factor": 0.3843}
        ],
        "FD-MB-3V (M)": [
            {"width": 300, "height": 300, "c_factor": 1.1152},
            {"width": 600, "height": 600, "c_factor": 0.7186},
            {"width": 900, "height": 900, "c_factor": 0.3843}
        ],
        "FD-MB-3V OW(M)": [
            {"width": 300, "height": 300, "c_factor": 1.1152},
            {"width": 600, "height": 600, "c_factor": 0.7186},
            {"width": 900, "height": 900, "c_factor": 0.3843}
        ],
        "FD-MB-3V OW": [
            {"width": 300, "height": 300, "c_factor": 1.1152},
            {"width": 600, "height": 600, "c_factor": 0.7186},
            {"width": 900, "height": 900, "c_factor": 0.3843}
        ],
        "FD-MB-3V FA": [
            {"width": 300, "height": 300, "c_factor": 1.1152},
            {"width": 600, "height": 600, "c_factor": 0.7186}
        ],
        "FD-MB-3V FA(M)": [
            {"width": 300, "height": 300, "c_factor": 1.1152},
            {"width": 600, "height": 600, "c_factor": 0.7186}
        ],
        "FDD-MB-3V": [
            {"width": 300, "height": 300, "c_factor": 1.1152},
            {"width": 600, "height": 600, "c_factor": 0.7186},
            {"width": 900, "height": 900, "c_factor": 0.3843}
        ],
        "FDD-MB-3V (M)": [
            {"width": 300, "height": 300, "c_factor": 1.1152},
            {"width": 600, "height": 600, "c_factor": 0.7186},
            {"width": 900, "height": 900, "c_factor": 0.3843}
        ],
        "FDD-MB-3V OW": [
            {"width": 300, "height": 300, "c_factor": 1.1152},
            {"width": 600, "height": 600, "c_factor": 0.7186}
        ],
        "FDD-MB-3V OW(M)": [
            {"width": 300, "height": 300, "c_factor": 1.1152},
            {"width": 600, "height": 600, "c_factor": 0.7186}
        ],
        "FDD-MB-3V FA": [
            {"width": 300, "height": 300, "c_factor": 1.1152},
            {"width": 600, "height": 600, "c_factor": 0.7186}
        ],
        "FDD-MB-3V FA (M)": [
            {"width": 300, "height": 300, "c_factor": 1.1152},
            {"width": 600, "height": 600, "c_factor": 0.7186}
        ],
        "FD-MB-AF": [
            {"width": 300, "height": 300, "c_factor": 0.6026},
            {"width": 600, "height": 600, "c_factor": 0.2421},
            {"width": 900, "height": 900, "c_factor": 0.1613}
        ],
        "FD-MB-AF (M)": [
            {"width": 300, "height": 300, "c_factor": 0.6026},
            {"width": 600, "height": 600, "c_factor": 0.2421},
            {"width": 900, "height": 900, "c_factor": 0.1613}
        ],
        "FD-MB-AF OW(M)": [
            {"width": 300, "height": 300, "c_factor": 0.6026},
            {"width": 600, "height": 600, "c_factor": 0.2421},
            {"width": 900, "height": 900, "c_factor": 0.1613}
        ],
        "FD-MB-AF OW": [
            {"width": 300, "height": 300, "c_factor": 0.6026},
            {"width": 600, "height": 600, "c_factor": 0.2421},
            {"width": 900, "height": 900, "c_factor": 0.1613}
        ],
        "FD-MB-AF FA": [
            {"width": 300, "height": 300, "c_factor": 0.6026},
            {"width": 600, "height": 600, "c_factor": 0.2421}
        ],
        "FD-MB-AF FA(M)": [
            {"width": 300, "height": 300, "c_factor": 0.6026},
            {"width": 600, "height": 600, "c_factor": 0.2421}
        ],
        "FDD-MB-AF": [
            {"width": 300, "height": 300, "c_factor": 0.6026},
            {"width": 600, "height": 600, "c_factor": 0.2421},
            {"width": 900, "height": 900, "c_factor": 0.1613}
        ],
        "FDD-MB-AF (M)": [
            {"width": 300, "height": 300, "c_factor": 0.6026},
            {"width": 600, "height": 600, "c_factor": 0.2421},
            {"width": 900, "height": 900, "c_factor": 0.1613}
        ],
        "FDD-MB-AF OW": [
            {"width": 300, "height": 300, "c_factor": 0.6026},
            {"width": 600, "height": 600, "c_factor": 0.2421}
        ],
        "FDD-MB-AF OW(M)": [
            {"width": 300, "height": 300, "c_factor": 0.6026},
            {"width": 600, "height": 600, "c_factor": 0.2421}
        ],
        "FDD-MB-AF FA": [
            {"width": 300, "height": 300, "c_factor": 0.6026},
            {"width": 600, "height": 600, "c_factor": 0.2421}
        ],
        "FDD-MB-AF FA (M)": [
            {"width": 300, "height": 300, "c_factor": 0.6026},
            {"width": 600, "height": 600, "c_factor": 0.2421}
        ]
    },
    "Fire & Smoke Damper": {
        # ... every model fully listed here (FSD-3V, FSD-AF, etc.) ...
        "FSD-3V-211-1.5 HR Class I": [
            {"width": 300, "height": 300, "c_factor": 1.1152},
            {"width": 600, "height": 600, "c_factor": 0.7186},
            {"width": 900, "height": 900, "c_factor": 0.3843}
        ],
        "FSD-3V-212-1.5 HR Class II": [
            {"width": 300, "height": 300, "c_factor": 1.1152},
            {"width": 600, "height": 600, "c_factor": 0.7186},
            {"width": 900, "height": 900, "c_factor": 0.3843}
        ],
        "FSD-3V-231-3 HR Class I": [
            {"width": 300, "height": 300, "c_factor": 1.1152},
            {"width": 600, "height": 600, "c_factor": 0.7186},
            {"width": 900, "height": 900, "c_factor": 0.3843}
        ],
        "FSD-3V-232-3 HR Class II": [
            {"width": 300, "height": 300, "c_factor": 1.1152},
            {"width": 600, "height": 600, "c_factor": 0.7186},
            {"width": 900, "height": 900, "c_factor": 0.3843}
        ],
        "FSD-3V-OW-211-1.5 HR Class II": [
            {"width": 300, "height": 300, "c_factor": 1.1152},
            {"width": 600, "height": 600, "c_factor": 0.7186},
            {"width": 900, "height": 900, "c_factor": 0.3843}
        ],
        "FSD-3V-OW-212-1.5 HR Class II": [
            {"width": 300, "height": 300, "c_factor": 1.1152},
            {"width": 600, "height": 600, "c_factor": 0.7186},
            {"width": 900, "height": 900, "c_factor": 0.3843}
        ],
        "FSD-3V-FA-211-1.5 HR Class I": [
            {"width": 300, "height": 300, "c_factor": 1.1152},
            {"width": 600, "height": 600, "c_factor": 0.7186}
        ],
        "FSD-3V-FA-212-1.5 HR Class II": [
            {"width": 300, "height": 300, "c_factor": 1.1152},
            {"width": 600, "height": 600, "c_factor": 0.7186}
        ],
        "FSD-3V-CR-211-1.5 HR Class I": [
            {"width": 300, "height": 300, "c_factor": 1.1152},
            {"width": 600, "height": 600, "c_factor": 0.7186}
        ],
        "FSD-3V-CR-212-1.5 HR Class II": [
            {"width": 300, "height": 300, "c_factor": 1.1152},
            {"width": 600, "height": 600, "c_factor": 0.7186}
        ],
        "FSD-3V-CR-231-3 HR Class I": [
            {"width": 300, "height": 300, "c_factor": 1.1152},
            {"width": 600, "height": 600, "c_factor": 0.7186}
        ],
        "FSD-3V-CR-232-3 HR Class II": [
            {"width": 300, "height": 300, "c_factor": 1.1152},
            {"width": 600, "height": 600, "c_factor": 0.7186}
        ],
        "FSD-AF-211-1.5 HR Class I": [
            {"width": 300, "height": 300, "c_factor": 0.6026},
            {"width": 600, "height": 600, "c_factor": 0.2421},
            {"width": 900, "height": 900, "c_factor": 0.1613}
        ],
        "FSD-AF-212-1.5 HR Class II": [
            {"width": 300, "height": 300, "c_factor": 0.6026},
            {"width": 600, "height": 600, "c_factor": 0.2421},
            {"width": 900, "height": 900, "c_factor": 0.1613}
        ],
        "FSD-AF-231-3 HR Class I": [
            {"width": 300, "height": 300, "c_factor": 0.6026},
            {"width": 600, "height": 600, "c_factor": 0.2421},
            {"width": 900, "height": 900, "c_factor": 0.1613}
        ],
        "FSD-AF-232-3 HR Class II": [
            {"width": 300, "height": 300, "c_factor": 0.6026},
            {"width": 600, "height": 600, "c_factor": 0.2421},
            {"width": 900, "height": 900, "c_factor": 0.1613}
        ],
        "FSD-AF-OW-211-1.5 HR Class II": [
            {"width": 300, "height": 300, "c_factor": 0.6026},
            {"width": 600, "height": 600, "c_factor": 0.2421}
        ],
        "FSD-AF-OW-212-1.5 HR Class II": [
            {"width": 300, "height": 300, "c_factor": 0.6026},
            {"width": 600, "height": 600, "c_factor": 0.2421}
        ],
        "FSD-AF-FA-211-1.5 HR Class I": [
            {"width": 300, "height": 300, "c_factor": 0.6026},
            {"width": 600, "height": 600, "c_factor": 0.2421}
        ],
        "FSD-AF-FA-212-1.5 HR Class II": [
            {"width": 300, "height": 300, "c_factor": 0.6026},
            {"width": 600, "height": 600, "c_factor": 0.2421}
        ],
        "F/S-AFM-PB-I & F/S-AFM-OB-I Modulating 1.5 HR, Class I": [
            {"width": 300, "height": 300, "c_factor": 0.6026},
            {"width": 600, "height": 600, "c_factor": 0.2421}
        ],
        "F/S-AFM-PB-II & F/S-AFM-OB-II Modulating 1.5 HR, Class II": [
            {"width": 300, "height": 300, "c_factor": 0.6026},
            {"width": 600, "height": 600, "c_factor": 0.2421}
        ],
        "F/S-AFM-PB-3-I & F/S-AFM-OB-3-I Modulating 3 HR, Class I": [
            {"width": 300, "height": 300, "c_factor": 0.6026},
            {"width": 600, "height": 600, "c_factor": 0.2421}
        ],
        "F/S-AFM-PB-3-II & F/S-AFM-OB-3-II Modulating 3 HR, Class II": [
            {"width": 300, "height": 300, "c_factor": 0.6026},
            {"width": 600, "height": 600, "c_factor": 0.2421}
        ]
    },
    "Smoke Damper": {
        "SSD-3V-201 CLASS I": [
            {"width": 300, "height": 300, "c_factor": 1.1152},
            {"width": 600, "height": 600, "c_factor": 0.7186},
            {"width": 900, "height": 900, "c_factor": 0.3843}
        ],
        "SSD-3V-202 CLASS II": [
            {"width": 300, "height": 300, "c_factor": 1.1152},
            {"width": 600, "height": 600, "c_factor": 0.7186},
            {"width": 900, "height": 900, "c_factor": 0.3843}
        ],
        "SSD-3V-OW-201-CLASS-I": [
            {"width": 300, "height": 300, "c_factor": 1.1152},
            {"width": 600, "height": 600, "c_factor": 0.7186},
            {"width": 900, "height": 900, "c_factor": 0.3843}
        ],
        "SSD-3V-OW-202-CLASS-II": [
            {"width": 300, "height": 300, "c_factor": 1.1152},
            {"width": 600, "height": 600, "c_factor": 0.7186},
            {"width": 900, "height": 900, "c_factor": 0.3843}
        ],
        "SSD-3V-FA-201 CLASS I": [
            {"width": 300, "height": 300, "c_factor": 1.1152},
            {"width": 600, "height": 600, "c_factor": 0.7186}
        ],
        "SSD-3V-FA-202 CLASS II": [
            {"width": 300, "height": 300, "c_factor": 1.1152},
            {"width": 600, "height": 600, "c_factor": 0.7186}
        ],
        "SSD-AF-201 CLASS I": [
            {"width": 300, "height": 300, "c_factor": 0.6026},
            {"width": 600, "height": 600, "c_factor": 0.2421},
            {"width": 900, "height": 900, "c_factor": 0.1613}
        ],
        "SSD-AF-202 CLASS II": [
            {"width": 300, "height": 300, "c_factor": 0.6026},
            {"width": 600, "height": 600, "c_factor": 0.2421},
            {"width": 900, "height": 900, "c_factor": 0.1613}
        ],
        "SSD-AF-OW-201-CLASS-I": [
            {"width": 300, "height": 300, "c_factor": 0.6026},
            {"width": 600, "height": 600, "c_factor": 0.2421}
        ],
        "SSD-AF-OW-202-CLASS-II": [
            {"width": 300, "height": 300, "c_factor": 0.6026},
            {"width": 600, "height": 600, "c_factor": 0.2421}
        ],
        "SSD-AF-FA-201 CLASS I": [
            {"width": 300, "height": 300, "c_factor": 0.6026},
            {"width": 600, "height": 600, "c_factor": 0.2421}
        ],
        "SSD-AF-FA-202 CLASS II": [
            {"width": 300, "height": 300, "c_factor": 0.6026},
            {"width": 600, "height": 600, "c_factor": 0.2421}
        ],
        "S-AFM-PB-I & S-AFM-OB-I Modulating Class I": [
            {"width": 300, "height": 300, "c_factor": 0.6026},
            {"width": 600, "height": 600, "c_factor": 0.2421}
        ],
        "S-AFM-PB-II & S-AFM-OB-II Modulating Class II": [
            {"width": 300, "height": 300, "c_factor": 0.6026},
            {"width": 600, "height": 600, "c_factor": 0.2421}
        ]
    }
}


# Session state initialization defaults
INITIAL_SESSION_STATE = {
    "PRODUCT_DATA": DEFAULT_PRODUCTS.copy(),
    "damper_table": pd.DataFrame(),
    "rows_to_delete": [],
    "uploaded_filename": None,
    "show_delete_modal": False,
    "show_clear_modal": False,
    "export_columns": [],
}
