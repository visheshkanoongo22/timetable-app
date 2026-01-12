import streamlit as st
import json
import pandas as pd
from datetime import date, datetime
import re

# --- 1. DYNAMIC IMPORTS (Live from GitHub) ---
# This allows you to edit these files online and see changes immediately
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

st.set_page_config(page_title="MBA Timetable", layout="centered", initial_sidebar_state="collapsed")

# --- 2. CSS STYLING ---
st.markdown("""
<style>
    .stApp { background-color: #0F172A; color: white; }
    .stTextInput input { background-color: #1E293B; color: white; border: 1px solid #334155; }
    .day-card { background: #1E293B; padding: 15px; border-radius: 10px; margin-bottom: 10px; border: 1px solid #334155; }
    .day-card.today { border: 2px solid #38BDF8; }
    .subject { font-weight: bold; font-size: 1.1em; color: white; }
    .meta { color: #94A3B8; font-size: 0.9em; }
    .menu-header { color: #38BDF8; font-weight: bold; text-transform: uppercase; font-size: 0.9em; margin-top: 5px;}
    ul { padding-left: 18px; margin-bottom: 5px; }
    li { color: #E2E8F0; font-size: 0.9em; margin-bottom: 2px; }
</style>
""", unsafe_allow_html=True)

# --- 3. LOGIC ---
def normalize(text):
    if not isinstance(text, str): return ""
    return text.replace(" ", "").replace("'", "").replace(".", "").upper()

@st.cache_data
def load_base_data():
    with open('db_students.json', 'r') as f:
        students = json.load(f)
    with open('db_schedule_base.json', 'r') as f:
        schedule = json.load(f)
    return students, schedule

try:
    students_db, base_schedule = load_base_data()
except FileNotFoundError:
    st.error("Data files missing. Please upload db_students.json and db_schedule_base.json")
    st.stop()

def get_schedule_with_overrides(roll_no):
    # 1. Identify Student
    roll_clean = str(roll_no).strip().upper().replace(" ", "")
    my_subjects = set()
    found_key = None
    
    # Robust Search
    for db_roll, subjs in students_db.items():
        db_clean = str(db_roll).strip().upper().replace(" ", "")
        if (roll_clean == db_clean) or \
           (roll_clean in db_clean and db_clean.endswith(roll_clean)) or \
           (db_clean in roll_clean and roll_clean.endswith(db_clean)):
            my_subjects = set(subjs)
            found_key = db_roll
            break
            
    if not my_subjects: return []

    # 2. Process Schedule (Apply Overrides Live)
    final_classes = []
    
    # A. Process Base Schedule
    for cls in base_schedule:
        # Check Subject Match (Normalized in JSON)
        if cls['Subject'] not in my_subjects: continue
        
        # Check Overrides (Live Logic)
        current_date = datetime.strptime(cls['Date'], "%Y-%m-%d").date()
        
        # Default State
        details = {
            'Venue': cls['Venue'],
            'Faculty': cls['Faculty'],
            'Time': cls['Time'],
            'Override': False
        }
        
        # Apply Override if exists
        if current_date in DAY_SPECIFIC_OVERRIDES:
            day_ov = DAY_SPECIFIC_OVERRIDES[current_date]
            # Check against overrides (Normalize keys to match JSON subject)
            for ov_subj, ov_data in day_ov.items():
                if normalize(ov_subj) in cls['Subject']: # Fuzzy match normalized strings
                    # Time Check
                    target = ov_data.get('Target_Time', cls['Time'])
                    if target == cls['Time']:
                        details.update(ov_data)
                        if 'Venue' in ov_data or 'Time' in ov_data: 
                            details['Override'] = True
        
        # Build Class Object
        cls_obj = cls.copy()
        cls_obj.update(details)
        final_classes.append(cls_obj)

    # B. Add Additional Classes (Live Logic)
    for ac in ADDITIONAL_CLASSES:
        norm_subj = normalize(ac['Subject'])
        if norm_subj in my_subjects:
            # Check Postponed/Cancelled keywords
            venue = ac.get('Venue', '').upper()
            is_ov = False
            # Usually we don't highlight these as venue changes, but you can if you want
            
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
    final_classes.sort(key=lambda x: (x['Date'], x['Time']))
    
    # Filter Past (Optional, usually good to show Today onwards)
    today_str = date.today().strftime("%Y-%m-%d")
    upcoming = [c for c in final_classes if c['Date'] >= today_str]
    
    return upcoming, found_key

# --- 4. HELPER: MESS MENU ---
def render_mess_menu():
    if not MESS_MENU: return
    today = date.today()
    week_dates = [today + pd.Timedelta(days=i) for i in range(5)]
    valid_dates = [d for d in week_dates if d in MESS_MENU]
    if not valid_dates: return

    with st.expander("🍽️ Mess Menu", expanded=False):
        opts = [d.strftime("%d %b") + (" (Today)" if d == today else "") for d in valid_dates]
        sel = st.radio("Select Day", opts, horizontal=True, label_visibility="collapsed")
        sel_date = valid_dates[opts.index(sel)]
        data = MESS_MENU[sel_date]
        
        def fmt(txt):
            if not txt or str(txt).lower() == 'nan': return "-"
            items = [i.strip() for i in str(txt).split('*') if i.strip()]
            return "\n".join([f"- {i}" for i in items])

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

# --- 5. UI ---
st.title("MBA Timetable")

if 'submitted' not in st.session_state: st.session_state.submitted = False
if 'roll' not in st.session_state: st.session_state.roll = ""

if not st.session_state.submitted:
    with st.form("login"):
        r = st.text_input("Enter Roll No (Last 3 digits):", placeholder="463").strip()
        if st.form_submit_button("View Schedule"):
            if r.isdigit():
                if int(r) < 100: r = f"21BCM{r}"
                elif int(r) <= 999: r = f"24MBA{r}"
            st.session_state.roll = r.upper()
            st.session_state.submitted = True
            st.rerun()
    render_mess_menu()

else:
    roll = st.session_state.roll
    c1, c2 = st.columns([3,1])
    with c1: st.subheader(f"Schedule: {roll}")
    with c2: 
        if st.button("Change"):
            st.session_state.submitted = False
            st.rerun()

    classes, db_key = get_schedule_with_overrides(roll)
    
    if not classes and not db_key:
        st.error("Roll number not found.")
        # Debug helper
        with st.expander("Debug"):
            st.write(f"Searching for: {roll}")
            st.write(f"Sample DB Keys: {list(students_db.keys())[:5]}")
    elif not classes:
        st.info(f"Student found ({db_key}), but no upcoming classes.")
    else:
        for c in classes:
            d_obj = datetime.strptime(c['Date'], "%Y-%m-%d").date()
            date_disp = d_obj.strftime("%d %b, %a")
            is_today = (d_obj == date.today())
            css = "today" if is_today else ""
            style = "color: #F87171;" if c['Override'] else ""
            
            st.markdown(f"""
            <div class="day-card {css}">
                <div style="display:flex; justify-content:space-between;">
                    <div>
                        <div class="meta">{date_disp} • {c['Time']}</div>
                        <div class="subject">{c['DisplaySubject']}</div>
                        <div class="meta">{c['Faculty']}</div>
                    </div>
                    <div style="text-align:right;">
                        <div class="meta">Venue</div>
                        <div style="{style} font-weight:bold;">{c['Venue']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown("---")
    st.caption(f"v3.1 Hybrid | {len(students_db)} students loaded")
