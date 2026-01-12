import streamlit as st
import pandas as pd
import json
import os
import re
from datetime import datetime, date, timedelta
import pytz
import hashlib
from collections import defaultdict
import gc
import time
from ics import Calendar, Event

# --- OPTIONAL IMPORTS ---
try:
    from streamlit_extras.st_keyup import st_keyup
except ImportError:
    st_keyup = None

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

# --- CONFIGURATION ---
TIMEZONE = 'Asia/Kolkata'
GOOGLE_CALENDAR_IMPORT_LINK = 'https://calendar.google.com/calendar/u/0/r/settings/export'
AUTO_REFRESH_INTERVAL = 10 * 60 

# --- MEMORY & REFRESH ---
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

if (time.time() - st.session_state.start_time) > AUTO_REFRESH_INTERVAL:
    st.cache_data.clear()
    gc.collect()
    st.session_state.start_time = time.time()
    st.rerun()

# --- CSS STYLING (YOUR EXACT STYLES) ---
st.set_page_config(page_title="MBA Timetable Assistant - Term 6", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
    <meta name="color-scheme" content="dark">
    <meta name="theme-color" content="#0F172A">
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
    
    /* Mess Menu Specifics */
    .menu-header { color: #38BDF8; font-weight: bold; text-transform: uppercase; font-size: 0.9em; margin-bottom: 5px; }
    div[data-testid="stMarkdownContainer"] ul { padding-left: 18px; margin-bottom: 10px; }
    div[data-testid="stMarkdownContainer"] li { margin-bottom: 2px; font-size: 0.9em; color: #E2E8F0; }

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

# --- HELPER FUNCTIONS ---
def normalize(text):
    if not isinstance(text, str): return ""
    return text.replace(" ", "").replace("'", "").replace(".", "").upper()

def get_sort_key(time_str):
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
        elif h in [8, 9, 10] and "PM" in time_str and "AM" not in time_str: h += 12
        return h * 60 + m
    except: return 9999

# --- DATA LOADING (HYBRID ARCHITECTURE) ---
@st.cache_data
def load_base_data():
    try:
        with open('db_students.json', 'r') as f:
            students = json.load(f)
        with open('db_schedule_base.json', 'r') as f:
            schedule = json.load(f)
        return students, schedule
    except FileNotFoundError:
        return {}, []

students_db, base_schedule = load_base_data()

def get_hybrid_schedule(roll_no):
    # 1. Identify Student
    roll_clean = str(roll_no).strip().upper().replace(" ", "")
    my_subjects = set()
    found_key = None
    
    # Robust Search (Your strict+fuzzy logic)
    for db_roll, subjs in students_db.items():
        db_clean = str(db_roll).strip().upper().replace(" ", "")
        if (roll_clean == db_clean) or \
           (roll_clean in db_clean and db_clean.endswith(roll_clean)) or \
           (db_clean in roll_clean and roll_clean.endswith(db_clean)):
            my_subjects = set(subjs)
            found_key = db_roll
            break
            
    if not my_subjects: return [], None

    # 2. Process Schedule (Apply Overrides Live)
    final_classes = []
    
    # A. Base Schedule + Overrides
    for cls in base_schedule:
        if cls['Subject'] not in my_subjects: continue
        
        # Apply Overrides
        d_obj = datetime.strptime(cls['Date'], "%Y-%m-%d").date()
        
        details = {
            'Venue': cls['Venue'],
            'Faculty': cls['Faculty'],
            'Time': cls['Time'],
            'Override': False
        }
        
        # Live Override Check
        if d_obj in DAY_SPECIFIC_OVERRIDES:
            day_ov = DAY_SPECIFIC_OVERRIDES[d_obj]
            for ov_subj, ov_data in day_ov.items():
                if normalize(ov_subj) in cls['Subject']:
                    target = ov_data.get('Target_Time', cls['Time'])
                    if target == cls['Time']:
                        details.update(ov_data)
                        if 'Venue' in ov_data or 'Time' in ov_data: 
                            details['Override'] = True
        
        cls_obj = cls.copy()
        cls_obj.update(details)
        final_classes.append(cls_obj)

    # B. Additional Classes (Live)
    for ac in ADDITIONAL_CLASSES:
        norm_subj = normalize(ac['Subject'])
        if norm_subj in my_subjects:
            venue = ac.get('Venue', '').upper()
            is_ov = False 
            # Logic: If it's just a normal added class, not an override. 
            # If it says "Postponed", treat as standard text.
            
            final_classes.append({
                "Date": ac['Date'].strftime("%Y-%m-%d"),
                "Time": ac['Time'],
                "Subject": norm_subj,
                "DisplaySubject": ac['Subject'],
                "Venue": ac.get('Venue', '-'),
                "Faculty": ac.get('Faculty', '-'),
                "Override": is_ov
            })

    # Sort
    final_classes.sort(key=lambda x: (x['Date'], get_sort_key(x['Time'])))
    return final_classes, found_key

def calculate_stats(student_schedule):
    if not student_schedule: return {}
    
    today_str = date.today().strftime("%Y-%m-%d")
    local_tz = pytz.timezone(TIMEZONE)
    now_dt = datetime.now(local_tz)
    
    counts = defaultdict(int)
    
    for cls in student_schedule:
        # Stop at today
        if cls['Date'] > today_str: continue
        
        # Check time for today
        is_past = False
        if cls['Date'] < today_str:
            is_past = True
        elif cls['Date'] == today_str:
            try:
                # Approximate end time parsing
                _, end_str = cls['Time'].split('-')
                # (Simplified logic for speed, can be enhanced)
                is_past = True # Count today's classes as "Happening"
            except: is_past = False
            
        if is_past:
            # Check for cancellations
            venue = str(cls['Venue']).upper()
            fac = str(cls['Faculty']).upper()
            if "CANCELLED" in venue or "POSTPONED" in venue or "PREPONED" in venue:
                continue # Don't count these
            
            counts[cls['DisplaySubject']] += 1
            
    return counts

def render_mess_menu():
    if not MESS_MENU: return
    today = date.today()
    week_dates = [today + pd.Timedelta(days=i) for i in range(7)]
    valid_dates = [d for d in week_dates if d in MESS_MENU]
    if not valid_dates: return

    with st.expander("🍽️ Mess Menu for the Week", expanded=False):
        opts = [d.strftime("%d %b") + (" (Today)" if d == today else "") for d in valid_dates]
        sel = st.radio("Select a day:", opts, index=0, horizontal=True, label_visibility="visible")
        sel_date = valid_dates[opts.index(sel)]
        data = MESS_MENU[sel_date]
        
        def fmt(txt):
            if not txt or str(txt).lower() == 'nan': return "-"
            items = [i.strip() for i in str(txt).split('*') if i.strip()]
            return "\n".join([f"- {i}" for i in items])

        st.markdown(f"**Menu for {sel_date.strftime('%d %B %Y')}**")
        c1, c2, c3, c4 = st.columns(4)
        with c1: 
            st.markdown('<div class="menu-header">Breakfast</div>', unsafe_allow_html=True)
            st.markdown(fmt(data.get('Breakfast')))
        with c2: 
            st.markdown('<div class="menu-header">Lunch</div>', unsafe_allow_html=True)
            st.markdown(fmt(data.get('Lunch')))
        with c3: 
            st.markdown('<div class="menu-header">Hi-Tea</div>', unsafe_allow_html=True)
            st.markdown(fmt(data.get('Hi-Tea')))
        with c4: 
            st.markdown('<div class="menu-header">Dinner</div>', unsafe_allow_html=True)
            st.markdown(fmt(data.get('Dinner')))

def generate_ics(classes):
    c = Calendar(creator="-//MBA Timetable//EN")
    local_tz = pytz.timezone(TIMEZONE)
    for cls in classes:
        venue = str(cls['Venue']).upper()
        if "CANCELLED" in venue or "POSTPONED" in venue: continue
        
        try:
            time_str = cls['Time']
            start_part, end_part = time_str.split('-')
            
            # Simple Time Logic
            s_match = re.search(r'(\d+)(?::(\d+))?', start_part)
            e_match = re.search(r'(\d+)(?::(\d+))?', end_part)
            
            sh, sm = int(s_match.group(1)), int(s_match.group(2) or 0)
            eh, em = int(e_match.group(1)), int(e_match.group(2) or 0)
            
            # AM/PM Logic guess (Simple)
            if "PM" in end_part and sh < 12 and sh != 11: sh += 12
            if "PM" in end_part and eh < 12: eh += 12
            
            d_obj = datetime.strptime(cls['Date'], "%Y-%m-%d").date()
            start_dt = local_tz.localize(datetime.combine(d_obj, datetime.min.time().replace(hour=sh, minute=sm)))
            end_dt = local_tz.localize(datetime.combine(d_obj, datetime.min.time().replace(hour=eh, minute=em)))
            
            e = Event()
            e.name = cls['DisplaySubject']
            e.begin = start_dt.astimezone(pytz.utc)
            e.end = end_dt.astimezone(pytz.utc)
            e.location = cls['Venue']
            e.description = f"Faculty: {cls['Faculty']}"
            c.events.add(e)
        except: continue
    return c.serialize()

# --- MAIN UI LOGIC ---

if 'submitted' not in st.session_state: st.session_state.submitted = False
if 'roll_number' not in st.session_state: st.session_state.roll_number = ""
if 'search_clear_counter' not in st.session_state: st.session_state.search_clear_counter = 0

# A. LANDING PAGE
if not st.session_state.submitted:
    st.markdown('<p class="main-header">MBA Timetable Assistant</p>', unsafe_allow_html=True)
    st.markdown('<div class="header-sub"> Your Term VI Schedule</div>', unsafe_allow_html=True)

    st.markdown("""
        <div class="welcome-box">
            Welcome! Enter your roll number to get started!</strong>.
        </div>
        """, unsafe_allow_html=True)
        
    with st.form("roll_number_form"):
        roll_input = st.text_input("Enter your Roll Number:", placeholder="e.g., 463 (Just the last 3 digits)").strip().upper()
        if st.form_submit_button("Generate Timetable"):
            if roll_input.isdigit():
                if int(roll_input) < 100: roll_input = f"21BCM{roll_input}"
                elif int(roll_input) <= 999: roll_input = f"24MBA{roll_input}"
            st.session_state.roll_number = roll_input
            st.session_state.submitted = True
            st.rerun()
            
    render_mess_menu()

# B. DASHBOARD PAGE
else:
    roll = st.session_state.roll_number
    
    # 1. Header Area
    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown(f"""
        <div class="welcome-message">
            Displaying schedule for: <strong>{roll}</strong>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        if st.button("Change Roll Number"):
            st.session_state.submitted = False
            st.session_state.roll_number = ""
            st.rerun()

    # 2. Get Data
    with st.spinner("Finding your schedule..."):
        schedule, db_key = get_hybrid_schedule(roll)

    if not schedule and not db_key:
        st.error(f"Roll Number '{roll}' not found in database.")
        with st.expander("Debug Info"):
            st.write(f"Searched for: {roll}")
            st.write(f"Sample DB Keys: {list(students_db.keys())[:5]}")
        if st.button("Go Back"):
            st.session_state.submitted = False
            st.rerun()
    else:
        # 3. Stats Section
        stats = calculate_stats(schedule)
        with st.expander("Sessions Taken till Now"):
            if not stats:
                st.info("No past classes recorded.")
            else:
                st.markdown("Total sessions held *to date*:")
                sc1, sc2 = st.columns(2)
                sorted_stats = sorted(stats.items())
                mid = len(sorted_stats) // 2 + (len(sorted_stats) % 2)
                
                with sc1:
                    for k, v in sorted_stats[:mid]: st.markdown(f"**{k}**: {v}")
                with sc2:
                    for k, v in sorted_stats[mid:]: st.markdown(f"**{k}**: {v}")

        # 4. Mess Menu (Again, for convenience)
        render_mess_menu()

        # 5. ICS Download
        ics_data = generate_ics(schedule)
        sanitized_name = re.sub(r'[^a-zA-Z0-9_]', '', str(db_key).replace(" ", "_")).upper()
        with st.expander("Download & Import to Calendar"):
            st.download_button(
                label="Download .ics Calendar File",
                data=ics_data,
                file_name=f"{sanitized_name}_Timetable.ics",
                mime='text/calendar'
            )
            st.markdown("**How to Import:** Download the file, go to Google Calendar settings, select 'Import & Export', and upload the file.")

        # 6. Date Sorting & Display
        schedule_by_date = defaultdict(list)
        for c in schedule: schedule_by_date[c['Date']].append(c)
        
        all_dates = sorted(schedule_by_date.keys())
        today_str = date.today().strftime("%Y-%m-%d")
        
        past_dates = [d for d in all_dates if d < today_str]
        future_dates = [d for d in all_dates if d >= today_str]

        # 7. Past Classes (Searchable)
        with st.expander("Show Previous Classes"):
            if st_keyup:
                q = st_keyup(label=None, placeholder="Search past classes...", debounce=300, key="hist_search").lower()
            else:
                q = st.text_input("Search past classes...").lower()
            
            found_any = False
            for d in sorted(past_dates, reverse=True):
                classes = schedule_by_date[d]
                if q:
                    classes = [c for c in classes if q in c['DisplaySubject'].lower() or q in c['Faculty'].lower()]
                
                if not classes: continue
                found_any = True
                
                d_obj = datetime.strptime(d, "%Y-%m-%d")
                st.markdown(f'<div class="day-header">{d_obj.strftime("%d %B %Y, %A")}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="day-card" style="opacity:0.8;">', unsafe_allow_html=True)
                for c in classes:
                    # Logic for strikethrough/venue colors
                    venue, fac = str(c['Venue']), str(c['Faculty'])
                    ven_up, fac_up = venue.upper(), fac.upper()
                    
                    is_canc = "CANCELLED" in ven_up or "CANCELLED" in fac_up
                    is_post = "POSTPONED" in ven_up or "POSTPONED" in fac_up
                    
                    status_cls = "strikethrough" if (is_canc or is_post) else ""
                    ven_cls = "venue-changed" if (is_canc or is_post or c['Override']) else "venue"
                    
                    st.markdown(f"""
                    <div class="class-entry">
                        <div class="left"><div class="subject-name {status_cls}">{c['DisplaySubject']}</div></div>
                        <div class="meta">
                            <span class="time {status_cls}">{c['Time']}</span>
                            <span class="{ven_cls}">{venue}</span>
                            <span class="faculty {status_cls}">{fac}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            if not found_any and q: st.warning("No matches found.")

        # 8. Upcoming Classes (Main Cards)
        st.markdown('<div id="upcoming-anchor"></div>', unsafe_allow_html=True)
        if not future_dates:
            st.info("No upcoming classes found.")
        
        for d in future_dates:
            d_obj = datetime.strptime(d, "%Y-%m-%d")
            is_today = (d == today_str)
            today_cls = "today" if is_today else ""
            
            if is_today:
                st.markdown(f'<div class="day-card {today_cls}"><div class="today-badge">TODAY</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="day-card {today_cls}">', unsafe_allow_html=True)
                
            st.markdown(f'<div class="day-header">{d_obj.strftime("%d %B %Y, %A")}</div>', unsafe_allow_html=True)
            
            classes = schedule_by_date[d]
            if not classes:
                st.markdown('<div style="color:#94A3B8; font-style:italic;">No classes scheduled</div>', unsafe_allow_html=True)
            
            for c in classes:
                venue, fac = str(c['Venue']), str(c['Faculty'])
                ven_up, fac_up = venue.upper(), fac.upper()
                
                is_canc = "CANCELLED" in ven_up or "CANCELLED" in fac_up
                is_post = "POSTPONED" in ven_up or "POSTPONED" in fac_up
                is_prep = "PREPONED" in ven_up or "PREPONED" in fac_up
                
                status_cls = "strikethrough" if (is_canc or is_post or is_prep) else ""
                ven_cls = "venue-changed" if (is_canc or is_post or is_prep or c['Override']) else "venue"
                
                st.markdown(f"""
                <div class="class-entry">
                    <div class="left"><div class="subject-name {status_cls}">{c['DisplaySubject']}</div></div>
                    <div class="meta">
                        <span class="time {status_cls}">{c['Time']}</span>
                        <span class="{ven_cls}">{venue}</span>
                        <span class="faculty {status_cls}">{fac}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("_Made by Vishesh_")
