import pandas as pd



DEFAULT_PRODUCTS = {
    # _____________________________Life Safety Dampers______________________
    "Life Safety Damper": {
        "Fire Damper - Static": {
            "FD-A-1.5 HR": [
                {"width": 1524, "height": 1524, "c_factor": 0.1832}
            ],
            "FD-SL-A-1.5 HR": [
                {"width": 1524, "height": 1524, "c_factor": 0.1832}
            ],
            "FD-USL-A-1.5 HR": [
                {"width": 1524, "height": 1524, "c_factor": 0.1832}
            ],
            "FD-OW-A-1.5 HR": [
                {"width": 1524, "height": 1524, "c_factor": 0.1832}
            ],
            "FD-OW-SL-A-1.5 HR": [
                {"width": 1524, "height": 1524, "c_factor": 0.1832}
            ],
            "FD-A-3 HR": [
                {"width": 1219, "height": 1219, "c_factor": 0.1832}
            ],
            "FD-SL-A-3 HR": [
                {"width": 1219, "height": 1219, "c_factor": 0.1832}
            ],
            "FD-USL-A-3 HR": [
                {"width": 1219, "height": 1219, "c_factor": 0.1832}
            ],
            "FD-OW-A-3 HR": [
                {"width": 1219, "height": 1219, "c_factor": 0.1832}
            ],
            "FD-OW-SL-A-3 HR": [
                {"width": 1219, "height": 1219, "c_factor": 0.1832}
            ],
            "FD-B-1.5 HR": [
                {"width": 1524, "height": 1397, "c_factor": 0.1759}
            ],
            "FD-SL-B-1.5 HR": [
                {"width": 1524, "height": 1397, "c_factor": 0.1759}
            ],
            "FD-USL-B-1.5 HR": [
                {"width": 1524, "height": 1397, "c_factor": 0.1759}
            ],
            "FD-OW-B-1.5 HR": [
                {"width": 1524, "height": 1397, "c_factor": 0.1759}
            ],
            "FD-OW-SL-B-1.5 HR": [
                {"width": 1524, "height": 1397, "c_factor": 0.1759}
            ],
            "FD-B-3 HR": [
                {"width": 1219, "height": 1092, "c_factor": 0.1759}
            ],
            "FD-SL-B-3 HR": [
                {"width": 1219, "height": 1092, "c_factor": 0.1759}
            ],
            "FD-USL-B-3 HR": [
                {"width": 1219, "height": 1092, "c_factor": 0.1759}
            ],
            "FD-OW-B-3 HR": [
                {"width": 1219, "height": 1092, "c_factor": 0.1759}
            ],
            "FD-OW-SL-B-3 HR": [
                {"width": 1219, "height": 1092, "c_factor": 0.1759}
            ],
            "FD-C-S/R-1.5 HR": [
                {"width": 1499, "height": 1372, "c_factor": 0.0637}
            ],
            "FD-SL-C-S/R-1.5 HR": [
                {"width": 1499, "height": 1372, "c_factor": 0.0637}
            ],
            "FD-USL-C-S/R-1.5 HR": [
                {"width": 1499, "height": 1372, "c_factor": 0.0637}
            ],
            "FD-OW-C-S/R-1.5 HR": [
                {"width": 1499, "height": 1372, "c_factor": 0.0637}
            ],
            "FD-OW-SL-C-S/R-1.5 HR": [
                {"width": 1499, "height": 1372, "c_factor": 0.0637}
            ],
            "FD-C-S/R-3 HR": [
                {"width": 1194, "height": 1067, "c_factor": 0.0637}
            ],
            "FD-SL-C-S/R-3 HR": [
                {"width": 1194, "height": 1067, "c_factor": 0.0637}
            ],
            "FD-USL-C-S/R-3 HR": [
                {"width": 1194, "height": 1067, "c_factor": 0.0637}
            ],
            "FD-OW-C-S/R-3 HR": [
                {"width": 1194, "height": 1067, "c_factor": 0.0637}
            ],
            "FD-OW-SL-C-S/R-3 HR": [
                {"width": 1194, "height": 1067, "c_factor": 0.0637}
            ]
        },

        "Fire Damper - Static - Multiblade": {
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
            ]
        },

        "Fire Damper - Dynamic": {
            "FDD-A-1.5 HR": [
                {"width": 914, "height": 914, "c_factor": 0.1832}
            ],
            "FDD-SL-A-1.5 HR": [
                {"width": 914, "height": 914, "c_factor": 0.1832}
            ],
            "FDD-USL-A-1.5 HR": [
                {"width": 914, "height": 914, "c_factor": 0.1832}
            ],
            "FDD-OW-A-1.5 HR": [
                {"width": 914, "height": 914, "c_factor": 0.1832}
            ],
            "FDD-OW-SL-A-1.5 HR": [
                {"width": 914, "height": 914, "c_factor": 0.1832}
            ],
            "FDD-A-3 HR": [
                {"width": 914, "height": 914, "c_factor": 0.1832}
            ],
            "FDD-SL-A-3 HR": [
                {"width": 914, "height": 914, "c_factor": 0.1832}
            ],
            "FDD-USL-A-3 HR": [
                {"width": 914, "height": 914, "c_factor": 0.1832}
            ],
            "FDD-OW-A-3 HR": [
                {"width": 914, "height": 914, "c_factor": 0.1832}
            ],
            "FDD-OW-SL-A-3 HR": [
                {"width": 914, "height": 914, "c_factor": 0.1832}
            ],
            "FDD-B-1.5 HR": [
                {"width": 914, "height": 813, "c_factor": 0.1759}
            ],
            "FDD-SL-B-1.5 HR": [
                {"width": 914, "height": 813, "c_factor": 0.1759}
            ],
            "FDD-USL-B-1.5 HR": [
                {"width": 914, "height": 813, "c_factor": 0.1759}
            ],
            "FDD-OW-B-1.5 HR": [
                {"width": 914, "height": 813, "c_factor": 0.1759}
            ],
            "FDD-OW-SL-B-1.5 HR": [
                {"width": 914, "height": 813, "c_factor": 0.1759}
            ],
            "FDD-B-3 HR": [
                {"width": 914, "height": 813, "c_factor": 0.1759}
            ],
            "FDD-SL-B-3 HR": [
                {"width": 914, "height": 813, "c_factor": 0.1759}
            ],
            "FDD-USL-B-3 HR": [
                {"width": 914, "height": 813, "c_factor": 0.1759}
            ],
            "FDD-OW-B-3 HR": [
                {"width": 914, "height": 813, "c_factor": 0.1759}
            ],
            "FDD-OW-SL-B-3 HR": [
                {"width": 914, "height": 813, "c_factor": 0.1759}
            ],
            "FDD-C-S/R-1.5 HR": [
                {"width": 889, "height": 787, "c_factor": 0.0637}
            ],
            "FDD-SL-C-S/R-1.5 HR": [
                {"width": 889, "height": 787, "c_factor": 0.0637}
            ],
            "FDD-USL-C-S/R-1.5 HR": [
                {"width": 889, "height": 787, "c_factor": 0.0637}
            ],
            "FDD-OW-C-S/R-1.5 HR": [
                {"width": 889, "height": 787, "c_factor": 0.0637}
            ],
            "FDD-OW-SL-C-S/R-1.5 HR": [
                {"width": 889, "height": 787, "c_factor": 0.0637}
            ],
            "FDD-C-S/R-3 HR": [
                {"width": 889, "height": 787, "c_factor": 0.0637}
            ],
            "FDD-SL-C-S/R-3 HR": [
                {"width": 889, "height": 787, "c_factor": 0.0637}
            ],
            "FDD-USL-C-S/R-3 HR": [
                {"width": 889, "height": 787, "c_factor": 0.0637}
            ],
            "FDD-OW-C-S/R-3 HR": [
                {"width": 889, "height": 787, "c_factor": 0.0637}
            ],
            "FDD-OW-SL-C-S/R-3 HR": [
                {"width": 889, "height": 787, "c_factor": 0.0637}
            ]
        },

        "Fire Damper - Dynamic - Multiblade": {
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

        "Fire & Smoke Damper - 3V Blade": {
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
            "FSD-3V-OW-211- 1.5 HR Class II": [
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
            ]
        },

        "Fire & Smoke Damper - AF Blade": {
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
            "FSD-AF-OW-211- 1.5 HR Class II": [
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
            "F/S-AFM-PB-I Modulating 1.5 HR, Class I": [
                {"width": 300, "height": 300, "c_factor": 0.6026},
                {"width": 600, "height": 600, "c_factor": 0.2421}
            ],
            "F/S-AFM-PB-II Modulating 1.5 HR, Class II": [
                {"width": 300, "height": 300, "c_factor": 0.6026},
                {"width": 600, "height": 600, "c_factor": 0.2421}
            ],
            "F/S-AFM-PB-3-I Modulating 3 HR,Class I": [
                {"width": 300, "height": 300, "c_factor": 0.6026},
                {"width": 600, "height": 600, "c_factor": 0.2421}
            ],
            "F/S-AFM-PB-3-II Modulating 3 HR,Class II": [
                {"width": 300, "height": 300, "c_factor": 0.6026},
                {"width": 600, "height": 600, "c_factor": 0.2421}
            ],
            "F/S-AFM-OB-I Modulating 1.5 HR, Class I": [
                {"width": 300, "height": 300, "c_factor": 0.6026},
                {"width": 600, "height": 600, "c_factor": 0.2421}
            ],
            "F/S-AFM-OB-II Modulating 1.5 HR, Class II": [
                {"width": 300, "height": 300, "c_factor": 0.6026},
                {"width": 600, "height": 600, "c_factor": 0.2421}
            ],
            "F/S-AFM-OB-3-I Modulating 3 HR,Class I": [
                {"width": 300, "height": 300, "c_factor": 0.6026},
                {"width": 600, "height": 600, "c_factor": 0.2421}
            ],
            "F/S-AFM-OB-3-II Modulating 3 HR,Class II": [
                {"width": 300, "height": 300, "c_factor": 0.6026},
                {"width": 600, "height": 600, "c_factor": 0.2421}
            ]
        },

        "Smoke Damper - 3V Blade": {
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
            ]
        },

        "Smoke Damper - AF Blade": {
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
            "S-AFM-PB-I Modulating Class I": [
                {"width": 300, "height": 300, "c_factor": 0.6026},
                {"width": 600, "height": 600, "c_factor": 0.2421}
            ],
            "S-AFM-PB-II Modulating Class II": [
                {"width": 300, "height": 300, "c_factor": 0.6026},
                {"width": 600, "height": 600, "c_factor": 0.2421}
            ],
            "S-AFM-OB-I Modulating Class I": [
                {"width": 300, "height": 300, "c_factor": 0.6026},
                {"width": 600, "height": 600, "c_factor": 0.2421}
            ],
            "S-AFM-OB-II Modulating Class II": [
                {"width": 300, "height": 300, "c_factor": 0.6026},
                {"width": 600, "height": 600, "c_factor": 0.2421}
            ]
        }
    },

    # _____________________________Commercial Control Dampers______________________
    "Commercial Control Damper": {
        "Rectangular Dampers": {
            "CDF-100-IN": [
                {"width": 300, "height": 300, "c_factor": 0.069},
                {"width": 600, "height": 600, "c_factor": 0.0299},
                {"width": 900, "height": 900, "c_factor": 0.0435}
            ],
            "CDF-100-EX": [
                {"width": 300, "height": 300, "c_factor": 0.0645},
                {"width": 600, "height": 600, "c_factor": 0.0252},
                {"width": 900, "height": 900, "c_factor": 0.0299}
            ],
            "CDH-125-IN": [
                {"width": 300, "height": 300, "c_factor": 0.4417},
                {"width": 600, "height": 600, "c_factor": 0.1745},
                {"width": 900, "height": 900, "c_factor": 0.1697}
            ],
            "CDH-125-EX": [
                {"width": 300, "height": 300, "c_factor": 0.424},
                {"width": 600, "height": 600, "c_factor": 0.1525},
                {"width": 900, "height": 900, "c_factor": 0.1955}
            ],
            "CDF-165-IN": [
                {"width": 300, "height": 300, "c_factor": 0.069},
                {"width": 600, "height": 600, "c_factor": 0.0299},
                {"width": 900, "height": 900, "c_factor": 0.0435}
            ],
            "CDF-165-EX": [
                {"width": 300, "height": 300, "c_factor": 0.0645},
                {"width": 600, "height": 600, "c_factor": 0.0252},
                {"width": 900, "height": 900, "c_factor": 0.0299}
            ]
        },

        "Backdraft Dampers": {
            "CB-600": [
                {"width": 1000, "height": 1000, "c_factor": 1.661}
            ],
            "CB-601": [
                {"width": 1000, "height": 1000, "c_factor": 1.661}
            ],
            "HCB-700": [
                {"width": 1219, "height": 1219, "c_factor": 0.41}
            ],
            "HCB-750": [
                {"width": 1219, "height": 1219, "c_factor": 0.41}
            ]
        },

        "Pressure Relief Dampers": {
            "CB-600": [
                {"width": 1000, "height": 1000, "c_factor": 1.661}
            ],
            "CB-601": [
                {"width": 1000, "height": 1000, "c_factor": 1.661}
            ],
            "HCB-700": [
                {"width": 1219, "height": 1219, "c_factor": 0.41}
            ],
            "HCB-750": [
                {"width": 1219, "height": 1219, "c_factor": 0.41}
            ]
        }
    }
}
CATEGORIES = list(DEFAULT_PRODUCTS.keys())
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
