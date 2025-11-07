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
from streamlit_javascript import st_javascript  # ✅ Added
import streamlit.components.v1 as components

# 2. CONFIGURATION
SCHEDULE_FILE_NAME = 'schedule.xlsx'
TIMEZONE = 'Asia/Kolkata'
GOOGLE_CALENDAR_IMPORT_LINK = 'https://calendar.google.com/calendar/u/0/r/settings/export'
COURSE_DETAILS_MAP = {
    'AN(A)': {'Faculty': 'Nitin Pillai', 'Venue': 'T6'}, 'AN(B)': {'Faculty': 'Nitin Pillai', 'Venue': 'T6'},
    'B2B(A)': {'Faculty': 'Sandip Trada', 'Venue': 'T5'}, 'B2B(B)': {'Faculty': 'Rupam Deb', 'Venue': 'E2'},
    "B2B('C)": {'Faculty': 'Rupam Deb', 'Venue': 'E2'}, 'BS': {'Faculty': 'Satish Nair', 'Venue': 'T6'},
    'CC&AU(A)': {'Faculty': 'Lalit Arora', 'Venue': 'T6'}, 'CC&AU(B)': {'Faculty': 'Lalit Arora', 'Venue': 'T6'},
    'CSE': {'Faculty': 'Shahir Bhatt', 'Venue': 'T6'}, 'DADM': {'Faculty': 'Mahesh K C', 'Venue': 'T3'},
    'DC': {'Faculty': 'Sapan Oza', 'Venue': 'T6'}, 'DM(A)': {'Faculty': 'Shailesh Prabhu', 'Venue': 'T7'},
    'DM(B)': {'Faculty': 'Shailesh Prabhu', 'Venue': 'T7'}, "DRM('C)": {'Faculty': 'Pankaj Agrawal', 'Venue': 'T5'},
    'DRM(A)': {'Faculty': 'Bhavesh Patel', 'Venue': 'T6'}, 'DRM(B)': {'Faculty': 'Bhavesh Patel', 'Venue': 'T6'},
    "DV&VS('C)": {'Faculty': 'Anand Kumar', 'Venue': 'E2'}, 'DV&VS(A)': {'Faculty': 'Somayya Madakam', 'Venue': 'E3'},
    'DV&VS(B)': {'Faculty': 'Somayya Madakam', 'Venue': 'E3'}, 'DV&VS(D)': {'Faculty': 'Anand Kumar', 'Venue': 'E2'},
    'IMC(A)': {'Faculty': 'Sanjay Jain', 'Venue': 'T1'}, 'IMC(B)': {'Faculty': 'Riddhi Ambavale', 'Venue': 'T7'},
    'INB(A)': {'Faculty': 'M C Gupta', 'Venue': 'T7'}, 'INB(B)': {'Faculty': 'M C Gupta', 'Venue': 'T7'},
    'INB(C)': {'Faculty': 'M C Gupta', 'Venue': 'T7'}, 'LSS(A)': {'Faculty': 'Rajesh Jain', 'Venue': 'T3'},
    'LSS(B)': {'Faculty': 'Rajesh Jain', 'Venue': 'T3'}, 'ML&AI(A)': {'Faculty': 'Omkar Sahoo', 'Venue': 'T5'},
    'ML&AI(B)': {'Faculty': 'Omkar Sahoo', 'Venue': 'T5'}, 'OMSD': {'Faculty': 'Dinesh Panchal', 'Venue': 'T3'},
    'PDBE(A)': {'Faculty': 'Nina Muncherji', 'Venue': 'T6'}, 'PDBE(B)': {'Faculty': 'Nina Muncherji', 'Venue': 'T6'},
    "SCM('C)": {'Faculty': 'Praneti Shah', 'Venue': 'T3'}, 'SCM(A)': {'Faculty': 'Praneti Shah', 'Venue': 'T3'},
    'SCM(B)': {'Faculty': 'Praneti Shah', 'Venue': 'T3'}, 'SMKT(A)': {'Faculty': 'Himanshu Chauhan', 'Venue': 'T6'},
    'SMKT(B)': {'Faculty': 'Kavita Saxena', 'Venue': 'T5'}, 'TEOM(A)': {'Faculty': 'P Ganesh', 'Venue': 'T3'},
    'TEOM(B)': {'Faculty': 'P Ganesh', 'Venue': 'T3'}, "VALU('C)": {'Faculty': 'Dimple Bhojwani', 'Venue': 'T6'},
    'VALU(A)': {'Faculty': 'Dipti Saraf', 'Venue': 'T5'}, 'VALU(B)': {'Faculty': 'Dipti Saraf', 'Venue': 'T5'},
    'VALU(D)': {'Faculty': 'Dimple Bhojwani', 'Venue': 'T6'}
}

# --- DAY-SPECIFIC OVERRIDES & ADDITIONS ---
DAY_SPECIFIC_OVERRIDES = {
    date(2025, 11, 8): {
        'DC': {'Venue': '216'}, 'VALUC': {'Venue': '216'}, 'VALUD': {'Venue': '216'}, 'IMCB': {'Venue': '216'},
    },
    date(2025, 11, 10): {
        'B2BB': {'Venue': 'E1'}, 'B2BC': {'Venue': 'E1'}, 'DVVSC': {'Venue': 'E2'},
        'DMB': {'Venue': '214'}, 'DMA': {'Venue': '214'}, 'OMSD': {'Venue': '214'},
    }
}
ADDITIONAL_CLASSES = [
    {'Date': date(2025, 11, 8), 'Time': '10:20-11:20AM', 'Subject': 'SCM(A)', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 11, 8), 'Time': '10:20-11:20AM', 'Subject': 'SCM(B)', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 11, 8), 'Time': '10:20-11:20AM', 'Subject': "SCM('C)", 'Faculty': 'Guest Session', 'Venue': 'Online'},
]

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
            subject_row, roll_no_columns = df.iloc[0], df.iloc[header_row_index][
                df.iloc[header_row_index].astype(str).str.upper().str.contains('ROLL')
            ].index
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
                start_hour > int(re.search(r'^\d+', end_str_part).group(0)) or start_hour == 11
            ):
                start_am_pm = "AM"
            full_start_str, full_end_str = f"{start_str_part}{start_am_pm}", end_str_part
            start_dt = local_tz.localize(pd.to_datetime(f"{class_info['Date'].strftime('%Y-%m-%d')} {full_start_str}"))
            end_dt = local_tz.localize(pd.to_datetime(f"{class_info['Date'].strftime('%Y-%m-%d')} {full_end_str}"))
            e.name, e.begin, e.end = (
                f"{class_info['Subject']}",
                start_dt.astimezone(pytz.utc),
                end_dt.astimezone(pytz.utc),
            )
            e.location, e.description = class_info['Venue'], f"Faculty: {class_info['Faculty']}"
            e.uid = (
                hashlib.md5(f"{start_dt.isoformat()}-{e.name}".encode("utf-8")).hexdigest() + "@timetable.app"
            )
            c.events.add(e)
        except Exception:
            continue
    return c.serialize()

# 4. STREAMLIT WEB APP INTERFACE
st.set_page_config(page_title="MBA Timetable Assistant", layout="centered", initial_sidebar_state="collapsed")
st.markdown("<meta name='color-scheme' content='dark'>", unsafe_allow_html=True)

# --- CSS (kept same as yours) ---
# You can keep your full CSS block exactly here

# --- APP HEADER ---
st.markdown('<p class="main-header">MBA Timetable Assistant</p>', unsafe_allow_html=True)
st.markdown('<div class="header-sub">Your Trimester V schedule, at your fingertips.</div>', unsafe_allow_html=True)

# --- LOAD DATA ---
master_schedule_df = load_and_clean_schedule(SCHEDULE_FILE_NAME)
student_data_map = get_all_student_data()

# --- INITIALIZE SESSION STATE ---
if 'submitted' not in st.session_state:
    st.session_state.submitted = False
if 'roll_number' not in st.session_state:
    st.session_state.roll_number = ""
if 'persisted_roll_number' not in st.session_state:
    st.session_state.persisted_roll_number = None

# ✅ --- FIXED LOCALSTORAGE LOGIN (no TypeError anymore) ---
if st.session_state.persisted_roll_number is None and not st.session_state.submitted:
    roll_from_local = st_javascript("localStorage.getItem('roll_number')")
    if roll_from_local:
        st.session_state.persisted_roll_number = roll_from_local
        st.session_state.roll_number = roll_from_local
        st.session_state.submitted = True
        st.rerun()

# --- MAIN APP LOGIC ---
if not master_schedule_df.empty and student_data_map:
    # --- AUTO LOGIN HANDLING ---
    if not st.session_state.submitted:
        st.markdown(
            """
            <div class="welcome-box">
                Welcome! This application helps you generate your personalized class schedule and export it as a <strong>.ics calendar file</strong>.
                Simply enter your roll number below to get started.
            </div>
            """,
            unsafe_allow_html=True,
        )
        with st.form("roll_number_form"):
            default_roll = st.session_state.persisted_roll_number or ""
            roll_number_input = st.text_input(
                "Enter your Roll Number:", value=default_roll, placeholder="e.g., 24MBA463"
            ).strip().upper()
            submitted_button = st.form_submit_button("Generate Timetable")

            if submitted_button:
                st.session_state.roll_number = roll_number_input
                st.session_state.submitted = True
                st.session_state.persisted_roll_number = roll_number_input
                st_javascript(f"localStorage.setItem('roll_number', '{roll_number_input}')")
                st.rerun()

    # --- PROCESS AND DISPLAY SCHEDULE IF SUBMITTED ---
    if st.session_state.submitted:
        roll_to_process = st.session_state.roll_number
        if not roll_to_process:
            st.session_state.submitted = False
            st.session_state.persisted_roll_number = None
            st.rerun()
        elif roll_to_process in student_data_map:
            student_info = student_data_map[roll_to_process]
            student_name, student_sections = student_info['name'], student_info['sections']

            col1, col2 = st.columns([3, 1])
            with col1:
                st.success(f"Displaying schedule for {student_name}")
            with col2:
                if st.button("Change Roll Number"):
                    st.session_state.submitted = False
                    st.session_state.roll_number = ""
                    st.session_state.persisted_roll_number = None
                    st_javascript("localStorage.removeItem('roll_number')")
                    st.rerun()

            with st.spinner(f'Compiling classes for {student_name}...'):
                NORMALIZED_COURSE_DETAILS_MAP = {
                    normalize_string(section): details for section, details in COURSE_DETAILS_MAP.items()
                }
                normalized_student_section_map = {normalize_string(sec): sec for sec in student_sections}
                time_slots = {
                    2: "8-9AM",
                    3: "9:10-10:10AM",
                    4: "10:20-11:20AM",
                    5: "11:30-12:30PM",
                    6: "12:30-1:30PM",
                    7: "1:30-2:30PM",
                    8: "2:40-3:40PM",
                    9: "3:50-4:50PM",
                    10: "5-6PM",
                    11: "6:10-7:10PM",
                    12: "7:20-8:20PM",
                    13: "8:30-9:30PM",
                }

                found_classes = []
                for index, row in master_schedule_df.iterrows():
                    class_date = row[0]
                    for col_idx in range(2, 14):
                        subject = str(row[col_idx]).strip()
                        if subject and subject != "nan":
                            normalized_subject = normalize_string(subject)
                            if normalized_subject in normalized_student_section_map:
                                subject_name = normalized_student_section_map[normalized_subject]
                                details = NORMALIZED_COURSE_DETAILS_MAP.get(normalized_subject, {})
                                found_classes.append({
                                    "Date": class_date,
                                    "Time": time_slots.get(col_idx, ""),
                                    "Subject": subject_name,
                                    "Faculty": details.get("Faculty", "TBD"),
                                    "Venue": details.get("Venue", "TBD")
                                })

                # Add any additional classes
                found_classes.extend(ADDITIONAL_CLASSES)

                # Display timetable
                for fc in found_classes:
                    st.write(f"📅 {fc['Date']} | {fc['Time']} | {fc['Subject']} | {fc['Venue']} | {fc['Faculty']}")

                # Allow user to export
                ics_data = generate_ics_content(found_classes)
                st.download_button(
                    label="📥 Download .ics Calendar",
                    data=ics_data,
                    file_name=f"{roll_to_process}_timetable.ics",
                    mime="text/calendar",
                )

else:
    st.error("Unable to load timetable data. Please ensure the Excel files are present.")