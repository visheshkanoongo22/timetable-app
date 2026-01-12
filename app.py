import streamlit as st
import json
import pandas as pd
from datetime import date, datetime
import re
from collections import defaultdict

# Optional: Keep mess menu if you want
try:
    from mess_menu import MESS_MENU
except ImportError:
    MESS_MENU = {}

st.set_page_config(page_title="MBA Timetable", layout="centered", initial_sidebar_state="collapsed")

# --- CSS ---
st.markdown("""
<style>
    .stApp { background-color: #0F172A; color: white; }
    .stTextInput input { background-color: #1E293B; color: white; border: 1px solid #334155; }
    .day-card { background: #1E293B; padding: 15px; border-radius: 10px; margin-bottom: 10px; border: 1px solid #334155; }
    .day-card.today { border: 2px solid #38BDF8; }
    .subject { font-weight: bold; font-size: 1.1em; color: white; }
    .meta { color: #94A3B8; font-size: 0.9em; }
    .menu-header { color: #38BDF8; font-weight: bold; text-transform: uppercase; font-size: 0.9em; }
    ul { padding-left: 18px; margin-bottom: 5px; }
    li { color: #E2E8F0; font-size: 0.9em; margin-bottom: 2px; }
</style>
""", unsafe_allow_html=True)

# --- LOAD DATA ---
@st.cache_data
def load_db():
    # Load the pre-calculated JSON files
    with open('db_students.json', 'r') as f:
        students = json.load(f)
    with open('db_schedule.json', 'r') as f:
        schedule = json.load(f)
    return students, schedule

try:
    students_db, master_schedule = load_db()
except FileNotFoundError:
    st.error("❌ Database files not found! Please upload db_students.json and db_schedule.json.")
    st.stop()

# --- HELPER: MESS MENU ---
def render_mess_menu():
    if not MESS_MENU: return
    today = date.today()
    
    # Simple Date Selector
    week_dates = [today + pd.Timedelta(days=i) for i in range(5)]
    valid_dates = [d for d in week_dates if d in MESS_MENU]
    if not valid_dates: return

    with st.expander("🍽️ Mess Menu", expanded=False):
        opts = [d.strftime("%d %b") + (" (Today)" if d == today else "") for d in valid_dates]
        sel = st.radio("Select Day", opts, horizontal=True, label_visibility="collapsed")
        
        sel_date = valid_dates[opts.index(sel)]
        data = MESS_MENU[sel_date]
        
        def fmt(txt):
            if not txt or str(txt) == 'nan': return "-"
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

# --- MAIN UI ---
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
    # --- SCHEDULE VIEW ---
    roll = st.session_state.roll
    
    # 1. Header
    c1, c2 = st.columns([3,1])
    with c1: st.subheader(f"Schedule: {roll}")
    with c2: 
        if st.button("Change"):
            st.session_state.submitted = False
            st.rerun()

    # 2. Logic: Find Matches
    # A. Get Student's Subjects
    my_subjects = set()
    
    # Exact Match
    if roll in students_db:
        my_subjects = set(students_db[roll])
    else:
        # Fuzzy Match (Suffix)
        for db_roll, subjs in students_db.items():
            if db_roll.endswith(roll):
                my_subjects = set(subjs)
                break
    
    if not my_subjects:
        st.error("Roll number not found in database.")
    else:
        # B. Filter Schedule
        my_classes = []
        today_str = date.today().strftime("%Y-%m-%d")
        
        for cls in master_schedule:
            # Only upcoming
            if cls['Date'] < today_str: continue
            
            # Check Subject Match
            # We compare the 'Subject' key (which is normalized in JSON) against our student's list
            # Note: student_db stores normalized names from generate_data.py
            if cls['Subject'] in my_subjects:
                my_classes.append(cls)
                
        # Sort
        my_classes.sort(key=lambda x: (x['Date'], x['Time']))
        
        # C. Render
        if not my_classes:
            st.info("No upcoming classes found.")
        else:
            for c in my_classes:
                # Format Date
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
    st.caption(f"v3.0 | Loaded {len(students_db)} students")
