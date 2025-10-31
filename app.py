import streamlit as st
import pandas as pd
import io
from datetime import datetime, date, timedelta
from ics import Calendar, Event

# ===============================
# APP HEADING & SETUP
# ===============================

st.set_page_config(page_title="Timetable to Calendar", layout="centered")

st.markdown("""
<h1 class="app-title">📅 Import Timetable to your Google Calendar</h1>
<p class="subtext">Upload your Excel timetable below and generate an .ics file to easily import into your Google Calendar.</p>
""", unsafe_allow_html=True)

# ===============================
# FILE UPLOAD SECTION
# ===============================

uploaded_file = st.file_uploader("Upload your timetable file (.xlsx)", type=["xlsx"])
roll_no = st.text_input("Enter your Roll Number", placeholder="e.g. 23MBA123")

generate_clicked = st.button("Generate Calendar File")

# ===============================
# FUNCTION TO PROCESS EXCEL
# ===============================

def process_excel(file):
    df = pd.read_excel(file)
    df.columns = [c.strip().capitalize() for c in df.columns]

    # Expecting columns: Subject, Date, Time, Venue, Faculty
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df.dropna(subset=["Date"], inplace=True)

    schedule_by_date = {}
    for _, row in df.iterrows():
        d = row["Date"].date()
        if d not in schedule_by_date:
            schedule_by_date[d] = []
        schedule_by_date[d].append({
            "Subject": row.get("Subject", ""),
            "Time": row.get("Time", ""),
            "Venue": row.get("Venue", ""),
            "Faculty": row.get("Faculty", "")
        })
    return schedule_by_date


# ===============================
# ICS FILE GENERATION FUNCTION
# ===============================

def generate_ics(schedule):
    cal = Calendar()
    for d, classes in schedule.items():
        for c in classes:
            event = Event()
            event.name = c["Subject"]
            event.begin = datetime.combine(d, datetime.strptime(c["Time"].split('-')[0].strip(), "%H:%M").time())
            event.end = datetime.combine(d, datetime.strptime(c["Time"].split('-')[1].strip(), "%H:%M").time())
            event.location = c["Venue"]
            event.description = f"Faculty: {c['Faculty']}"
            cal.events.add(event)
    return cal.serialize()


# ===============================
# MAIN LOGIC
# ===============================

if uploaded_file and generate_clicked:
    schedule_by_date = process_excel(uploaded_file)
    ics_data = generate_ics(schedule_by_date)
    st.success("✅ Your calendar file is ready!")
    st.download_button("📥 Download .ics file", data=ics_data, file_name=f"{roll_no}_timetable.ics", mime="text/calendar")

    # DISPLAY THE TIMETABLE
    st.markdown("---")
    st.markdown("### 🗓️ Your Schedule Preview")

    TODAY = date.today()

    for date_item in sorted(schedule_by_date.keys()):
        classes_today = schedule_by_date[date_item]
        is_today = (date_item == TODAY)
        card_class = "day-card today-card" if is_today else "day-card"
        card_id = f"day-{date_item.strftime('%Y%m%d')}"

        st.markdown(f"""
        <div id="{card_id}" class="{card_class}">
            <div class="day-header">
                <div class="date-badge">{date_item.strftime("%d %b")}</div>
                <div>{date_item.strftime("%A, %d %B %Y")}</div>
            </div>
        """, unsafe_allow_html=True)

        for class_info in classes_today:
            subject = class_info.get("Subject", "Unknown Subject")
            time_ = class_info.get("Time", "")
            venue = class_info.get("Venue", "")
            faculty = class_info.get("Faculty", "")

            st.markdown(f"""
            <div class="class-entry">
                <div class="left">
                    <div class="subject-name">{subject}</div>
                </div>
                <div class="meta">
                    <span class="time">🕒 {time_}</span>
                    <span class="venue">📍 {venue}</span>
                    <span class="faculty">🧑‍🏫 {faculty}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)


# ===============================
# CSS STYLING
# ===============================

st.markdown("""
<style>

body {
    background-color: #121212;
    color: #eaeaea;
    font-family: 'Inter', sans-serif;
}

.app-title {
    text-align: center;
    color: #00ffff;
    font-size: 2rem;
    margin-bottom: 0.2rem;
    margin-top: 0.5rem;
}

.subtext {
    text-align: center;
    color: #bbbbbb;
    margin-bottom: 2rem;
}

input, .stTextInput, .stButton>button {
    border-radius: 8px !important;
}

.stButton>button {
    background: linear-gradient(90deg, #007BFF, #00FFFF);
    color: black;
    font-weight: 600;
    border: none;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    transition: 0.3s;
}
.stButton>button:hover {
    transform: scale(1.05);
}

.day-card {
    background-color: rgba(30, 30, 30, 0.9);
    padding: 18px;
    border-radius: 12px;
    margin: 24px 0;
    color: #fff;
    box-shadow: 0 2px 6px rgba(0,0,0,0.4);
    position: relative;
    border-top: 1px solid rgba(255,255,255,0.1);
}

.day-card::before {
    content: "";
    display: block;
    height: 1px;
    background: linear-gradient(to right, rgba(0,255,255,0.5), rgba(255,255,255,0.05), rgba(0,255,255,0.5));
    margin-bottom: 10px;
}

.day-header {
    font-weight: 600;
    font-size: 1.1rem;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.date-badge {
    background: rgba(0,255,255,0.15);
    border: 1px solid rgba(0,255,255,0.4);
    border-radius: 6px;
    padding: 3px 8px;
    font-size: 0.9rem;
}

.class-entry {
    background-color: rgba(255,255,255,0.05);
    padding: 10px 12px;
    border-radius: 10px;
    margin-bottom: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.subject-name {
    font-weight: 600;
    font-size: 1rem;
    color: #00ffff;
}

.meta {
    display: flex;
    gap: 12px;
    font-size: 0.9rem;
    color: rgba(255,255,255,0.75);
}

.today-card {
    border: 2px solid #00ffff;
    box-shadow: 0 0 12px rgba(0,255,255,0.4);
    border-radius: 12px;
    scroll-margin-top: 60px;
}

.today-card::before {
    content: "⭐ Today";
    display: inline-block;
    background: linear-gradient(90deg, #00ffff, #007bff);
    color: #000;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 3px 8px;
    border-radius: 6px;
    margin-bottom: 8px;
}
</style>
""", unsafe_allow_html=True)


# ===============================
# AUTO-SCROLL TO TODAY
# ===============================

st.components.v1.html("""
<script>
setTimeout(() => {
  const todayCard = window.parent.document.querySelector('.today-card');
  if (todayCard) {
    todayCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }
}, 800);
</script>
""", height=0)
