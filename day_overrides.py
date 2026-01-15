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
    }
}
