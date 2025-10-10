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
from collections import defaultdict

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
        # sheet_name=1 as in original script (second sheet)
        df = pd.read_excel(file_path, sheet_name=1, header=None, skiprows=3)
        schedule_df = df.iloc[:, 0:14].copy()
        schedule_df[0] = pd.to_datetime(schedule_df[0], errors='coerce').dt.date
        schedule_df.dropna(subset=[0], inplace=True)
        return schedule_df
    except FileNotFoundError:
        st.error(f"FATAL ERROR: The main schedule file '{file_path}' was not found. Please make sure it's in the same folder as the app.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"FATAL ERROR: Could not load the main schedule file. Details: {e}")
        return pd.DataFrame()

@st.cache_data
def get_all_student_data(folder_path='.'):
    """Scans all student files once and caches the result for performance."""
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

def generate_ics_content(found_classes):
    """Generates the content for an iCalendar (.ics) file."""
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
            # heuristic: if end is PM and start hour < 12 and start_hour > end_hour OR start_hour == 11, adjust
            if end_am_pm == "PM" and start_hour < 12 and (start_hour > int(re.search(r'^\d+', end_str_part).group(0)) or start_hour == 11):
                start_am_pm = "AM"
            full_start_str, full_end_str = f"{start_str_part}{start_am_pm}", end_str_part
            start_dt = local_tz.localize(pd.to_datetime(f"{class_info['Date'].strftime('%Y-%m-%d')} {full_start_str}"))
            end_dt = local_tz.localize(pd.to_datetime(f"{class_info['Date'].strftime('%Y-%m-%d')} {full_end_str}"))
            e.name, e.begin, e.end = f"{class_info['Subject']}", start_dt.astimezone(pytz.utc), end_dt.astimezone(pytz.utc)
            e.location, e.description = class_info['Venue'], f"Faculty: {class_info['Faculty']}"
            e.uid = hashlib.md5(f"{start_dt.isoformat()}-{e.name}".encode('utf-8')).hexdigest() + "@timetable.app"
            c.events.add(e)
        except Exception:
            continue
    return c.serialize()

# ---------- UI: DROP-IN REPLACEMENT ----------
st.set_page_config(page_title="Import Timetable", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
<style>
:root{
  --page-bg: #eef3f5;        /* slightly darker-than-white page */
  --card-bg: #f7fafb;        /* content card */
  --muted: #57606a;
  --accent: #2ea6a1;         /* teal-ish accent */
  --card-border: rgba(10,20,30,0.04);
  --rounded: 12px;
}

/* page */
.stApp {
  background: linear-gradient(180deg, var(--page-bg), #e9eef0 120%);
  color: #0b1720;
  font-family: Inter, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
}

/* simple header */
.header-wrap { display:flex; align-items:center; justify-content:center; margin-top:18px; margin-bottom:8px; }
.main-header {
  font-size: 1.8rem;
  font-weight:800;
  margin:0;
  color:#07363a;
}

/* small subtitle */
.header-sub { text-align:center; color:var(--muted); margin-bottom:18px; }

/* container card */
.container {
  width:760px;
  margin: 0 auto 36px auto;
}

/* controls card */
.controls {
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  padding: 14px;
  border-radius: var(--rounded);
  box-shadow: 0 8px 20px rgba(10,20,30,0.03);
  display:flex;
  gap:12px;
  align-items:center;
}

/* form input in controls */
.controls .left { flex:1; display:flex; gap:12px; align-items:center; }
.stTextInput>div>div>input {
  background: rgba(0,0,0,0.02) !important;
  border-radius: 8px !important;
  padding: 10px 12px !important;
  border: 1px solid rgba(10,20,30,0.04) !important;
  color: #0b1720 !important;
}

/* generate button styling */
.stButton>button, .stForm button {
  background: linear-gradient(180deg, var(--accent), #1f8f8a);
  color: white;
  font-weight:700;
  border-radius: 8px;
  padding: 8px 14px;
  border: none;
  box-shadow: 0 8px 22px rgba(46,166,161,0.08);
}
.stButton>button:hover { transform: translateY(-3px); }

/* quick download + expander area */
.action-row { display:flex; gap:12px; align-items:center; margin-top:12px; }

/* cards list */
.day-card {
  background: var(--card-bg);
  border-radius: 10px;
  border: 1px solid var(--card-border);
  margin-top:16px;
  overflow:hidden;
  box-shadow: 0 10px 30px rgba(10,20,30,0.03);
}
.day-card .card-header {
  background: linear-gradient(90deg, rgba(46,166,161,0.12), rgba(20,110,110,0.06));
  padding:10px 14px;
  font-weight:700;
  color:#0b3e3d;
  display:flex; justify-content:space-between; align-items:center;
}
.card-body { padding:12px 14px; }
.class-entry {
  display:flex; justify-content:space-between; gap:12px; align-items:center;
  padding:12px 0;
  border-top: 1px solid rgba(10,20,30,0.02);
}
.class-entry:first-child { border-top:none; padding-top:6px; }
.subject { font-weight:700; color:#0b3e3d; }
.details { color:var(--muted); font-size:0.92rem; }

/* subtle thin divider above each day-card when stacked */
.day-card + .day-card { margin-top:18px; }

/* smaller text */
.small-muted { color:var(--muted); font-size:0.92rem; margin-top:6px; }

/* responsive */
@media (max-width:820px){
  .container { width:92%; padding:0 8px; }
  .controls { flex-direction:column; align-items:stretch; }
  .action-row { flex-direction:column; align-items:stretch; gap:8px; }
}
</style>
""", unsafe_allow_html=True)

# header
st.markdown('<div class="header-wrap"><p class="main-header">📅 Import Timetable to Your Google Calendar</p></div>', unsafe_allow_html=True)
st.markdown('<div class="header-sub">Generate an .ics file from your schedule and import it into Google Calendar.</div>', unsafe_allow_html=True)

# container
st.markdown('<div class="container">', unsafe_allow_html=True)

# Controls: use a form so the Generate button aligns with the input
with st.form("roll_form"):
    st.markdown('<div class="controls">', unsafe_allow_html=True)
    # left: input
    st.markdown('<div class="left">', unsafe_allow_html=True)
    roll_number = st.text_input("Roll number", placeholder="e.g., 24MBA463").strip().upper()
    st.markdown('</div>', unsafe_allow_html=True)
    # right: generate button (aligned inside form)
    generate_clicked = st.form_submit_button("Generate")
    st.markdown('</div>', unsafe_allow_html=True)

# After form: show download + instructions if generated
master_schedule_df = load_and_clean_schedule(SCHEDULE_FILE_NAME)
student_data_map = get_all_student_data()

if not master_schedule_df.empty and student_data_map:
    if generate_clicked and roll_number:
        if roll_number in student_data_map:
            student_info = student_data_map[roll_number]
            student_name, student_sections = student_info['name'], student_info['sections']

            with st.spinner(f'Finding classes for {student_name}...'):
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
                                    details = NORMALIZED_COURSE_DETAILS_MAP.get(norm_sec, {'Faculty': 'N/A', 'Venue': '-'})
                                    found_classes.append({
                                        "Date": date, "Day": day, "Time": time, "Subject": orig_sec,
                                        "Faculty": details.get('Faculty', 'N/A'), "Venue": details.get('Venue', '-')
                                    })
                found_classes = [dict(t) for t in {tuple(d.items()) for d in found_classes}]

            st.success(f"Found {len(found_classes)} classes for **{student_name}**.")

            if found_classes:
                ics_content = generate_ics_content(found_classes)
                sanitized_name = re.sub(r'[^a-zA-Z0-9_]', '', str(student_name).replace(" ", "_")).upper()

                # download + instructions
                st.markdown('<div class="action-row">', unsafe_allow_html=True)
                st.download_button("📅 Download .ics (Google Calendar)", data=ics_content, file_name=f"{sanitized_name}_Timetable.ics", mime='text/calendar')
                with st.expander("How to import to Google Calendar", expanded=False):
                    st.markdown(f"""
                    1. Click the **'Download .ics'** button above to save the schedule.  
                    2. Go to the [**Google Calendar Import Page**]({GOOGLE_CALENDAR_IMPORT_LINK}).  
                    3. Under 'Import from computer', click **'Select file from your computer'**.  
                    4. Choose the `.ics` file you downloaded.  
                    5. Click **'Import'** to add the events.
                    """)
                st.markdown('</div>', unsafe_allow_html=True)

                # render timetable
                schedule_by_date = defaultdict(list)
                for class_info in found_classes:
                    schedule_by_date[class_info['Date']].append(class_info)
                sorted_dates = sorted(schedule_by_date.keys())
                time_sorter = {time: i for i, time in enumerate(time_slots.values())}

                for date in sorted_dates:
                    schedule_by_date[date].sort(key=lambda x: time_sorter.get(x['Time'], 99))
                    st.markdown('<div class="day-card">', unsafe_allow_html=True)
                    st.markdown(f'<div class="card-header"><div class="date">{date.strftime("%A, %d %B %Y")}</div><div class="count">Total: {len(schedule_by_date[date])}</div></div>', unsafe_allow_html=True)
                    st.markdown('<div class="card-body">', unsafe_allow_html=True)

                    for class_info in schedule_by_date[date]:
                        st.markdown(f'''
                            <div class="class-entry">
                              <div class="left">
                                <div class="subject">{class_info["Subject"]}</div>
                                <div class="details">Faculty: {class_info["Faculty"]} · {class_info["Time"]} · {class_info["Venue"]}</div>
                              </div>
                              <div class="badge">{class_info["Time"]}</div>
                            </div>
                        ''', unsafe_allow_html=True)

                    st.markdown('</div>', unsafe_allow_html=True)  # close card-body
                    st.markdown('</div>', unsafe_allow_html=True)  # close day-card

        else:
            st.error(f"Roll Number '{roll_number}' not found. Please check the number and try again.")
else:
    st.warning("Application is initializing or required data files are missing. Please wait or check the folder.")

st.markdown('</div>', unsafe_allow_html=True)  # close container
