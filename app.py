# --- (FIXED) Function to load ALL schedules ---
@st.cache_data
def load_all_schedules(file_list):
    all_dfs = []
    for file_path in file_list:
        # Use the existing function, but suppress errors for old files
        df = load_and_clean_schedule(file_path, is_stats_file=True) 
        if not df.empty:
            all_dfs.append(df)
            
    if not all_dfs:
        return pd.DataFrame()
        
    combined_df = pd.concat(all_dfs)
    # --- REMOVED: drop_duplicates. We now sum all entries from all files.
    combined_df = combined_df.sort_values(by=[0]) # Sort by date
    return combined_df

# --- (FIXED) Function to calculate and display stats ---
def calculate_and_display_stats():
    st.markdown("---") # Separator
    with st.expander("Show Course Session Statistics"):
        with st.spinner("Calculating session statistics..."):
            all_schedules_df = load_all_schedules(SCHEDULE_FILES)
            
            if all_schedules_df.empty:
                st.warning("Could not load schedule files to calculate stats. Please check file names.")
                return

            local_tz = pytz.timezone(TIMEZONE)
            now_dt = datetime.now(local_tz)
            today_date = now_dt.date()
            
            class_counts = defaultdict(int)
            
            # Time slots mapping columns to end times for comparison
            time_slot_end_times = {
                2: "9:00AM", 3: "10:10AM", 4: "11:20AM", 5: "12:30PM",
                6: "1:30PM", 7: "2:30PM", 8: "3:40PM", 9: "4:50PM",
                10: "6:00PM", 11: "7:10PM", 12: "8:20PM", 13: "9:30PM"
            }
            
            # Create a normalized map of all known courses
            normalized_course_map = {normalize_string(k): k for k in COURSE_DETAILS_MAP.keys()}
            
            for _, row in all_schedules_df.iterrows():
                class_date = row[0]
                
                if class_date > today_date:
                    continue # Skip all future dates

                for col_idx, end_time_str in time_slot_end_times.items():
                    # Check if the class has already happened
                    if class_date < today_date:
                        # This class was on a previous day, so it definitely happened.
                        is_in_past = True
                    else:
                        # This class is today. We must check the time.
                        try:
                            class_end_dt = local_tz.localize(pd.to_datetime(f"{class_date.strftime('%Y-%m-%d')} {end_time_str}"))
                            is_in_past = class_end_dt < now_dt
                        except Exception:
                            is_in_past = False # Error parsing, skip
                    
                    if is_in_past:
                        cell_value = str(row[col_idx])
                        if cell_value and cell_value != 'nan':
                            normalized_cell = normalize_string(cell_value)
                            
                            # Check every known class against the cell
                            for norm_name, orig_name in normalized_course_map.items():
                                if norm_name in normalized_cell:
                                    class_counts[orig_name] += 1
            
            if not class_counts:
                st.info("No past classes were found to calculate statistics.")
                return

            # Display the stats in two columns
            st.markdown("This shows the total number of sessions held *to date*, compiled from all past and current schedule files.")
            sorted_counts = sorted(class_counts.items())
            midpoint = len(sorted_counts) // 2 + (len(sorted_counts) % 2)
            col1, col2 = st.columns(2)
            
            with col1:
                for subject, count in sorted_counts[:midpoint]:
                    st.markdown(f"**{subject}:** {count} sessions")
            
            with col2:
                for subject, count in sorted_counts[midpoint:]:
                    st.markdown(f"**{subject}:** {count} sessions")
