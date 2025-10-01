# 1. IMPORTS
import pandas as pd
import os
import glob
from datetime import datetime
import re
import streamlit as st
from ics import Calendar, Event
import pytz
import hashlib

# 2. CONFIGURATION
SCHEDULE_FILE_NAME = 'schedule.xlsx'
TIMEZONE = 'Asia/Kolkata'
GOOGLE_CALENDAR_IMPORT_LINK = 'https://calendar.google.com/calendar/u/0/r/settings/export'

COURSE_DETAILS_MAP = {
    'AN(A)': {'Faculty': 'Nitin Pillai', 'Venue': 'T6'}, 'AN(B)': {'Faculty': 'Nitin Pillai', 'Venue': 'T6'},
    'B2B(A)': {'Faculty': 'Sandip Trada', 'Venue': 'T5'}, 'B2B(B)': {'Faculty': 'Rupam Deb', 'Venue': '208-B'},
    "B2B('C)": {'Faculty': 'Nityesh Bhatt', 'Venue': '208-B'}, 'BS': {'Faculty': 'Satish Nair', 'Venue': 'T6'},
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
    'TEOM(B)': {'Faculty': 'P Ganesh', 'Venue': 'T3'}, "VALU('C)": {'Faculty': 'Dimple Bhojwani', 'Venue': 'T5'},
    'VALU(A)': {'Faculty': 'Dipti Saraf', 'Venue': 'T6'}, 'VALU(B)': {'Faculty': 'Dipti Saraf', 'Venue': 'T6'},
    'VALU(D)': {'Faculty': 'Dimple Bhojwani', 'Venue': 'T5'}
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
        schedule_df[0] = pd.to_datetime(schedule_df[0], errors='coerce')
        schedule_df.dropna(subset=[0], inplace=True)
        return schedule_df
    except FileNotFoundError:
        st.error(f"FATAL ERROR: The main schedule file '{file_path}' was not found.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"FATAL ERROR: Could not load the main schedule file. Details: {e}")
        return pd.DataFrame()

# --- UPDATED: This function now also captures the Serial Number ---
@st.cache_data
def get_all_student_data(folder_path='.'):
    """Scans all student files and caches a map of roll numbers to their name, sections, and serial numbers."""
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
            
            subject_row = df.iloc[0]
            header_row = df.iloc[header_row_index]
            roll_no_columns = header_row[header_row.astype(str).str.upper().str.contains('ROLL')].index

            for col_idx in roll_no_columns:
                section_name = subject_row[col_idx]
                name_col_idx = col_idx + 1
                sr_no_col_idx = col_idx - 1 # Assume Sr.No is to the left of Roll No.

                for _, row in df.iloc[header_row_index + 1:].iterrows():
                    roll_no = str(row[col_idx]).upper()
                    student_name = row[name_col_idx]
                    sr_no = row.get(sr_no_col_idx, 'N/A') # Safely get serial number

                    if roll_no not in student_data_map:
                        student_data_map[roll_no] = {'name': student_name, 'sections': {}}
                    
                    student_data_map[roll_no]['sections'][section_name] = sr_no
        except Exception:
            continue
    return student_data_map

def generate_ics_content(found_classes):
    """Generates the content for an iCalendar (.ics) file, now including Sr. No."""
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
            end_hour = int(re.search(r'^\d+', end_str_part).group(0))
            if end_am_pm == "PM" and start_hour < 12 and (start_hour > end_hour or start_hour == 11):
                start_am_pm = "AM"
            full_start_str, full_end_str = f"{start_str_part}{start_am_pm}", end_str_part
            start_dt = local_tz.localize(pd.to_datetime(f"{class_info['Date'].strftime('%Y-%m-%d')} {full_start_str}"))
            end_dt = local_tz.localize(pd.to_datetime(f"{class_info['Date'].strftime('%Y-%m-%d')} {full_end_str}"))
            
            e.name = f"{class_info['Subject']}"
            e.begin = start_dt.astimezone(pytz.utc)
            e.end = end_dt.astimezone(pytz.utc)
            e.location = class_info['Venue']
            # --- NEW: Add Sr. No. to calendar event description ---
            e.description = f"Faculty: {class_info['Faculty']}\nVenue: {class_info['Venue']}\nSr. No: {class_info['SrNo']}"
            e.uid = hashlib.md5(f"{start_dt.isoformat()}-{e.name}".encode('utf-8')).hexdigest() + "@timetable.app"
            c.events.add(e)
        except Exception:
            continue
    return c.serialize()

# 4. STREAMLIT WEB APP INTERFACE
st.set_page_config(page_title="Student Timetable Generator", layout="wide")
st.title("🎓 Student Timetable Generator")

master_schedule_df = load_and_clean_schedule(SCHEDULE_FILE_NAME)
student_data_map = get_all_student_data()

if not master_schedule_df.empty and student_data_map:
    roll_number = st.text_input("Enter your Roll Number:", placeholder="e.g., 24MBA463").strip().upper()

    if roll_number in student_data_map:
        student_info = student_data_map[roll_number]
        # --- NEW: Student data now includes a map of sections to serial numbers ---
        student_name, student_sections_map = student_info['name'], student_info['sections']
        student_sections = list(student_sections_map.keys())
        
        with st.spinner(f'Finding classes for {student_name}...'):
            NORMALIZED_COURSE_DETAILS_MAP = {normalize_string(section): details for section, details in COURSE_DETAILS_MAP.items()}
            normalized_student_section_map = {normalize_string(sec): sec for sec in student_sections}
            time_slots = {2: "8-9AM", 3: "9:10-10:10AM", 4: "10:20-11:20AM", 5: "11:30-12:30PM", 6: "12:30-1:30PM", 7: "1:30-2:30PM", 8: "2:40-3:40PM", 9: "3:50-4:50PM", 10: "5-6PM", 11: "6:10-7:10PM", 12: "7:20-8:20PM", 13: "8:30-9:30PM"}
            found_classes = []
            for index, row in master_schedule_df.iterrows():
                date, day = row[0], row[1]
                for col_index, time in time_slots.items():
                    cell_value = row[col_index]
                    if isinstance(cell_value, str):
                        normalized_cell = normalize_string(cell_value)
                        for norm_sec, orig_sec in normalized_student_section_map.items():
                            if norm_sec in normalized_cell:
                                details = NORMALIZED_COURSE_DETAILS_MAP.get(norm_sec, {'Faculty': 'N/A', 'Venue': '-'})
                                # --- NEW: Get the serial number for this specific subject ---
                                sr_no = student_sections_map.get(orig_sec, 'N/A')
                                found_classes.append({"Date": date, "Day": day, "Time": time, "Subject": orig_sec, "Faculty": details['Faculty'], "Venue": details['Venue'], "SrNo": sr_no})
            found_classes = [dict(t) for t in {tuple(d.items()) for d in found_classes}]

        st.success(f"Found {len(found_classes)} classes for **{student_name}**.")
        
        if found_classes:
            ics_content = generate_ics_content(found_classes)
            sanitized_name = re.sub(r'[^a-zA-Z0-9_]', '', student_name.replace(" ", "_")).upper()
            
            st.download_button(label="📅 Download Calendar (.ics) File", data=ics_content, file_name=f"{sanitized_name}_Timetable.ics", mime='text/calendar')
            
            with st.expander("**How to Import to Google Calendar**"):
                st.markdown(f"""
                1. Click the **'Download Calendar (.ics) File'** button above to save the schedule.
                2. Go to the [**Google Calendar Import Page**]({GOOGLE_CALENDAR_IMPORT_LINK}).
                3. Under 'Import from computer', click **'Select file from your computer'**.
                4. Choose the `.ics` file you just downloaded.
                5. Finally, click the blue **'Import'** button to add all your classes at once.
                """)
            
            st.markdown("---")
            st.subheader("Timetable Preview")
            
            timetable_df = pd.DataFrame(found_classes)
            # --- NEW: Add Sr. No. to the display string ---
            timetable_df['Class Info'] = timetable_df['Subject'] + '\n(Sr.No: ' + timetable_df['SrNo'].astype(str) + ')'
            
            timetable_df['Day/Date'] = timetable_df['Date'].dt.strftime('%A, %d-%b')
            sorted_times = [time_slots[key] for key in sorted(time_slots.keys())]
            final_schedule = timetable_df.pivot_table(index='Day/Date', columns='Time', values='Class Info', aggfunc='first')
            times_with_classes = [time for time in sorted_times if time in final_schedule.columns]
            final_schedule = final_schedule[times_with_classes]
            final_schedule.fillna('', inplace=True)
            final_schedule = final_schedule.reindex(sorted(final_schedule.index, key=lambda x: pd.to_datetime(x.split(', ')[1] + " 2025")))
            
            st.dataframe(final_schedule)
            
    elif roll_number:
        st.error(f"Roll Number '{roll_number}' not found. Please check the number and try again.")
else:
    st.warning("Application is initializing or required data files are missing. Please wait or check the folder.")
