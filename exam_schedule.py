from datetime import date

# Format:
# 'Subject_Code': The base code used in your main app (e.g., 'VALU', 'B2B')
# 'Full_Name': The name written on the exam sheet
# 'Date': date(YYYY, MM, DD)
# 'Time': String for the slot

EXAM_SCHEDULE_DATA = [
    # --- 22 Dec ---
    {'Subject_Code': 'VALU', 'Full_Name': 'Valuation', 'Date': date(2025, 12, 22), 'Time': '02:00 PM - 05:00 PM'},
    
    # --- 23 Dec ---
    {'Subject_Code': 'DRM', 'Full_Name': 'Derivatives and Risk Management', 'Date': date(2025, 12, 23), 'Time': '09:15 AM - 12:15 PM'},
    {'Subject_Code': 'B2B', 'Full_Name': 'Business-to-Business Marketing', 'Date': date(2025, 12, 23), 'Time': '02:00 PM - 05:00 PM'},

    # --- 24 Dec ---
    {'Subject_Code': 'IMC', 'Full_Name': 'Integrated Marketing Communication', 'Date': date(2025, 12, 24), 'Time': '09:15 AM - 12:15 PM'},
    {'Subject_Code': 'SCM', 'Full_Name': 'Supply Chain Management', 'Date': date(2025, 12, 24), 'Time': '02:00 PM - 05:00 PM'},

    # --- 26 Dec ---
    {'Subject_Code': 'CSE', 'Full_Name': 'Case Study of Entrepreneurs', 'Date': date(2025, 12, 26), 'Time': '09:15 AM - 12:15 PM'},

    # --- 29 Dec ---
    {'Subject_Code': 'DC', 'Full_Name': 'Digital Consulting', 'Date': date(2025, 12, 29), 'Time': '09:15 AM - 12:15 PM'},
    {'Subject_Code': 'LSS', 'Full_Name': 'Lean Six Sigma', 'Date': date(2025, 12, 29), 'Time': '02:00 PM - 05:00 PM'},

    # --- 30 Dec ---
    {'Subject_Code': 'TEOM', 'Full_Name': 'Technology Enabled Operations Management', 'Date': date(2025, 12, 30), 'Time': '09:15 AM - 12:15 PM'},
    {'Subject_Code': 'INB', 'Full_Name': 'Investment Banking', 'Date': date(2025, 12, 30), 'Time': '02:00 PM - 05:00 PM'},

    # --- 31 Dec ---
    {'Subject_Code': 'ML&AI', 'Full_Name': 'Machine Learning & Artificial Intelligence', 'Date': date(2025, 12, 31), 'Time': '09:15 AM - 12:15 PM'},
    # Note: 31st Afternoon has two electives. Code will filter based on what student has.
    {'Subject_Code': 'CC&AU', 'Full_Name': 'Commercial Credit Analysis & Underwriting', 'Date': date(2025, 12, 31), 'Time': '02:00 PM - 05:00 PM'},
    {'Subject_Code': 'OMSD', 'Full_Name': 'Operations Management in Services and Distribution', 'Date': date(2025, 12, 31), 'Time': '02:00 PM - 05:00 PM'},

    # --- 01 Jan 2026 ---
    {'Subject_Code': 'AN', 'Full_Name': 'Art of Negotiation', 'Date': date(2026, 1, 1), 'Time': '09:15 AM - 12:15 PM'},
    {'Subject_Code': 'PDBE', 'Full_Name': 'Personality Development and Business Etiquette', 'Date': date(2026, 1, 1), 'Time': '02:00 PM - 05:00 PM'},

    # --- 02 Jan 2026 ---
    {'Subject_Code': 'DM', 'Full_Name': 'Digital Marketing', 'Date': date(2026, 1, 2), 'Time': '09:15 AM - 12:15 PM'},
    {'Subject_Code': 'SMKT', 'Full_Name': 'Services Marketing', 'Date': date(2026, 1, 2), 'Time': '02:00 PM - 05:00 PM'},

    # --- 03 Jan 2026 ---
    {'Subject_Code': 'DADM', 'Full_Name': 'Data Analytics & Data Mining', 'Date': date(2026, 1, 3), 'Time': '09:15 AM - 12:15 PM'},
]
