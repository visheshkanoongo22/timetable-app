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
from datetime import date as dt_date
TODAY = dt_date.today()

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

# 4. STREAMLIT WEB APP INTERFACE
st.set_page_config(page_title="Import Timetable to Google Calendar", layout="centered", initial_sidebar_state="collapsed")

# --- UPDATED: Vibrant, professional dark theme CSS ---
# Notes on design choices:
# - Deep navy background with a subtle radial gradient for depth
# - Accent gradient (teal -> coral) for headings and highlights — energetic but mature
# - Glassmorphism cards with subtle borders, soft shadows and hover lift
# - Smooth transitions on hover, readable typography, small decorative accent line
st.markdown("""
<style>
    :root{
        --bg:#070812;               /* very dark navy */
        --card:#0e1220;             /* card background (slightly lighter) */
        --muted:#bfc8d6;            /* muted readable text */
        --accent-start:#47c6b7;     /* teal */
        --accent-end:#ff7a66;       /* coral */
        --accent-text: linear-gradient(90deg, var(--accent-start), var(--accent-end));
        --glass-border: rgba(255,255,255,0.04);
    }

    /* App base */
    .stApp {
        background: radial-gradient(1200px 600px at 10% 10%, rgba(71,198,183,0.06), transparent 10%),
                    radial-gradient(1000px 500px at 90% 90%, rgba(255,122,102,0.04), transparent 10%),
                    var(--bg);
        color: #ffffff;
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
    }

    /* Header style */
    .main-header {
        font-size: 2.4rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 1.5rem;
        background: -webkit-linear-gradient(90deg, var(--accent-start), var(--accent-end));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 0.2px;
    }

    /* Subtitle / small accent line under header */
    .header-sub {
        text-align:center;
        color:var(--muted);
        margin-top:-0.25rem;
        margin-bottom:1.5rem;
        font-size:0.95rem;
    }

    /* Cards (glass feel) */
    .day-card {
        background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
        border-radius: 14px;
        padding: 1.25rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 8px 30px rgba(2,6,23,0.6);
        border: 1px solid var(--glass-border);
        transition: transform 0.18s ease, box-shadow 0.18s ease;
    }

    .day-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 18px 40px rgba(2,6,23,0.75);
    }

    .day-header {
        display:flex;
        align-items:center;
        gap:0.6rem;
        font-size:1.25rem;
        font-weight:700;
        color:#eaf6f1; /* light mint */
        margin-bottom:0.6rem;
    }

    .day-header .date-badge {
        font-size:0.85rem;
        padding:0.28rem 0.55rem;
        border-radius:8px;
        background: linear-gradient(90deg, rgba(71,198,183,0.06), rgba(255,122,102,0.04));
        color:var(--muted);
        border:1px solid rgba(255,255,255,0.02);
    }

    .class-entry {
        display:flex;
        flex-direction:row;
        align-items:center;
        justify-content:space-between;
        padding-top:0.65rem;
        padding-bottom:0.65rem;
        border-bottom:1px solid rgba(255,255,255,0.02);
    }
    .day-card .class-entry:last-child { border-bottom: none; padding-bottom: 0; }

    .left {
        display:flex;
        flex-direction:column;
        gap:0.2rem;
    }

    .subject-name {
        font-size:1.05rem;
        font-weight:700;
        margin:0;
        color: transparent;
        background: var(--accent-text);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .class-details {
        font-size:0.94rem;
        color:var(--muted);
    }

    .meta {
        text-align:right;
        min-width:170px;
    }

    .meta .time {
        display:block;
        font-weight:600;
        color:#fff;
        font-size:0.97rem;
    }

    .meta .venue, .meta .faculty {
        display:block;
        font-size:0.85rem;
        color:var(--muted);
    }

    /* Styled download button */
    .stDownloadButton>button {
        background: linear-gradient(90deg, var(--accent-start), var(--accent-end));
        color: #0b0b0b;
        font-weight:700;
        padding: 0.5rem 0.9rem;
        border-radius:10px;
        border:none;
        box-shadow: 0 8px 20px rgba(71,198,183,0.08);
    }
    .stDownloadButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 14px 30px rgba(71,198,183,0.12);
    }

    /* Links and small controls */
    a {
        color: #9fe6d8;
        font-weight:600;
    }

    /* Make sure default streamlit containers use readable text */
    .css-1d391kg, .css-1v3fvcr, .css-18ni7ap {
        color: #ffffff;
    }

    /* Form input styles (improve contrast) */
    .stTextInput>div>div>input, .stTextInput>div>div>textarea {
        background: rgba(255,255,255,0.02) !important;
        color: #e6eef2 !important;
        border: 1px solid rgba(255,255,255,0.04) !important;
        padding: 0.6rem !important;
        border-radius: 8px !important;
    }

    /* Small responsive tweaks */
    @media (max-width: 600px) {
        .meta { min-width: 120px; font-size:0.9rem; }
        .main-header { font-size: 1.8rem; }
    }

    /* Highlight today's schedule card */
.today-card {
    border: 2px solid #00ffaa !important;
    box-shadow: 0 0 20px rgba(0,255,170,0.3);
    position: relative;
}

.today-card::before {
    content: "Today";
    position: absolute;
    top: -10px;
    right: 15px;
    background: linear-gradient(90deg, #00ffaa, #00ffcc);
    color: #000;
    font-size: 0.7rem;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 6px;
}

</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">📅 Import Timetable to Your Google Calendar</p>', unsafe_allow_html=True)
st.markdown('<div class="header-sub">Elegant • Clean • Vibrant — your weekly classes, neatly organized</div>', unsafe_allow_html=True)

master_schedule_df = load_and_clean_schedule(SCHEDULE_FILE_NAME)
student_data_map = get_all_student_data()

if not master_schedule_df.empty and student_data_map:
    with st.form("roll_number_form"):
        roll_number = st.text_input("Enter your Roll Number:", placeholder="e.g., 24MBA463").strip().upper()
        submitted = st.form_submit_button("Generate Timetable")

    if submitted and roll_number:
        if roll_number in student_data_map:
            student_info = student_data_map[roll_number]
            student_name, student_sections = student_info['name'], student_info['sections']
            
            with st.spinner(f'Finding classes for {student_name}...'):
                # map normalized course names to details (normalized keys)
                NORMALIZED_COURSE_DETAILS_MAP = {normalize_string(section): details for section, details in COURSE_DETAILS_MAP.items()}

                # map normalized student-section -> original section (to keep original for display)
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
                            # iterate over normalized student sections and their original form
                            for norm_sec, orig_sec in normalized_student_section_map.items():
                                # if student's normalized section appears in the cell -> it's a match
                                if norm_sec in normalized_cell:
                                    # LOOKUP corrected: use normalized key (norm_sec) to fetch details
                                    details = NORMALIZED_COURSE_DETAILS_MAP.get(norm_sec, {'Faculty': 'N/A', 'Venue': '-'})
                                    found_classes.append({
                                        "Date": date,
                                        "Day": day,
                                        "Time": time,
                                        "Subject": orig_sec,        # display original section name
                                        "Faculty": details.get('Faculty', 'N/A'),
                                        "Venue": details.get('Venue', '-')
                                    })

                # deduplicate entries
                found_classes = [dict(t) for t in {tuple(d.items()) for d in found_classes}]

            st.success(f"Found {len(found_classes)} classes for **{student_name}**.")
            
            if found_classes:
                ics_content = generate_ics_content(found_classes)
                sanitized_name = re.sub(r'[^a-zA-Z0-9_]', '', str(student_name).replace(" ", "_")).upper()
                
                st.download_button(
                    label="📅 Download Calendar (.ics) File",
                    data=ics_content,
                    file_name=f"{sanitized_name}_Timetable.ics",
                    mime='text/calendar'
                )
                
                # --- Collapsible instructions (click to expand) ---
                with st.expander("How to Import to Google Calendar", expanded=False):
                    st.markdown(f"""
                    1. Click the **'Download Calendar (.ics) File'** button above to save the schedule.  
                    2. Go to the [**Google Calendar Import Page**]({GOOGLE_CALENDAR_IMPORT_LINK}).  
                    3. Under 'Import from computer', click **'Select file from your computer'**.  
                    4. Choose the `.ics` file you just downloaded.  
                    5. Click **'Import'** to add the events.
                    """)

                
                st.markdown("---")
                st.subheader("Timetable Preview")

                schedule_by_date = defaultdict(list)
                for class_info in found_classes:
                    schedule_by_date[class_info['Date']].append(class_info)
                
                sorted_dates = sorted(schedule_by_date.keys())
                
                time_sorter = {time: i for i, time in enumerate(time_slots.values())}
                for date in sorted_dates:
                    schedule_by_date[date].sort(key=lambda x: time_sorter.get(x['Time'], 99))

                for date in sorted_dates:
                # Add 'today-card' class if it’s today
                    card_class = "day-card today-card" if date == TODAY else "day-card"
                    card_id = f"day-{date.strftime('%Y%m%d')}"
                    st.markdown(f'<div id="{card_id}" class="{card_class}">', unsafe_allow_html=True)
                    st.markdown(f'<div class="day-header"><div class="date-badge">{date.strftime("%d %b")}</div><div>{date.strftime("%A, %d %B %Y")}</div></div>', unsafe_allow_html=True)
                    
                    classes_today = schedule_by_date[date]
                    for class_info in classes_today:
                        # structured layout for each class
                        meta_html = f'<div class="meta"><span class="time">🕒 {class_info["Time"]}</span><span class="venue">📍 {class_info["Venue"]}</span><span class="faculty">🧑‍🏫 {class_info["Faculty"]}</span></div>'
                        st.markdown(f'''
                            <div class="class-entry">
                                <div class="left">
                                    <div class="subject-name">{class_info["Subject"]}</div>
                                    <div class="class-details"></div>
                                </div>
                                {meta_html}
                            </div>
                        ''', unsafe_allow_html=True)
                    
                    st.markdown(f'</div>', unsafe_allow_html=True)
                    # --- Auto-scroll to today's card on load ---
                    st.markdown("""
                    <script>
                    window.addEventListener('load', function() {
                        const todayCard = document.querySelector('.today-card');
                        if (todayCard) {
                            todayCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
                        }
                    });
                    </script>
                    """, unsafe_allow_html=True)

                
        elif submitted:
            st.error(f"Roll Number '{roll_number}' not found. Please check the number and try again.")
else:
    st.warning("Application is initializing or required data files are missing. Please wait or check the folder.")







