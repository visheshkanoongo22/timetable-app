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
        "PPC('C)": {'Venue': 'T7'},
        "PPC(A)": {'Venue': '216'},
        "PPC(B)": {'Venue': '216'},
        "SNA":    {'Venue': '216'},
        "MC":     {'Venue': 'E1'}
    },

    date(2026, 1, 30): {
        "MC": {"Venue": "POSTPONED"}
    },
    date(2026, 1, 31): {
        # T5 Classroom Sessions
        "PPC(A)": {"Venue": "T5"},
        "PPC(B)": {"Venue": "T5"},
        "PPC('C)":    {"Venue": "T5"},
        "SNA":    {"Venue": "T5"},
        "GBL":    {"Venue": "T7"},
        "DIW":    {"Venue": "T7"}
    },

    # CRM Postponement
    date(2026, 2, 6): {
        "CRM": {"Venue": "POSTPONED"},
        "M&A(A)": {"Venue": "POSTPONED"},
        "M&A(B)": {"Venue": "POSTPONED"},
        "M&A(C)": {"Venue": "POSTPONED"}
    },

    date(2026, 2, 2): {
        "PS&PS": {"Venue": "E3"}
    },


   date(2026, 2, 3): {
        "PPC('C)": {'Venue': '216'},
        "PPC(A)": {'Venue': '216'},
        "PPC(B)": {'Venue': '216'},
        "IF(A)": {'Venue': 'E3'},
        "IGR&MC": {'Venue': 'E3'},
    },

    # --- M&A Postponements (Feb 4 & Feb 6) ---
    date(2026, 2, 4): {
        "M&A(A)": {"Venue": "POSTPONED"},
        "M&A(C)": {"Venue": "POSTPONED"},
        "M&A(B)": {"Venue": "POSTPONED"},
        "MA":     {"Venue": "T1"},
        "IGR&MC": {"Venue": "E3"},
        "IM":     {"Venue": "T1"},
        "PRM(A)": {"Venue": "T1"},
        "PRM(B)": {"Venue": "T1"}
    },

    date(2026, 2, 5): {
        "RURMKT(A)": {"Venue": "T1"},
        "RURMKT(B)": {"Venue": "T3", "Time": '8-9AM'},
        "PPC(A)": {"Venue": "T7"},
        "PPC(B)": {"Venue": "T7"},
        "IF(A)":  {"Venue": "T3"},
        "IGR&MC": {"Venue": "E3"}
    },

    date(2026, 2, 7): {
        "RUR.MKT(A)": {"Venue": "T3"},
        "RUR.MKT(B)": {"Venue": "T3"},
        "PPC(C)":     {"Venue": "T6"}
    },
    date(2026, 2, 11): {
        "D&IT": {"Venue": "CANCELLED"}
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
        "PPC(B)": {"Venue": "CANCELLED"},
        "PPC(C)": {"Venue": "CANCELLED"}
    },

    # PPC Preponement (20 Mar)
    date(2026, 3, 20): {
        "PPC(B)": {"Venue": "CANCELLED"}
    }

}
