import streamlit as st
import pandas as pd
import os
import glob
from datetime import datetime, date
import re
from ics import Calendar, Event
import pytz
import gc 
import time

# Note: We import these inside functions or use try/except to avoid crashes if missing
try:
    from streamlit_extras.st_keyup import st_keyup
except ImportError:
    st_keyup = None

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="MBA Timetable", layout="centered", initial_sidebar_state="collapsed")

SCHEDULE_FILE_NAME = 'schedule.xlsx' 
TIMEZONE = 'Asia/Kolkata'
GOOGLE_CALENDAR_IMPORT_LINK = 'https://calendar.google.com/calendar/u/0/r/settings/export'

# --- 2. CSS STYLING ---
st.markdown("""
<style>
    .stApp { background-color: #0F172A; color: white; }
    .stTextInput input { background-color: #1E293B; color: white; border: 1px solid #334155; }
    .day-card { background: #1E293B; padding: 15px; border-radius: 10px; margin-bottom: 10px; border: 1px solid #334155; }
    .day-card.today { border: 2px solid #38BDF8; }
    .subject { font-weight: bold; font-size: 1.1em; color: white; }
    .meta { color: #94A3B8; font-size: 0.9em; }
    .venue-change { color: #F87171; font-weight: bold; }
    
    /* Mess Menu Styling Fixes */
    .menu-header {
        font-weight: bold;
        color: #38BDF8; /* Light Blue for Headers */
        margin-bottom: 5px;
        font-size: 1.0em;
        text-transform: uppercase;
        letter-spacing: 1px;
        border-bottom: 1px solid #334155;
        padding-bottom: 2px;
    }
    /* Fix bullet point rendering in Streamlit columns */
    div[data-testid="stMarkdownContainer"] ul {
        padding-left: 18px;
        margin-bottom: 10px;
    }
    div[data-testid="stMarkdownContainer"] li {
        margin-bottom: 2px;
        font-size: 0.9em;
        color: #E2E8F0;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. DATA CONSTANTS ---
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

# Optional Imports
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

# --- 4. FUNCTIONS ---

def normalize_string(text):
    if isinstance(text, str):
        return text.replace(" ", "").replace("'", "").replace(".", "").upper()
    return ""

@st.cache_resource(show_spinner="Initializing database...", ttl=3600)
def build_master_index(folder_path='.'):
    """Singleton Database: Reads files ONCE."""
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

            # Process Blocks
            for roll_col in roll_col_indices:
                name_col = roll_col + 1
                
                # Identify Subject
                raw_section_name = ""
                if header_row_idx > 0:
                    start_search = max(0, roll_col - 2)
                    end_search = min(df.shape[1], roll_col + 3)
                    for check_col in range(start_search, end_search):
                        val_above = str(df.iloc[header_row_idx-1, check_col]).strip()
                        if val_above and val_above.lower() != 'nan':
                            raw_section_name = val_above
                            break 
                
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
    try:
        master_index = build_master_index(folder_path)
    except Exception:
        return "System Busy", set()

    target_clean = str(target_roll).strip().upper()
    if target_clean in master_index:
        data = master_index[target_clean]
        return data['Name'], data['Subjects']
    
    for db_roll, data in master_index.items():
        if target_clean in db_roll or db_roll in target_clean:
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
        # Logic fix for 12PM
        start_am_pm = end_am_pm 
        if end_am_pm == "PM" and start_hour < 12 and (start_hour == 11 or start_hour <= 10):
               start_am_pm = "AM"

        full_start_str = f"{start_str_part}{start_am_pm}" if not start_str_part[-2:].isalpha() else start_str_part
        start_dt = local_tz.localize(pd.to_datetime(f"{date_obj.strftime('%Y-%m-%d')} {full_start_str}"))
        end_dt = local_tz.localize(pd.to_datetime(f"{date_obj.strftime('%Y-%m-%d')} {end_str_part}"))
        return start_dt, end_dt
    except Exception:
        return None, None

def render_mess_menu_expander():
    try:
        menu_source = MESS_MENU if 'MESS_MENU' in globals() else {}
    except ImportError: return 
    
    local_tz = pytz.timezone(TIMEZONE)
    now_dt = datetime.now(local_tz)
    today = now_dt.date()
    start_date = today if now_dt.hour < 23 else today + pd.Timedelta(days=1)
    
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

    with st.expander("🍽️ Mess Menu", expanded=False):
        selected_label = st.radio("Select Day:", options, index=default_index, horizontal=True)
        selected_idx = options.index(selected_label)
        selected_date = valid_dates[selected_idx]
        menu_data = menu_source[selected_date]
        
        # --- MENU FORMATTER FUNCTION (Smart Cleanup) ---
        def fmt_menu(text):
            if not text or str(text).lower() == 'nan': return "-"
            # 1. Split by '*'
            items = str(text).split('*')
            # 2. Strip whitespace and remove empty strings
            clean_items = [i.strip() for i in items if i.strip()]
            
            if not clean_items: return "-"
            # 3. Join with bullet points
            return "\n".join([f"- {item}" for item in clean_items])

        st.markdown(f"**Menu for {selected_date.strftime('%d %B')}**")
        c1, c2, c3, c4 = st.columns(4)
        
        # Use HTML headers to prevent size issues
        with c1: 
            st.markdown('<div class="menu-header">Breakfast</div>', unsafe_allow_html=True)
            st.markdown(fmt_menu(menu_data.get('Breakfast', '-')))
        with c2: 
            st.markdown('<div class="menu-header">Lunch</div>', unsafe_allow_html=True)
            st.markdown(fmt_menu(menu_data.get('Lunch', '-')))
        with c3: 
            st.markdown('<div class="menu-header">Hi-Tea</div>', unsafe_allow_html=True)
            st.markdown(fmt_menu(menu_data.get('Hi-Tea', '-')))
        with c4: 
            st.markdown('<div class="menu-header">Dinner</div>', unsafe_allow_html=True)
            st.markdown(fmt_menu(menu_data.get('Dinner', '-')))

# --- 5. MAIN UI ---

# --- 1. MEMORY SAFETY ---
if 'has_cleaned_memory' not in st.session_state:
    gc.collect()
    st.session_state.has_cleaned_memory = True

if 'submitted' not in st.session_state: st.session_state.submitted = False
if 'roll_number' not in st.session_state: st.session_state.roll_number = ""
if 'search_clear_counter' not in st.session_state: st.session_state.search_clear_counter = 0
if 'just_submitted' not in st.session_state: st.session_state.just_submitted = False

if not st.session_state.submitted:
    st.title("MBA Timetable")
    with st.form("roll_form"):
        roll_in = st.text_input("Enter Roll No (Last 3 digits):", placeholder="463").strip()
        if st.form_submit_button("Get Schedule"):
            if roll_in:
                # Normalize Roll No
                if roll_in.isdigit():
                     if int(roll_in) < 100: roll_in = f"21BCM{roll_in}"
                     elif int(roll_in) <= 999: roll_in = f"24MBA{roll_in}"
                st.session_state.roll_number = roll_in.upper()
                st.session_state.submitted = True
                st.session_state.just_submitted = True
                st.rerun()
    render_mess_menu_expander()

else:
    # --- RESULT DASHBOARD ---
    roll = st.session_state.roll_number
    
    c1, c2 = st.columns([3,1])
    with c1: st.subheader(f"Schedule: {roll}")
    with c2: 
        if st.button("Change"):
            st.session_state.submitted = False
            st.rerun()

    # Ensure this runs once per submission
    if st.session_state.just_submitted:
        with st.spinner("Finding your schedule..."):
            name, subjects = find_subjects_for_roll(roll)
            
        if not subjects:
            st.error("Roll number not found.")
            if st.button("Go Back"):
                st.session_state.submitted = False
                st.rerun()
            st.stop()
        else:
            st.session_state.student_name = name
            st.session_state.student_sections = subjects
            st.session_state.just_submitted = False

    # Retrieve from session state
    if 'student_sections' in st.session_state:
        name = st.session_state.student_name
        subjects = st.session_state.student_sections

        schedule_df = load_and_clean_schedule(SCHEDULE_FILE_NAME)
        if schedule_df.empty:
            st.error("Schedule file missing.")
        else:
            # Process Schedule
            found_classes = []
            normalized_subjects = {normalize_string(s): s for s in subjects}
            time_slots = {2: "8-9 AM", 3: "9:10-10:10 AM", 4: "10:20-11:20 AM", 5: "11:30-12:30 PM",
                          6: "12:30-1:30 PM", 7: "1:30-2:30 PM", 8: "2:40-3:40 PM", 9: "3:50-4:50 PM",
                          10: "5-6 PM", 11: "6:10-7:10 PM", 12: "7:20-8:20 PM", 13: "8:30-9:30 PM"}

            for _, row in schedule_df.iterrows():
                row_date = row[0]
                if pd.isna(row_date): continue
                
                for col_idx, time_str in time_slots.items():
                    cell_val = str(row[col_idx])
                    if not cell_val or cell_val.lower() == 'nan': continue
                    
                    parts = cell_val.split('/')
                    for part in parts:
                        norm_part = normalize_string(part)
                        matched_subj = None
                        
                        # Match logic
                        if norm_part in normalized_subjects:
                            matched_subj = normalized_subjects[norm_part]
                        else:
                            for s_norm in normalized_subjects:
                                if s_norm == norm_part: 
                                    matched_subj = normalized_subjects[s_norm]; break
                        
                        if matched_subj:
                            details = {'Venue': '-', 'Faculty': 'N/A'}
                            norm_key = normalize_string(matched_subj)
                            # Find details
                            for k, v in COURSE_DETAILS_MAP.items():
                                if normalize_string(k) == norm_key: details = v.copy(); break
                            
                            # Overrides
                            is_override = False
                            if row_date in DAY_SPECIFIC_OVERRIDES:
                                if norm_key in DAY_SPECIFIC_OVERRIDES[row_date]:
                                    ov = DAY_SPECIFIC_OVERRIDES[row_date][norm_key]
                                    # Time match check
                                    if ov.get('Target_Time', time_str) == time_str:
                                        details.update(ov)
                                        if 'Venue' in ov: is_override = True
                            
                            found_classes.append({
                                'Date': row_date, 'Time': details.get('Time', time_str),
                                'Subject': matched_subj, 'Venue': details['Venue'],
                                'Faculty': details['Faculty'], 'Override': is_override
                            })

            # Add Additional Classes
            for ac in ADDITIONAL_CLASSES:
                norm_ac = normalize_string(ac['Subject'])
                if any(norm_ac in normalize_string(s) for s in subjects):
                    found_classes.append({
                        'Date': ac['Date'], 'Time': ac['Time'], 'Subject': ac['Subject'],
                        'Venue': ac.get('Venue','-'), 'Faculty': ac.get('Faculty','-'), 'Override': False
                    })
            
            # Sort and Render
            today = date.today()
            
            # --- DATE LOGIC FIX (Prevents Infinite Loop) ---
            # Get only dates present in the data, plus today
            unique_dates = sorted(list(set([c['Date'] for c in found_classes])))
            if not unique_dates: unique_dates = [today]
            
            # Only show Upcoming (Today onwards)
            upcoming = [c for c in found_classes if c['Date'] >= today]
            upcoming.sort(key=lambda x: (x['Date'], x['Time']))

            if not upcoming:
                st.info("No upcoming classes found.")
            else:
                for c in upcoming:
                    is_today = (c['Date'] == today)
                    css = "today" if is_today else ""
                    style = "color: #F87171;" if c['Override'] else ""
                    
                    st.markdown(f"""
                    <div class="day-card {css}">
                        <div style="display:flex; justify-content:space-between;">
                            <div>
                                <div class="meta">{c['Date'].strftime('%d %b, %a')} • {c['Time']}</div>
                                <div class="subject">{c['Subject']}</div>
                                <div class="meta">{c['Faculty']}</div>
                            </div>
                            <div style="text-align:right;">
                                <div class="meta">Venue</div>
                                <div style="{style} font-weight:bold;">{c['Venue']}</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            # Show Past Classes (Expander)
            with st.expander("Show Past Classes"):
                 if st_keyup:
                    query = st_keyup("Search history:", key="hist_search").lower()
                 else:
                    query = st.text_input("Search history:").lower()

                 past = [c for c in found_classes if c['Date'] < today]
                 past.sort(key=lambda x: (x['Date'], x['Time']), reverse=True)
                 
                 for c in past:
                     if query and query not in str(c).lower(): continue
                     st.markdown(f"**{c['Date'].strftime('%d %b')}**: {c['Subject']} ({c['Time']}) - {c['Venue']}")
st.markdown("---")
st.caption("_Made by Vishesh_")
