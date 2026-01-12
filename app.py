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

# --- 1. MEMORY SAFETY ---
# Clear RAM immediately to prevent inheritance of garbage data
if 'has_cleaned_memory' not in st.session_state:
    gc.collect()
    st.session_state.has_cleaned_memory = True

# --- 2. CONFIGURATION ---
SCHEDULE_FILE_NAME = 'schedule.xlsx' 
TIMEZONE = 'Asia/Kolkata'
GOOGLE_CALENDAR_IMPORT_LINK = 'https://calendar.google.com/calendar/u/0/r/settings/export'

# --- TERM 6 COURSE DETAILS ---
COURSE_DETAILS_MAP = {
    'D&IT':     {'Faculty': 'Dhaval Patanvadia', 'Venue': 'T6'},
    'IF(A)':    {'Faculty': 'Parag Rijwani',     'Venue': 'T6'},
    'IF(B)':    {'Faculty': 'Parag Rijwani',     'Venue': 'T6'},
    'M&A(A)':   {'Faculty': 'Dipti Saraf',       'Venue': 'T5'},
    'M&A(B)':   {'Faculty': 'Dipti Saraf',       'Venue': 'T5'},
    'M&A(C)':   {'Faculty': 'Dipti Saraf',       'Venue': 'T5'},
    'PPC(A)':   {'Faculty': 'Ritesh Patel',      'Venue': 'T3'},
    'PPC(B)':   {'Faculty': 'Ritesh Patel',      'Venue': 'T3'},
    'PPC(C)':   {'Faculty': 'Ritesh Patel',      'Venue': 'T3'},
    'MA':       {'Faculty': 'Jayesh Aagja / Sanjay Jain', 'Venue': 'T6'},
    'CRM':      {'Faculty': 'T. S. Joshi',       'Venue': 'T6'},
    'RURMKT(A)': {'Faculty': 'Sapna Parshar / Shailesh Prabhu', 'Venue': 'T6'},
    'RURMKT(B)': {'Faculty': 'Sapna Parshar / Kavita Saxena',   'Venue': 'T6'},
    'IM':       {'Faculty': 'Pradeep Kautish',   'Venue': 'T6'},
    'MS(A)':    {'Faculty': 'Ashwini Awasthi',   'Venue': 'T6'},
    'MS(B)':    {'Faculty': 'Ashwini Awasthi',   'Venue': 'T6'},
    'MS(C)':    {'Faculty': 'Jayesh Aagja',      'Venue': 'T5'},
    'MS(D)':    {'Faculty': 'Sanjay Jain',       'Venue': 'T5'},
    'GBL':      {'Faculty': 'Sadhana Sargam',    'Venue': 'T5'},
    'DIW':      {'Faculty': 'Nitin Pillai',      'Venue': 'T5'},
    'PS&PS':    {'Faculty': 'Shilpa Tanna',      'Venue': 'E3'},
    'MC':       {'Faculty': 'VF',                'Venue': 'T3'},
    'FT(A)':    {'Faculty': 'Omkar Sahoo',       'Venue': 'T7'},
    'FT(B)':    {'Faculty': 'Omkar Sahoo',       'Venue': 'T7'},
    'SNA':      {'Faculty': 'Anand Kumar',       'Venue': 'T3'},
    'IGR&MC':   {'Faculty': 'Somayya Madakam',   'Venue': 'T6'},
    'PRM(A)':   {'Faculty': 'Chetan Jhaveri',    'Venue': 'T6'},
    'PRM(B)':   {'Faculty': 'Chetan Jhaveri',    'Venue': 'T6'},
    'IL(A)':    {'Faculty': 'Praneti Shah',      'Venue': 'T5'},
    'IL(B)':    {'Faculty': 'Praneti Shah',      'Venue': 'T5'}
}

# --- OPTIONAL IMPORTS ---
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

# --- 3. CORE FUNCTIONS ---
def normalize_string(text):
    if isinstance(text, str):
        return text.replace(" ", "").replace("'", "").replace(".", "").upper()
    return ""

@st.cache_resource(show_spinner="Initializing student database...", ttl=3600)
def build_master_index(folder_path='.'):
    """
    SINGLETON DATABASE: Reads all files ONCE and saves to RAM.
    This prevents the "Too many open files" crash.
    """
    master_index = {}
    search_path = os.path.join(folder_path, '*.xlsx')
    files = [f for f in glob.glob(search_path) 
             if os.path.basename(f) != 'schedule.xlsx' 
             and not os.path.basename(f).startswith('~')]

    if not files: return {}

    for file in files:
        try:
            with pd.ExcelFile(file) as xls:
                df = pd.read_excel(xls, header=None)

            # Find Header
            header_row_idx = -1
            for r in range(min(20, len(df))):
                row_values = [str(val).strip().lower() for val in df.iloc[r]]
                if any("roll no" in v for v in row_values):
                    header_row_idx = r
                    break
            
            if header_row_idx == -1: continue

            # Find Roll Columns
            roll_col_indices = []
            for c in range(df.shape[1]):
                val = str(df.iloc[header_row_idx, c]).strip().lower()
                if "roll no" in val:
                    roll_col_indices.append(c)

            # Process Each Block
            for roll_col in roll_col_indices:
                name_col = roll_col + 1
                
                # Identify Subject Name
                raw_section_name = ""
                if header_row_idx > 0:
                    start_search = max(0, roll_col - 2)
                    end_search = min(df.shape[1], roll_col + 3)
                    for check_col in range(start_search, end_search):
                        val_above = str(df.iloc[header_row_idx-1, check_col]).strip()
                        if val_above and val_above.lower() != 'nan':
                            raw_section_name = val_above
                            break 
                
                # Normalize Subject
                clean_header = normalize_string(raw_section_name)
                clean_filename = normalize_string(os.path.basename(file).replace('.xlsx', ''))
                
                course_name = clean_filename 
                if clean_header:
                    if clean_header in [normalize_string(k) for k in COURSE_DETAILS_MAP.keys()]:
                        course_name = clean_header
                    elif "(" in clean_header:
                        course_name = clean_header
                course_name = course_name.replace("RURMKT", "RURMKT")

                # Extract Student
                if name_col < df.shape[1]:
                    data_block = df.iloc[header_row_idx+1:, [roll_col, name_col]]
                else:
                    data_block = df.iloc[header_row_idx+1:, [roll_col]]
                    data_block['Name'] = "Student"

                for _, row in data_block.iterrows():
                    raw_roll = str(row.iloc[0]).strip().upper()
                    if raw_roll == 'NAN' or not raw_roll: continue
                    r_val = raw_roll.split('.')[0]
                    
                    if len(data_block.columns) > 1:
                        n_val = str(row.iloc[1]).strip()
                    else:
                        n_val = "Student"

                    if r_val not in master_index:
                        master_index[r_val] = {'Name': "Student", 'Subjects': set()}
                    master_index[r_val]['Subjects'].add(course_name)
                    if n_val and n_val.lower() != 'nan':
                        master_index[r_val]['Name'] = n_val
            
            del df
        except Exception:
            continue
            
    gc.collect()
    return master_index

def find_subjects_for_roll(target_roll, folder_path='.'):
    """Fast Fuzzy Search"""
    try:
        master_index = build_master_index(folder_path)
    except Exception:
        return "System Busy", set()

    target_clean = str(target_roll).strip().upper()
    
    # Direct Match
    if target_clean in master_index:
        data = master_index[target_clean]
        return data['Name'], data['Subjects']
    
    # Fuzzy Match
    for db_roll, data in master_index.items():
        if target_clean in db_roll or db_roll in target_clean:
            # Suffix check to ensure "463" matches "24MBA463" but "24" doesn't
            if db_roll.endswith(target_clean) or target_clean.endswith(db_roll):
                return data['Name'], data['Subjects']

    return "Student", set()

@st.cache_data
def load_and_clean_schedule(file_path):
    try:
        df = pd.read_excel(file_path, sheet_name=1, header=None, skiprows=3)
        schedule_df = df.iloc[:, 0:14].copy()
        schedule_df[0] = pd.to_datetime(schedule_df[0], errors='coerce').dt.date
        schedule_df.dropna(subset=[0], inplace=True)
        return schedule_df
    except Exception:
        return pd.DataFrame()

# --- HELPER: PARSE CLASS TIMES ---
def parse_class_times(time_str, date_obj, local_tz):
    try:
        start_str_part, end_str_part = time_str.split('-')
        start_str_part = start_str_part.strip()
        end_str_part = end_str_part.strip()
        end_am_pm = end_str_part[-2:].upper()
        
        start_match = re.search(r'^\d+', start_str_part)
        end_match = re.search(r'^\d+', end_str_part)
        if not start_match or not end_match: return None, None
        
        start_hour = int(start_match.group(0))
        end_hour = int(end_match.group(0))
        
        start_am_pm = end_am_pm 
        if end_am_pm == "PM" and start_hour < 12 and (start_hour == 11 or start_hour <= 10):
               start_am_pm = "AM"

        full_start_str = f"{start_str_part}{start_am_pm}" if not start_str_part[-2:].isalpha() else start_str_part
        start_dt = local_tz.localize(pd.to_datetime(f"{date_obj.strftime('%Y-%m-%d')} {full_start_str}"))
        end_dt = local_tz.localize(pd.to_datetime(f"{date_obj.strftime('%Y-%m-%d')} {end_str_part}"))
        return start_dt,

# ... [PASTE THIS AFTER THE PREVIOUS CODE BLOCK] ...

def render_mess_menu_expander():
    try:
        menu_source = MESS_MENU if 'MESS_MENU' in globals() else {}
    except ImportError: return 

    local_tz = pytz.timezone(TIMEZONE)
    now_dt = datetime.now(local_tz)
    today = now_dt.date()
    
    # Logic: Show today unless it's late night (after 11 PM), then show tomorrow
    start_date = today 
    if now_dt.hour >= 23:
        start_date = today + pd.Timedelta(days=1)

    # Get valid dates for the next 7 days
    week_dates = [start_date + pd.Timedelta(days=i) for i in range(7)]
    valid_dates = [d for d in week_dates if d in menu_source]
    
    if not valid_dates: return 

    options = []
    default_index = 0
    for idx, d in enumerate(valid_dates):
        label = d.strftime("%d %b") 
        if d == today:
            label += " (Today)"
            default_index = idx
        elif d == today + pd.Timedelta(days=1):
            label += " (Tomorrow)"
        options.append(label)

    with st.expander("🍽️ Mess Menu for the Week", expanded=False):
        selected_label = st.radio("Select a day:", options, index=default_index, horizontal=True)
        selected_idx = options.index(selected_label)
        selected_date = valid_dates[selected_idx]
        menu_data = menu_source[selected_date]

        st.markdown(f"**Menu for {selected_date.strftime('%d %B %Y')}**")
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.markdown(f"**Breakfast**\n{menu_data.get('Breakfast', '-')}")
        with c2: st.markdown(f"**Lunch**\n{menu_data.get('Lunch', '-')}")
        with c3: st.markdown(f"**Hi-Tea**\n{menu_data.get('Hi-Tea', '-')}")
        with c4: st.markdown(f"**Dinner**\n{menu_data.get('Dinner', '-')}")

# --- HELPER: ICS GENERATION ---
def generate_ics_content(found_classes):
    c = Calendar(creator="-//Timetable App//EN")
    local_tz = pytz.timezone(TIMEZONE)
    for class_info in found_classes:
        # Skip cancelled classes
        venue = class_info.get('Venue', '').upper()
        if "CANCELLED" in venue or "POSTPONED" in venue: continue

        try:
            time_str = class_info['Time']
            start_dt, end_dt = parse_class_times(time_str, class_info['Date'], local_tz)
            if not start_dt or not end_dt: continue
            
            e = Event()
            e.name = class_info['Subject']
            e.begin = start_dt.astimezone(pytz.utc)
            e.end = end_dt.astimezone(pytz.utc)
            e.location = class_info.get('Venue', 'TBA')
            e.description = f"Faculty: {class_info.get('Faculty', 'N/A')}"
            c.events.add(e)
        except Exception:
            continue
    return c.serialize()

# --- 4. MAIN APP UI ---
st.set_page_config(page_title="MBA Timetable", layout="centered", initial_sidebar_state="collapsed")

# Simple Dark Mode CSS
st.markdown("""
<style>
    .stApp { background-color: #0F172A; color: white; }
    .stTextInput input { background-color: #1E293B; color: white; border: 1px solid #334155; }
    .day-card { background: #1E293B; padding: 15px; border-radius: 10px; margin-bottom: 10px; border: 1px solid #334155; }
    .day-card.today { border: 2px solid #38BDF8; box-shadow: 0 0 10px rgba(56, 189, 248, 0.3); }
    .subject { font-weight: bold; font-size: 1.1em; color: white; }
    .meta { color: #94A3B8; font-size: 0.9em; }
    .venue-change { color: #F87171; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

if 'submitted' not in st.session_state: st.session_state.submitted = False
if 'roll_number' not in st.session_state: st.session_state.roll_number = ""

# --- A. LANDING PAGE ---
if not st.session_state.submitted:
    st.title("MBA Timetable Assistant")
    st.caption("Term 6 Schedule")
    
    with st.form("roll_form"):
        roll_in = st.text_input("Enter Roll Number (e.g., 463):").strip().upper()
        if st.form_submit_button("View Schedule"):
            if len(roll_in) < 3:
                st.error("Please enter a valid roll number.")
            else:
                st.session_state.roll_number = roll_in
                st.session_state.submitted = True
                st.rerun()

    render_mess_menu_expander()

# --- B. SCHEDULE DASHBOARD ---
else:
    roll = st.session_state.roll_number
    
    # Header with Back Button
    c1, c2 = st.columns([3, 1])
    with c1: st.subheader(f"Schedule: {roll}")
    with c2: 
        if st.button("Change Roll"):
            st.session_state.submitted = False
            st.rerun()

    # --- THE SEARCH (Safe & Cached) ---
    with st.spinner("Fetching data..."):
        name, subjects = find_subjects_for_roll(roll)

    if not subjects:
        st.error(f"Roll number '{roll}' not found in the database.")
        st.info("Try checking the full ID (e.g., 24MBA463) or ensure your Excel files are uploaded.")
    else:
        # Load Schedule File
        schedule_df = load_and_clean_schedule(SCHEDULE_FILE_NAME)
        if schedule_df.empty:
            st.error("Schedule file missing. Please upload 'schedule.xlsx'.")
        else:
            # --- PROCESS SCHEDULE ---
            found_classes = []
            normalized_subjects = {normalize_string(s): s for s in subjects}
            
            # Map of column index to Time Slot
            time_slots = {2: "8-9AM", 3: "9:10-10:10AM", 4: "10:20-11:20AM", 5: "11:30-12:30PM",
                          6: "12:30-1:30PM", 7: "1:30-2:30PM", 8: "2:40-3:40PM", 9: "3:50-4:50PM",
                          10: "5-6PM", 11: "6:10-7:10PM", 12: "7:20-8:20PM", 13: "8:30-9:30PM"}

            # Scan Master Schedule
            for idx, row in schedule_df.iterrows():
                row_date, day_name = row[0], row[1]
                
                for col_idx, time_str in time_slots.items():
                    cell_val = str(row[col_idx])
                    if not cell_val or cell_val.lower() == 'nan': continue
                    
                    # Handle Merged Cells (Subject1 / Subject2)
                    parts = cell_val.split('/')
                    for part in parts:
                        norm_part = normalize_string(part)
                        
                        # Check if student has this subject
                        matched_subj = None
                        if norm_part in normalized_subjects:
                            matched_subj = normalized_subjects[norm_part]
                        else:
                            # Fuzzy Match for things like "FT(A)"
                            for s_norm in normalized_subjects.keys():
                                if s_norm in norm_part:
                                    matched_subj = normalized_subjects[s_norm]
                                    break
                        
                        if matched_subj:
                            # Default Details
                            details = {'Venue': '-', 'Faculty': 'N/A'}
                            norm_key = normalize_string(matched_subj)
                            for k, v in COURSE_DETAILS_MAP.items():
                                if normalize_string(k) == norm_key:
                                    details = v.copy()
                                    break
                            
                            # Check Overrides
                            is_override = False
                            if row_date in DAY_SPECIFIC_OVERRIDES:
                                # Check logic for exact subject match in overrides
                                for override_subj, override_data in DAY_SPECIFIC_OVERRIDES[row_date].items():
                                    if normalize_string(override_subj) == norm_key:
                                        details.update(override_data)
                                        if 'Venue' in override_data: is_override = True
                            
                            found_classes.append({
                                'Date': row_date, 'Day': day_name, 'Time': time_str,
                                'Subject': matched_subj, 'Venue': details['Venue'],
                                'Faculty': details['Faculty'], 'Override': is_override
                            })

            # Add Additional Classes
            for ac in ADDITIONAL_CLASSES:
                norm_ac = normalize_string(ac['Subject'])
                if any(norm_ac in normalize_string(s) for s in subjects):
                    found_classes.append({
                        'Date': ac['Date'], 'Day': ac['Date'].strftime("%A"), 'Time': ac['Time'],
                        'Subject': ac['Subject'], 'Venue': ac.get('Venue', '-'),
                        'Faculty': ac.get('Faculty', '-'), 'Override': False
                    })

            # Remove Duplicates
            found_classes = [dict(t) for t in {tuple(d.items()) for d in found_classes}]
            
            # Sort by Date & Time
            def sort_key(x):
                t_str = x['Time'].split('-')[0]
                h = int(re.search(r'\d+', t_str).group())
                if "PM" in x['Time'] and h < 12: h += 12
                return (x['Date'], h)
            
            found_classes.sort(key=sort_key)

            # --- RENDER CARDS ---
            today = date.today()
            upcoming = [c for c in found_classes if c['Date'] >= today]
            
            if not upcoming:
                st.info("No upcoming classes found.")
            else:
                for c in upcoming:
                    is_today = (c['Date'] == today)
                    css_class = "today" if is_today else ""
                    
                    venue_style = 'venue-change' if c['Override'] else ''
                    venue_text = c['Venue']
                    
                    st.markdown(f"""
                    <div class="day-card {css_class}">
                        <div style="display:flex; justify-content:space-between;">
                            <div>
                                <div class="meta">{c['Date'].strftime('%d %b, %a')} • {c['Time']}</div>
                                <div class="subject">{c['Subject']}</div>
                                <div class="meta">Prof. {c['Faculty']}</div>
                            </div>
                            <div style="text-align:right;">
                                <div class="meta">Venue</div>
                                <div class="{venue_style}">{venue_text}</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
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

# --- UI START ---
if not st.session_state.submitted:
    st.markdown('<p class="main-header">MBA Timetable Assistant</p>', unsafe_allow_html=True)
    st.markdown('<div class="header-sub"> Your Term VI Schedule</div>', unsafe_allow_html=True)

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
    # --- DASHBOARD PAGE ---
    roll_to_process = st.session_state.roll_number
    
    if not roll_to_process:
        st.session_state.submitted = False
        st.rerun()
    
    # LAZY LOADING: Only load specific student data NOW
    student_name = "Student"
    student_sections = set()
    
# Ensure this runs once per submission
    if st.session_state.just_submitted:
        # --- UI CHANGE: Sleek Spinner instead of Progress Bar ---
        with st.spinner("Finding your schedule..."):
            found_name, found_sections = find_subjects_for_roll(roll_to_process)
            
        if not found_sections:
            st.error(f"Roll Number '{roll_to_process}' not found. Please check the number and try again.")
            if st.button("Go Back"):
                st.session_state.submitted = False
                st.session_state.roll_number = ""
                st.rerun()
            st.stop() # Stop execution here
        else:
            # Store in session state to avoid re-searching on refresh
            st.session_state.student_name = found_name
            st.session_state.student_sections = found_sections
            st.session_state.just_submitted = False
    
    # Retrieve from session state
    if 'student_sections' in st.session_state:
        student_name = st.session_state.student_name
        student_sections = st.session_state.student_sections
        
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
                    if 'student_sections' in st.session_state:
                        del st.session_state.student_sections
                    st.rerun()
            
            with st.spinner(f'Compiling classes for {student_name}...'):
                # Create normalized map for easy lookup
                NORMALIZED_COURSE_DETAILS_MAP = {normalize_string(section): details for section, details in COURSE_DETAILS_MAP.items()}
                
                # Create a normalized set of the student's registered courses
                normalized_student_courses = {normalize_string(sec): sec for sec in student_sections}
                
                time_slots = {2: "8-9 AM", 3: "9:10-10:10 AM", 4: "10:20-11:20 AM", 5: "11:30-12:30 PM",
                              6: "12:30-1:30 PM", 7: "1:30-2:30 PM", 8: "2:40-3:40 PM", 9: "3:50-4:50 PM",
                              10: "5-6 PM", 11: "6:10-7:10 PM", 12: "7:20-8:20 PM", 13: "8:30-9:30 PM"}
                
                found_classes = []
                
                for index, row in master_schedule_df.iterrows():
                    row_date, day = row[0], row[1] # <--- FIXED VARIABLE SHADOWING
                    
                    for col_index, slot_time in time_slots.items(): # <--- FIXED VARIABLE SHADOWING
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
                                    if row_date in DAY_SPECIFIC_OVERRIDES:
                                        if matched_course_norm in DAY_SPECIFIC_OVERRIDES[row_date]:
                                            override_data = DAY_SPECIFIC_OVERRIDES[row_date][matched_course_norm]
                                            
                                            should_apply_override = True
                                            if 'Target_Time' in override_data:
                                                if override_data['Target_Time'] != slot_time:
                                                    should_apply_override = False
                                            
                                            if should_apply_override:
                                                if 'Venue' in override_data:
                                                    is_venue_override = True
                                                details.update(override_data)
                                    
                                    found_classes.append({
                                        "Date": row_date, "Day": day, 
                                        "Time": details.get('Time', slot_time),
                                        "Subject": orig_sec,
                                        "Faculty": details.get('Faculty', 'N/A'),
                                        "Venue": details.get('Venue', '-'),
                                        "is_venue_override": is_venue_override
                                    })
                
                # Add Additional Classes
                for added_class in ADDITIONAL_CLASSES:
                    norm_added_subject = normalize_string(added_class['Subject'])
                    
                    # Only add if the student is registered for this subject
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
                            is_override = False 

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

                for date_key in sorted_dates: # <--- RENAMED TO AVOID SHADOWING
                    schedule_by_date[date_key].sort(key=get_sort_key)
                
                # --- HARDCODED DATE LOGIC ---
                all_dates = []
                
                # Start: First date found in the Excel schedule (to keep history)
                if not master_schedule_df.empty:
                    first_date = master_schedule_df[0].min()
                else:
                    first_date = date.today()

                # End: HARDCODED (18th Jan 2026)
                last_date = date(2026, 1, 18)

                current_date = first_date
                
                # Simple loop from start to hardcoded end
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
