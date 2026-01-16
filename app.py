import streamlit as st
import json
import re
from datetime import datetime, date, timedelta
import pytz
from collections import defaultdict
import gc
from ics import Calendar, Event
import extra_streamlit_components as stx

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
SCHEDULE_END_DATE = "2026-01-18" 

# --- CSS STYLING ---
st.set_page_config(page_title="MBA Timetable", layout="centered", initial_sidebar_state="collapsed")

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
        border-radius: 14px; padding: 1.25rem; margin-bottom: 1.5rem;
        border: 1px solid var(--glass-border); 
        position: relative;
        overflow: visible;
        box-shadow: 0 8px 30px rgba(0,0,0,0.4);
    }
    .day-card.today {
        border: 2px solid var(--today-glow);
        box-shadow: 0 0 25px var(--today-glow-shadow);
    }
    .today-badge {
        position: absolute; 
        top: -14px; right: 20px; 
        background: #5D5D5D; 
        color: white; font-size: 0.7rem; font-weight: 800; 
        padding: 4px 10px; border-radius: 6px;
        letter-spacing: 0.5px; text-transform: uppercase; 
        z-index: 10; box-shadow: 0 2px 10px rgba(0,0,0,0.5);
    }
    .day-header { font-size: 1.15rem; font-weight: 700; color: #E2E8F0; margin-bottom: 0.8rem; }
    
    .class-entry {
        display:flex; flex-direction:row; align-items:center; justify-content:space-between;
        padding-top:0.75rem; padding-bottom:0.75rem; border-bottom:1px solid rgba(255,255,255,0.04);
    }
    .class-entry:last-child { border-bottom: none; padding-bottom: 0; }
    
    .left { display:flex; flex-direction:column; gap:0.2rem; }
    .subject-name { font-size:1.1rem; font-weight:700; margin:0; color: #FFFFFF; }
    .meta { text-align:right; min-width:140px; }
    .meta .time { display:block; font-weight:600; color:#fff; font-size:0.95rem; }
    .meta .venue, .meta .faculty { display:block; font-size:0.85rem; color:var(--muted); text-align: right;}
    .venue-changed { color: var(--venue-change-color) !important; font-weight: 600; }
    .strikethrough { text-decoration: line-through; opacity: 0.6; }
    
    .stTextInput>div>div>input {
        background: rgba(255,255,255,0.02) !important; color: #E2E8F0 !important;
        border: 1px solid rgba(255,255,255,0.06) !important; padding: 0.6rem !important; border-radius: 8px !important;
    }
    .stDownloadButton>button, div[data-testid="stForm"] button[kind="primary"] {
        background: linear-gradient(90deg, var(--accent-start), var(--accent-end)); 
        color: var(--bg); font-weight:700; padding: 0.5rem 0.9rem; border-radius:10px; border:none;
        box-shadow: 0 8px 20px rgba(96,165,250,0.1); width: 100%;
        transition: transform 0.18s ease, box-shadow 0.18s ease;
    }
    .stDownloadButton>button:hover, div[data-testid="stForm"] button[kind="primary"]:hover {
        transform: translateY(-3px); box-shadow: 0 14px 30px rgba(96,165,250,0.15);
    }
    .stButton>button {
        width: 100%; border-radius: 8px; font-weight: 600;
        background-color: #0F172A !important; 
        color: #FFFFFF !important; 
        border: 1px solid #334155 !important;
        background-image: none !important;
    }
    .stButton>button:hover { 
        border-color: #60A5FA !important; color: #60A5FA !important;
    }
    
    .menu-header { color: #38BDF8; font-weight: bold; text-transform: uppercase; font-size: 0.9em; margin-bottom: 5px; }
    div[data-testid="stMarkdownContainer"] ul { padding-left: 18px; margin-bottom: 10px; }
    div[data-testid="stMarkdownContainer"] li { margin-bottom: 2px; font-size: 0.9em; color: #E2E8F0; }

    @media (max-width: 600px) {
        .day-card { padding: 0.8rem; margin-bottom: 1rem; }
        .main-header { font-size: 1.6rem; }
        .header-sub { font-size: 0.8rem; margin-bottom: 1.5rem; }
        .day-header { font-size: 0.9rem; }
        .subject-name { font-size: 0.9rem; }
        .meta .time { font-size: 0.85rem; }
        .meta .venue, .meta .faculty { font-size: 0.75rem; }
        .stDownloadButton>button, div[data-testid="stForm"] button[kind="primary"], .stButton>button {
            padding: 0.4rem 0.8rem; font-size: 0.9rem;
        }
    }
</style>
"""
st.markdown(local_css_string, unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---
def get_ist_today():
    return datetime.now(pytz.timezone('Asia/Kolkata')).date()

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

# --- DATA LOADING ---
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

# --- HYBRID SCHEDULE ENGINE ---
def get_hybrid_schedule(roll_no):
    roll_clean = str(roll_no).strip().upper().replace(" ", "")
    my_subjects = set()
    found_key = None
    
    for db_roll, subjs in students_db.items():
        db_clean = str(db_roll).strip().upper().replace(" ", "")
        if (roll_clean == db_clean) or \
           (roll_clean in db_clean and db_clean.endswith(roll_clean)) or \
           (db_clean in roll_clean and roll_clean.endswith(db_clean)):
            my_subjects = set(subjs)
            found_key = db_roll
            break
            
    if not my_subjects: return [], None

    final_classes = []
    
    # Process Base Schedule
    for cls in base_schedule:
        if cls['Date'] > SCHEDULE_END_DATE: continue
        if cls['Subject'] not in my_subjects: continue
        
        d_obj = datetime.strptime(cls['Date'], "%Y-%m-%d").date()
        details = {'Venue': cls['Venue'], 'Faculty': cls['Faculty'], 'Time': cls['Time'], 'Override': False}
        
        if d_obj in DAY_SPECIFIC_OVERRIDES:
            day_ov = DAY_SPECIFIC_OVERRIDES[d_obj]
            for ov_subj, ov_data in day_ov.items():
                if normalize(ov_subj) in cls['Subject']:
                    if ov_data.get('Target_Time', cls['Time']) == cls['Time']:
                        details.update(ov_data)
                        if 'Venue' in ov_data or 'Time' in ov_data: details['Override'] = True
        
        cls_obj = cls.copy()
        cls_obj.update(details)
        final_classes.append(cls_obj)

    # 2. Additional Classes
    for ac in ADDITIONAL_CLASSES:
        norm_subj = normalize(ac['Subject'])
        if norm_subj in my_subjects:
            final_classes.append({
                "Date": ac['Date'].strftime("%Y-%m-%d"),
                "Time": ac['Time'],
                "Subject": norm_subj,
                "DisplaySubject": ac['Subject'],
                "Venue": ac.get('Venue', '-'),
                "Faculty": ac.get('Faculty', '-'),
                "Override": True
            })

    final_classes.sort(key=lambda x: (x['Date'], get_sort_key(x['Time'])))
    return final_classes, found_key

# --- STATS ---
@st.cache_data
def calculate_global_stats(today_str):
    if not base_schedule: return {}
    counts = defaultdict(int)
    
    for cls in base_schedule:
        if cls['Date'] > today_str: continue
        d_obj = datetime.strptime(cls['Date'], "%Y-%m-%d").date()
        is_cancelled = False
        if d_obj in DAY_SPECIFIC_OVERRIDES:
            day_ov = DAY_SPECIFIC_OVERRIDES[d_obj]
            for ov_subj, ov_data in day_ov.items():
                if normalize(ov_subj) in cls['Subject']:
                    if ov_data.get('Target_Time', cls['Time']) == cls['Time']:
                        v_txt = ov_data.get('Venue', '').upper()
                        if "CANCELLED" in v_txt or "POSTPONED" in v_txt or "PREPONED" in v_txt:
                            is_cancelled = True
        if not is_cancelled: counts[cls['DisplaySubject']] += 1

    for ac in ADDITIONAL_CLASSES:
        if ac['Date'].strftime("%Y-%m-%d") <= today_str: counts[ac['Subject']] += 1
    return counts

# --- ICS GENERATOR ---
def generate_ics_safe(classes):
    c = Calendar(creator="-//MBA Timetable//EN")
    local_tz = pytz.timezone('Asia/Kolkata')
    
    for cls in classes:
        venue = str(cls['Venue']).upper()
        if "CANCELLED" in venue or "POSTPONED" in venue: continue
        try:
            time_str = cls['Time']
            start_part, end_part = time_str.split('-')
            s_match = re.search(r'(\d+)(?::(\d+))?', start_part)
            e_match = re.search(r'(\d+)(?::(\d+))?', end_part)
            sh, sm = int(s_match.group(1)), int(s_match.group(2) or 0)
            eh, em = int(e_match.group(1)), int(e_match.group(2) or 0)
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

# --- MESS MENU ---
def render_mess_menu():
    if not MESS_MENU: return
    today = get_ist_today()
    week_dates = [today + timedelta(days=i) for i in range(7)]
    valid_dates = [d for d in week_dates if d in MESS_MENU]
    if not valid_dates: return

    with st.expander("🍽️ Mess Menu for the Week", expanded=False):
        opts = [d.strftime("%d %b") + (" (Today)" if d == today else "") for d in valid_dates]
        sel = st.radio("Select a day:", opts, index=0, horizontal=True)
        sel_date = valid_dates[opts.index(sel)]
        data = MESS_MENU[sel_date]
        def fmt(txt):
            if not txt or str(txt).lower() == 'nan': return "-"
            items = [i.strip() for i in str(txt).split('*') if i.strip()]
            return "\n".join([f"- {i}" for i in items])
        st.markdown(f"**Menu for {sel_date.strftime('%d %B %Y')}**")
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.markdown('<div class="menu-header">Breakfast</div>', unsafe_allow_html=True); st.markdown(fmt(data.get('Breakfast')))
        with c2: st.markdown('<div class="menu-header">Lunch</div>', unsafe_allow_html=True); st.markdown(fmt(data.get('Lunch')))
        with c3: st.markdown('<div class="menu-header">Hi-Tea</div>', unsafe_allow_html=True); st.markdown(fmt(data.get('Hi-Tea')))
        with c4: st.markdown('<div class="menu-header">Dinner</div>', unsafe_allow_html=True); st.markdown(fmt(data.get('Dinner')))

# --- COOKIE MANAGER SETUP ---
@st.cache_resource(experimental_allow_widgets=True)
def get_cookie_manager():
    return stx.CookieManager()

cookie_manager = get_cookie_manager()

# --- UI CONTROLLER ---

if 'submitted' not in st.session_state: st.session_state.submitted = False
if 'roll_number' not in st.session_state: st.session_state.roll_number = ""

# Check Cookie on Load
cookie_roll = cookie_manager.get(cookie="roll_number")
if not st.session_state.submitted and cookie_roll:
    st.session_state.roll_number = cookie_roll
    st.session_state.submitted = True

# --- PART A: LANDING PAGE ---
if not st.session_state.submitted:
    st.markdown('<p class="main-header">MBA Timetable Assistant</p>', unsafe_allow_html=True)
    st.markdown('<div class="header-sub"> Your Term VI Schedule</div>', unsafe_allow_html=True)

    st.markdown("""<div class="welcome-box">Welcome! Enter your roll number to get started!</strong>.</div>""", unsafe_allow_html=True)
    
    with st.form("roll_number_form"):
        roll_input = st.text_input("Enter your Roll Number:", placeholder="e.g., 463 (Just the last 3 digits)").strip().upper()
        if st.form_submit_button("Generate Timetable"):
            if roll_input.isdigit():
                if int(roll_input) < 100: roll_input = f"21BCM{roll_input}"
                elif int(roll_input) <= 999: roll_input = f"24MBA{roll_input}"
            
            # SET COOKIE ON LOGIN
            cookie_manager.set("roll_number", roll_input, expires_at=datetime.now() + timedelta(days=30))
            
            st.session_state.roll_number = roll_input
            st.session_state.submitted = True
            st.rerun()

    current_ist_str = get_ist_today().strftime("%Y-%m-%d")
    stats = calculate_global_stats(current_ist_str)
    with st.expander("Sessions Taken till Now"):
        if not stats:
            st.info("No past classes recorded.")
        else:
            st.markdown("Total sessions held *to date* (Global):")
            sc1, sc2 = st.columns(2)
            sorted_stats = sorted(stats.items())
            mid = len(sorted_stats) // 2 + (len(sorted_stats) % 2)
            with sc1:
                for k, v in sorted_stats[:mid]: st.markdown(f"**{k}**: {v}")
            with sc2:
                for k, v in sorted_stats[mid:]: st.markdown(f"**{k}**: {v}")

    render_mess_menu()

# --- PART B: DASHBOARD PAGE ---
else:
    roll = st.session_state.roll_number
    
    c1, c2 = st.columns([3, 1])
    with c1: st.markdown(f"""<div class="welcome-message">Displaying schedule for: <strong>{roll}</strong></div>""", unsafe_allow_html=True)
    with c2:
        if st.button("Change Roll Number"):
            # DELETE COOKIE ON LOGOUT
            cookie_manager.delete("roll_number")
            st.session_state.submitted = False
            st.session_state.roll_number = ""
            st.rerun()

    with st.spinner("Finding your schedule..."):
        schedule, db_key = get_hybrid_schedule(roll)

    if not schedule and not db_key:
        st.error(f"Roll Number '{roll}' not found in database.")
        with st.expander("Debug Info"):
            st.write(f"Searched for: {roll}")
            st.write(f"Sample DB Keys: {list(students_db.keys())[:5]}")
        if st.button("Go Back"):
            cookie_manager.delete("roll_number") # Also delete if invalid roll
            st.session_state.submitted = False
            st.rerun()
    else:
        ics_str = generate_ics_safe(schedule)
        sanitized_name = re.sub(r'[^a-zA-Z0-9_]', '', str(db_key).replace(" ", "_")).upper()
        with st.expander("Download & Import to Calendar"):
            st.download_button(
                label="Download .ics Calendar File",
                data=ics_str,
                file_name=f"{sanitized_name}_Timetable.ics",
                mime='text/calendar'
            )
            st.markdown("**How to Import:** Download the file, go to Google Calendar settings, select 'Import & Export', and upload the file.")

        schedule_by_date = defaultdict(list)
        for c in schedule: schedule_by_date[c['Date']].append(c)
        
        today_obj = get_ist_today()
        today_str = today_obj.strftime("%Y-%m-%d")
        
        past_dates = sorted([d for d in schedule_by_date.keys() if d < today_str], reverse=True)
        with st.expander("Show Previous Classes"):
            if st_keyup:
                q = st_keyup(label=None, placeholder="Search past classes...", debounce=300, key="hist_search").lower()
            else:
                q = st.text_input("Search past classes...").lower()
            
            found_any = False
            for d in past_dates:
                classes = schedule_by_date[d]
                if q:
                    classes = [c for c in classes if q in c['DisplaySubject'].lower() or q in c['Faculty'].lower()]
                
                if not classes: continue
                found_any = True
                
                d_obj = datetime.strptime(d, "%Y-%m-%d")
                rows_html = ""
                for c in classes:
                    venue, fac = str(c['Venue']), str(c['Faculty'])
                    ven_up, fac_up = venue.upper(), fac.upper()
                    is_canc = "CANCELLED" in ven_up or "CANCELLED" in fac_up
                    is_post = "POSTPONED" in ven_up or "POSTPONED" in fac_up
                    status_cls = "strikethrough" if (is_canc or is_post) else ""
                    ven_cls = "venue-changed" if (is_canc or is_post or c['Override']) else "venue"
                    
                    rows_html += f"""<div class="class-entry"><div class="left"><div class="subject-name {status_cls}">{c['DisplaySubject']}</div></div><div class="meta"><span class="time {status_cls}">{c['Time']}</span><span class="{ven_cls}">{venue}</span><span class="faculty {status_cls}">{fac}</span></div></div>"""
                
                st.markdown(f"""<div class="day-card" style="opacity:0.8;"><div class="day-header">{d_obj.strftime("%d %B %Y, %A")}</div>{rows_html}</div>""", unsafe_allow_html=True)

            if not found_any and q: st.warning("No matches found.")

        st.markdown('<div id="upcoming-anchor"></div>', unsafe_allow_html=True)
        upcoming_week = [today_obj + timedelta(days=i) for i in range(7)]
        
        for d_obj in upcoming_week:
            d_str = d_obj.strftime("%Y-%m-%d")
            
            if d_str > SCHEDULE_END_DATE: 
                break

            is_today = (d_obj == today_obj)
            today_cls = "today" if is_today else ""
            badge_html = '<div class="today-badge">TODAY</div>' if is_today else ''
            
            classes = schedule_by_date.get(d_str, [])
            rows_html = ""
            
            if not classes:
                rows_html = '<div style="color:#94A3B8; font-style:italic; padding:10px;">No classes scheduled</div>'
            else:
                for c in classes:
                    venue, fac = str(c['Venue']), str(c['Faculty'])
                    ven_up, fac_up = venue.upper(), fac.upper()
                    is_canc = "CANCELLED" in ven_up or "CANCELLED" in fac_up
                    is_post = "POSTPONED" in ven_up or "POSTPONED" in fac_up
                    is_prep = "PREPONED" in ven_up or "PREPONED" in fac_up
                    status_cls = "strikethrough" if (is_canc or is_post or is_prep) else ""
                    ven_cls = "venue-changed" if (is_canc or is_post or is_prep or c['Override']) else "venue"
                    
                    rows_html += f"""<div class="class-entry"><div class="left"><div class="subject-name {status_cls}">{c['DisplaySubject']}</div></div><div class="meta"><span class="time {status_cls}">{c['Time']}</span><span class="{ven_cls}">{venue}</span><span class="faculty {status_cls}">{fac}</span></div></div>"""
            
            st.markdown(f"""<div class="day-card {today_cls}">{badge_html}<div class="day-header">{d_obj.strftime("%d %B %Y, %A")}</div>{rows_html}</div>""", unsafe_allow_html=True)

st.markdown("---")
st.caption("_Made by Vishesh_")
