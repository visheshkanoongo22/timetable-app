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
from streamlit_extras.st_keyup import st_keyup 
import gc 
import time 

# --- IMPORT DATA FROM EXTERNAL FILES ---
try:
    from day_overrides import DAY_SPECIFIC_OVERRIDES
except ImportError:
    DAY_SPECIFIC_OVERRIDES = {}

try:
    from additional_classes import ADDITIONAL_CLASSES
except ImportError:
    ADDITIONAL_CLASSES = []

try:
    from mess_menu import MESS_MENU
except ImportError:
    MESS_MENU = {}

# --- AUTO REFRESH EVERY 10 MINUTES ---
AUTO_REFRESH_INTERVAL = 10 * 60 

if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

elapsed = time.time() - st.session_state.start_time

if elapsed > AUTO_REFRESH_INTERVAL:
    with st.spinner("🔄 Refreshing app to keep it fast and stable..."):
        st.cache_data.clear()      
        st.cache_resource.clear()  
        gc.collect()
        st.session_state.clear() 
        time.sleep(2) 
        st.rerun()

if "run_counter" not in st.session_state:
    st.session_state.run_counter = 0
st.session_state.run_counter += 1

if st.session_state.run_counter % 100 == 0:
    st.cache_data.clear()      
    st.cache_resource.clear()  
    gc.collect()

# 2. CONFIGURATION
SCHEDULE_FILE_NAME = 'schedule.xlsx'
TIMEZONE = 'Asia/Kolkata'
GOOGLE_CALENDAR_IMPORT_LINK = 'https://calendar.google.com/calendar/u/0/r/settings/export'

# --- TERM 6 COURSE DETAILS ---
COURSE_DETAILS_MAP = {
    # Finance & Accounting
    'D&IT':     {'Faculty': 'Dhaval Patanvadia', 'Venue': 'T6'},
    'IF(A)':    {'Faculty': 'Parag Rijwani',     'Venue': 'T6'},
    'IF(B)':    {'Faculty': 'Parag Rijwani',     'Venue': 'T6'},
    'M&A(A)':   {'Faculty': 'Dipti Saraf',       'Venue': 'T5'},
    'M&A(B)':   {'Faculty': 'Dipti Saraf',       'Venue': 'T5'},
    'M&A(C)':   {'Faculty': 'Dipti Saraf',       'Venue': 'T5'},

    # Economics & Finance
    'PPC(A)':   {'Faculty': 'Ritesh Patel',      'Venue': 'T6'},
    'PPC(B)':   {'Faculty': 'Ritesh Patel',      'Venue': 'T6'},
    'PPC(C)':   {'Faculty': 'Ritesh Patel',      'Venue': 'T6'},

    # Marketing
    'MA':       {'Faculty': 'Jayesh Aagja',      'Venue': 'T6'},
    'CRM':      {'Faculty': 'T. S. Joshi',       'Venue': 'T6'},
    'RURMKT(A)': {'Faculty': 'Sapna Parshar',    'Venue': 'T6'},
    'RURMKT(B)': {'Faculty': 'Sapna Parshar',    'Venue': 'T6'},
    'IM':       {'Faculty': 'Pradeep Kautish',   'Venue': 'T6'},
    'MS(A)':    {'Faculty': 'Jayesh Aagja',      'Venue': 'T5'},
    'MS(B)':    {'Faculty': 'Jayesh Aagja',      'Venue': 'T5'},
    'MS(C)':    {'Faculty': 'Jayesh Aagja',      'Venue': 'T5'},
    'MS(D)':    {'Faculty': 'Jayesh Aagja',      'Venue': 'T5'},

    # HRM / OB & Communication
    'GBL':      {'Faculty': 'Sadhana Sargam',    'Venue': 'T5'},
    'DIW':      {'Faculty': 'Nitin Pillai',      'Venue': 'T5'},
    'PS&PS':    {'Faculty': 'Shilpa Tanna',      'Venue': 'E3'},

    # General Management
    'MC':       {'Faculty': 'VF',                'Venue': 'T3'},

    # DnA
    'FT(A)':    {'Faculty': 'Omkar Sahoo',       'Venue': 'T7'},
    'FT(B)':    {'Faculty': 'Omkar Sahoo',       'Venue': 'T7'},
    'SNA':      {'Faculty': 'Anand Kumar',       'Venue': 'T3'},
    'IGR&MC':   {'Faculty': 'Somayya Madakam',   'Venue': 'T6'},

    # OM&DS
    'PRM(A)':   {'Faculty': 'Chetan Jhaveri',    'Venue': 'T6'},
    'PRM(B)':   {'Faculty': 'Chetan Jhaveri',    'Venue': 'T6'},
    'IL(A)':    {'Faculty': 'Praneti Shah',      'Venue': 'T5'},
    'IL(B)':    {'Faculty': 'Praneti Shah',      'Venue': 'T5'}
}

# 3. FUNCTIONS
def normalize_string(text):
    """
    Strict normalization to ensure file headers match COURSE_DETAILS_MAP keys.
    """
    if isinstance(text, str):
        # Example: "RUR.MKT (A)" -> "RURMKT(A)"
        return text.replace(" ", "").replace("(", "").replace(")", "").replace("'", "").replace(".", "").upper()
    return ""

def clean_roll_number(roll):
    """Standardizes roll number format."""
    # Handle floats (e.g. 463.0) -> "463"
    if isinstance(roll, float):
        roll = int(roll)
    return str(roll).strip().upper()

@st.cache_data
def load_and_clean_schedule(file_path):
    try:
        # Assuming schedule format is consistent (Sheet 1, skip 3 rows)
        df = pd.read_excel(file_path, sheet_name=1, header=None, skiprows=3)
        schedule_df = df.iloc[:, 0:14].copy()
        schedule_df[0] = pd.to_datetime(schedule_df[0], errors='coerce').dt.date
        schedule_df.dropna(subset=[0], inplace=True)
        return schedule_df
    except FileNotFoundError:
        return pd.DataFrame()
    except Exception as e:
        return pd.DataFrame()

@st.cache_data
def get_all_student_data(folder_path='.'):
    """
    Robust parser for horizontal block layout.
    Scans for "Roll No" and looks for Subject Name in the row above.
    """
    student_data_map = {} # {RollNo: {'name': 'Name', 'sections': {Set of Courses}}}
    
    # Get all xlsx files excluding schedule
    files = [f for f in glob.glob(os.path.join(folder_path, '*.xlsx')) 
             if os.path.basename(f) != SCHEDULE_FILE_NAME 
             and not os.path.basename(f).startswith('~')]
    
    for file in files:
        try:
            # Read header=None to see the absolute layout
            df = pd.read_excel(file, header=None)
            
            # 1. Find the Header Row (containing "Roll No.")
            header_row_idx = -1
            for r in range(min(5, len(df))):
                row_values = [str(val).strip().lower() for val in df.iloc[r]]
                if any("roll no" in v for v in row_values):
                    header_row_idx = r
                    break
            
            if header_row_idx == -1:
                continue # Skip files without "Roll No"
                
            # 2. Find ALL columns in that row that contain "Roll No."
            roll_col_indices = []
            for c in range(df.shape[1]):
                val = str(df.iloc[header_row_idx, c]).strip().lower()
                if "roll no" in val:
                    roll_col_indices.append(c)
                    
            # 3. Process each block
            for roll_col in roll_col_indices:
                # A. Identify Section Name
                # It is in the row ABOVE the header (header_row_idx - 1)
                # It could be merged, so we check roll_col AND up to 2 cols to the LEFT
                
                raw_section_name = ""
                
                if header_row_idx > 0:
                    # Scan left to right in the row above, around the roll column
                    # Often merged cells put value in the leftmost column
                    # We check: roll_col-2, roll_col-1, roll_col
                    
                    found_header = False
                    start_search = max(0, roll_col - 2)
                    end_search = min(df.shape[1], roll_col + 2)
                    
                    for check_col in range(start_search, end_search):
                        val_above = str(df.iloc[header_row_idx-1, check_col]).strip()
                        if val_above and val_above.lower() != 'nan':
                            raw_section_name = val_above
                            found_header = True
                            # Prefer the value closest to the left if multiple exist (unlikely in merged header)
                            break 
                
                # B. Normalize and Match
                course_name = ""
                clean_header = normalize_string(raw_section_name)
                clean_filename = normalize_string(os.path.basename(file).replace('.xlsx', ''))

                # Logic: 
                # 1. If header has "Subject(Section)", use it.
                # 2. If header is just "(A)" or "Section A", combine with Filename base.
                # 3. If header is missing, use Filename.

                if clean_header:
                    # If header matches a known key (e.g. "M&A(A)"), use it directly
                    if clean_header in [normalize_string(k) for k in COURSE_DETAILS_MAP.keys()]:
                        course_name = clean_header
                    else:
                        # Header might be partial like "(A)"
                        # Try to extract just the section letter if present
                        if "(" in clean_header and ")" in clean_header:
                            # Trust the header if it looks like code
                            course_name = clean_header
                        else:
                            # Combine Filename Base + Header info? 
                            # Usually filename is "M&A(A)...". 
                            # If filename is specific, assume filename is the source of truth if header is ambiguous
                            if "(" in clean_filename and ")" in clean_filename:
                                # Filename is "M&A(A),M&A(B).xlsx". We can't use full filename.
                                # But if filename is single subject "CRM.xlsx", clean_filename is CRM.
                                pass
                            
                            course_name = clean_header # Default to what we found
                else:
                    course_name = clean_filename
                
                # Cleanup: remove dot if needed (RUR.MKT -> RURMKT)
                course_name = course_name.replace("RURMKT", "RURMKT") # Already normalized but just in case
                
                # C. Extract Students
                name_col = roll_col + 1 # Name is strictly next to Roll No
                
                start_row = header_row_idx + 1
                for r in range(start_row, len(df)):
                    roll_val = df.iloc[r, roll_col]
                    name_val = df.iloc[r, name_col]
                    
                    clean_roll = str(roll_val).strip().upper()
                    
                    if clean_roll == 'NAN' or clean_roll == '' or clean_roll == 'NONE':
                        continue
                        
                    if clean_roll.replace('.','',1).isdigit():
                        clean_roll = str(int(float(clean_roll)))
                    
                    if len(clean_roll) < 2: 
                        continue

                    if clean_roll not in student_data_map:
                        student_data_map[clean_roll] = {'name': 'Student', 'sections': set()}
                    
                    student_data_map[clean_roll]['sections'].add(course_name)
                    
                    clean_name = str(name_val).strip()
                    if clean_name and clean_name.lower() != 'nan':
                         student_data_map[clean_roll]['name'] = clean_name
                        
        except Exception as e:
            continue
            
    return student_data_map

def get_class_end_datetime(class_info, local_tz):
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
    page_title="MBA Timetable Assistant - Term 6", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)
st.markdown("""
    <meta name="color-scheme" content="dark">
    <meta name="theme-color" content="#0F172A">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
""", unsafe_allow_html=True)

local_css_string = """
<style>
    * { color-scheme: dark !important; }
    html, body { background-color: var(--bg) !important; }
    [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {
        background-color: var(--bg) !important; color: #ffffff !important;
    }
    [data-testid="stHeader"] { display: none; visibility: hidden; height: 0; }
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
    .main-header { font-size: 2.4rem; font-weight: 800; text-align: center; margin-bottom: 0.5rem; }
    .header-sub { text-align:center; color:var(--muted); margin-top:0rem; margin-bottom:2rem; font-size:1.0rem; }
    .welcome-box {
        background: var(--card); border: 1px solid var(--glass-border); padding: 1rem 1.25rem;
        border-radius: 14px; margin-bottom: 1.5rem; color: var(--muted); font-size: 0.95rem;
    }
    .welcome-box strong { color: #ffffff; font-weight: 600; }
    .welcome-message { margin-top: 0rem; margin-bottom: 1rem; font-size: 1.1rem; color: var(--muted); }
    .welcome-message strong { color: #ffffff; }
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
    .strikethrough { text-decoration: line-through; opacity: 0.6; }
    .stDownloadButton>button, div[data-testid="stForm"] button[kind="primary"], .stButton>button {
        background: linear-gradient(90deg, var(--accent-start), var(--accent-end)); color: var(--bg);
        font-weight:700; padding: 0.5rem 0.9rem; border-radius:10px; border:none;
        box-shadow: 0 8px 20px rgba(96,165,250,0.1); width: 100%;
        transition: transform 0.18s ease, box-shadow 0.18s ease;
    }
    .stDownloadButton>button:hover, div[data-testid="stForm"] button[kind="primary"]:hover, .stButton>button:hover {
        transform: translateY(-3px); box-shadow: 0 14px 30px rgba(96,165,250,0.15);
    }
    .stButton>button {
        width: auto; padding: 0.25rem 0.6rem; font-size: 0.8rem;
        background: var(--card); color: var(--muted); border: 1px solid var(--glass-border);
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
    @media (max-width: 600px) {
        .day-card { padding: 0.8rem; margin-bottom: 1rem; }
        .results-container { padding: 0.8rem; }
        .main-header { font-size: 1.6rem; }
        .header-sub { font-size: 0.8rem; margin-bottom: 1.5rem; }
        .day-header { font-size: 0.9rem; }
        .subject-name { font-size: 0.9rem; }
        .meta .time { font-size: 0.85rem; }
        .meta .venue, .meta .faculty { font-size: 0.75rem; }
        .class-entry { padding-top: 0.5rem; padding-bottom: 0.5rem; }
        .meta { min-width: 120px; font-size: 0.85rem; }
        .stDownloadButton>button, div[data-testid="stForm"] button[kind="primary"], .stButton>button {
            padding: 0.4rem 0.8rem; font-size: 0.9rem;
        }
        .stButton>button { padding: 0.25rem 0.6rem; font-size: 0.8rem; }
    }
</style>
"""
st.markdown(local_css_string, unsafe_allow_html=True)

if 'submitted' not in st.session_state:
    st.session_state.submitted = False
if 'roll_number' not in st.session_state:
    st.session_state.roll_number = ""
if 'search_clear_counter' not in st.session_state:
    st.session_state.search_clear_counter = 0
if 'just_submitted' not in st.session_state: 
    st.session_state.just_submitted = False

if not st.session_state.submitted:
    st.markdown('<p class="main-header">MBA Timetable Assistant</p>', unsafe_allow_html=True)
    st.markdown('<div class="header-sub">Term 6 Schedule</div>', unsafe_allow_html=True)

# --- DYNAMIC DATA LOADING ---
student_data_map = get_all_student_data()

if not student_data_map:
    st.markdown('<p class="main-header">MBA Timetable Assistant</p>', unsafe_allow_html=True)
    st.markdown('<div class="header-sub">Course Statistics & Schedule Tool</div>', unsafe_allow_html=True)
    st.error("FATAL ERROR: Could not load any student data. Please check that your subject Excel files are in the directory.")
else:
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
            roll_number_input = st.text_input("Enter your Roll Number:", placeholder="e.g., 463 (Just the last 3 digits)").strip().upper()
            submitted_button = st.form_submit_button("Generate Timetable")
            
            if submitted_button:
                final_roll = roll_number_input
                if roll_number_input.isdigit():
                    val = int(roll_number_input)
                    if 0 <= val < 100:
                        final_roll = f"21BCM{roll_number_input}"
                    elif 100 <= val <= 999:
                        final_roll = f"24MBA{roll_number_input}"
                
                st.session_state.roll_number = final_roll
                st.session_state.submitted = True
                st.session_state.just_submitted = True 
                st.rerun()
        
        render_mess_menu_expander()
        calculate_and_display_stats()

    else:
        roll_to_process = st.session_state.roll_number
        
        if not roll_to_process:
            st.session_state.submitted = False
            st.rerun()
        elif roll_to_process not in student_data_map:
            st.error(f"Roll Number '{roll_to_process}' not found. Please check the number and try again.")
            if st.button("Go Back"):
                st.session_state.submitted = False
                st.session_state.roll_number = ""
                st.rerun()
        else:
            student_info = student_data_map[roll_to_process]
            student_name = student_info['name']
            student_sections = student_info['sections'] # This is now a Set of Course Names
            
            master_schedule_df = load_and_clean_schedule(SCHEDULE_FILE_NAME)
            
            if master_schedule_df.empty:
                st.error("Could not load the Master Schedule file.")
            else:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"""
                    <div class="welcome-message">
                        Displaying schedule for: <strong>{roll_to_process}</strong>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    if st.button("Change Roll Number"):
                        st.session_state.submitted = False
                        st.session_state.roll_number = ""
                        st.session_state.search_clear_counter = 0 
                        st.session_state.just_submitted = False 
                        st.rerun()
                
                with st.spinner(f'Compiling classes for {student_name}...'):
                    # Create normalized map for easy lookup
                    NORMALIZED_COURSE_DETAILS_MAP = {normalize_string(section): details for section, details in COURSE_DETAILS_MAP.items()}
                    
                    # Create a normalized set of the student's registered courses
                    normalized_student_courses = {normalize_string(sec): sec for sec in student_sections}
                    
                    time_slots = {2: "8-9AM", 3: "9:10-10:10AM", 4: "10:20-11:20AM", 5: "11:30-12:30PM",
                                  6: "12:30-1:30PM", 7: "1:30-2:30PM", 8: "2:40-3:40PM", 9: "3:50-4:50PM",
                                  10: "5-6PM", 11: "6:10-7:10PM", 12: "7:20-8:20PM", 13: "8:30-9:30PM"}
                    
                    found_classes = []
                    
                    for index, row in master_schedule_df.iterrows():
                        date, day = row[0], row[1]
                        
                        for col_index, time in time_slots.items():
                            cell_value = str(row[col_index])
                            if cell_value and cell_value != 'nan':
                                # Split by '/' to handle merged cells if any (e.g., "FT(A) / FT(B)")
                                cell_parts = cell_value.split('/')
                                
                                for part in cell_parts:
                                    normalized_cell_part = normalize_string(part)
                                    
                                    # Check if this part matches any of the student's courses
                                    matched_course_norm = None
                                    
                                    # 1. Exact match check
                                    if normalized_cell_part in normalized_student_courses:
                                        matched_course_norm = normalized_cell_part
                                    else:
                                        # 2. Substring check (safer for things like "FT(A)" matching "FT(A)")
                                        for s_norm in normalized_student_courses.keys():
                                            if s_norm == normalized_cell_part:
                                                matched_course_norm = s_norm
                                                break
                                    
                                    if matched_course_norm:
                                        orig_sec = normalized_student_courses[matched_course_norm]
                                        details = NORMALIZED_COURSE_DETAILS_MAP.get(matched_course_norm, {'Faculty': 'N/A', 'Venue': '-'}).copy()
                                        is_venue_override = False
                                        
                                        # Check Day Overrides
                                        if date in DAY_SPECIFIC_OVERRIDES:
                                            if matched_course_norm in DAY_SPECIFIC_OVERRIDES[date]:
                                                override_data = DAY_SPECIFIC_OVERRIDES[date][matched_course_norm]
                                                
                                                should_apply_override = True
                                                if 'Target_Time' in override_data:
                                                    if override_data['Target_Time'] != time:
                                                        should_apply_override = False
                                                
                                                if should_apply_override:
                                                    if 'Venue' in override_data:
                                                        is_venue_override = True
                                                    details.update(override_data)
                                        
                                        found_classes.append({
                                            "Date": date, "Day": day, 
                                            "Time": details.get('Time', time),
                                            "Subject": orig_sec,
                                            "Faculty": details.get('Faculty', 'N/A'),
                                            "Venue": details.get('Venue', '-'),
                                            "is_venue_override": is_venue_override
                                        })
                    
                    # Add Additional Classes
                    for added_class in ADDITIONAL_CLASSES:
                        norm_added_subject = normalize_string(added_class['Subject'])
                        
                        # Only add if the student is registered for this subject
                        # OR if it matches a registered subject (fuzzy match)
                        is_relevant = False
                        if norm_added_subject in normalized_student_courses:
                            is_relevant = True
                        
                        if is_relevant:
                            venue_text = added_class.get('Venue', '').upper()
                            faculty_text = added_class.get('Faculty', '').upper()
                            is_override = False 
                            
                            if ("POSTPONED" in venue_text or "POSTPONED" in faculty_text or
                                "CANCELLED" in venue_text or "CANCELLED" in faculty_text or
                                "PREPONED" in venue_text or "PREPONED" in faculty_text or
                                "(RESCHEDULED)" in venue_text or "(PREPONED)" in venue_text):
                                is_override = False # It is an override but we don't skip it, just style it

                            day_of_week = added_class['Date'].strftime('%A')
                            found_classes.append({
                                "Date": added_class['Date'], "Day": day_of_week, "Time": added_class['Time'],
                                "Subject": added_class['Subject'], 
                                "Faculty": added_class.get('Faculty', 'N/A'),
                                "Venue": added_class.get('Venue', '-'), 
                                "is_venue_override": is_override 
                            })

                    # Remove duplicates
                    found_classes = [dict(t) for t in {tuple(d.items()) for d in found_classes}]
                    
                if found_classes:
                    ics_content = generate_ics_content(found_classes)
                    sanitized_name = re.sub(r'[^a-zA-Z0-9_]', '', str(student_name).replace(" ", "_")).upper()
                    
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
                    
                    def get_sort_key(class_item):
                        time_str = class_item['Time'].upper()
                        try:
                            start_part = time_str.split('-')[0].strip()
                            if ':' in start_part:
                                h_str, m_str = start_part.split(':')
                                h = int(re.search(r'\d+', h_str).group())
                                m = int(re.search(r'\d+', m_str).group())
                            else:
                                h = int(re.search(r'\d+', start_part).group())
                                m = 0
                            
                            if h < 8: h += 12
                            elif h in [8, 9, 10] and "PM" in time_str and "AM" not in time_str:
                                h += 12
                            return h * 60 + m
                        except:
                            return 9999

                    for date in sorted_dates:
                        schedule_by_date[date].sort(key=get_sort_key)
                    
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

                    with st.expander("Show Previous Classes"):
                        search_query = st_keyup(
                            label=None,
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
                                continue 
                            
                            st.markdown(f'''
                                <div class="day-card" id="date-card-past-{date_obj.toordinal()}">
                                    <div class="day-header">
                                        {date_obj.strftime("%d %B %Y, %A")}
                                    </div>
                            ''', unsafe_allow_html=True)
                            
                            for class_info in classes_today:
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

                    st.markdown('<div id="search-anchor-div"></div>', unsafe_allow_html=True)

                    if not upcoming_dates:
                         st.markdown('<p style="color: var(--muted); font-style: italic;">No upcoming classes found.</p>', unsafe_allow_html=True)

                    for idx, date_obj in enumerate(upcoming_dates):
                        is_today = (date_obj == today)
                        today_class = "today" if is_today else ""
                        card_id = f"date-card-{idx}"
                        
                        if is_today: 
                            today_anchor_id = card_id
                        
                        classes_today = schedule_by_date.get(date_obj, [])
                        
                        if not classes_today:
                            st.markdown(f'''
                                <div class="day-card {today_class}" id="{card_id}">
                                    <div class="day-header">
                                        {date_obj.strftime("%d %B %Y, %A")}
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
                            if is_today:
                                st.markdown(f'''
                                    <div class="day-card {today_class}" id="{card_id}">
                                        <div class="today-badge">TODAY</div>
                                        <div class="day-header">
                                            {date_obj.strftime("%d %B %Y, %A")}
                                        </div>
                                ''', unsafe_allow_html=True)
                            else:
                                st.markdown(f'''
                                    <div class="day-card {today_class}" id="{card_id}">
                                        <div class="day-header">
                                            {date_obj.strftime("%d %B %Y, %A")}
                                        </div>
                                ''', unsafe_allow_html=True)

                            for class_info in classes_today:
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
                    
                else:
                    st.warning("No classes found for your registered sections in the master schedule.")
            
st.markdown("---")
st.caption("_Made by Vishesh_")
