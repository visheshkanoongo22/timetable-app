import streamlit as st
import json
import re
from datetime import datetime, date, timedelta
import pytz
from collections import defaultdict
import gc
from ics import Calendar, Event

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

# --- CONFIGURATION ---
TIMEZONE = 'Asia/Kolkata'
SCHEDULE_END_DATE = "2026-03-25" 

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
    
    /* 1. REMOVE HUGE TOP WHITE SPACE (For Dashboard) */
    div.block-container {
        padding-top: 2rem !important;
        padding-bottom: 5rem !important;
    }

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
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
    
    /* UTILS & ALIGNMENT */
    .main-header { font-size: 2rem; font-weight: 800; text-align: center; margin-bottom: 0.5rem; line-height: 1.2; }
    .header-sub { text-align:center; color:var(--muted); margin-top:0rem; margin-bottom:1.5rem; font-size:0.95rem; }
    
    /* Center the Footer */
    div.stCaption { text-align: center !important; margin-top: 2rem; }

    /* WELCOME MESSAGE SPACING */
    .welcome-message { 
        margin-top: 0rem; 
        margin-bottom: 0.5rem; 
        font-size: 1rem; 
        color: var(--muted); 
    }
    .welcome-message strong { color: #ffffff; }

    /* INPUTS */
    .stTextInput>div>div>input {
        background: rgba(255,255,255,0.02) !important; color: #E2E8F0 !important;
        border: 1px solid rgba(255,255,255,0.06) !important; padding: 0.6rem !important; border-radius: 8px !important;
        text-align: left; /* Left Aligned Text */
    }
    .stTextInput label { display: flex; justify-content: flex-start; width: 100%; }

    /* BUTTONS */
    .stButton>button {
        width: 100%; border-radius: 8px; font-weight: 600;
        background-color: #0F172A !important; color: #FFFFFF !important; 
        border: 1px solid #334155 !important; background-image: none !important;
        padding: 0.4rem 0.8rem;
        display: flex; justify-content: center; align-items: center; 
    }
    .stButton>button:hover { border-color: #60A5FA !important; color: #60A5FA !important; }

    /* CARD DESIGN - COMPACT */
    .day-card {
        background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
        border-radius: 14px; 
        padding: 1rem; 
        margin-bottom: 1rem;
        border: 1px solid var(--glass-border); 
        position: relative; overflow: visible;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    .day-card.today {
        border: 2px solid var(--today-glow);
        box-shadow: 0 0 20px var(--today-glow-shadow);
    }
    .today-badge {
        position: absolute; top: -12px; right: 15px; 
        background: #5D5D5D; color: white; font-size: 0.65rem; font-weight: 800; 
        padding: 3px 8px; border-radius: 5px; text-transform: uppercase; 
        z-index: 10; box-shadow: 0 2px 8px rgba(0,0,0,0.5);
    }
    .day-header { 
        font-size: 1rem; font-weight: 700; color: #E2E8F0; 
        margin-bottom: 0.8rem; padding-bottom: 0.4rem; 
        border-bottom: 1px solid rgba(255,255,255,0.05); 
    }

    /* COMPACT CLASS ROW */
    .class-row {
        display: flex; 
        align-items: center; 
        justify-content: space-between;
        margin-bottom: 8px; 
        padding: 8px 10px; 
        background: rgba(255,255,255,0.02);
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.03);
    }
    .class-info-left {
        display: flex; 
        flex-direction: column; 
        gap: 1px;
        flex-grow: 1;
    }
    .subj-title { font-size: 0.95rem; font-weight: 700; color: #FFFFFF; }
    .faculty-name { font-size: 0.75rem; color: #94A3B8; font-weight: 500; }
    .meta-row { 
        display: flex; gap: 8px; 
        font-size: 0.75rem; 
        margin-top: 3px; 
        color: #CBD5E1; 
        font-family: monospace; 
    }
    
    .session-badge-container {
        display: flex; 
        flex-direction: column; 
        align-items: center; 
        justify-content: center;
        min-width: 55px; 
        margin-left: 8px;
        background: linear-gradient(135deg, rgba(96,165,250,0.1), rgba(129,140,248,0.1));
        border: 1px solid rgba(129,140,248,0.2);
        border-radius: 8px;
        padding: 6px 2px;
    }
    .session-num { font-size: 1.1rem; font-weight: 800; color: #60A5FA; line-height: 1; }
    .session-label { font-size: 0.55rem; text-transform: uppercase; color: #94A3B8; letter-spacing: 0.5px; margin-top: 2px; }

    /* STATES */
    .strikethrough { text-decoration: line-through; opacity: 0.5; }
    .venue-changed { color: #F87171 !important; font-weight: 700; }
    
    /* MENU */
    .menu-header { color: #38BDF8; font-weight: bold; text-transform: uppercase; font-size: 0.85em; margin-bottom: 4px; }
    
    @media (max-width: 600px) {
        .main-header { font-size: 1.5rem; }
        .day-card { padding: 0.8rem; }
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

    all_term_classes = []
    
    # 2. Gather ALL classes
    for cls in base_schedule:
        # RAW Subject from DB
        subj_raw = cls['Subject']
        subj_upper = subj_raw.upper()
        raw_disp = cls.get('DisplaySubject', '').upper()
        
        # 1. Determine if this subject is relevant to the student
        norm_subj = normalize(subj_raw)
        is_my_subject = norm_subj in my_subjects
        
        # 2. Check MC Variants (Strict Check)
        is_mc_variant = ("MC (AB)" in subj_upper) or ("MC (AS)" in subj_upper) or ("MC (RK)" in subj_upper)
        
        # If student has "MC" in their list, and this is a variant, allow it
        if "MC" in my_subjects and is_mc_variant:
            is_my_subject = True
            
        if not is_my_subject: continue

        # 3. Create Class Object
        d_obj = datetime.strptime(cls['Date'], "%Y-%m-%d").date()
        details = {'Venue': cls['Venue'], 'Faculty': cls['Faculty'], 'Time': cls['Time'], 'Override': False}
        
        cls_obj = cls.copy()
        
        # 4. Apply MC Special Logic (Overrides)
        if is_mc_variant:
            # Force Subject Name to MC for grouping
            cls_obj['DisplaySubject'] = "MC" 
            cls_obj['Subject'] = "MC" 
            
            # Force Faculty Name
            if "MC  (AS)" in subj_upper: details['Faculty'] = "Arvind Singh"
            elif "MC (AB)" in subj_upper: details['Faculty'] = "Anupam Bhatnagar"
            elif "MC (RK)" in subj_upper: details['Faculty'] = "Rajesh Kikani"
        else:
            # For non-MC classes, ensure DisplaySubject exists
            if 'DisplaySubject' not in cls_obj:
                cls_obj['DisplaySubject'] = cls_obj['Subject']

        # 5. Apply Day Overrides
        if d_obj in DAY_SPECIFIC_OVERRIDES:
            day_ov = DAY_SPECIFIC_OVERRIDES[d_obj]
            for ov_subj, ov_data in day_ov.items():
                # Check against the Normalized Subject
                current_subj_norm = normalize(cls_obj['Subject'])
                if normalize(ov_subj) == current_subj_norm:
                    if ov_data.get('Target_Time', cls['Time']) == cls['Time']:
                        details.update(ov_data)
                        if 'Venue' in ov_data or 'Time' in ov_data: details['Override'] = True
        
        cls_obj.update(details)
        all_term_classes.append(cls_obj)

    # 3. Add Additional Classes
    for ac in ADDITIONAL_CLASSES:
        norm_subj = normalize(ac['Subject'])
        if norm_subj in my_subjects:
            all_term_classes.append({
                "Date": ac['Date'].strftime("%Y-%m-%d"),
                "Time": ac['Time'],
                "Subject": norm_subj,
                "DisplaySubject": ac['Subject'],
                "Venue": ac.get('Venue', '-'),
                "Faculty": ac.get('Faculty', '-'),
                "Override": True
            })

    # 4. Sort Chronologically
    all_term_classes.sort(key=lambda x: (x['Date'], get_sort_key(x['Time'])))

    # 5. Assign Session Numbers
    subject_counters = defaultdict(int)
    final_processed_classes = []
    
    for cls in all_term_classes:
        v_upper = str(cls['Venue']).upper()
        is_cancelled = "CANCELLED" in v_upper or "POSTPONED" in v_upper
        
        if not is_cancelled:
            subject_counters[cls['DisplaySubject']] += 1
            cls['SessionNumber'] = subject_counters[cls['DisplaySubject']]
        else:
            cls['SessionNumber'] = "-"
            
        final_processed_classes.append(cls)

    return final_processed_classes, found_key

# --- STATS ---
@st.cache_data
def calculate_stats_from_schedule(classes_list, today_str):
    counts = defaultdict(int)
    for cls in classes_list:
        if cls['Date'] <= today_str:
            if cls['SessionNumber'] != "-":
                counts[cls['DisplaySubject']] += 1
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
            e.description = f"Faculty: {cls['Faculty']}\nSession: {cls.get('SessionNumber', '')}"
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

# --- UI CONTROLLER ---

if 'submitted' not in st.session_state: st.session_state.submitted = False
if 'roll_number' not in st.session_state: st.session_state.roll_number = ""

# --- PART A: LANDING PAGE (VISUALLY CENTERED) ---
if not st.session_state.submitted:
    # Use Padding to visually center, but allow scrolling
    st.markdown("""
    <style>
    div.block-container {
        display: block !important;
        padding-top: 15vh !important; /* Push down to visual center */
        padding-bottom: 5rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<p class="main-header">MBA Timetable Assistant</p>', unsafe_allow_html=True)
    st.markdown('<div class="header-sub"> Your Term VI Schedule</div>', unsafe_allow_html=True)
    
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

# --- PART B: DASHBOARD PAGE (TOP ALIGNED) ---
else:
    # Reset padding for dashboard view
    st.markdown("""
    <style>
    div.block-container {
        display: block; 
        padding-top: 2rem !important;
        padding-bottom: 5rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

    roll = st.session_state.roll_number
    
    c1, c2 = st.columns([3, 1], gap="small")
    with c1: 
        st.markdown(f"""<div class="welcome-message">Displaying schedule for: <strong>{roll}</strong></div>""", unsafe_allow_html=True)
    with c2:
        if st.button("Change Roll Number"):
            st.session_state.submitted = False
            st.session_state.roll_number = ""
            st.rerun()

    with st.spinner("Finding your schedule..."):
        all_classes_processed, db_key = get_hybrid_schedule(roll)

    if not all_classes_processed and not db_key:
        st.error(f"Roll Number '{roll}' not found in database.")
        with st.expander("Debug Info"):
            st.write(f"Searched for: {roll}")
            st.write(f"Sample DB Keys: {list(students_db.keys())[:5]}")
        if st.button("Go Back"):
            st.session_state.submitted = False
            st.rerun()
    else:
        # ICS Download
        ics_str = generate_ics_safe(all_classes_processed)
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
        for c in all_classes_processed:
            schedule_by_date[c['Date']].append(c)
        
        today_obj = get_ist_today()
        today_str = today_obj.strftime("%Y-%m-%d")
        
        # --- PAST CLASSES ---
        past_dates = sorted([d for d in schedule_by_date.keys() if d < today_str], reverse=True)
        with st.expander("Show Previous Classes"):
            q = st.text_input("Search past classes...").lower()
            found_any = False
            
            for d in past_dates:
                classes = schedule_by_date[d]
                if q:
                    classes = [c for c in classes if q in c['DisplaySubject'].lower() or q in c['Faculty'].lower()]
                
                if not classes: continue
                found_any = True
                
                d_obj_past = datetime.strptime(d, "%Y-%m-%d")
                rows_html = ""
                for c in classes:
                    venue, fac = str(c['Venue']), str(c['Faculty'])
                    ven_up, fac_up = venue.upper(), fac.upper()
                    is_canc = "CANCELLED" in ven_up or "CANCELLED" in fac_up
                    is_post = "POSTPONED" in ven_up or "POSTPONED" in fac_up
                    status_cls = "strikethrough" if (is_canc or is_post) else ""
                    ven_cls = "venue-changed" if (is_canc or is_post or c['Override']) else "venue"
                    
                    rows_html += f"""<div class="class-row"><div class="class-info-left"><div class="subj-title {status_cls}">{c['DisplaySubject']}</div><div class="faculty-name {status_cls}">{fac}</div><div class="meta-row"><span class="{status_cls}">{c['Time']}</span><span style="color: #475569;">|</span><span class="{ven_cls}">{venue}</span></div></div><div class="session-badge-container"><div class="session-num">{c['SessionNumber']}</div><div class="session-label">SESSION</div></div></div>"""
                
                st.markdown(f"""<div class="day-card" style="opacity:0.8;"><div class="day-header">{d_obj_past.strftime("%d %B %Y, %A")}</div>{rows_html}</div>""", unsafe_allow_html=True)

            if not found_any and q: st.warning("No matches found.")

        # --- UPCOMING CLASSES ---
        st.markdown('<div id="upcoming-anchor"></div>', unsafe_allow_html=True)
        
        end_date_obj = datetime.strptime(SCHEDULE_END_DATE, "%Y-%m-%d").date()
        days_to_display = (end_date_obj - today_obj).days + 1
        if days_to_display < 0: days_to_display = 0
        
        upcoming_dates = [today_obj + timedelta(days=i) for i in range(days_to_display)]
        
        for d_obj in upcoming_dates:
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
                    
                    rows_html += f"""<div class="class-row"><div class="class-info-left"><div class="subj-title {status_cls}">{c['DisplaySubject']}</div><div class="faculty-name {status_cls}">{fac}</div><div class="meta-row"><span class="{status_cls}">{c['Time']}</span><span style="color: #475569;">|</span><span class="{ven_cls}">{venue}</span></div></div><div class="session-badge-container"><div class="session-num">{c['SessionNumber']}</div><div class="session-label">SESSION</div></div></div>"""
            
            st.markdown(f"""<div class="day-card {today_cls}">{badge_html}<div class="day-header">{d_obj.strftime("%d %B %Y, %A")}</div>{rows_html}</div>""", unsafe_allow_html=True)

st.markdown("---")
st.caption("_Made by [Vishesh](https://www.linkedin.com/in/vishesh-kanoongo-8b192433b)_")
