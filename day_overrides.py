from datetime import date

# --- DAY-SPECIFIC OVERRIDES ---
# Format: date(YYYY, MM, DD): {'SUBJECT': {'Venue': '...'}, ...}
DAY_SPECIFIC_OVERRIDES = {
    date(2025, 11, 8): {
        'DC': {'Venue': '216'}, 'VALUC': {'Venue': '216'}, 'VALUD': {'Venue': '216'}, 'IMCB': {'Venue': '216'},
    },
    date(2025, 11, 10): {
        'B2BB': {'Venue': 'E1'}, 'B2BC': {'Venue': 'E1'}, 'DV&VSC': {'Venue': 'E2'},
        'DMB': {'Venue': '214'}, 'DMA': {'Venue': '214'}, 'OMSD': {'Venue': '214'},
    },
    date(2025, 11, 11): {
        'SMKTB': {'Venue': 'POSTPONED', 'Faculty': 'Session Postponed'}, 'IMCA': {'Venue': 'T3'}
    },
    date(2025, 11, 12): {
        'INBA': {'Venue': 'POSTPONED', 'Faculty': 'Session Postponed'}
    },
    date(2025, 11, 13): {
        'SMKTA': {'Venue': 'T7'},
        'BS':    {'Venue': 'T7'},
        'ANA':   {'Venue': 'T7'},
        'ANB':   {'Venue': 'T7'},
        'LSSA':  {'Venue': 'T1'},
        'B2BA':  {'Venue': 'E1'},
        'DVVSC': {'Venue': 'E2'},
        'OMSD':  {'Venue': 'T3'},
        'B2BB':  {'Venue': 'POSTPONED', 'Faculty': 'Session Postponed'}, 
        'B2BC':  {'Venue': 'POSTPONED', 'Faculty': 'Session Postponed'}, 
        'IMCA':  {'Venue': 'T3'},
    },
    date(2025, 11, 14): {
        'B2BB': {'Venue': 'CANCELLED', 'Faculty': 'Session Cancelled'}, 
        'B2BC': {'Venue': 'CANCELLED', 'Faculty': 'Session Cancelled'},
        'SCMB': {'Venue': 'T4'}, 
    },
    date(2025, 11, 15): {
        'DADM': {'Venue': 'POSTPONED', 'Faculty': 'Session Postponed'}, 
        'LSSA': {'Venue': 'E2'},
        'IMCA': {'Venue': 'T6'}, 
    },
    date(2025, 11, 16): { 
        'IMCB': {'Venue': 'T7'}, 
    },
    date(2025, 11, 17): {
        'DV&VSC': {'Venue': 'POSTPONED', 'Faculty': 'Session Postponed'},
        'B2BB':  {'Venue': 'E1'},
        'B2BC':  {'Venue': 'E1'},
        'B2BA':  {'Venue': 'E2'},
        'OMSD':  {'Venue': '214'},
        'TEOMA': {'Venue': '216'},
        'TEOMB': {'Venue': '216'},
    },
    date(2025, 11, 18): {
        'DV&VSD': {'Venue': 'CANCELLED', 'Faculty': 'Session Cancelled'},
    },
    date(2025, 11, 19): {
        'DV&VSD': {'Venue': 'CANCELLED', 'Faculty': 'Session Cancelled'},
        'DV&VSA': {'Venue': 'POSTPONED', 'Faculty': 'Session Postponed'}, 
        'SMKTA': {'Venue': 'POSTPONED', 'Faculty': 'Session Postponed'}, 
        'SMKTB': {'Venue': 'POSTPONED', 'Faculty': 'Session Postponed'}, 
        'VALUB': {'Time': '02:30-03:30PM'},
        'BS':    {'Venue': 'T4'},
    },
    date(2025, 11, 20): {
        'DV&VSC': {'Venue': 'POSTPONED', 'Faculty': 'Session Postponed'},
        'IMCA':   {'Venue': 'T3'}, 
        'IMCB':   {'Venue': 'T3'}, 
        'B2BB':   {'Venue': 'E2'}, 
        'B2BC':   {'Venue': 'E2'}, 
        'DMA':    {'Venue': 'T6'}, 
        'DMB':    {'Venue': 'T6'}, 
        'OMSD':   {'Venue': 'T3'}, 
        'ML&AIA': {'Venue': 'T7'},
        'SMKTB':  {'Venue': 'T7'},
        'B2BA':   {'Venue': 'T7'},
        'SMKTA':  {'Venue': 'POSTPONED', 'Faculty': 'Session Postponed'},
    },
    date(2025, 11, 21): {
        'DV&VSC': {'Venue': 'CANCELLED', 'Faculty': 'Session Cancelled'},
        'DRMC':   {'Venue': 'T7'},
        'B2BB':   {'Venue': 'E1'}, 
        'B2BC':   {'Venue': 'E1'}, 
        'B2BA':   {'Venue': 'E2'}, 
        'DMA':    {'Venue': 'T6'}, 
        'DMB':    {'Venue': 'T6'}, 
    },
    date(2025, 11, 22): {
        'DC':    {'Venue': '214'},
        'SMKTB': {'Venue': '214'},
        'IMCB':  {'Venue': '214'},
        'VALUC': {'Venue': 'POSTPONED', 'Faculty': 'Session Postponed'}, 
        'VALUD': {'Venue': 'POSTPONED', 'Faculty': 'Session Postponed'}, 
    },
    date(2025, 11, 24): {
        'DV&VSC': {'Venue': 'CANCELLED', 'Faculty': 'Session Cancelled'},
        'DRMC':   {'Venue': 'T7'},
        'B2BB':   {'Venue': 'E3'},
        'B2BC':   {'Venue': 'E3'},
        'B2BA':   {'Venue': 'E1'},
        'DMA':    {'Venue': '215'},
        'DMB':    {'Venue': '215'},
        'OMSD':   {'Venue': '215'},
    },
    date(2025, 11, 25): {
        'IMCA':  {'Venue': 'T1'},
        'VALUC': {'Venue': 'E1'},
        'VALUD': {'Venue': 'E1'},
        'DC':    {'Venue': '215'},
    },
    date(2025, 11, 26): {
        'VALUA': {'Time': '01:30-02:30PM'},
        'VALUB': {'Time': '01:30-02:30PM'},
        'VALUC': {'Time': '01:30-02:30PM'},
        'VALUD': {'Time': '01:30-02:30PM'},
        'DV&VSA': {'Venue': 'T7'},
        'IMCB':   {'Venue': 'T6'},
    },
    date(2025, 11, 27): {
        'IMCA': {'Venue': 'T3'},
        'B2BB': {'Venue': 'E1'},
        'B2BC': {'Venue': 'E1'},
        'B2BA': {'Venue': 'E2'},
        'DMA':  {'Venue': 'T6'},
        'DMB':  {'Venue': 'T6'},
        'OMSD': {'Venue': 'T6'},
    },
    date(2025, 11, 28): {
        'VALUA': {'Venue': 'CANCELLED', 'Faculty': 'Session Cancelled'},
        'DRMA':  {'Venue': 'CANCELLED', 'Faculty': 'Session Cancelled'},
        'DRMB':  {'Venue': 'CANCELLED', 'Faculty': 'Session Cancelled'},
        'B2BB':  {'Venue': 'E1'},
        'B2BC':  {'Venue': 'E1'},
        'B2BA':  {'Venue': 'E2'},
        'DMA':   {'Venue': '214'},
        'DMB':   {'Venue': '214'},
    },
    date(2025, 11, 29): {
        'IMCA': {'Venue': 'T6'},
        'IMCB': {'Venue': 'T3'},
        'DMA':  {'Venue': 'T3'},
        'DMB':  {'Venue': 'T3'},
    },
    date(2025, 12, 1): {
        'B2BB':   {'Venue': '208 B'},
        'B2BC':   {'Venue': '208 B'},
        'B2BA':   {'Venue': 'E1'},
        'DV&VSC': {'Venue': 'E2'},
        'DMA':    {'Venue': '215'},
        'DMB':    {'Venue': '215'},
        'OMSD':   {'Venue': '215'},
    },
    date(2025, 12, 2): {
        'IMCA':   {'Venue': 'T3'},
        'DV&VSD': {'Venue': 'T5'},
        'DC':     {'Venue': 'T3'},
        'VALUC':  {'Venue': 'T3'},
        'VALUD':  {'Venue': 'T3'},
        'DV&VSA': {'Venue': 'T1'},
    },
    date(2025, 12, 3): {
        'DV&VSA': {'Time': '06:10-08:20PM'},
        'DV&VSD': {'Time': '06:10-08:20PM', 'Venue': 'E1'},
        'IMCB':   {'Time': '08:30-09:30PM', 'Venue': 'E2'},
        'VALUC':  {'Venue': 'E2'},
        'VALUD':  {'Venue': 'E2'},
        'DADM':   {'Venue': 'E2'},
    },
    date(2025, 12, 4): {
        'IMCA': {'Venue': 'T3'},
        'DMA':  {'Venue': 'T3'},
        'DMB':  {'Venue': 'T3'},
        'OMSD': {'Venue': 'T3'},
        'B2BB': {'Venue': 'E2'},
        'B2BC': {'Venue': 'E2'},
        'B2BA': {'Venue': 'E1'},
    },
    date(2025, 12, 5): {
        'VALUB': {'Venue': 'CANCELLED', 'Faculty': 'Session Cancelled'},
        'VALUA': {'Venue': '214'},
        'ANA':   {'Venue': '214'},
        'ANB':   {'Venue': '214'},
        'DMA':   {'Venue': '214'},
        'DMB':   {'Venue': '214'},
        'B2BB':  {'Venue': 'E3'},
        'B2BC':  {'Venue': 'E3'},
        'B2BA':  {'Venue': 'E1'},
        'SCMA':  {'Venue': '309-F'},
        'SCMB':  {'Venue': '309-F'},
        'SCMC':  {'Venue': '309-F'},
    },
    date(2025, 12, 6): {
        # Morning session cancelled (Partial Cancellation Logic)
        'IMCA': {'Venue': 'CANCELLED', 'Faculty': 'Session Cancelled', 'Target_Time': '8-9AM'},
        # New venue for IMC(B)
        'IMCB': {'Venue': 'E3'}, 
    },
    date(2025, 12, 8): {
        'DRMC':   {'Venue': 'T7'},
        'B2BB':   {'Venue': 'E3'},
        'B2BC':   {'Venue': 'E3'},
        'DV&VSC': {'Venue': 'E3'},
        'DMA':    {'Venue': '215'},
        'DMB':    {'Venue': '215'},
        'OMSD':   {'Venue': '215'},
        'SCMA':   {'Venue': '309-F'},
        'SCMB':   {'Venue': '309-F'},
        'SCMC':   {'Venue': '309-F'},
        'B2BA':   {'Venue': 'E2'},
        'DV&VSA': {'Venue': 'CANCELLED', 'Faculty': 'Session Cancelled'}, # <-- NEW
        'DV&VSB': {'Venue': 'CANCELLED', 'Faculty': 'Session Cancelled'}, # <-- NEW
    },
    date(2025, 12, 9): {
        'IMCA':   {'Venue': 'T3'},
        'VALUC':  {'Venue': 'T3'},
        'VALUD':  {'Venue': 'T3'},
        'ML&AIA': {'Venue': '216'},
        'ML&AIB': {'Venue': '216'},
        'SMKTB':  {'Venue': '216'},
        'VALUA':  {'Venue': 'E3'},
        'VALUB':  {'Venue': 'E3'},
        'DV&VSD': {'Venue': 'E3'},
        'DC':     {'Venue': 'E3'},
        'DV&VSA': {'Venue': 'CANCELLED', 'Faculty': 'Session Cancelled'}, # <-- NEW
        'DV&VSB': {'Venue': 'CANCELLED', 'Faculty': 'Session Cancelled'}, # <-- NEW
    },

    date(2025, 12, 10): {
        'DV&VSA': {'Venue': 'CANCELLED', 'Faculty': 'Session Cancelled'},
        'DV&VSB': {'Venue': 'CANCELLED', 'Faculty': 'Session Cancelled'},
        'SCMA':   {'Venue': '309-F'},
        'SCMB':   {'Venue': '309-F'},
        'SCMC':   {'Venue': '309-F'},
        'VALUC':  {'Venue': 'T3'}, # <-- NEW
        'VALUD':  {'Venue': 'T3'}, # <-- NEW
        'IMCB':   {'Venue': 'T3'}, # <-- NEW
        'SMKTA':  {'Venue': 'T3'}, # <-- NEW
        'DV&VSD': {'Venue': 'E3'}, # <-- NEW
        'SMKTB':  {'Venue': 'T1'}, # <-- NEW
        'BS':  {'Venue': 'E2'}, # <-- NEW
    },

    date(2025, 12, 11): {
        'DV&VSA': {'Venue': 'CANCELLED', 'Faculty': 'Session Cancelled'},
        'DV&VSB': {'Venue': 'CANCELLED', 'Faculty': 'Session Cancelled'},
        'IMCA':   {'Venue': 'T3'},
        'B2BA':   {'Venue': 'E3'},
        'B2BB':   {'Venue': '214'},
        'B2BC':   {'Venue': '214'}, # <-- NEW
        'DMA':    {'Venue': '215'}, # <-- NEW
        'DMB':    {'Venue': '215'}, # <-- NEW
        'OMSD':   {'Venue': '215'}, # <-- NEW
    },

    date(2025, 12, 12): {
        'VALUA': {'Venue': 'CANCELLED', 'Faculty': 'Session Cancelled'},
        'VALUB': {'Venue': 'CANCELLED', 'Faculty': 'Session Cancelled'},
        'B2BB':  {'Venue': 'E5'},   # <-- NEW
        'B2BC':  {'Venue': 'E5'},   # <-- NEW
        'B2BA':  {'Venue': 'E2'},   # <-- NEW
        'DMA':   {'Venue': '215'},  # <-- NEW
        'DMB':   {'Venue': '215'},  # <-- NEW
        'TEOMA': {'Venue': '216'}, # <-- NEW
        'TEOMB': {'Venue': '216'}, # <-- NEW
   },

    # --- 13.12.2025 (Saturday) ---
    date(2025, 12, 13): {
        'DC':    {'Venue': 'T3'},
        'DADM':  {'Venue': 'T3'},
        'VALUC': {'Venue': 'T3'},
        'VALUD': {'Venue': 'T3'},
        'IMCB':  {'Venue': 'T3'},
        'SMKTB': {'Venue': '214'},
    },
    # --- 15.12.2025 (Monday) ---
    date(2025, 12, 15): {
        'B2BB':   {'Venue': 'E1'},
        'B2BC':   {'Venue': 'E1'},
        'DV&VSC': {'Venue': 'E1'},
        'B2BA':   {'Venue': 'E2'},
        'DMB':    {'Venue': '215'},
        'DMA':    {'Venue': '215'},
        'OMSD':   {'Venue': '215'},
    },
    date(2025, 12, 16): {
        'IMCA':   {'Venue': 'T3'},
        'DV&VSA': {'Venue': 'T4'},
        'DV&VSD': {'Venue': 'T5'},
        'DC':     {'Venue': 'T3'},
    },
    # --- 17.12.2025 (Wednesday) ---
    date(2025, 12, 17): {
        'VALUC': {'Venue': 'T3'},
        'VALUD': {'Venue': 'T3'},
        'IMCB':  {'Venue': 'T3'},
        'IMCA':  {'Venue': 'T1'},
        'INBA': {'Venue': 'POSTPONED', 'Faculty': 'Session Postponed'}, 
    },
    # --- 18.12.2025 (Thursday) ---
    date(2025, 12, 18): {
        'IMCA':   {'Venue': 'T3'},
        'B2BA':   {'Venue': '216'},
        'B2BB':   {'Venue': '216'},
        'B2BC':   {'Venue': '216'},
        'DMA':    {'Venue': '215'},
        'DMB':    {'Venue': '215'},
        'OMSD':   {'Venue': '215'},
        'DC':     {'Venue': '215'},
    },


    date(2025, 12, 19): {
        'VALUA': {'Venue': 'CANCELLED', 'Faculty': 'Session Cancelled'},
        'VALUB': {'Venue': 'CANCELLED', 'Faculty': 'Session Cancelled'},
        'B2BB': {'Venue': 'T3'},
        'B2BC': {'Venue': 'T3'},
        'DMA':  {'Venue': '215'},
        'DMB':  {'Venue': '215'},
        'INBA': {'Venue': 'CANCELLED', 'Faculty': 'Session Postponed'}, # <-- NEW
        'INBB': {'Venue': 'CANCELLED', 'Faculty': 'Session Postponed'}, # <-- NEW
        'INBC': {'Venue': 'CANCELLED', 'Faculty': 'Session Postponed'}, # <-- NEW
    },
# --- 20.12.2025 (Saturday) ---
    date(2025, 12, 20): {
        'VALUC': {'Venue': 'CANCELLED', 'Faculty': 'Session Cancelled'},
        'VALUD': {'Venue': 'CANCELLED', 'Faculty': 'Session Cancelled'},
    }
}
