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
from streamlit_extras.st_keyup import st_keyup # For live search
import gc 
import streamlit.runtime.caching as st_cache
import time 

# --- NEW: AUTO REFRESH EVERY 10 MINUTES (HARD REBOOT) ---
AUTO_REFRESH_INTERVAL = 10 * 60  # 10 minutes in seconds

# Store the start time in session_state
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

elapsed = time.time() - st.session_state.start_time

if elapsed > AUTO_REFRESH_INTERVAL:
    with st.spinner("🔄 Refreshing app to keep it fast and stable..."):
        st_cache.clear_cache()
        gc.collect()
        st.session_state.clear()  # Clears all stored state (logs user out)
        time.sleep(2)  # short pause for smooth refresh
        st.experimental_rerun()
# --- END NEW BLOCK ---


# --- Cache Clearing Logic ---
if "run_counter" not in st.session_state:
    st.session_state.run_counter = 0
st.session_state.run_counter += 1

if st.session_state.run_counter % 100 == 0:
    st_cache.clear_cache()
    gc.collect()

# 2. CONFIGURATION
SCHEDULE_FILE_NAME = 'schedule.xlsx'
# --- List of all schedule files, from oldest to newest ---
SCHEDULE_FILES = ['schedule1.xlsx', 'schedule2.xlsx', 'schedule3.xlsx', 'schedule.xlsx'] 
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
        'DADM': {'Venue': 'E2'},
        'LSSA': {'Venue': 'E2'},
        'IMCA': {'Venue': 'T6'}, 
    },
    date(2025, 11, 16): { 
        'IMCB': {'Venue': 'T7'}, 
    },
    date(2025, 11, 17): {
        'DVVSC': {'Venue': 'POSTPONED', 'Faculty': 'Session Postponed'},
    },
    date(2025, 11, 18): {
        'DVVSD': {'Venue': 'CANCELLED', 'Faculty': 'Session Cancelled'},
    },
    date(2025, 11, 19): {
        'DVVSD': {'Venue': 'CANCELLED', 'Faculty': 'Session Cancelled'},
    },
    date(2025, 11, 20): {
        'DVVSC': {'Venue': 'POSTPONED', 'Faculty': 'Session Postponed'},
    },
    date(2025, 11, 21): {
        'DVVSC': {'Venue': 'CANCELLED', 'Faculty': 'Session Cancelled'},
    },
    date(2025, 11, 24): {
        'DVVSC': {'Venue': 'CANCELLED', 'Faculty': 'Session Cancelled'},
    },
    date(2025, 11, 28): {
        'VALUA': {'Venue': 'CANCELLED', 'Faculty': 'Session Cancelled'},
    },
    date(2025, 12, 5): {
        'VALUB': {'Venue': 'CANCELLED', 'Faculty': 'Session Cancelled'},
    },
    date(2025, 12, 12): {
        'VALUA': {'Venue': 'CANCELLED', 'Faculty': 'Session Cancelled'},
        'VALUB': {'Venue': 'CANCELLED', 'Faculty': 'Session Cancelled'},
    },
    date(2025, 12, 15): {
        'DRMC': {'Venue': 'PREPONED', 'Faculty': 'Session Preponed'}, 
    },
    date(2025, 12, 19): {
        'VALUA': {'Venue': 'CANCELLED', 'Faculty': 'Session Cancelled'},
        'VALUB': {'Venue': 'CANCELLED', 'Faculty': 'Session Cancelled'},
    }
}
ADDITIONAL_CLASSES = [
    {'Date': date(2025, 11, 8), 'Time': '10:20-11:20AM', 'Subject': 'SCM(A)', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 11, 8), 'Time': '10:20-11:20AM', 'Subject': 'SCM(B)', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 11, 8), 'Time': '10:20-11:20AM', 'Subject': "SCM('C)", 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2WELCOME-MESSAGE_ROLL_NO): date(2025, 11, 13), 'Time': '6:10-7:10PM', 'Subject': 'INB(A)', 'Faculty': 'M C Gupta', 'Venue': 'T6 (Rescheduled)'},
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

    # --- NEW: DV&VS(C) Rescheduled ---
    {'Date': date(2025, 11, 28), 'Time': '3:50-4:50PM', 'Subject': "DV&VS('C)", 'Faculty': 'Anand Kumar', 'Venue': 'E2 (Rescheduled)'},
    {'Date': date(2025, 11, 28), 'Time': '5-6PM', 'Subject': "DV&VS('C)", 'Faculty': 'Anand Kumar', 'Venue': 'E2 (Rescheduled)'},
    {'Date': date(2025, 12, 5), 'Time': '3:50-4:50PM', 'Subject': "DV&VS('C)", 'Faculty': 'Anand Kumar', 'Venue': 'E2 (Rescheduled)'},
    {'Date': date(2025, 12, 5), 'Time': '5-6PM', 'Subject': "DV&VS('C)", 'Faculty': 'Anand Kumar', 'Venue': 'E2 (Rescheduled)'},
]


# 3. FUNCTIONS
def normalize_string(text):
    if isinstance(text, str):
        return text.replace(" ", "").replace("(", "").replace(")", "").replace("'", "").upper()
    return ""

# --- MODIFIED: Use @st.cache_resource ---
@st.cache_resource
def load_and_clean_schedule(file_path, is_stats_file=False):
    try:
        df = pd.read_excel(file_path, sheet_name=1, header=None, skiprows=3)
        schedule_df = df.iloc[:, 0:14].copy()
        schedule_df[0] = pd.to_datetime(schedule_df[0], errors='coerce').dt.date
        schedule_df.dropna(subset=[0], inplace=True)
        return schedule_df
    except FileNotFoundError:
        if not is_stats_file: # Only show error for the main schedule file
            st.error(f"FATAL ERROR: The main schedule file '{file_path}' was not found. Please make sure it's in the same folder as the app.")
        return pd.DataFrame()
    except Exception as e:
        if not is_stats_file:
            st.error(f"FATAL ERROR: Could not load the main schedule file. Details: {e}")
        return pd.DataFrame()

# --- MODIFIED: Use @st.cache_resource ---
@st.cache_resource
def load_all_schedules(file_list):
    all_dfs = []
    for file_path in file_list:
        # Use the existing function, but suppress errors for old files
        df = load_and_clean_schedule(file_path, is_stats_file=True) 
        if not df.empty:
            all_dfs.append(df)
            
    if not all_dfs:
        return pd.DataFrame()
        
    combined_df = pd.concat(all_dfs)
    # --- THIS IS THE FIX: We DO NOT drop duplicates. We sum from all files.
    combined_df = combined_df.sort_values(by=[0]) # Sort by date
    return combined_df

# --- (FIXED) Function to calculate and display stats ---
def calculate_and_display_stats():
    # --- Separator REMOVED ---
    with st.expander("Sessions Taken till Now"):
        with st.spinner("Calculating session statistics..."):
            # --- MODIFIED: Load only the main schedule file ---
            all_schedules_df = load_and_clean_schedule(SCHEDULE_FILE_NAME) 
            
            if all_schedules_df.empty:
                st.warning("Could not load schedule file to calculate stats.")
                return

            local_tz = pytz.timezone(TIMEZONE)
            now_dt = datetime.now(local_tz)
            today_date = now_dt.date()
            
            class_counts = defaultdict(int)
            
            # Time slots mapping columns to end times for comparison
            time_slot_end_times = {
                2: "9:00AM", 3: "10:10AM", 4: "11:20AM", 5: "12:30PM",
                6: "1:30PM", 7: "2:30PM", 8: "3:40PM", 9: "4:50PM",
                10: "6:00PM", 11: "7:10PM", 12: "8:20PM", 13: "9:30PM"
            }
            
            # Create a normalized map of all known courses
            normalized_course_map = {normalize_string(k): k for k in COURSE_DETAILS_MAP.keys()}
            
            # --- THIS IS THE START OF THE FIXED LOGIC ---
            # We iterate over the full concatenated dataframe
            for _, row in all_schedules_df.iterrows():
                class_date = row[0]
                
                if class_date > today_date:
                    continue # Skip all future dates

                for col_idx, end_time_str in time_slot_end_times.items():
                    # Check if the class has already happened
                    is_in_past = False # Reset for each time slot
                    if class_date < today_date:
                        # This class was on a previous day
                        is_in_past = True
                    elif class_date == today_date:
                        # This class is today. We must check the time.
                        try:
                            class_end_dt = local_tz.localize(pd.to_datetime(f"{class_date.strftime('%Y-%m-%d')} {end_time_str}"))
                            is_in_past = class_end_dt < now_dt
                        except Exception:
                            is_in_past = False # Error parsing, skip
                    
                    if is_in_past:
                        cell_value = str(row[col_idx])
                        if cell_value and cell_value != 'nan':
                            normalized_cell = normalize_string(cell_value)
                            
                            # Check every known class against the cell
                            for norm_name, orig_name in normalized_course_map.items():
                                if norm_name in normalized_cell:
                                    # --- CHECK FOR OVERRIDES ---
                                    is_overridden = False
                                    if class_date in DAY_SPECIFIC_OVERRIDES and norm_name in DAY_SPECIFIC_OVERRIDES[class_date]:
                                        override_details = DAY_SPECIFIC_OVERRIDES[class_date][norm_name]
                                        venue_text = override_details.get('Venue', '').upper()
                                        faculty_text = override_details.get('Faculty', '').upper()
                                        
                                        if "POSTPONED" in venue_text or "POSTPONED" in faculty_text or \
                                           "CANCELLED" in venue_text or "CANCELLED" in faculty_text or \
                                           "PREPONED" in venue_text or "PREPONED" in faculty_text:
                                            is_overridden = True # Don't count this class
                                            
                                    if not is_overridden:
                                        class_counts[orig_name] += 1

            # 2. Add classes from ADDITIONAL_CLASSES
            for added_class in ADDITIONAL_CLASSES:
                class_date = added_class['Date']
                if class_date > today_date:
                    continue # Skip future classes
                
                is_in_past = False
                if class_date < today_date:
                    is_in_past = True
                elif class_date == today_date:
                    try:
                        # Need to parse the time from the 'Time' string
                        _, end_time_str = added_class['Time'].split('-')
                        class_end_dt = local_tz.localize(pd.to_datetime(f"{class_date.strftime('%Y-%m-%d')} {end_time_str}"))
                        is_in_past = class_end_dt < now_dt
                    except Exception:
                        is_in_past = False
                
                if is_in_past:
                    # Check if this class is a valid subject
                    norm_name = normalize_string(added_class['Subject'])
                    if norm_name in normalized_course_map:
                        orig_name = normalized_course_map[norm_name]
                        class_counts[orig_name] += 1
            
            if not class_counts:
                st.info("No past classes were found to calculate statistics.")
                return

            st.markdown("This shows the total number of sessions held *to date*, accounting for all schedule changes.")
            
            # --- NEW: Grouping Logic ---
            grouped_counts = defaultdict(dict)
            for full_name, count in class_counts.items():
                # Find the course and section
                match = re.match(r"(.*?)\((.*)\)", full_name)
                if match:
                    course_name = match.group(1)
                    section_name = match.group(2).replace("'", "") # Clean up 'C -> C
                else:
                    course_name = full_name
                    section_name = "Main" # For subjects like 'BS'
                
                grouped_counts[course_name][section_name] = count
            
            # --- NEW: Display Logic ---
            sorted_courses = sorted(grouped_counts.keys())
            midpoint = len(sorted_courses) // 2 + (len(sorted_courses) % 2)
            col1, col2 = st.columns(2)

            with col1:
                for course_name in sorted_courses[:midpoint]:
                    st.markdown(f"**{course_name}**")
                    sections = grouped_counts[course_name]
                    for section_name in sorted(sections.keys()):
                        count = sections[section_name]
                        if section_name == "Main":
                            st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;Total Sessions: {count}")
                        else:
                            st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;Section {section_name}: {count} sessions")
                    st.markdown("") # Add a little space

            with col2:
                for course_name in sorted_courses[midpoint:]:
                    st.markdown(f"**{course_name}**")
                    sections = grouped_counts[course_name]
                    for section_name in sorted(sections.keys()):
                        count = sections[section_name]
                        if section_name == "Main":
                            st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;Total Sessions: {count}")
                        else:
                            st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;Section {section_name}: {count} sessions")
                    st.markdown("") # Add a little space

# --- MODIFIED: Kept @st.cache_data ---
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
                    header_row_index = i; break
            if header_row_index == -1: continue
            subject_row, roll_no_columns = df.iloc[0], df.iloc[header_row_index][df.iloc[header_row_index].astype(str).str.upper().str.contains('ROLL')].index
            for col_idx in roll_no_columns:
                section_name = subject_row[col_idx]
                name_column_index = col_idx + 1
                for _, row in df.iloc[header_row_index + 1:].iterrows():
                    roll_no = str(row[col_idx]).upper()
                    if 'NAN' in roll_no: continue
                    student_name = row[name_column_index]
                    if roll_no not in student_data_map:
                        student_data_map[roll_no] = {'name': student_name, 'sections': set()}
                    student_data_map[roll_no]['sections'].add(section_name)
        except Exception:
            continue
    return student_data_map
    
def get_class_end_datetime(class_info, local_tz):
    """Parses class info to get its end datetime."""
    try:
        time_str = class_info['Time']
        date_obj = class_info['Date']
        
        start_str_part, end_str_part = time_str.split('-')
        end_am_pm = end_str_part[-2:]
        
        start_am_pm = end_am_pm
        start_hour = int(re.search(r'^\d+', start_str_part).group(0))
        if end_am_pm == "PM" and start_hour < 12 and (start_hour > int(re.search(r'^\d+', end_str_part).group(0)) or start_hour == 11):
            start_am_pm = "AM"
        
        full_end_str = end_str_part
        end_dt = local_tz.localize(pd.to_datetime(f"{date_obj.strftime('%Y-%m-%d')} {full_end_str}"))
        return end_dt
    except Exception:
        return None

def generate_ics_content(found_classes):
    c = Calendar(creator="-//Student Timetable Script//EN")
    local_tz = pytz.timezone(TIMEZONE)
    for class_info in found_classes:
        # --- MODIFIED: Skip all special status classes ---
        venue_text = class_info.get('Venue', '').upper()
        faculty_text = class_info.get('Faculty', '').upper()
        if ("POSTPONED" in venue_text or "POSTPONED" in faculty_text or
            "CANCELLED" in venue_text or "CANCELLED" in faculty_text or
            "PREPONED" in venue_text or "PREPONED" in faculty_text):
            continue
            
        end_dt = get_class_end_datetime(class_info, local_tz)
        if not end_dt: 
            continue
            
        try:
            e = Event()
            time_str = class_info['Time']
            start_str_part, _ = time_str.split('-')
            _, end_str_part = time_str.split('-')
            end_am_pm = end_str_part[-2:]
            
            start_am_pm = end_am_pm
            start_hour = int(re.search(r'^\d+', start_str_part).group(0))
            if end_am_pm == "PM" and start_hour < 12 and (start_hour > int(re.search(r'^\d+', end_str_part).group(0)) or start_hour == 11):
                start_am_pm = "AM"
                
            full_start_str = f"{start_str_part}{start_am_pm}"
            start_dt = local_tz.localize(pd.to_datetime(f"{class_info['Date'].strftime('%Y-%m-%d')} {full_start_str}"))
                
            e.name, e.begin, e.end = f"{class_info['Subject']}", start_dt.astimezone(pytz.utc), end_dt.astimezone(pytz.utc)
            e.location, e.description = class_info['Venue'], f"Faculty: {class_info['Faculty']}"
            e.uid = hashlib.md5(f"{start_dt.isoformat()}-{e.name}".encode('utf-8')).hexdigest() + "@timetable.app"
            c.events.add(e)
        except Exception:
            continue
    return c.serialize()
# 4. STREAMLIT WEB APP INTERFACE
st.set_page_config(
    page_title="MBA Timetable Assistant", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)
st.markdown("""
    <meta name="color-scheme" content="dark">
    <meta name="theme-color" content="#0F172A">
    
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
""", unsafe_allow_html=True)
# --- CSS STYLING ---
local_css_string = """
<style>
    /* ... (your existing CSS from root to .results-container) ... */
    * { color-scheme: dark !important; }
    [data-testid="stAppViewContainer"], [data-testid="stHeader"], section[data-testid="stSidebar"] {
        background-color: var(--bg) !important; color: #ffffff !important;
    }
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    :root{
        --bg:#0F172A; --card:#1E293B; --muted:#94A3B8; --accent-start:#60A5FA; --accent-end:#818CF8;
        --glass-border: rgba(255,255,255,0.08); --today-glow: #38BDF8; --today-glow-shadow: rgba(56, 189, 248, 0.4);
        --venue-change-color: #F87171;
    }
    .stApp {
        background: radial-gradient(1200px 600px at 10% 10%, rgba(96,165,250,0.08), transparent 10%),
                    radial-gradient(1000px 500px at 90% 90%, rgba(129,140,248,0.06), transparent 10%), var(--bg);
        color: #ffffff; font-family: 'Inter', ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
    }
    .main-header {
        font-size: 2.4rem; font-weight: 800; text-align: center; margin-bottom: 0.5rem;
    }
    .header-sub { text-align:center; color:var(--muted); margin-top:0rem; margin-bottom:2rem; font-size:1.0rem; }
    .welcome-box {
        background: var(--card); border: 1px solid var(--glass-border); padding: 1rem 1.25rem;
        border-radius: 14px; margin-bottom: 1.5rem; color: var(--muted); font-size: 0.95rem;
    }
    .welcome-box strong { color: #ffffff; font-weight: 600; }
    
    /* --- NEW WELCOME MESSAGE --- */
    .welcome-message {
        margin-top: -2rem; /* Pulls it up */
        margin-bottom: 1rem; /* Adds space before the next element */
        font-size: 1.1rem; /* Smaller than h3, larger than caption */
        color: var(--muted); /* Use the muted color */
    }
    .welcome-message strong {
        color: #ffffff; /* Make the roll number white */
    }

    .day-card {
        background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
        border-radius: 14px; padding: 1.25rem; margin-bottom: 1.25rem; box-shadow: 0 8px 30px rgba(0,0,0,0.4);
        border: 1px solid var(--glass-border); transition: transform 0.18s ease, box-shadow 0.18s ease;
        scroll-margin-top: 85px; position: relative;
    }
    .day-card:hover { transform: translateY(-6px); box-shadow: 0 18px 40px rgba(0,0,0,0.6); }
    .day-card.today {
        border: 3px solid var(--today-glow);
        box-shadow: 0 0 35px var(--today-glow-shadow), 0 0 60px rgba(56, 189, 248, 0.2), 0 8px 30px rgba(0,0,0,0.4);
        animation: pulse-glow 2s ease-in-out infinite;
    }
    .today-badge {
        position: absolute; top: -12px; right: 20px; background: var(--today-glow); color: var(--bg);
        font-size: 0.75rem; font-weight: 800; padding: 0.35rem 0.75rem; border-radius: 6px;
        letter-spacing: 0.5px; text-transform: uppercase; box-shadow: 0 4px 15px var(--today-glow-shadow); z-index: 10;
    }
    @keyframes pulse-glow {
        0%, 100% { box-shadow: 0 0 35px var(--today-glow-shadow), 0 0 60px rgba(56, 189, 248, 0.2), 0 8px 30px rgba(0,0,0,0.4); }
        50% { box-shadow: 0 0 45px rgba(56, 189, 248, 0.6), 0 0 80px rgba(56, 189, 248, 0.3), 0 8px 30px rgba(0,0,0,0.4); }
    }
    .day-header { font-size: 1.15rem; font-weight: 700; color: #E2E8F0; margin-bottom: 0.5rem; }
    .class-entry {
        display:flex; flex-direction:row; align-items:center; justify-content:space-between;
        padding-top:0.65rem; padding-bottom:0.65rem; border-bottom:1px solid rgba(255,255,255,0.04);
    }
    .day-card .class-entry:last-child { border-bottom: none; padding-bottom: 0; }
    .left { display:flex; flex-direction:column; gap:0.2rem; }
    .subject-name { font-size:1.05rem; font-weight:700; margin:0; color: #FFFFFF; }
    .class-details { font-size:0.94rem; color:var(--muted); }
    .meta { text-align:right; min-width:170px; }
    .meta .time { display:block; font-weight:600; color:#fff; font-size:0.97rem; }
    .meta .venue, .meta .faculty { display:block; font-size:0.85rem; color:var(--muted); }
    .venue-changed { color: var(--venue-change-color) !important; font-weight: 600; }
    
    /* --- NEW: Strikethrough Class --- */
    .strikethrough {
        text-decoration: line-through;
        opacity: 0.6;
    }
    
    .stDownloadButton>button, div[data-testid="stForm"] button[kind="primary"], .stButton>button {
        background: linear-gradient(90deg, var(--accent-start), var(--accent-end)); color: var(--bg);
        font-weight:700; padding: 0.5rem 0.9rem; border-radius:10px; border:none;
        box-shadow: 0 8px 20px rgba(96,165,250,0.1); width: 100%;
        transition: transform 0.18s ease, box-shadow 0.18s ease;
    }
    .stDownloadButton>button:hover, div[data-testid="stForm"] button[kind="primary"]:hover, .stButton>button:hover {
        transform: translateY(-3px); box-shadow: 0 14px 30px rgba(96,165,250,0.15);
    }
    
    /* --- MODIFIED: Smaller Change Button --- */
    .stButton>button {
        width: auto; 
        padding: 0.25rem 0.6rem; /* Smaller padding */
        font-size: 0.8rem; /* Smaller font */
        background: var(--card);
        color: var(--muted); 
        border: 1px solid var(--glass-border);
    }
    .stButton>button:hover { color: var(--accent-start); border-color: var(--accent-start); }
    
    a { color: var(--accent-start); font-weight:600; }
    .css-1d391kg, .css-1v3fvcr, .css-18ni7ap { color: #ffffff; }
    .stTextInput>div>div>input, .stTextInput>div>div>textarea {
        background: rgba(255,255,255,0.02) !important; color: #E2E8F0 !important;
        border: 1px solid rgba(255,255,255,0.06) !important; padding: 0.6rem !important; border-radius: 8px !important;
    }
    .results-container {
        background: var(--card); border: 1px solid var(--glass-border); padding: 1.25rem;
        border-radius: 14px; margin-bottom: 1.5rem;
    }
    .results-container h3 { color: #E2E8F0; margin-top: 0; margin-bottom: 1rem; font-size: 1.3rem; }
    .results-container h3:not(:first-child) { margin-top: 1.5rem; }
    
    /* --- MODIFIED: Mobile View Adjustments --- */
    @media (max-width: 600px) {
        /* Reduce padding on cards */
        .day-card {
            padding: 0.8rem; /* Further reduced padding */
            margin-bottom: 1rem;
        }
        .results-container {
            padding: 0.8rem;
        }
        /* Reduce font sizes */
        .main-header { font-size: 1.6rem; } /* Further reduced */
        .header-sub { font-size: 0.8rem; margin-bottom: 1.5rem; } /* Further reduced */
        .day-header { font-size: 0.9rem; } /* Further reduced */
        .subject-name { font-size: 0.9rem; } /* Further reduced */
        .meta .time { font-size: 0.85rem; } /* Further reduced */
        .meta .venue, .meta .faculty { font-size: 0.75rem; } /* Further reduced */
        /* Reduce padding on class entries */
        .class-entry {
            padding-top: 0.5rem;
            padding-bottom: 0.5rem;
        }
        .meta { 
            min-width: 120px; 
            font-size: 0.85rem; /* Further reduced */
        }
        /* Make buttons slightly smaller */
        .stDownloadButton>button, div[data-testid="stForm"] button[kind="primary"], .stButton>button {
            padding: 0.4rem 0.8rem;
            font-size: 0.9rem;
        }
        /* Make change button even smaller on mobile */
        .stButton>button {
            padding: 0.25rem 0.6rem;
            font-size: 0.8rem;
        }
    }
</style>
"""
st.markdown(local_css_string, unsafe_allow_html=True)

# --- INITIALIZE SESSION STATE ---
if 'submitted' not in st.session_state:
    st.session_state.submitted = False
if 'roll_number' not in st.session_state:
    st.session_state.roll_number = ""
if 'search_clear_counter' not in st.session_state:
    st.session_state.search_clear_counter = 0
if 'just_submitted' not in st.session_state: # <-- For one-time scroll
    st.session_state.just_submitted = False


# --- APP HEADER ---
if not st.session_state.submitted:
    # Only show headers on the login page
    st.markdown('<p class="main-header">MBA Timetable Assistant</p>', unsafe_allow_html=True)
    st.markdown('<div class="header-sub">Course Statistics & Schedule Tool</div>', unsafe_allow_html=True)
else:
    # On the main app page, show nothing here.
    # The "welcome-message" div will be the first thing shown.
    pass


# --- MAIN APP LOGIC ---
# Load student data (needed for both login and stats)
student_data_map = get_all_student_data()

if not student_data_map:
    # Fatal error, can't even show stats
    st.error("FATAL ERROR: Could not load any student data. Please check your Excel files.")
else:
    # --- DISPLAY LOGIN PAGE ---
    if not st.session_state.submitted:
        st.markdown(
            """
            <div class="welcome-box">
                Welcome! Enter your roll number to get started!</strong>.
            </div>
            """,
            unsafe_allow_html=True
        )
        with st.form("roll_number_form"):
            roll_number_input = st.text_input("Enter your Roll Number:", placeholder="e.g., 24MBA463").strip().upper()
            submitted_button = st.form_submit_button("Generate Timetable")
            
            if submitted_button:
                st.session_state.roll_number = roll_number_input
                st.session_state.submitted = True
                st.session_state.just_submitted = True # <-- Set scroll flag
                st.rerun()
        
        # --- DISPLAY STATS ON LOGIN PAGE ---
        calculate_and_display_stats()

    # --- DISPLAY TIMETABLE PAGE ---
    else:
        roll_to_process = st.session_state.roll_number
        
        # Handle empty submission
        if not roll_to_process:
            st.session_state.submitted = False
            st.rerun()
        # Handle invalid roll number
        elif roll_to_process not in student_data_map:
            st.error(f"Roll Number '{roll_to_process}' not found. Please check the number and try again.")
            st.session_state.submitted = False
            st.session_state.roll_number = ""
            st.rerun()
        # Handle valid roll number
        else:
            student_info = student_data_map[roll_to_process]
            student_name, student_sections = student_info['name'], student_info['sections']
            
            # Load the main schedule file *only after* login
            master_schedule_df = load_and_clean_schedule(SCHEDULE_FILE_NAME)
            
            if master_schedule_df.empty:
                # Error is already handled by load_and_clean_schedule
                pass
            else:
                # Display header with "Change" button
                col1, col2 = st.columns([3, 1])
                with col1:
                    # --- MODIFIED: Welcome message uses roll number ---
                    st.markdown(f"""
                    <div class="welcome-message">
                        Displaying schedule for: <strong>{roll_to_process}</strong>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    if st.button("Change Roll Number"):
                        st.session_state.submitted = False
                        st.session_state.roll_number = ""
                        st.session_state.search_clear_counter = 0 # Reset search
                        st.session_state.just_submitted = False # Reset scroll flag
                        st.rerun()
                
                with st.spinner(f'Compiling classes for {student_name}...'):
                    NORMALIZED_COURSE_DETAILS_MAP = {normalize_string(section): details for section, details in COURSE_DETAILS_MAP.items()}
                    normalized_student_section_map = {normalize_string(sec): sec for sec in student_sections}
                    time_slots = {2: "8-9AM", 3: "9:10-10:10AM", 4: "10:20-11:20AM", 5: "11:30-12:30PM",
                                  6: "12:30-1:30PM", 7: "1:30-2:30PM", 8: "2:40-3:40PM", 9: "3:50-4:50PM",
                                  10: "5-6PM", 11: "6:10-7:10PM", 12: "7:20-8:20PM", 13: "8:30-9:30PM"}
                    found_classes = []
                    for index, row in master_schedule_df.iterrows():
                        date, day = row[0], row[1]
                        for col_index, time in time_slots.items():
                            cell_value = str(row[col_index])
                            if cell_value and cell_value != 'nan':
                                normalized_cell = normalize_string(cell_value)
                                for norm_sec, orig_sec in normalized_student_section_map.items():
                                    if norm_sec in normalized_cell:
                                        details = NORMALIZED_COURSE_DETAILS_MAP.get(norm_sec, {'Faculty': 'N/A', 'Venue': '-'}).copy()
                                        is_venue_override = False
                                        
                                        if date in DAY_SPECIFIC_OVERRIDES:
                                            if norm_sec in DAY_SPECIFIC_OVERRIDES[date]:
                                                if 'Venue' in DAY_SPECIFIC_OVERRIDES[date][norm_sec]:
                                                    is_venue_override = True
                                                details.update(DAY_SPECIFIC_OVERRIDES[date][norm_sec])
                                                
                                        found_classes.append({
                                            "Date": date, "Day": day, "Time": time, "Subject": orig_sec,
                                            "Faculty": details.get('Faculty', 'N/A'),
                                            "Venue": details.get('Venue', '-'),
                                            "is_venue_override": is_venue_override
                                        })
                    
                    for added_class in ADDITIONAL_CLASSES:
                        norm_added_subject = normalize_string(added_class['Subject'])
                        if norm_added_subject in normalized_student_section_map:
                            day_of_week = added_class['Date'].strftime('%A')
                            found_classes.append({
                                "Date": added_class['Date'], "Day": day_of_week, "Time": added_class['Time'],
                                "Subject": added_class['Subject'], "Faculty": added_class.get('Faculty', 'N/A'),
                                "Venue": added_class.get('Venue', '-'), "is_venue_override": False
                            })

                    found_classes = [dict(t) for t in {tuple(d.items()) for d in found_classes}]
                    
                # --- ORGANIZED RESULTS SECTION ---
                if found_classes:
                    ics_content = generate_ics_content(found_classes)
                    sanitized_name = re.sub(r'[^a-zA-Z0-9_]', '', str(student_name).replace(" ", "_")).upper()
                    
                    # --- NEW: Combined Download & Import Expander ---
                    with st.expander("Download & Import to Calendar"):
                        st.download_button(
                            label="Download .ics Calendar File",
                            data=ics_content,
                            file_name=f"{sanitized_name}_Timetable.ics",
                            mime='text/calendar'
                        )
                        st.markdown(f"""
                        **How to Import to Google Calendar:**
                        1. Click the 'Download .ics' button above.
                        2. Go to [**Google Calendar Import Page**]({GOOGLE_CALENDAR_IMPORT_LINK}).
                        3. Under 'Import from computer', click 'Select file...'.
                        4. Choose the `.ics` file you just downloaded and click 'Import'.
                        """)
                    
                    schedule_by_date = defaultdict(list)
                    for class_info in found_classes:
                        schedule_by_date[class_info['Date']].append(class_info)
                    
                    sorted_dates = sorted(schedule_by_date.keys())
                    time_sorter = {time: i for i, time in enumerate(time_slots.values())}
                    for date in sorted_dates:
                        schedule_by_date[date].sort(key=lambda x: time_sorter.get(x['Time'], 99))
                    
                    all_dates = []
                    if sorted_dates:
                        first_date = sorted_dates[0]
                        last_date = sorted_dates[-1]
                        current_date = first_date
                        while current_date <= last_date:
                            all_dates.append(current_date)
                            current_date = date.fromordinal(current_date.toordinal() + 1)
                    
                    local_tz = pytz.timezone(TIMEZONE)
                    today_dt = datetime.now(local_tz)
                    today = today_dt.date()
                    today_anchor_id = None
                    
                    past_dates = sorted([d for d in all_dates if d < today], reverse=True)
                    upcoming_dates = sorted([d for d in all_dates if d >= today])

                    # --- 1. RENDER PAST CLASSES (IN AN EXPANDER) ---
                    with st.expander("Show Previous Classes"):
                        # --- SEARCH BAR MOVED HERE ---
                        search_query = st_keyup(
                            label=None, # <-- Label removed
                            placeholder="Search past classes...",
                            debounce=300, 
                            key=f"search_bar_past_{st.session_state.search_clear_counter}" 
                        )
                        search_query = search_query.lower() if search_query else ""
                        
                        if search_query: 
                            if st.button("Clear Search"):
                                st.session_state.search_clear_counter += 1
                                st.rerun()

                        if search_query:
                            st.subheader(f"Search Results for '{search_query}'")
                        
                        found_past_search = False
                        if not past_dates and not search_query:
                            st.markdown('<p style="color: var(--muted); font-style: italic;">No previous classes found.</p>', unsafe_allow_html=True)
                        
                        for date_obj in past_dates:
                            classes_today = schedule_by_date.get(date_obj, [])
                            
                            # --- Filter logic for past classes ---
                            if search_query:
                                classes_today = [
                                    c for c in classes_today if
                                    (search_query in c['Subject'].lower() or
                                     search_query in c['Faculty'].lower() or
                                     search_query in c['Venue'].lower())
                                ]
                                if classes_today:
                                    found_past_search = True
                            
                            if not classes_today:
                                continue # Skip empty days
                            
                            st.markdown(f'''
                                <div class="day-card" id="date-card-past-{date_obj.toordinal()}">
                                    <div class="day-header">
                                        {date_obj.strftime("%A, %d %B %Y")}
                                    </div>
                            ''', unsafe_allow_html=True)
                            
                            for class_info in classes_today:
                                # --- STRIKETHROUGH LOGIC ---
                                venue_text = class_info.get("Venue", "-")
                                faculty_text = class_info.get("Faculty", "-")
                                venue_text_upper = venue_text.upper()
                                faculty_text_upper = faculty_text.upper()

                                is_postponed = "POSTPONED" in venue_text_upper or "POSTPONED" in faculty_text_upper
                                is_cancelled = "CANCELLED" in venue_text_upper or "CANCELLED" in faculty_text_upper
                                is_preponed = "PREPONED" in venue_text_upper or "PREPONED" in faculty_text_upper
                                
                                status_class = ""
                                venue_display = ""
                                faculty_display = f'<span class="faculty">{faculty_text}</span>' 

                                if is_postponed:
                                    status_class = "strikethrough"
                                    venue_display = f'<span class="venue venue-changed">Postponed</span>'
                                    if "POSTPONED" not in faculty_text_upper:
                                         faculty_display = f'<span class="faculty {status_class}">{faculty_text}</span>'
                                    else:
                                         faculty_display = f'<span class="faculty venue-changed">{faculty_text.title()}</span>'
                                elif is_cancelled:
                                    status_class = "strikethrough"
                                    venue_display = f'<span class="venue venue-changed">Cancelled</span>'
                                    if "CANCELLED" not in faculty_text_upper:
                                         faculty_display = f'<span class="faculty {status_class}">{faculty_text}</span>'
                                    else:
                                         faculty_display = f'<span class="faculty venue-changed">{faculty_text.title()}</span>'
                                elif is_preponed:
                                    status_class = "strikethrough"
                                    venue_display = f'<span class="venue venue-changed">Preponed</span>'
                                    if "PREPONED" not in faculty_text_upper:
                                         faculty_display = f'<span class="faculty {status_class}">{faculty_text}</span>'
                                    else:
                                         faculty_display = f'<span class="faculty venue-changed">{faculty_text.title()}</span>'
                                elif class_info.get('is_venue_override', False):
                                    venue_display = f'<span class="venue venue-changed">Venue changed to {venue_text}</span>'
                                    faculty_display = f'<span class="faculty">{faculty_text}</span>'
                                else:
                                    venue_display = f'<span class="venue">{venue_text}</span>'
                                    faculty_display = f'<span class="faculty">{faculty_text}</span>'
                                
                                meta_html = f'''
                                    <div class="meta">
                                        <span class="time {status_class}">{class_info["Time"]}</span>
                                        {venue_display}
                                        {faculty_display}
                                    </div>
                                '''
                                
                                st.markdown(f'''
                                    <div class="class-entry">
                                        <div class="left">
                                            <div class="subject-name {status_class}">{class_info["Subject"]}</div>
                                        </div>
                                        {meta_html}
                                    </div>
                                ''', unsafe_allow_html=True)
                            st.markdown('</div>', unsafe_allow_html=True)
                        
                        if search_query and not found_past_search:
                            st.warning(f"No past classes found matching your search for '{search_query}'.")

                    
                    # --- 2. RENDER UPCOMING CLASSES ---
                    
                    # --- SEARCH ANCHOR ---
                    st.markdown('<div id="search-anchor-div"></div>', unsafe_allow_html=True)

                    # --- "Upcoming Classes" subheader REMOVED ---

                    if not upcoming_dates:
                         st.markdown('<p style="color: var(--muted); font-style: italic;">No upcoming classes found.</p>', unsafe_allow_html=True)

                    
                    # --- "Holiday" fix. Iterate over all upcoming dates first ---
                    for idx, date_obj in enumerate(upcoming_dates):
                        is_today = (date_obj == today)
                        today_class = "today" if is_today else ""
                        card_id = f"date-card-{idx}"
                        
                        if is_today: 
                            today_anchor_id = card_id
                        
                        classes_today = schedule_by_date.get(date_obj, [])
                        
                        if not classes_today:
                            # This is the "No classes scheduled" card for holidays/weekends
                            st.markdown(f'''
                                <div class="day-card {today_class}" id="{card_id}">
                                    <div class="day-header">
                                        {date_obj.strftime("%A, %d %B %Y")}
                                    </div>
                                    <div class="class-entry">
                                        <div class="left">
                                            <div class="subject-name" style="color: var(--muted); font-style: italic;">No classes scheduled</div>
                                        </div>
                                        <div class="meta"><span class="time" style="color: var(--muted);">—</span></div>
                                    </div>
                                </div>
                            ''', unsafe_allow_html=True)
                        else:
                            # Render the day card with classes
                            if is_today:
                                st.markdown(f'''
                                    <div class="day-card {today_class}" id="{card_id}">
                                        <div class="today-badge">TODAY</div>
                                        <div class="day-header">
                                            {date_obj.strftime("%A, %d %B %Y")}
                                        </div>
                                ''', unsafe_allow_html=True)
                            else:
                                st.markdown(f'''
                                    <div class="day-card {today_class}" id="{card_id}">
                                        <div class="day-header">
                                            {date_obj.strftime("%A, %d %B %Y")}
                                        </div>
                                ''', unsafe_allow_html=True)

                            for class_info in classes_today:
                                # --- STRIKETHROUGH LOGIC (COPIED FOR UPCOMING) ---
                                venue_display = ""
                                venue_text = class_info.get("Venue", "-")
                                faculty_text = class_info.get("Faculty", "-")
                                venue_text_upper = venue_text.upper()
                                faculty_text_upper = faculty_text.upper()

                                is_postponed = "POSTPONED" in venue_text_upper or "POSTPONED" in faculty_text_upper
                                is_cancelled = "CANCELLED" in venue_text_upper or "CANCELLED" in faculty_text_upper
                                is_preponed = "PREPONED" in venue_text_upper or "PREPONED" in faculty_text_upper
                                
                                status_class = ""
                                venue_display = ""
                                faculty_display = f'<span class="faculty">{faculty_text}</span>' 

                                if is_postponed:
                                    status_class = "strikethrough"
                                    venue_display = f'<span class="venue venue-changed">Postponed</span>'
                                    if "POSTPONED" not in faculty_text_upper:
                                         faculty_display = f'<span class="faculty {status_class}">{faculty_text}</span>'
                                    else:
                                         faculty_display = f'<span class="faculty venue-changed">{faculty_text.title()}</span>'
                                elif is_cancelled:
                                    status_class = "strikethrough"
                                    venue_display = f'<span class="venue venue-changed">Cancelled</span>'
                                    if "CANCELLED" not in faculty_text_upper:
                                         faculty_display = f'<span class="faculty {status_class}">{faculty_text}</span>'
                                    else:
                                         faculty_display = f'<span class="faculty venue-changed">{faculty_text.title()}</span>'
                                elif is_preponed:
                                    status_class = "strikethrough"
                                    venue_display = f'<span class="venue venue-changed">Preponed</span>'
                                    if "PREPONED" not in faculty_text_upper:
                                         faculty_display = f'<span class="faculty {status_class}">{faculty_text}</span>'
                                    else:
                                         faculty_display = f'<span class="faculty venue-changed">{faculty_text.title()}</span>'
                                elif class_info.get('is_venue_override', False):
                                    venue_display = f'<span class="venue venue-changed">Venue changed to {venue_text}</span>'
                                    faculty_display = f'<span class="faculty">{faculty_text}</span>'
                                else:
                                    venue_display = f'<span class="venue">{venue_text}</span>'
                                    faculty_display = f'<span class="faculty">{faculty_text}</span>'
                                
                                meta_html = f'''
                                    <div class="meta">
                                        <span class="time {status_class}">{class_info["Time"]}</span>
                                        {venue_display}
                                        {faculty_display}
                                    </div>
                                '''
                                
                                st.markdown(f'''
                                    <div class="class-entry">
                                        <div class="left">
                                            <div class="subject-name {status_class}">{class_info["Subject"]}</div>
                                        </div>
                                        {meta_html}
                                    </div>
                                ''', unsafe_allow_html=True)
                            
                            st.markdown('</div>', unsafe_allow_html=True)

                    # --- AUTO-SCROLL SCRIPT ---
                    if st.session_state.just_submitted:
                        components.html(f"""
                        <script>
                            let attempts = 0;
                            const scrollInterval = setInterval(() => {{
                                attempts++;
                                const searchAnchor = window.parent.document.getElementById('search-anchor-div');
                                
                                if (searchAnchor) {{
                                    clearInterval(scrollInterval);
                                    const rect = searchAnchor.getBoundingClientRect();
                                    const currentScrollY = window.parent.scrollY;
                                    const targetY = rect.top + currentScrollY - 85; 
                                    window.parent.scrollTo({{ top: targetY, behavior: 'smooth' }});
                                }}
                                if (attempts > 20) {{
                                    clearInterval(scrollInterval);
                                }}
                            }}, 250);
                        </script>
                        """, height=0)
                        st.session_state.just_submitted = False # Unset the flag
                    
                else:
                    st.warning("No classes found for your registered sections in the master schedule.")
            
# --- ADDED CAPTION AT THE VERY END ---
st.markdown("---")
st.caption("_Made by Vishesh_")
