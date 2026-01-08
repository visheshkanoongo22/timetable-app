from datetime import date

DAY_SPECIFIC_OVERRIDES = {
    # --- PREVIOUS ENTRIES (Example) ---
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
        'MS(C)':     {'Venue': 'POSTPONED (TBA)'}
    }
}
