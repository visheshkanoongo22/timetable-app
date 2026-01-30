from datetime import date

DAY_SPECIFIC_OVERRIDES = {
    # --- PREVIOUS ENTRIES ---
    date(2026, 1, 6): {
        'PS&PS': {'Venue': 'POSTPONED (TBA)'}
    },

    # --- NEW ENTRIES FOR JAN 8 ---
    date(2026, 1, 8): {
        'RURMKT(A)': {'Venue': 'E6'},
        'RURMKT(B)': {'Venue': 'E6'},
        'IF(A)':     {'Venue': 'E6'},
        'IF(B)':     {'Venue': 'E6'},
        'MS(A)':     {'Venue': 'E6'},
        'GBL':       {'Venue': '308-C'},
        'MS(C)':     {'Venue': 'POSTPONED (TBA)'},
        'MC':        {'Venue': 'POSTPONED (TBA)'}
    },

    # --- NEW ENTRIES FOR JAN 9 ---
    date(2026, 1, 9): {
        'D&IT':   {'Venue': 'E6'},
        'IM':     {'Venue': 'E6'},
        'PRM(A)': {'Venue': 'E6'},
        'PRM(B)': {'Venue': 'E6'}
    },

    # --- NEW ENTRIES FOR JAN 10 ---
    date(2026, 1, 10): {
        'CRM': {'Venue': 'E2'}
    },

    date(2026, 1, 15): {
        'MS(A)': {'Venue': 'E1'},
        'IGR&MC': {'Venue': 'E1'},
        'MS(C)': {'Venue': 'E2'}
    },

    date(2026, 1, 21): {
        "D&IT": {"Venue": "POSTPONED"},
        "IGR&MC": {"Venue": "POSTPONED"}
    },

    date(2026, 1, 22): {
        "GBL": {"Venue": "T7"},
        "DIW": {"Venue": "T7"} 
    },

    date(2026, 1, 27): {
        "MS(A)": {"Venue": "POSTPONED"} 
    },

    date(2026, 1, 28): {
        "PS&PS": {"Venue": "POSTPONED"} 
    },

    date(2026, 1, 29): {
        "PPC(C)": {'Venue': 'T7'},
        "PPC(A)": {'Venue': '216'},
        "PPC(B)": {'Venue': '216'},
        "SNA":    {'Venue': '216'},
        "MC":     {'Venue': 'E1'}
    },
    # CRM Postponement
    date(2026, 2, 6): {
        "CRM": {"Venue": "POSTPONED"}
    },

    # IGR&MC Postponements
    date(2026, 2, 18): {
        "IGR&MC": {"Venue": "POSTPONED"}
    },
    date(2026, 3, 11): {
        "IGR&MC": {"Venue": "CANCELLED"}
    },
    date(2026, 3, 18): {
        "IGR&MC": {"Venue": "CANCELLED"}
    },

    # PPC Preponements (20 Feb)
    date(2026, 2, 20): {
        "PPC(B)": {"Venue": "PREPONED"},
        "PPC(C)": {"Venue": "PREPONED"}
    },

    # PPC Preponement (20 Mar)
    date(2026, 3, 20): {
        "PPC(B)": {"Venue": "PREPONED"}
    }

}
