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

# 2. CONFIGURATION
SCHEDULE_FILE_NAME = 'schedule.xlsx'
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
    "DV&VS('C)": {'Faculty': 'Anand Kumar', 'Venue': 'E2'}, 'DV&VS(A)': {'Faculty': 'Somayya Madakam', 'Venue': 'E3'},
    'DV&VS(B)': {'Faculty': 'Somayya Madakam', 'Venue': 'E3'}, 'DV&VS(D)': {'Faculty': 'Anand Kumar', 'Venue': 'E2'},
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
st.set_page_config(page_title="Academic Timetable", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    :root {
        --primary-gradient: linear-gradient(135deg, #D6CC99 0%, #FDE5D4 100%);
        --secondary-gradient: linear-gradient(135deg, #445D48 0%, #5E3023 100%);
        --bg-light: #001524;
        --bg-card: rgba(255, 255, 255, 0.05);
        --text-primary: #FDE5D4;
        --text-secondary: #D6CC99;
        --accent: #445D48;
        --border-color: rgba(214, 204, 153, 0.2);
        --today-glow: rgba(214, 204, 153, 0.4);
        --almost-black: #001524;
        --rosy-creme: #FDE5D4;
        --almost-mint: #D6CC99;
        --olive-green: #445D48;
        --espresso: #5E3023;
    }

    .stApp {
        background: #001524;
        color: #FDE5D4;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    }
    
    .main .block-container {
        position: relative;
        z-index: 1;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .main-header {
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.02em;
        animation: fadeInDown 0.8s ease-out;
    }

    .header-sub {
        text-align: center;
        color: var(--text-primary);
        margin-bottom: 3rem;
        font-size: 1.1rem;
        font-weight: 300;
        opacity: 0.9;
        animation: fadeInDown 0.8s ease-out 0.1s both;
    }

    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
        font-size: 1rem !important;
        padding: 0.75rem 1rem !important;
        transition: all 0.3s ease !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: var(--accent) !important;
        background: rgba(255, 255, 255, 0.15) !important;
        box-shadow: 0 0 0 3px rgba(214, 204, 153, 0.3) !important;
    }

    .stTextInput > label {
        color: var(--text-secondary) !important;
        font-size: 0.9rem !important;
        margin-bottom: 0.5rem !important;
        font-weight: 500 !important;
    }

    div[data-testid="stForm"] {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 2rem;
        backdrop-filter: blur(10px);
        animation: fadeInUp 0.8s ease-out 0.2s both;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }

    .stButton > button {
        background: var(--secondary-gradient) !important;
        color: #FDE5D4 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 10px rgba(68, 93, 72, 0.4) !important;
        width: 100% !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(68, 93, 72, 0.5) !important;
    }

    .stButton > button:active {
        transform: translateY(0) !important;
    }

    .stDownloadButton > button {
        background: var(--primary-gradient) !important;
        color: #001524 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 10px rgba(214, 204, 153, 0.4) !important;
    }

    .stDownloadButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(214, 204, 153, 0.5) !important;
    }

    .day-card {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
        scroll-margin-top: 2rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
        position: relative;
    }

    .day-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
        border-color: rgba(214, 204, 153, 0.3);
    }

    .day-card.today {
        border-color: var(--accent);
        background: linear-gradient(135deg, rgba(214, 204, 153, 0.2), rgba(253, 229, 212, 0.1));
        box-shadow: 0 0 20px var(--today-glow), 0 4px 20px rgba(0, 0, 0, 0.4);
    }

    .today-badge {
        position: absolute;
        top: 1.5rem;
        right: 1.5rem;
        background: var(--primary-gradient);
        color: #001524;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        box-shadow: 0 2px 8px rgba(214, 204, 153, 0.3);
    }

    .day-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid var(--border-color);
    }

    .day-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #FDE5D4;
        margin-bottom: 0.25rem;
    }

    .day-date {
        color: #D6CC99;
        font-size: 0.9rem;
    }

    .class-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 0;
        border-bottom: 1px solid var(--border-color);
        transition: all 0.2s ease;
    }

    .class-item:last-child {
        border-bottom: none;
        padding-bottom: 0;
    }

    .class-item:hover {
        padding-left: 0.5rem;
    }

    .class-subject {
        font-size: 1.1rem;
        font-weight: 600;
        color: #FDE5D4;
        margin-bottom: 0.25rem;
    }

    .class-meta {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        gap: 0.25rem;
    }

    .class-time {
        font-weight: 500;
        color: #FDE5D4;
    }

    .class-venue, .class-faculty {
        font-size: 0.85rem;
        color: #D6CC99;
    }

    .section-title {
        font-size: 1.8rem;
        font-weight: 600;
        margin-bottom: 2rem;
        text-align: center;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .stExpander {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(214, 204, 153, 0.2);
        border-radius: 8px;
        margin-top: 1rem;
    }

    .stExpander > div > div > div > div {
        color: #D6CC99 !important;
    }

    div[data-testid="stMarkdownContainer"] a {
        color: #445D48 !important;
        font-weight: 500;
    }

    hr {
        border-color: rgba(214, 204, 153, 0.2) !important;
        margin: 2rem 0 !important;
    }

    h2, h3 {
        color: #FDE5D4 !important;
    }
    
    p, li, div {
        color: #FDE5D4 !important;
    }
    
    .stSpinner > div {
        border-top-color: #D6CC99 !important;
    }
    
    .stAlert {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(214, 204, 153, 0.2) !important;
        color: #FDE5D4 !important;
    }

    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
        }
        
        .class-item {
            flex-direction: column;
            align-items: flex-start;
            gap: 0.5rem;
        }
        
        .class-meta {
            align-items: flex-start;
        }
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">Academic Timetable</p>', unsafe_allow_html=True)
st.markdown('<div class="header-sub">Your personalized schedule, beautifully organized</div>', unsafe_allow_html=True)

master_schedule_df = load_and_clean_schedule(SCHEDULE_FILE_NAME)
student_data_map = get_all_student_data()

if not master_schedule_df.empty and student_data_map:
    with st.form("roll_number_form"):
        roll_number = st.text_input("Enter Your Roll Number", placeholder="e.g., 24MBA463").strip().upper()
        submitted = st.form_submit_button("Generate Timetable")

    if submitted and roll_number:
        if roll_number in student_data_map:
            student_info = student_data_map[roll_number]
            student_name, student_sections = student_info['name'], student_info['sections']
            
            with st.spinner(f'Finding classes for {student_name}...'):
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
                                    details = NORMALIZED_COURSE_DETAILS_MAP.get(norm_sec, {'Faculty': 'N/A', 'Venue': '-'})
                                    found_classes.append({
                                        "Date": date,
                                        "Day": day,
                                        "Time": time,
                                        "Subject": orig_sec,
                                        "Faculty": details.get('Faculty', 'N/A'),
                                        "Venue": details.get('Venue', '-')
                                    })

                found_classes = [dict(t) for t in {tuple(d.items()) for d in found_classes}]

            if found_classes:
                ics_content = generate_ics_content(found_classes)
                sanitized_name = re.sub(r'[^a-zA-Z0-9_]', '', str(student_name).replace(" ", "_")).upper()
                
                st.download_button(
                    label="Download Calendar File",
                    data=ics_content,
                    file_name=f"{sanitized_name}_Timetable.ics",
                    mime='text/calendar'
                )
                
                with st.expander("How to Import to Google Calendar", expanded=False):
                    st.markdown(f"""
                    1. Click the **'Download Calendar File'** button above to save the schedule.  
                    2. Go to the [**Google Calendar Import Page**]({GOOGLE_CALENDAR_IMPORT_LINK}).  
                    3. Under 'Import from computer', click **'Select file from your computer'**.  
                    4. Choose the `.ics` file you just downloaded.  
                    5. Click **'Import'** to add the events.
                    """)

                st.markdown("---")
                st.markdown('<h2 class="section-title">Your Weekly Schedule</h2>', unsafe_allow_html=True)

                schedule_by_date = defaultdict(list)
                for class_info in found_classes:
                    schedule_by_date[class_info['Date']].append(class_info)
                
                sorted_dates = sorted(schedule_by_date.keys())
                time_sorter = {time: i for i, time in enumerate(time_slots.values())}
                for date in sorted_dates:
                    schedule_by_date[date].sort(key=lambda x: time_sorter.get(x['Time'], 99))

                today = date.today()
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
                                <div class="today-badge">Today</div>
                                <div class="day-header">
                                    <div>
                                        <div class="day-title">{date_obj.strftime("%A")}</div>
                                        <div class="day-date">{date_obj.strftime("%B %d, %Y")}</div>
                                    </div>
                                </div>
                        ''', unsafe_allow_html=True)
                    else:
                        st.markdown(f'''
                            <div class="day-card {today_class}" id="{card_id}">
                                <div class="day-header">
                                    <div>
                                        <div class="day-title">{date_obj.strftime("%A")}</div>
                                        <div class="day-date">{date_obj.strftime("%B %d, %Y")}</div>
                                    </div>
                                </div>
                        ''', unsafe_allow_html=True)
                    
                    classes_today = schedule_by_date[date_obj]
                    for class_info in classes_today:
                        st.markdown(f'''
                            <div class="class-item">
                                <div>
                                    <div class="class-subject">{class_info["Subject"]}</div>
                                </div>
                                <div class="class-meta">
                                    <div class="class-time">{class_info["Time"]}</div>
                                    <div class="class-venue">{class_info["Venue"]}</div>
                                    <div class="class-faculty">{class_info["Faculty"]}</div>
                                </div>
                            </div>
                        ''', unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                
                if today_anchor_id:
                    components.html(f"""
                    <script>
                        function scrollToToday() {{
                            const todayCard = window.parent.document.getElementById('{today_anchor_id}');
                            if (todayCard) {{
                                todayCard.scrollIntoView({{behavior: 'smooth', block: 'center'}});
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
                
        elif submitted:
            st.error(f"Roll Number '{roll_number}' not found. Please check the number and try again.")
else:
    st.warning("Application is initializing or required data files are missing. Please wait or check the folder.")
