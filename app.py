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

# 4. STREAMLIT WEB APP INTERFACE — PREMIUM LAYOUT
st.set_page_config(page_title="Import Timetable", layout="wide", initial_sidebar_state="auto")

# ---------- STYLES ----------
st.markdown("""
<style>
:root{
  --bg: #f7fafc;
  --panel: #ffffff;
  --muted: #6b7280;
  --accent1: #0ea5a4; /* teal */
  --accent2: #2563eb; /* blue */
  --glass: rgba(15,23,42,0.04);
  --rounded: 14px;
}

/* page background */
.stApp {
  background: linear-gradient(180deg,#fbfdff 0%, #f3f7fb 100%);
  color:#0f172a;
  font-family: Inter, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
}

/* top nav */
.navbar {
  background: linear-gradient(90deg,var(--accent1),var(--accent2));
  padding: 12px 22px;
  border-radius: 10px;
  color: white;
  display:flex;
  align-items:center;
  justify-content:space-between;
  margin-bottom: 18px;
  box-shadow: 0 8px 28px rgba(30,41,59,0.06);
}
.brand { display:flex; gap:12px; align-items:center; font-weight:800; font-size:1.05rem; }
.brand .logo {
  width:40px; height:40px; background:rgba(255,255,255,0.14); border-radius:8px; display:flex; align-items:center; justify-content:center;
  font-weight:900;
}

/* main layout: sidebar + content */
.layout {
  display:grid;
  grid-template-columns: 320px 1fr;
  gap:24px;
  align-items:start;
}

/* left panel controls */
.controls {
  background: var(--panel);
  padding:18px;
  border-radius: var(--rounded);
  border:1px solid rgba(15,23,42,0.04);
  box-shadow: 0 8px 24px rgba(15,23,42,0.04);
  height:fit-content;
}
.controls h4 { margin:0 0 8px 0; font-size:1.05rem; }
.small-muted { color:var(--muted); font-size:0.9rem; margin-top:10px; }

/* right content area */
.content {
  display:flex; flex-direction:column; gap:14px;
}

/* quick stats / download card */
.quick {
  display:flex; gap:12px; align-items:center; justify-content:space-between;
  background: linear-gradient(180deg, rgba(14,165,164,0.02), rgba(37,99,235,0.01));
  padding:14px; border-radius:12px; border:1px solid rgba(15,23,42,0.03);
}
.quick .left { display:flex; flex-direction:column; gap:4px; }
.quick .big { font-weight:800; font-size:1.05rem; }
.quick .muted { color:var(--muted); font-size:0.9rem; }

/* day card list */
.day-list { display:flex; flex-direction:column; gap:12px; }
.day-card {
  background: var(--panel);
  border-radius: 10px;
  padding:0;
  border:1px solid rgba(15,23,42,0.04);
  overflow:hidden;
  box-shadow: 0 8px 20px rgba(15,23,42,0.03);
}

/* header bar on each day card */
.day-card .card-header {
  background: linear-gradient(90deg,var(--accent2),var(--accent1));
  color: white;
  padding:10px 14px;
  font-weight:700;
  display:flex; justify-content:space-between; align-items:center;
}
.card-header .date { font-size:0.97rem; }
.card-header .count { font-size:0.9rem; opacity:0.95; }

/* list of classes inside card */
.card-body { padding:12px 14px; }
.class-entry {
  display:flex; justify-content:space-between; gap:12px; align-items:center;
  padding:12px 0;
  border-top: 1px solid rgba(15,23,42,0.03);
}
.class-entry:first-child { border-top:none; padding-top:6px; }
.left {
  display:flex; flex-direction:column; gap:6px;
}
.subject { font-weight:700; color:#062a4a; }
.details { font-size:0.9rem; color:var(--muted); }
.badge {
  display:inline-block; padding:6px 10px; border-radius:8px; background:var(--glass);
  font-size:0.9rem; color:#073045; font-weight:700;
  border:1px solid rgba(2,6,23,0.04);
  text-align:right;
  min-width:120px;
}

/* responsive */
@media (max-width:1000px){
  .layout { grid-template-columns: 1fr; }
  .controls { order:2; }
  .content { order:1; }
}
</style>
""", unsafe_allow_html=True)

# ---------- TOP NAV ----------
st.markdown(f"""
<div class="navbar">
  <div class="brand">
    <div class="logo">📘</div>
    Class Schedule
  </div>
  <div style="display:flex;gap:18px;align-items:center;">
    <div style="color:rgba(255,255,255,0.95);font-weight:600">My Schedule</div>
    <div style="color:rgba(255,255,255,0.95);font-weight:600">Faculty</div>
    <div style="color:rgba(255,255,255,0.95);font-weight:600">Support</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ---------- LAYOUT (controls + content) ----------
st.markdown('<div class="layout">', unsafe_allow_html=True)

# ---- LEFT: Controls ----
st.markdown('<div class="controls">', unsafe_allow_html=True)
st.markdown('<h4>Search & Export</h4>', unsafe_allow_html=True)

# keep the existing text_input and button but inside controls
roll_col1, roll_col2 = st.columns([3,1])
with roll_col1:
    roll_number = st.text_input("Roll number", placeholder="e.g., 24MBA463").strip().upper()
with roll_col2:
    submitted = st.button("Generate", key="generate_btn")

st.markdown('<div class="small-muted">Enter your campus roll to generate an .ics file for Google Calendar.</div>', unsafe_allow_html=True)

# accent choice (simple)
accent = st.selectbox("Accent color", ["Teal (default)", "Sapphire", "Coral"], index=0)

# quick stats: once attempted generation, show counts
if 'preview_count' not in st.session_state:
    st.session_state.preview_count = 0

st.markdown('<hr style="opacity:0.06">', unsafe_allow_html=True)
st.markdown('<h4>Quick Actions</h4>', unsafe_allow_html=True)

if st.button("Preview timetable (count)"):
    st.session_state.preview_count += 1

st.markdown(f'<div style="margin-top:8px"><b>Previews:</b> {st.session_state.preview_count}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # close controls

# ---- RIGHT: Content ----
st.markdown('<div class="content">', unsafe_allow_html=True)

# Quick top card with download placeholder
st.markdown('<div class="quick"><div class="left"><div class="big">Import Timetable</div><div class="muted">Generate a calendar file and import into Google Calendar</div></div><div style="display:flex;flex-direction:column;gap:8px;align-items:flex-end"><div style="font-weight:700">Export</div></div></div>', unsafe_allow_html=True)

# Now plug your existing data-loading logic
master_schedule_df = load_and_clean_schedule(SCHEDULE_FILE_NAME)
student_data_map = get_all_student_data()

if not master_schedule_df.empty and student_data_map:
    if submitted and roll_number:
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
                c1, c2 = st.columns([3,1])
                with c1:
                    st.download_button("📅 Download .ics (Google Calendar)", data=ics_content, file_name=f"{sanitized_name}_Timetable.ics", mime='text/calendar')
                with c2:
                    with st.expander("How to import to Google Calendar", expanded=False):
                        st.markdown(f"""
                        1. Click the **'Download .ics'** button above to save the schedule.  
                        2. Go to the **Google Calendar Import** page.  
                        3. Under 'Import from computer', click **'Select file from your computer'**.  
                        4. Choose the `.ics` file you downloaded.  
                        5. Click **'Import'** to add the events.
                        """)

                # build schedule grouped by date
                schedule_by_date = defaultdict(list)
                for class_info in found_classes:
                    schedule_by_date[class_info['Date']].append(class_info)
                sorted_dates = sorted(schedule_by_date.keys())
                time_sorter = {time: i for i, time in enumerate(time_slots.values())}

                # render day cards (modern look)
                st.markdown('<div class="day-list">', unsafe_allow_html=True)
                for date in sorted_dates:
                    schedule_by_date[date].sort(key=lambda x: time_sorter.get(x['Time'], 99))
                    # day card header
                    st.markdown('<div class="day-card">', unsafe_allow_html=True)
                    st.markdown(f'<div class="card-header"><div class="date">{date.strftime("%A, %d %B %Y")}</div><div class="count">Total: {len(schedule_by_date[date])}</div></div>', unsafe_allow_html=True)
                    st.markdown('<div class="card-body">', unsafe_allow_html=True)

                    for class_info in schedule_by_date[date]:
                        meta_html = f'<div class="badge">🕒 {class_info["Time"]}<br><span style="font-weight:600;color:var(--muted);font-size:0.8rem">📍 {class_info["Venue"]}</span></div>'
                        st.markdown(f'''
                            <div class="class-entry">
                                <div class="left">
                                    <div class="subject">{class_info["Subject"]}</div>
                                    <div class="details">Faculty: {class_info["Faculty"]}</div>
                                </div>
                                {meta_html}
                            </div>
                        ''', unsafe_allow_html=True)

                    st.markdown('</div>', unsafe_allow_html=True)  # close card-body
                    st.markdown('</div>', unsafe_allow_html=True)  # close day-card

                st.markdown('</div>', unsafe_allow_html=True)  # close day-list

        else:
            st.error(f"Roll Number '{roll_number}' not found. Please check the number and try again.")

else:
    st.warning("Application is initializing or required data files are missing. Please wait or check the folder.")

st.markdown('</div>', unsafe_allow_html=True)  # close content
st.markdown('</div>', unsafe_allow_html=True)  # close layout
