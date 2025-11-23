from datetime import date

# --- ADDITIONAL CLASSES ---
ADDITIONAL_CLASSES = [
    {'Date': date(2025, 11, 8), 'Time': '10:20-11:20AM', 'Subject': 'SCM(A)', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 11, 8), 'Time': '10:20-11:20AM', 'Subject': 'SCM(B)', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 11, 8), 'Time': '10:20-11:20AM', 'Subject': "SCM('C)", 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 11, 13), 'Time': '6:10-7:10PM', 'Subject': 'INB(A)', 'Faculty': 'M C Gupta', 'Venue': 'T6 (Rescheduled)'},
    {'Date': date(2025, 11, 29), 'Time': '8:30-9:30PM', 'Subject': "DRM('C)", 'Faculty': 'Pankaj Agrawal', 'Venue': 'T5 (Preponed)'}, 
    {'Date': date(2025, 12, 6), 'Time': '6:10-7:10PM', 'Subject': 'B2B(B)', 'Faculty': 'Rupam Deb', 'Venue': 'E2 (Rescheduled)'}, 
    {'Date': date(2025, 12, 6), 'Time': '7:20-8:20PM', 'Subject': "B2B('C)", 'Faculty': 'Rupam Deb', 'Venue': 'E2 (Rescheduled)'},
    
    # --- VALUATION 14.11.2025 ---
    {'Date': date(2025, 11, 14), 'Time': '7:20-8:20PM', 'Subject': 'VALU(A)', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 11, 14), 'Time': '8:30-9:30PM', 'Subject': 'VALU(A)', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 11, 14), 'Time': '7:20-8:20PM', 'Subject': 'VALU(B)', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 11, 14), 'Time': '8:30-9:30PM', 'Subject': 'VALU(B)', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 11, 14), 'Time': '7:20-8:20PM', 'Subject': "VALU('C)", 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 11, 14), 'Time': '8:30-9:30PM', 'Subject': "VALU('C)", 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 11, 14), 'Time': '7:20-8:20PM', 'Subject': 'VALU(D)', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 11, 14), 'Time': '8:30-9:30PM', 'Subject': 'VALU(D)', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    
    # --- DV&VS 16.11.2025 ---
    {'Date': date(2025, 11, 16), 'Time': '5-6PM', 'Subject': 'DV&VS(A)', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 11, 16), 'Time': '6:10-7:10PM', 'Subject': 'DV&VS(A)', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 11, 16), 'Time': '5-6PM', 'Subject': 'DV&VS(B)', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 11, 16), 'Time': '6:10-7:10PM', 'Subject': 'DV&VS(B)', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 11, 16), 'Time': '5-6PM', 'Subject': "DV&VS('C)", 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 11, 16), 'Time': '6:10-7:10PM', 'Subject': "DV&VS('C)", 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 11, 16), 'Time': '5-6PM', 'Subject': 'DV&VS(D)', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 11, 16), 'Time': '6:10-7:10PM', 'Subject': 'DV&VS(D)', 'Faculty': 'Guest Session', 'Venue': 'Online'},

    # --- VALUATION 21.11.2025 ---
    {'Date': date(2025, 11, 21), 'Time': '7:20-8:20PM', 'Subject': 'VALU(A)', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 11, 21), 'Time': '8:30-9:30PM', 'Subject': 'VALU(A)', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 11, 21), 'Time': '7:20-8:20PM', 'Subject': 'VALU(B)', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 11, 21), 'Time': '8:30-9:30PM', 'Subject': 'VALU(B)', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 11, 21), 'Time': '7:20-8:20PM', 'Subject': "VALU('C)", 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 11, 21), 'Time': '8:30-9:30PM', 'Subject': "VALU('C)", 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 11, 21), 'Time': '7:20-8:20PM', 'Subject': 'VALU(D)', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 11, 21), 'Time': '8:30-9:30PM', 'Subject': 'VALU(D)', 'Faculty': 'Guest Session', 'Venue': 'Online'},

    # --- NEW: DV&VS 23.11.2025 (Sunday) ---
    # Sections A & B (2PM - 4PM)
    {'Date': date(2025, 11, 23), 'Time': '2:00-3:00PM', 'Subject': 'DV&VS(A)', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 11, 23), 'Time': '3:00-4:00PM', 'Subject': 'DV&VS(A)', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 11, 23), 'Time': '2:00-3:00PM', 'Subject': 'DV&VS(B)', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 11, 23), 'Time': '3:00-4:00PM', 'Subject': 'DV&VS(B)', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    # Sections C & D (5PM - 7PM)
    {'Date': date(2025, 11, 23), 'Time': '5:00-6:00PM', 'Subject': "DV&VS('C)", 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 11, 23), 'Time': '6:00-7:00PM', 'Subject': "DV&VS('C)", 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 11, 23), 'Time': '5:00-6:00PM', 'Subject': 'DV&VS(D)', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 11, 23), 'Time': '6:00-7:00PM', 'Subject': 'DV&VS(D)', 'Faculty': 'Guest Session', 'Venue': 'Online'},

    # --- NEW: DV&VS(C) Rescheduled ---
    {'Date': date(2025, 11, 28), 'Time': '3:50-4:50PM', 'Subject': "DV&VS('C)", 'Faculty': 'Anand Kumar', 'Venue': 'E2 (Rescheduled)'},
    {'Date': date(2025, 11, 28), 'Time': '5-6PM', 'Subject': "DV&VS('C)", 'Faculty': 'Anand Kumar', 'Venue': 'E2 (Rescheduled)'},
    {'Date': date(2025, 12, 5), 'Time': '3:50-4:50PM', 'Subject': "DV&VS('C)", 'Faculty': 'Anand Kumar', 'Venue': 'E2 (Rescheduled)'},
    {'Date': date(2025, 12, 5), 'Time': '5-6PM', 'Subject': "DV&VS('C)", 'Faculty': 'Anand Kumar', 'Venue': 'E2 (Rescheduled)'},
]
