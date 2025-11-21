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
import streamlit.runtime.caching as st_cache
import time 

# --- AUTO REFRESH EVERY 10 MINUTES (HARD REBOOT) ---
AUTO_REFRESH_INTERVAL = 10 * 60  # 10 minutes in seconds

# Store the start time in session_state
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

elapsed = time.time() - st.session_state.start_time

if elapsed > AUTO_REFRESH_INTERVAL:
    with st.spinner("🔄 Refreshing app to keep it fast and stable..."):
        st_cache.clear_cache()
        gc.collect()
        st.session_state.clear()  # Clears all stored state
        time.sleep(2)
        st.rerun()
# --- END NEW BLOCK ---


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

# --- DAY-SPECIFIC OVERRIDES & ADDITIONS ---
DAY_SPECIFIC_OVERRIDES = {
    date(2025, 11, 8): {
        'DC': {'Venue': '216'}, 'VALUC': {'Venue': '216'}, 'VALUD': {'Venue': '216'}, 'IMCB': {'Venue': '216'},
    },
    date(2025, 11, 10): {
        'B2BB': {'Venue': 'E1'}, 'B2BC': {'Venue': 'E1'}, 'DV&VSC': {'Venue': 'E2'},
        'DMB': {'Venue': '214'}, 'DMA': {'Venue': '214'}, 'OMSD': {'Venue': '214'},
    },
    date(2025, 11, 11): {
        'SMKTB': {'Venue': 'POSTPONED', 'Faculty': 'Session Postponed'}, 'IMCA': {'Venue': 'T3'}
    },
    date(2025, 11, 12): {
        'INBA': {'Venue': 'POSTPONED', 'Faculty': 'Session Postponed'}
    },
    date(2025, 11, 13): {
        'SMKTA': {'Venue': 'T7'},
        'BS':    {'Venue': 'T7'},
        'ANA':   {'Venue': 'T7'},
        'ANB':   {'Venue': 'T7'},
        'LSSA':  {'Venue': 'T1'},
        'B2BA':  {'Venue': 'E1'},
        'DVVSC': {'Venue': 'E2'},
        'OMSD':  {'Venue': 'T3'},
        'B2BB':  {'Venue': 'POSTPONED', 'Faculty': 'Session Postponed'}, 
        'B2BC':  {'Venue': 'POSTPONED', 'Faculty': 'Session Postponed'}, 
        'IMCA':  {'Venue': 'T3'},
    },
    date(2025, 11, 14): {
        'B2BB': {'Venue': 'CANCELLED', 'Faculty': 'Session Cancelled'}, 
        'B2BC': {'Venue': 'CANCELLED', 'Faculty': 'Session Cancelled'},
        'SCMB': {'Venue': 'T4'}, 
    },
    date(2025, 11, 15): {
        'DADM': {'Venue': 'POSTPONED', 'Faculty': 'Session Postponed'}, 
        'LSSA': {'Venue': 'E2'},
        'IMCA': {'Venue': 'T6'}, 
    },
    date(2025, 11, 16): { 
        'IMCB': {'Venue': 'T7'}, 
    },
    date(2025, 11, 17): {
        'DV&VSC': {'Venue': 'POSTPONED', 'Faculty': 'Session Postponed'},
        'B2BB':  {'Venue': 'E1'},
        'B2BC':  {'Venue': 'E1'},
        'B2BA':  {'Venue': 'E2'},
        'OMSD':  {'Venue': '214'},
        'TEOMA': {'Venue': '216'},
        'TEOMB': {'Venue': '216'},
    },
    date(2025, 11, 18): {
        'DV&VSD': {'Venue': 'CANCELLED', 'Faculty': 'Session Cancelled'},
    },
    date(2025, 11, 19): {
        'DV&VSD': {'Venue': 'CANCELLED', 'Faculty': 'Session Cancelled'},
        'DV&VSA': {'Venue': 'POSTPONED', 'Faculty': 'Session Postponed'}, 
        'SMKTA': {'Venue': 'POSTPONED', 'Faculty': 'Session Postponed'}, 
        'SMKTB': {'Venue': 'POSTPONED', 'Faculty': 'Session Postponed'}, 
        'VALUB': {'Time': '02:30-03:30PM'},
        'BS':    {'Venue': 'T4'},
    },
    date(2025, 11, 20): {
        'DV&VSC': {'Venue': 'POSTPONED', 'Faculty': 'Session Postponed'},
        'IMCA':   {'Venue': 'T3'}, 
        'IMCB':   {'Venue': 'T3'}, 
        'B2BB':   {'Venue': 'E2'}, 
        'B2BC':   {'Venue': 'E2'}, 
        'DMA':    {'Venue': 'T6'}, 
        'DMB':    {'Venue': 'T6'}, 
        'OMSD':   {'Venue': 'T3'}, 
        'ML&AIA': {'Venue': 'T7'},
        'SMKTB':  {'Venue': 'T7'},
        'B2BA':   {'Venue': 'T7'},
        'SMKTA':  {'Venue': 'POSTPONED', 'Faculty': 'Session Postponed'},
    },
    date(2025, 11, 21): {
        'DV&VSC': {'Venue': 'CANCELLED', 'Faculty': 'Session Cancelled'},
        'DRMC':   {'Venue': 'T7'},
        'B2BB':   {'Venue': 'E1'}, 
        'B2BC':   {'Venue': 'E1'}, 
        'B2BA':   {'Venue': 'E2'}, 
        'DMA':    {'Venue': 'T6'}, 
        'DMB':    {'Venue': 'T6'}, 
    },
    date(2025, 11, 22): {
        'DC':    {'Venue': '214'},
        'SMKTB': {'Venue': '214'},
        'IMCB':  {'Venue': '214'},
        'VALUC': {'Venue': 'POSTPONED', 'Faculty': 'Session Postponed'}, 
        'VALUD': {'Venue': 'POSTPONED', 'Faculty': 'Session Postponed'}, 
    },
    date(2025, 11, 24): {
        'DV&VSC': {'Venue': 'CANCELLED', 'Faculty': 'Session Cancelled'},
    },
    date(2025, 11, 28): {
        'VALUA': {'Venue': 'CANCELLED', 'Faculty': 'Session Cancelled'},
    },
    date(2025, 12, 5): {
        'VALUB': {'Venue': 'CANCELLED', 'Faculty': 'Session Cancelled'},
    },
    date(2025, 12, 12): {
        'VALUA': {'Venue': 'CANCELLED', 'Faculty': 'Session Cancelled'},
        'VALUB': {'Venue': 'CANCELLED', 'Faculty': 'Session Cancelled'},
    },
    date(2025, 12, 15): {
        'DRMC': {'Venue': 'PREPONED', 'Faculty': 'Session Preponed'}, 
    },
    date(2025, 12, 19): {
        'VALUA': {'Venue': 'CANCELLED', 'Faculty': 'Session Cancelled'},
        'VALUB': {'Venue': 'CANCELLED', 'Faculty': 'Session Cancelled'},
    }
}
ADDITIONAL_CLASSES = [
    {'Date': date(2025, 11, 8), 'Time': '10:20-11:20AM', 'Subject': 'SCM(A)', 'Faculty': 'Guest Session', 'Venue': 'Online'},
    {'Date': date(2025, 11, 8), 'Time': '10:20-11:20AM', 'Subject': 'SCM(B)', 'Faculty': '
