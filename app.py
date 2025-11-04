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

SCHEDULE_FILE_NAME = 'schedule.xlsx'
TIMEZONE = 'Asia/Kolkata'
GOOGLE_CALENDAR_IMPORT_LINK = 'https://calendar.google.com/calendar/u/0/r/settings/export'
COURSE_DETAILS_MAP = {
    'AN(A)': {'Faculty': 'Nitin Pillai', 'Venue': 'T6'}, 'AN(B)': {'Faculty': 'Nitin Pillai', 'Venue': 'T6'},
    'B2B(A)': {'Faculty': 'Sandip Trada', 'Venue': 'T5'}, 'B2B(B)': {'Faculty': 'Rupam Deb', 'Venue': '309-F'},
    "B2B('C)": {'Faculty': 'Rupam Deb', 'Venue': '309-F'}, 'BS': {'Faculty': 'Satish Nair', 'Venue': 'T6'},
    'CC&AU(A)': {'Faculty': 'Lalit Arora', 'Venue': 'T6'}, 'CC&AU(B)': {'Faculty': 'Lalit Arora', 'Venue': 'T6'},
    'CSE': {'Faculty': 'Shahir Bhatt', 'Venue': 'T6'}, 'DADM': {'Faculty': 'Mahesh K C', 'Venue': 'T3'},
    'DC': {'Faculty': 'Sapan Oza', 'Venue': 'T6'}, 'DM(A)': {'Faculty': 'Shailesh Prabhu', 'Venue': '214'},
    'DM(B)': {'Faculty': 'Shailesh Prabhu', 'Venue': '214'}, "DRM('C)": {'Faculty': 'Pankaj Agrawal', 'Venue': 'T5'},
    'DRM(A)': {'Faculty': 'Bhavesh Patel', 'Venue': 'T6'}, 'DRM(B)': {'Faculty': 'Bhavesh Patel', 'Venue': 'T6'},
    "DV&VS('C)": {'Faculty': 'Anand Kumar', 'Venue': 'E2'}, 'DV&VS(A)': {'Faculty': 'Somayya Madakam', 'Venue': 'E3'},
    'DV&VS(B)': {'Faculty': 'Somayya Madakam', 'Venue': 'E3'}, 'DV&VS(D)': {'Faculty': 'Anand Kumar', 'Venue': 'T5'},
    'IMC(A)': {'Faculty': 'Sanjay Jain', 'Venue': 'T3'}, 'IMC(B)': {'Faculty': 'Riddhi Ambavale', 'Venue': 'T7'},
    'INB(A)': {'Faculty': 'M C Gupta', 'Venue': 'T7'}, 'INB(B)': {'Faculty': 'M C Gupta', 'Venue': 'T7'},
    'INB(C)': {'Faculty': 'M C Gupta', 'Venue': 'T7'}, 'LSS(A)': {'Faculty': 'Rajesh Jain', 'Venue': 'T3'},
    'LSS(B)': {'Faculty': 'Rajesh Jain', 'Venue': 'T3'}, 'ML&AI(A)': {'Faculty': 'Omkar Sahoo', 'Venue': 'T5'},
    'ML&AI(B)': {'Faculty': 'Omkar Sahoo', 'Venue': 'T5'}, 'OMSD': {'Faculty': 'Dinesh Panchal', 'Venue': '214'},
    'PDBE(A)': {'Faculty': 'Nina Muncherji', 'Venue': 'T6'}, 'PDBE(B)': {'Faculty': 'Nina Muncherji', 'Venue': 'T6'},
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
        st.error(f"FATAL ERROR: The main schedule file '{file_path}' was not found. Please make sure it's in the same folder as the app.")
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
st.set_page_config(
    page_title="MBA Timetable Assistant", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# Force dark mode by injecting meta tags and overriding system preferences
st.markdown("""
    <meta name="color-scheme" content="dark">
    <meta name="theme-color" content="#0F172A">
""", unsafe_allow_html=True)

# --- CSS STYLING ---
local_css_string = """
<style>
    /* --- FORCE DARK MODE --- */
    * {
        color-scheme: dark !important;
    }
    
    /* Override any light mode settings from Streamlit */
    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"],
    section[data-testid="stSidebar"] {
        background-color: var(--bg) !important;
        color: #ffffff !important;
    }
    
    /* --- FONT IMPORT --- */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

    :root{
        --bg:#0F172A; /* Darker, more muted background */
        --card:#1E293B; /* Darker card background */
        --muted:#94A3B8; /* Muted text color */
        --accent-start:#60A5FA; /* Muted blue accent */
        --accent-end:#818CF8; /* Muted violet accent */
        --glass-border: rgba(255,255,255,0.08); /* Slightly more visible border */
        --today-glow: #38BDF8; /* Muted sky blue for today's highlight */
        --today-glow-shadow: rgba(56, 189, 248, 0.4);
    }

    .stApp {
        background: radial-gradient(1200px 600px at 10% 10%, rgba(96,165,250,0.08), transparent 10%), /* Muted blue gradient */
                    radial-gradient(1000px 500px at 90% 90%, rgba(129,140,248,0.06), transparent 10%), /* Muted violet gradient */
                    var(--bg);
        color: #ffffff;
        font-family: 'Inter', ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
    }

    /* --- PAGE HEADER --- */
    .main-header {
        font-size: 2.4rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.5rem;
        background: -webkit-linear-gradient(90deg, var(--accent-start), var(--accent-end));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 0.2px;
    }

    .header-sub {
        text-align:center;
        color:var(--muted);
        margin-top:0rem;
        margin-bottom:2rem;
        font-size:1.0rem;
    }
    
    /* --- WELCOME BOX --- */
    .welcome-box {
        background: var(--card);
        border: 1px solid var(--glass-border);
        padding: 1rem 1.25rem;
        border-radius: 14px;
        margin-bottom: 1.5rem;
        color: var(--muted);
        font-size: 0.95rem;
    }
    .welcome-box strong {
        color: #ffffff;
        font-weight: 600;
    }

    /* --- DAY PREVIEW CARD --- */
    .day-card {
        background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
        border-radius: 14px;
        padding: 1.25rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 8px 30px rgba(0,0,0,0.4); /* Darker shadow */
        border: 1px solid var(--glass-border);
        transition: transform 0.18s ease, box-shadow 0.18s ease;
        scroll-margin-top: 85px; /* Offset for Streamlit's header bar */
        position: relative;
    }
    .day-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 18px 40px rgba(0,0,0,0.6); /* Darker shadow on hover */
    }

    /* --- TODAY'S HIGHLIGHT (Adjusted glow colors) --- */
    .day-card.today {
        border: 3px solid var(--today-glow);
        box-shadow: 0 0 35px var(--today-glow-shadow), 
                    0 0 60px rgba(56, 189, 248, 0.2), /* Muted blue glow */
                    0 8px 30px rgba(0,0,0,0.4);
        animation: pulse-glow 2s ease-in-out infinite;
    }
    .today-badge {
        position: absolute;
        top: -12px;
        right: 20px;
        background: var(--today-glow);
        color: var(--bg); /* Use background color for text to make it subtle */
        font-size: 0.75rem;
        font-weight: 800;
        padding: 0.35rem 0.75rem;
        border-radius: 6px;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        box-shadow: 0 4px 15px var(--today-glow-shadow);
        z-index: 10;
    }
    @keyframes pulse-glow {
        0%, 100% {
            box-shadow: 0 0 35px var(--today-glow-shadow), 
                        0 0 60px rgba(56, 189, 248, 0.2),
                        0 8px 30px rgba(0,0,0,0.4);
        }
        50% {
            box-shadow: 0 0 45px rgba(56, 189, 248, 0.6), /* Muted blue glow */
                        0 0 80px rgba(56, 189, 248, 0.3),
                        0 8px 30px rgba(0,0,0,0.4);
        }
    }
    
    /* --- CARD CONTENT --- */
    .day-header {
        font-size: 1.15rem; /* Reduced font size */
        font-weight: 700;
        color: #E2E8F0; /* Slightly brighter text for headers */
        margin-bottom: 0.5rem; /* Reduced margin */
    }
    
    .class-entry {
        display:flex;
        flex-direction:row;
        align-items:center;
        justify-content:space-between;
        padding-top:0.65rem;
        padding-bottom:0.65rem;
        border-bottom:1px solid rgba(255,255,255,0.04); /* Slightly thicker/darker border */
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
        color: #FFFFFF; /* Set to solid white for max contrast */
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
    
    /* --- INPUT & BUTTON STYLES --- */
    .stDownloadButton>button, div[data-testid="stForm"] button[kind="primary"], .stButton>button {
        background: linear-gradient(90deg, var(--accent-start), var(--accent-end));
        color: var(--bg); /* Text color from background */
        font-weight:700;
        padding: 0.5rem 0.9rem;
        border-radius:10px;
        border:none;
        box-shadow: 0 8px 20px rgba(96,165,250,0.1); /* Muted shadow */
        width: 100%;
        transition: transform 0.18s ease, box-shadow 0.18s ease;
    }
    .stDownloadButton>button:hover, div[data-testid="stForm"] button[kind="primary"]:hover, .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 14px 30px rgba(96,165,250,0.15); /* Muted shadow on hover */
    }
    
    /* --- Style for the "Change" button --- */
    .stButton>button {
        width: auto; /* Allow the change button to be smaller */
        padding: 0.4rem 0.8rem;
        font-size: 0.9rem;
        background: var(--card); /* Make it look different */
        color: var(--muted);
        border: 1px solid var(--glass-border);
    }
    .stButton>button:hover {
        color: var(--accent-start);
        border-color: var(--accent-start);
    }

    a {
        color: var(--accent-start); /* Use one of the accent colors for links */
        font-weight:600;
    }
    
    /* --- FORM INPUT STYLING --- */
    .css-1d391kg, .css-1v3fvcr, .css-18ni7ap {
        color: #ffffff;
    }
    .stTextInput>div>div>input, .stTextInput>div>div>textarea {
        background: rgba(255,255,255,0.02) !important;
        color: #E2E8F0 !important; /* Brighter text for input */
        border: 1px solid rgba(255,255,255,0.06) !important; /* Slightly more visible border */
        padding: 0.6rem !important;
        border-radius: 8px !important;
    }
    
    /* --- RESULTS CONTAINER --- */
    .results-container {
        background: var(--card);
        border: 1px solid var(--glass-border);
        padding: 1.25rem;
        border-radius: 14px;
        margin-bottom: 1.5rem;
    }
    .results-container h3 {
        color: #E2E8F0; /* Subheader color */
        margin-top: 0;
        margin-bottom: 1rem;
        font-size: 1.3rem;
    }
    .results-container h3:not(:first-child) {
        margin-top: 1.5rem; /* Space between sections */
    }

    @media (max-width: 600px) {
        .meta { min-width: 120px; font-size:0.9rem; }
        .main-header { font-size: 1.8rem; }
    }
</style>
"""
st.markdown(local_css_string, unsafe_allow_html=True)

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

# --- MAIN APP LOGIC ---
if not master_schedule_df.empty and student_data_map:
    
    # --- DISPLAY FORM IF NOT SUBMITTED ---
    if not st.session_state.submitted:
        st.markdown(
            """
            <div class="welcome-box">
                Welcome! This application helps you generate your personalized class schedule and export it as a <strong>.ics calendar file</strong>.
                Simply enter your roll number below to get started.
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
                st.rerun()

    # --- PROCESS AND DISPLAY SCHEDULE IF SUBMITTED ---
    if st.session_state.submitted:
        roll_to_process = st.session_state.roll_number
        
        # Handle empty submission
        if not roll_to_process:
            st.session_state.submitted = False
            st.rerun()

        # Handle valid roll number
        elif roll_to_process in student_data_map:
            student_info = student_data_map[roll_to_process]
            student_name, student_sections = student_info['name'], student_info['sections']
            
            # Display header with "Change" button
            col1, col2 = st.columns([3, 1])
            with col1:
                st.success(f"Displaying schedule for {student_name}")
            with col2:
                if st.button("Change Roll Number"):
                    st.session_state.submitted = False
                    st.session_state.roll_number = ""
                    st.rerun()
            
            with st.spinner(f'Compiling classes for {student_name}...'):
                NORMALIZED_COURSE_DETAILS_MAP = {normalize_string(section): details for section, details in COURSE_DETAILS_MAP.items()}
                normalized_student_section_map = {normalize_string(sec): sec for sec in student_sections}

                time_slots = {2: "8-9AM", 3: "9:10-10:10AM", 4: "10:20-11:20AM", 5: "11:30-12:30PM",
                              6: "12:30-1:30PM", 7: "1:30-2:30PM", 8: "2:40-3:40PM", 9: "3:50-4:50PM",
                              10: "5-6PM", 11: "6:10-7:10PM", 12: "7:20-8:20PM", 13: "8:30-9:3App-c"}
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
                                        "Faculty": details.get('Faculty', 'N/A'),
                                        "Venue": details.get('Venue', '-')
                                    })

                found_classes = [dict(t) for t in {tuple(d.items()) for d in found_classes}]

            # --- ORGANIZED RESULTS SECTION ---
            if found_classes:
                ics_content = generate_ics_content(found_classes)
                sanitized_name = re.sub(r'[^a-zA-Z0.9_]', '', str(student_name).replace(" ", "_")).upper()
                
                with st.container():
                    st.markdown('<div class="results-container">', unsafe_allow_html=True)
                    st.markdown("### 1. Download Calendar File")
                    st.download_button(
                        label="Download .ics Calendar File",
                        data=ics_content,
                        file_name=f"{sanitized_name}_Timetable.ics",
                        mime='text/calendar'
                    )
                    
                    st.markdown("### 2. How to Import to Google Calendar")
                    with st.expander("Click to view import instructions", expanded=False):
                        st.markdown(f"""
                        1. Click the **'Download .ics Calendar File'** button above to save your schedule.  
                        2. Navigate to the [**Google Calendar Import Page**]({GOOGLE_CALENDAR_IMPORT_LINK}).  
                        3. Under 'Import from computer', click **'Select file from your computer'**.  
                        4. Choose the `.ics` file you just downloaded.  
                        5. Click **'Import'** to add the events to your calendar.
                        """)
                    st.markdown('</div>', unsafe_allow_html=True)

                # --- PREVIEW SECTION ---
                st.markdown("---")
                st.subheader("Your Timetable Preview")

                schedule_by_date = defaultdict(list)
                for class_info in found_classes:
                    schedule_by_date[class_info['Date']].append(class_info)
                
                sorted_dates = sorted(schedule_by_date.keys())
                time_sorter = {time: i for i, time in enumerate(time_slots.values())}
                for date in sorted_dates:
                    schedule_by_date[date].sort(key=lambda x: time_sorter.get(x['Time'], 99))

                # Fill in missing dates between first and last class date
                if sorted_dates:
                    first_date = sorted_dates[0]
                    last_date = sorted_dates[-1]
                    current_date = first_date
                    all_dates = []
                    
                    while current_date <= last_date:
                        all_dates.append(current_date)
                        current_date = date.fromordinal(current_date.toordinal() + 1)
                    
                    sorted_dates = all_dates

                today = datetime.now(pytz.timezone(TIMEZONE)).date()
                today_anchor_id = None
                
                for idx, date_obj in enumerate(sorted_dates):
                    is_today = (date_obj == today)
                    today_class = "today" if is_today else ""
                    card_id = f"date-card-{idx}"
                    
                    if is_today:
                        today_anchor_id = card_id
                    
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
                    
                    classes_today = schedule_by_date.get(date_obj, [])
                    
                    if not classes_today:
                        # No classes scheduled for this day
                        st.markdown('''
                            <div class="class-entry">
                                <div class="left">
                                    <div class="subject-name" style="color: var(--muted); font-style: italic;">No classes scheduled</div>
                                </div>
                                <div class="meta"><span class="time" style="color: var(--muted);">—</span></div>
                            </div>
                        ''', unsafe_allow_html=True)
                    else:
                        for class_info in classes_today:
                            meta_html = f'<div class="meta"><span class="time">{class_info["Time"]}</span><span class="venue">{class_info["Venue"]}</span><span class="faculty">{class_info["Faculty"]}</span></div>'
                            st.markdown(f'''
                                <div class="class-entry">
                                    <div class="left">
                                        <div class="subject-name">{class_info["Subject"]}</div>
                                    </div>
                                    {meta_html}
                                </div>
                            ''', unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                
                if today_anchor_id:
                    components.html(f"""
                    <script>
                        function scrollToToday() {{
                            const todayCard = window.parent.document.getElementById('{today_anchor_id}');
                            if (todayCard) {{
                                todayCard.scrollIntoView({{behavior: 'smooth', block: 'start'}});
                                return true;
                            }}
                            return false;
                        }}
                        
                        if (!scrollToToday()) {{
                            setTimeout(scrollToToday, 500);
                        }}
                        setTimeout(scrollToToday, 1500);
                    </script>
                    """, height=0)
            else:
                st.warning("No classes found for your registered sections in the master schedule.")
                
        # Handle invalid roll number
        else:
            st.error(f"Roll Number '{roll_to_process}' not found. Please check the number and try again.")
            st.session_state.submitted = False
            st.session_state.roll_number = ""
            st.rerun()

elif master_schedule_df.empty or not student_data_map:
    st.warning("Application is initializing or required data files are missing. Please wait or check the folder.")

# --- ADDED CAPTION AT THE VERY END ---
st.markdown("---")
st.caption("_Made by Vishesh_")


