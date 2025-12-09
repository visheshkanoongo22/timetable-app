from datetime import date

# --- ADDITIONAL CLASSES ---
ADDITIONAL_CLASSES = [
    {'Date': date(2025, 11, 8), 'Time': '10:20-11:20AM', 'Subject': 'SCM(A)', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 11, 8), 'Time': '10:20-11:20AM', 'Subject': 'SCM(B)', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 11, 8), 'Time': '10:20-11:20AM', 'Subject': "SCM('C)", 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 11, 13), 'Time': '6:10-7:10PM', 'Subject': 'INB(A)', 'Faculty': 'M C Gupta', 'Venue': 'T6 (Rescheduled)'},
    {'Date': date(2025, 11, 29), 'Time': '8:30-9:30PM', 'Subject': "DRM('C)", 'Faculty': 'Pankaj Agrawal', 'Venue': 'T3'}, 
    
    # --- B2B Rescheduled to 06.12.2025 ---
    {'Date': date(2025, 12, 6), 'Time': '6:10-7:10PM', 'Subject': 'B2B(B)', 'Faculty': 'Rupam Deb', 'Venue': 'E2'}, 
    {'Date': date(2025, 12, 6), 'Time': '7:20-8:20PM', 'Subject': "B2B('C)", 'Faculty': 'Rupam Deb', 'Venue': 'E2'},
    
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

    # --- DV&VS 23.11.2025 (Sunday) ---
    {'Date': date(2025, 11, 23), 'Time': '2:00-3:00PM', 'Subject': 'DV&VS(A)', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 11, 23), 'Time': '3:00-4:00PM', 'Subject': 'DV&VS(A)', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 11, 23), 'Time': '2:00-3:00PM', 'Subject': 'DV&VS(B)', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 11, 23), 'Time': '3:00-4:00PM', 'Subject': 'DV&VS(B)', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 11, 23), 'Time': '5:00-6:00PM', 'Subject': "DV&VS('C)", 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 11, 23), 'Time': '6:00-7:00PM', 'Subject': "DV&VS('C)", 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 11, 23), 'Time': '5:00-6:00PM', 'Subject': 'DV&VS(D)', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 11, 23), 'Time': '6:00-7:00PM', 'Subject': 'DV&VS(D)', 'Faculty': 'Guest Session', 'Venue': 'Online'},

    # --- LSS Sessions (26.11.2025 & 28.11.2025) ---
    {'Date': date(2025, 11, 26), 'Time': '8:30-9:30PM', 'Subject': 'LSS(A)', 'Faculty': 'Rajesh Jain', 'Venue': 'T3'},
    {'Date': date(2025, 11, 26), 'Time': '8:30-9:30PM', 'Subject': 'LSS(B)', 'Faculty': 'Rajesh Jain', 'Venue': 'T1'},
    
    {'Date': date(2025, 11, 28), 'Time': '7:20-8:20PM', 'Subject': 'LSS(A)', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 11, 28), 'Time': '8:30-9:30PM', 'Subject': 'LSS(A)', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 11, 28), 'Time': '7:20-8:20PM', 'Subject': 'LSS(B)', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 11, 28), 'Time': '8:30-9:30PM', 'Subject': 'LSS(B)', 'Faculty': 'Guest Session', 'Venue': 'Online'},

    # --- VALUATION (B/D) 26.11.2025 ---
    {'Date': date(2025, 11, 26), 'Time': '2:40-3:40PM', 'Subject': 'VALU(B)', 'Faculty': 'Extra Session', 'Venue': 'TBA'},
    {'Date': date(2025, 11, 26), 'Time': '2:40-3:40PM', 'Subject': 'VALU(D)', 'Faculty': 'Extra Session', 'Venue': 'TBA'},

    # --- DV&VS(C) Rescheduled ---
    {'Date': date(2025, 11, 28), 'Time': '3:50-4:50PM', 'Subject': "DV&VS('C)", 'Faculty': 'Anand Kumar', 'Venue': 'E2 (Rescheduled)'},
    {'Date': date(2025, 11, 28), 'Time': '5-6PM', 'Subject': "DV&VS('C)", 'Faculty': 'Anand Kumar', 'Venue': 'E2 (Rescheduled)'},
    {'Date': date(2025, 12, 5), 'Time': '3:50-4:50PM', 'Subject': "DV&VS('C)", 'Faculty': 'Anand Kumar', 'Venue': 'E2 (Rescheduled)'},
    {'Date': date(2025, 12, 5), 'Time': '5-6PM', 'Subject': "DV&VS('C)", 'Faculty': 'Anand Kumar', 'Venue': 'E2 (Rescheduled)'},
    
    # --- SMKT Guest Sessions 03.12.2025 ---
    {'Date': date(2025, 12, 3), 'Time': '3:50-4:50PM', 'Subject': 'SMKT(A)', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 12, 3), 'Time': '5:00-6:00PM', 'Subject': 'SMKT(A)', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 12, 3), 'Time': '3:50-4:50PM', 'Subject': 'SMKT(B)', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 12, 3), 'Time': '5:00-6:00PM', 'Subject': 'SMKT(B)', 'Faculty': 'Guest Session', 'Venue': 'Online'},

    # --- DADM Extra Sessions 03.12.2025 ---
    {'Date': date(2025, 12, 3), 'Time': '3:50-4:50PM', 'Subject': 'DADM', 'Faculty': 'Extra Session', 'Venue': 'TBA'},
    {'Date': date(2025, 12, 3), 'Time': '5:00-6:00PM', 'Subject': 'DADM', 'Faculty': 'Extra Session', 'Venue': 'TBA'},

    # --- IMC(A) Sessions 06.12.2025 ---
    {'Date': date(2025, 12, 6), 'Time': '3:50-4:50PM', 'Subject': 'IMC(A)', 'Faculty': 'Sanjay Jain', 'Venue': 'E2'},
    {'Date': date(2025, 12, 6), 'Time': '5:00-6:00PM', 'Subject': 'IMC(A)', 'Faculty': 'Sanjay Jain', 'Venue': 'E2'},

    # --- DADM Guest Sessions 07.12.2025 ---
    {'Date': date(2025, 12, 7), 'Time': '10:20-11:20AM', 'Subject': 'DADM', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 12, 7), 'Time': '11:30-12:30PM', 'Subject': 'DADM', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    # --- SMKT Guest Session 10.12.2025 ---
    {'Date': date(2025, 12, 10), 'Time': '7:20-8:20PM', 'Subject': 'SMKT(A)', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 12, 10), 'Time': '7:20-8:20PM', 'Subject': 'SMKT(B)', 'Faculty': 'Guest Session', 'Venue': 'Online'},

    # --- DADM Guest Sessions 13.12.2025 ---
    {'Date': date(2025, 12, 13), 'Time': '10:20-11:20AM', 'Subject': 'DADM', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 12, 13), 'Time': '11:30-12:30PM', 'Subject': 'DADM', 'Faculty': 'Guest Session', 'Venue': 'Online'},

    # --- ML&AI Guest Sessions 14.12.2025 ---
    {'Date': date(2025, 12, 14), 'Time': '5:00-6:00PM', 'Subject': 'ML&AI(A)', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 12, 14), 'Time': '6:10-7:10PM', 'Subject': 'ML&AI(A)', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 12, 14), 'Time': '5:00-6:00PM', 'Subject': 'ML&AI(B)', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 12, 14), 'Time': '6:10-7:10PM', 'Subject': 'ML&AI(B)', 'Faculty': 'Guest Session', 'Venue': 'Online'},

    # --- ML&AI Guest Sessions 15.12.2025 ---
    {'Date': date(2025, 12, 15), 'Time': '8:30-9:30PM', 'Subject': 'ML&AI(A)', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 12, 15), 'Time': '8:30-9:30PM', 'Subject': 'ML&AI(B)', 'Faculty': 'Guest Session', 'Venue': 'Online'},

    # --- ML&AI Guest Sessions 16.12.2025 ---
    {'Date': date(2025, 12, 16), 'Time': '8:30-9:30PM', 'Subject': 'ML&AI(A)', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 12, 16), 'Time': '8:30-9:30PM', 'Subject': 'ML&AI(B)', 'Faculty': 'Guest Session', 'Venue': 'Online'},


    # --- CC&AU Guest Sessions 13.12.2025 ---
    {'Date': date(2025, 12, 13), 'Time': '6:10-7:10PM', 'Subject': 'CC&AU(A)', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 12, 13), 'Time': '7:20-8:20PM', 'Subject': 'CC&AU(A)', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 12, 13), 'Time': '6:10-7:10PM', 'Subject': 'CC&AU(B)', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 12, 13), 'Time': '7:20-8:20PM', 'Subject': 'CC&AU(B)', 'Faculty': 'Guest Session', 'Venue': 'Online'},

    # --- CC&AU Guest Sessions 14.12.2025 ---
    {'Date': date(2025, 12, 14), 'Time': '10:20-11:20AM', 'Subject': 'CC&AU(A)', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 12, 14), 'Time': '11:30-12:30PM', 'Subject': 'CC&AU(A)', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 12, 14), 'Time': '10:20-11:20AM', 'Subject': 'CC&AU(B)', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 12, 14), 'Time': '11:30-12:30PM', 'Subject': 'CC&AU(B)', 'Faculty': 'Guest Session', 'Venue': 'Online'},
]
