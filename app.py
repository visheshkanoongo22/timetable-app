import streamlit as st
import os
import glob
import subprocess
import sys

st.set_page_config(page_title="Debug Mode")

st.title("🛠️ Diagnostic Mode")

# 1. CHECK PACKAGES
st.subheader("1. Package Check")
try:
    # Count installed packages
    result = subprocess.run([sys.executable, "-m", "pip", "list"], capture_output=True, text=True)
    packages = result.stdout.split('\n')
    count = len(packages)
    st.write(f"**Total Installed Packages:** {count}")
    
    if count > 30:
        st.error(f"❌ CRITICAL: You have {count} packages installed! This causes the crash.")
        st.write("Streamlit is likely still using the old 'Cached' environment.")
        with st.expander("View all packages"):
            st.text(result.stdout)
    else:
        st.success(f"✅ PASS: Environment is clean ({count} packages).")

except Exception as e:
    st.error(f"Could not run package check: {e}")

# 2. CHECK FILES
st.subheader("2. File Check")
files = glob.glob("*.xlsx")
if not files:
    st.error("❌ CRITICAL: No Excel (.xlsx) files found in the main folder!")
    st.write("Current Folder:", os.getcwd())
    st.write("All files:", os.listdir('.'))
else:
    st.success(f"✅ PASS: Found {len(files)} Excel files.")
    st.write(files)

# 3. MEMORY CHECK
st.subheader("3. Memory Test")
try:
    import pandas as pd
    st.success("✅ PASS: Pandas imported successfully.")
except ImportError:
    st.error("❌ FAIL: Pandas is not installed.")

st.button("If you can see this button, the App is NOT crashing!")
