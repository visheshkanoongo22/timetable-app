
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
import time 

# --- IMPORT DATA FROM EXTERNAL FILES ---
from day_overrides import DAY_SPECIFIC_OVERRIDES
from additional_classes import ADDITIONAL_CLASSES
from mess_menu import MESS_MENU
from exam_schedule import EXAM_SCHEDULE_DATA

# --- AUTO REFRESH EVERY 10 MINUTES (HARD REBOOT) ---
AUTO_REFRESH_INTERVAL = 10 * 60  # 10 minutes in seconds

# Store the start time in session_state
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

# --- Cache Clearing Logic ---
if "run_counter" not in st.session_state:
    st.session_state.run_counter = 0
st.session_state.run_counter += 1

if st.session_state.run_counter % 100 == 0:
    st.cache_data.clear()      
    st.cache_resource.clear()  
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
    "DV&VS('C)": {'Faculty': 'Anand Kumar', 'Venue': 'T5'}, 'DV&VS(A)': {'Faculty': 'Somayya Madakam', 'Venue': 'E3'},
    'DV&VS(B)': {'Faculty': 'Somayya Madakam', 'Venue': 'E3'}, 'DV&VS(D)': {'Faculty': 'Anand Kumar', 'Venue': 'T5'},
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

# 3. FUNCTIONS
def normalize_string(text):
    if isinstance(text, str):
        return text.replace(" ", "").replace("(", "").replace(")", "").replace("'", "").upper()
    return ""

@st.cache_data
def load_and_clean_schedule(file_path, is_stats_file=False):
    try:
        df = pd.read_excel(file_path, sheet_name=1, header=None, skiprows=3)
        schedule_df = df.iloc[:, 0:14].copy()
        schedule_df[0] = pd.to_datetime(schedule_df[0], errors='coerce').dt.date
        schedule_df.dropna(subset=[0], inplace=True)
        return schedule_df
    except FileNotFoundError:
        if not is_stats_file:
            st.error(f"FATAL ERROR: The main schedule file '{file_path}' was not found.")
        return pd.DataFrame()
    except Exception as e:
        if not is_stats_file:
            st.error(f"FATAL ERROR: Could not load the main schedule file. Details: {e}")
        return pd.DataFrame()

@st.cache_data
def load_all_schedules(file_list):
    all_dfs = []
    for file_path in file_list:
        df = load_and_clean_schedule(file_path, is_stats_file=True) 
        if not df.empty:
            all_dfs.append(df)
            
    if not all_dfs:
        return pd.DataFrame()
        
    combined_df = pd.concat(all_dfs)
    combined_df = combined_df.sort_values(by=[0])
    return combined_df

# --- NEW: Function to display Exam Schedule ---
def display_exam_schedule(student_sections):
    # 1. Normalize student sections to get base codes
    student_base_codes = set()
    for sec in student_sections:
        base = re.sub(r"\(.*$", "", sec).strip()
        student_base_codes.add(base)
        if "B2B" in sec: student_base_codes.add("B2B")
        if "DV&VS" in sec: student_base_codes.add("DV&VS")
        if "ML&AI" in sec: student_base_codes.add("ML&AI")
        if "CC&AU" in sec: student_base_codes.add("CC&AU")

    # 2. Filter exams
    my_exams = []
    for exam in EXAM_SCHEDULE_DATA:
        if exam['Subject_Code'] in student_base_codes:
            my_exams.append(exam)
    
    if not my_exams:
        return

    # 3. Display
    with st.expander("📝 End Term Examinations (Term V)"):
        # Sort by date
        my_exams.sort(key=lambda x: x['Date'])
        
        for exam in my_exams:
            # FORMAT CHANGE: Removed Day Name (%A)
            date_str = exam['Date'].strftime('%d %b %Y')
            st.markdown(f"""
            <div style="
                background-color: rgba(255, 255, 255, 0.05); 
                padding: 10px; 
                border-radius: 8px; 
                margin-bottom: 8px; 
                border-left: 4px solid #60A5FA;">
                <div style="font-weight: 700; font-size: 1.1em; color: #fff;">{exam['Full_Name']}</div>
                <div style="display: flex; justify-content: space-between; color: #94A3B8; font-size: 0.9em; margin-top: 4px;">
                    <span>{date_str}</span>
                    <span>{exam['Time']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

def render_mess_menu_expander():
    """Show weekly mess menu with a day selector."""
    local_tz = pytz.timezone(TIMEZONE)
    now_dt = datetime.now(local_tz)
    today = now_dt.date()

    start_date = today
    if now_dt.hour >= 23:
        start_date = today + pd.Timedelta(days=1)

    week_dates = [start_date + pd.Timedelta(days=i) for i in range(7)]
    valid_dates = [d for d in week_dates if d in MESS_MENU]
    if not valid_dates:
        return 

    options = []
    default_index = 0
    for idx, d in enumerate(valid_dates):
        # FORMAT CHANGE: Removed Day Name (%a)
        label = d.strftime("%d %b") 
        if d == today:
            label += " (Today)"
            default_index = idx
        elif d == today + pd.Timedelta(days=1):
            label += " (Tomorrow)"
        options.append(label)

    with st.expander("🍽️ Mess Menu for the Week", expanded=False):
        selected_label = st.radio(
            "Select a day:",
            options,
            index=default_index,
            horizontal=True,
        )

        selected_idx = options.index(selected_label)
        selected_date = valid_dates[selected_idx]
        menu_data = MESS_MENU[selected_date]

        # FORMAT CHANGE: Removed Day Name (%A)
        st.markdown(
            f"**Menu for {selected_date.strftime('%d %B %Y')}**"
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown("#### Breakfast")
            st.markdown(menu_data.get("Breakfast", "Not available"))

        with col2:
            st.markdown("#### Lunch")
            st.markdown(menu_data.get("Lunch", "Not available"))

        with col3:
            st.markdown("#### Hi-Tea")
            st.markdown(menu_data.get("Hi-Tea", "Not available"))

        with col4:
            st.markdown("#### Dinner")
            st.markdown(menu_data.get("Dinner", "Not available"))

def calculate_and_display_stats():
    with st.expander("Sessions Taken till Now"):
        with st.spinner("Calculating session statistics..."):
            all_schedules_df = load_and_clean_schedule(SCHEDULE_FILE_NAME) 
            
            if all_schedules_df.empty:
                st.warning("Could not load schedule file to calculate stats.")
                return

            local_tz = pytz.timezone(TIMEZONE)
            now_dt = datetime.now(local_tz)
            today_date = now_dt.date()
            
            class_counts = defaultdict(int)
            
            time_slot_end_times = {
                2: "9:00AM", 3: "10:10AM", 4: "11:20AM", 5: "12:30PM",
                6: "1:30PM", 7: "2:30PM", 8: "3:40PM", 9: "4:50PM",
                10: "6:00PM", 11: "7:10PM", 12: "8:20PM", 13: "9:30PM"
            }
            
            normalized_course_map = {normalize_string(k): k for k in COURSE_DETAILS_MAP.keys()}
            
            for _, row in all_schedules_df.iterrows():
                class_date = row[0]
                
                if class_date > today_date:
                    continue 

                for col_idx, end_time_str in time_slot_end_times.items():
                    is_in_past = False 
                    if class_date < today_date:
                        is_in_past = True
                    elif class_date == today_date:
                        try:
                            class_end_dt = local_tz.localize(pd.to_datetime(f"{class_date.strftime('%Y-%m-%d')} {end_time_str}"))
                            is_in_past = class_end_dt < now_dt
                        except Exception:
                            is_in_past = False 
                    
                    if is_in_past:
                        cell_value = str(row[col_idx])
                        if cell_value and cell_value != 'nan':
                            normalized_cell = normalize_string(cell_value)
                            
                            for norm_name, orig_name in normalized_course_map.items():
                                if norm_name in normalized_cell:
                                    is_overridden = False
                                    if class_date in DAY_SPECIFIC_OVERRIDES and norm_name in DAY_SPECIFIC_OVERRIDES[class_date]:
                                        override_details = DAY_SPECIFIC_OVERRIDES[class_date][norm_name]
                                        venue_text = override_details.get('Venue', '').upper()
                                        faculty_text = override_details.get('Faculty', '').upper()
                                        
                                        if "POSTPONED" in venue_text or "POSTPONED" in faculty_text or \
                                           "CANCELLED" in venue_text or "CANCELLED" in faculty_text or \
                                           "PREPONED" in venue_text or "PREPONED" in faculty_text:
                                            is_overridden = True 
                                            
                                    if not is_overridden:
                                        class_counts[orig_name] += 1

            for added_class in ADDITIONAL_CLASSES:
                class_date = added_class['Date']
                if class_date > today_date:
                    continue 
                
                is_in_past = False
                if class_date < today_date:
                    is_in_past = True
                elif class_date == today_date:
                    try:
                        _, end_time_str = added_class['Time'].split('-')
                        class_end_dt = local_tz.localize(pd.to_datetime(f"{class_date.strftime('%Y-%m-%d')} {end_time_str}"))
                        is_in_past = class_end_dt < now_dt
                    except Exception:
                        is_in_past = False
                
                if is_in_past:
                    norm_name = normalize_string(added_class['Subject'])
                    if norm_name in normalized_course_map:
                        orig_name = normalized_course_map[norm_name]
                        class_counts[orig_name] += 1
            
            if not class_counts:
                st.info("No past classes were found to calculate statistics.")
                return

            st.markdown("This shows the total number of sessions held *to date*, accounting for all schedule changes.")
            
            grouped_counts = defaultdict(dict)
            for full_name, count in class_counts.items():
                match = re.match(r"(.*?)\((.*)\)", full_name)
                if match:
                    course_name = match.group(1)
                    section_name = match.group(2).replace("'", "") 
                else:
                    course_name = full_name
                    section_name = "Main" 
                
                grouped_counts[course_name][section_name] = count
            
            sorted_courses = sorted(grouped_counts.keys())
            midpoint = len(sorted_courses) // 2 + (len(sorted_courses) % 2)
            col1, col2 = st.columns(2)

            def display_course_stats(column, course_list):
                with column:
                    for course_name in course_list:
                        st.markdown(f"**{course_name}**")
                        sections = grouped_counts[course_name]
                        
                        max_lectures = 30
                        if "DV&VS" in course_name or course_name == "BS":
                            max_lectures = 40
                            
                        for section_name in sorted(sections.keys()):
                            count = sections[section_name]
                            if section_name == "Main":
                                st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;Total Sessions: {count}/{max_lectures}")
                            else:
                                st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;Section {section_name}: {count}/{max_lectures} sessions")
                        st.markdown("") 

            display_course_stats(col1, sorted_courses[:midpoint])
            display_course_stats(col2, sorted_courses[midpoint:])

@st.cache_data
def get_all_student_data(folder_path='.'):
    student_data_map = {}
    subject_files = [
        f for f in glob.glob(os.path.join(folder_path, '*.xlsx')) 
        if os.path.basename(f) != SCHEDULE_FILE_NAME 
        and not os.path.basename(f).startswith('~')
    ]
    
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
    page_title="MBA Timetable Assistant", 
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
    st.markdown('<div class="header-sub">Made by Vishesh</div>', unsafe_allow_html=True)

student_data_map = get_all_student_data()

if not student_data_map:
    st.markdown('<p class="main-header">MBA Timetable Assistant</p>', unsafe_allow_html=True)
    st.markdown('<div class="header-sub">Course Statistics & Schedule Tool</div>', unsafe_allow_html=True)
    st.error("FATAL ERROR: Could not load any student data. Please check your Excel files.")
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
            st.session_state.submitted = False
            st.session_state.roll_number = ""
            st.rerun()
        else:
            student_info = student_data_map[roll_to_process]
            student_name, student_sections = student_info['name'], student_info['sections']
            
            master_schedule_df = load_and_clean_schedule(SCHEDULE_FILE_NAME)
            
            if master_schedule_df.empty:
                pass
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
                
                display_exam_schedule(student_sections)

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
                                                override_data = DAY_SPECIFIC_OVERRIDES[date][norm_sec]
                                                
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
                    
                    for added_class in ADDITIONAL_CLASSES:
                        norm_added_subject = normalize_string(added_class['Subject'])
                        if norm_added_subject in normalized_student_section_map:
                            
                            venue_text = added_class.get('Venue', '').upper()
                            faculty_text = added_class.get('Faculty', '').upper()
                            is_override = False 
                            
                            if ("POSTPONED" in venue_text or "POSTPONED" in faculty_text or
                                "CANCELLED" in venue_text or "CANCELLED" in faculty_text or
                                "PREPONED" in venue_text or "PREPONED" in faculty_text or
                                "(RESCHEDULED)" in venue_text or "(PREPONED)" in venue_text):
                                is_override = True

                            day_of_week = added_class['Date'].strftime('%A')
                            found_classes.append({
                                "Date": added_class['Date'], "Day": day_of_week, "Time": added_class['Time'],
                                "Subject": added_class['Subject'], 
                                "Faculty": added_class.get('Faculty', 'N/A'),
                                "Venue": added_class.get('Venue', '-'), 
                                "is_venue_override": is_override 
                            })

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
                            
                            # FORMAT CHANGE: Removed Day Name (%A)
                            st.markdown(f'''
                                <div class="day-card" id="date-card-past-{date_obj.toordinal()}">
                                    <div class="day-header">
                                        {date_obj.strftime("%d %B %Y")}
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
                            # FORMAT CHANGE: Removed Day Name (%A)
                            st.markdown(f'''
                                <div class="day-card {today_class}" id="{card_id}">
                                    <div class="day-header">
                                        {date_obj.strftime("%d %B %Y")}
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
                            # FORMAT CHANGE: Removed Day Name (%A)
                            if is_today:
                                st.markdown(f'''
                                    <div class="day-card {today_class}" id="{card_id}">
                                        <div class="today-badge">TODAY</div>
                                        <div class="day-header">
                                            {date_obj.strftime("%d %B %Y")}
                                        </div>
                                ''', unsafe_allow_html=True)
                            else:
                                st.markdown(f'''
                                    <div class="day-card {today_class}" id="{card_id}">
                                        <div class="day-header">
                                            {date_obj.strftime("%d %B %Y")}
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
