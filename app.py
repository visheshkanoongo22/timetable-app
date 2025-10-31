# 1. IMPORTS
import pandas as pd
import os
import glob
from datetime import datetime, date
import re
import streamlit as st
from ics import Calendar, Event
import pytz
import hashlib
from collections import defaultdict
import streamlit.components.v1 as components

# 2. CONFIGURATION
SCHEDULE_FILE_NAME = 'schedule.xlsx'
TIMEZONE = 'Asia/Kolkata'
GOOGLE_CALENDAR_IMPORT_LINK = 'https://calendar.google.com/calendar/u/0/r/settings/export'

COURSE_DETAILS_MAP = {
    'AN(A)': {'Faculty': 'Nitin Pillai', 'Venue': 'T6'}, 'AN(B)': {'Faculty': 'Nitin Pillai', 'Venue': 'T6'},
    'B2B(A)': {'Faculty': 'Sandip Trada', 'Venue': 'T5'}, 'B2B(B)': {'Faculty': 'Rupam Deb', 'Venue': '208-B'},
    "B2B('C)": {'Faculty': 'Rupam Deb', 'Venue': '208-B'}, 'BS': {'Faculty': 'Satish Nair', 'Venue': 'T6'},
    'CC&AU(A)': {'Faculty': 'Lalit Arora', 'Venue': 'T6'}, 'CC&AU(B)': {'Faculty': 'Lalit Arora', 'Venue': 'T6'},
    'CSE': {'Faculty': 'Shahir Bhatt', 'Venue': 'T6'}, 'DADM': {'Faculty': 'Mahesh K C', 'Venue': 'T3'},
    'DC': {'Faculty': 'Sapan Oza', 'Venue': 'T6'}, 'DM(A)': {'Faculty': 'Shailesh Prabhu', 'Venue': 'T7'},
    'DM(B)': {'Faculty': 'Shailesh Prabhu', 'Venue': 'T7'}, "DRM('C)": {'Faculty': 'Pankaj Agrawal', 'Venue': 'T5'},
    'DRM(A)': {'Faculty': 'Bhavesh Patel', 'Venue': 'T6'}, 'DRM(B)': {'Faculty': 'Bhavesh Patel', 'Venue': 'T6'},
    "DV&VS('C)": {'Faculty': 'Anand Kumar', 'Venue': 'T5'}, 'DV&VS(A)': {'Faculty': 'Somayya Madakam', 'Venue': 'E3'},
    'DV&VS(B)': {'Faculty': 'Somayya Madakam', 'Venue': 'E3'}, 'DV&VS(D)': {'Faculty': 'Anand Kumar', 'Venue': 'T5'},
    'IMC(A)': {'Faculty': 'Sanjay Jain', 'Venue': 'T7'}, 'IMC(B)': {'Faculty': 'Riddhi Ambavale', 'Venue': 'T7'},
    'INB(A)': {'Faculty': 'M C Gupta', 'Venue': 'T6'}, 'INB(B)': {'Faculty': 'M C Gupta', 'Venue': 'T6'},
    'INB(C)': {'Faculty': 'M C Gupta', 'Venue': 'T6'}, 'LSS(A)': {'Faculty': 'Rajesh Jain', 'Venue': 'T3'},
    'LSS(B)': {'Faculty': 'Rajesh Jain', 'Venue': 'T3'}, 'ML&AI(A)': {'Faculty': 'Omkar Sahoo', 'Venue': 'T5'},
    'ML&AI(B)': {'Faculty': 'Omkar Sahoo', 'Venue': 'T5'}, 'OMSD': {'Faculty': 'Dinesh Panchal', 'Venue': 'T3'},
    'PDBE(A)': {'Faculty': 'Nina Muncherji', 'Venue': 'T7'}, 'PDBE(B)': {'Faculty': 'Nina Muncherji', 'Venue': 'T7'},
    "SCM('C)": {'Faculty': 'Praneti Shah', 'Venue': 'T3'}, 'SCM(A)': {'Faculty': 'Praneti Shah', 'Venue': 'T3'},
    'SCM(B)': {'Faculty': 'Praneti Shah', 'Venue': 'T3'}, 'SMKT(A)': {'Faculty': 'Himanshu Chauhan', 'Venue': 'T6'},
    'SMKT(B)': {'Faculty': 'Kavita Saxena', 'Venue': 'T5'}, 'TEOM(A)': {'Faculty': 'P Ganesh', 'Venue': 'T3'},
    'TEOM(B)': {'Faculty': 'P Ganesh', 'Venue': 'T3'}, "VALU('C)": {'Faculty': 'Dimple Bhojwani', 'Venue': 'T6'},
    'VALU(A)': {'Faculty': 'Dipti Saraf', 'Venue': 'T5'}, 'VALU(B)': {'Faculty': 'Dipti Saraf', 'Venue': 'T5'},
    'VALU(D)': {'Faculty': 'Dimple Bhojwani', 'Venue': 'T6'}
}

# 3. FUNCTIONS
def normalize_string(text):
    if isinstance(text, str):
        return text.replace(" ", "").replace("(", "").replace(")", "").replace("'", "").upper()
    return ""

@st.cache_data
def load_and_clean_schedule(file_path):
    try:
        df = pd.read_excel(file_path, sheet_name=1, header=None, skiprows=3)
        schedule_df = df.iloc[:, 0:14].copy()
        schedule_df[0] = pd.to_datetime(schedule_df[0], errors='coerce').dt.date
        schedule_df.dropna(subset=[0], inplace=True)
        return schedule_df
    except FileNotFoundError:
        st.error(f"FATAL ERROR: The main schedule file '{file_path}' was not found.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"FATAL ERROR: Could not load the main schedule file. Details: {e}")
        return pd.DataFrame()

@st.cache_data
def get_all_student_data(folder_path='.'):
    student_data_map = {}
    subject_files = [f for f in glob.glob(os.path.join(folder_path, '*.xlsx')) if os.path.basename(f) != SCHEDULE_FILE_NAME]
    for file in subject_files:
        try:
            df = pd.read_excel(file, header=None)
            header_row_index = -1
            for i in range(min(5, len(df))):
                if df.iloc[i].astype(str).str.upper().str.contains('ROLL').any():
                    header_row_index = i
                    break
            if header_row_index == -1:
                continue
            subject_row = df.iloc[0]
            roll_no_columns = df.iloc[header_row_index][df.iloc[header_row_index].astype(str).str.upper().str.contains('ROLL')].index
            for col_idx in roll_no_columns:
                section_name = subject_row[col_idx]
                name_column_index = col_idx + 1
                for _, row in df.iloc[header_row_index + 1:].iterrows():
                    roll_no = str(row[col_idx]).upper()
                    if 'NAN' in roll_no:
                        continue
                    student_name = row[name_column_index]
                    if roll_no not in student_data_map:
                        student_data_map[roll_no] = {'name': student_name, 'sections': set()}
                    student_data_map[roll_no]['sections'].add(section_name)
        except Exception:
            continue
    return student_data_map

def generate_ics_content(found_classes):
    c = Calendar(creator="-//Student Timetable Script//EN")
    local_tz = pytz.timezone(TIMEZONE)
    for class_info in found_classes:
        try:
            e = Event()
            time_str = class_info['Time']
            start_str_part, end_str_part = time_str.split('-')
            end_am_pm = end_str_part[-2:]
            start_am_pm = end_am_pm
            start_hour = int(re.search(r'^\d+', start_str_part).group(0))
            if end_am_pm == "PM" and start_hour < 12 and (
                start_hour > int(re.search(r'^\d+', end_str_part).group(0)) or start_hour == 11):
                start_am_pm = "AM"
            full_start_str = f"{start_str_part}{start_am_pm}"
            full_end_str = end_str_part
            start_dt = local_tz.localize(pd.to_datetime(f"{class_info['Date']} {full_start_str}"))
            end_dt = local_tz.localize(pd.to_datetime(f"{class_info['Date']} {full_end_str}"))
            e.name = f"{class_info['Subject']}"
            e.begin = start_dt.astimezone(pytz.utc)
            e.end = end_dt.astimezone(pytz.utc)
            e.location = class_info['Venue']
            e.description = f"Faculty: {class_info['Faculty']}"
            e.uid = hashlib.md5(f"{start_dt.isoformat()}-{e.name}".encode('utf-8')).hexdigest() + "@timetable.app"
            c.events.add(e)
        except Exception:
            continue
    return c.serialize()

# 4. STREAMLIT WEB APP INTERFACE
st.set_page_config(page_title="Import Timetable to Google Calendar", layout="centered", initial_sidebar_state="collapsed")

# (CSS and UI part unchanged — your same styling)
# ... [Keep your CSS block exactly as before]

# ✅ Correct placement of import
from datetime import date as dt_date

# ✅ Now inside the loop (correct indentation)
# Everything after “if roll_number in student_data_map” remains same as before

# (you can paste back your HTML/CSS + loop section here — no indentation errors now)
