# --- (FIXED) Function to calculate and display stats ---
def calculate_and_display_stats():
    st.markdown("---") # Separator
    with st.expander("Sessions Taken till Now"):
        with st.spinner("Calculating session statistics..."):
            
            # --- THIS IS THE NEW, CORRECTED LOGIC ---
            
            # 1. Load the main schedule file
            all_schedules_df = load_and_clean_schedule(SCHEDULE_FILE_NAME) 
            if all_schedules_df.empty:
                st.warning("Could not load schedule file to calculate stats.")
                return

            local_tz = pytz.timezone(TIMEZONE)
            now_dt = datetime.now(local_tz)
            today_date = now_dt.date()
            
            class_counts = defaultdict(int)
            
            time_slots_map = {
                2: ("8:00AM", "9:00AM"), 3: ("9:10AM", "10:10AM"), 4: ("10:20AM", "11:20AM"), 5: ("11:30AM", "12:30PM"),
                6: ("12:30PM", "1:30PM"), 7: ("1:30PM", "2:30PM"), 8: ("2:40PM", "3:40PM"), 9: ("3:50PM", "4:50PM"),
                10: ("5:00PM", "6:00PM"), 11: ("6:10PM", "7:10PM"), 12: ("7:20PM", "8:20PM"), 13: ("8:30PM", "9:30PM")
            }
            
            normalized_course_map = {normalize_string(k): k for k in COURSE_DETAILS_MAP.keys()}
            
            # 1. Count classes from the main schedule
            for _, row in all_schedules_df.iterrows():
                class_date = row[0]
                
                if class_date > today_date:
                    continue # Skip all future dates

                for col_idx, (start_time_str, end_time_str) in time_slots_map.items():
                    # Check if the class has already happened
                    is_in_past = False
                    if class_date < today_date:
                        is_in_past = True
                    elif class_date == today_date:
                        try:
                            class_end_dt = local_tz.localize(pd.to_datetime(f"{class_date.strftime('%Y-%m-%d')} {end_time_str}"))
                            is_in_past = class_end_dt < now_dt
                        except Exception:
                            is_in_past = False
                    
                    if is_in_past:
                        cell_value = str(row[col_idx])
                        if cell_value and cell_value != 'nan':
                            normalized_cell = normalize_string(cell_value)
                            
                            for norm_name, orig_name in normalized_course_map.items():
                                if norm_name in normalized_cell:
                                    
                                    # --- CHECK FOR OVERRIDES ---
                                    is_overridden = False
                                    if class_date in DAY_SPECIFIC_OVERRIDES and norm_name in DAY_SPECIFIC_OVERRIDES[class_date]:
                                        override_details = DAY_SPECIFIC_OVERRIDES[class_date][norm_name]
                                        venue_text = override_details.get('Venue', '').upper()
                                        faculty_text = override_details.get('Faculty', '').upper()
                                        
                                        if "POSTPONED" in venue_text or "POSTPONED" in faculty_text or \
                                           "CANCELLED" in venue_text or "CANCELLED" in faculty_text or \
                                           "PREPONED" in venue_text or "PREPONED" in faculty_text:
                                            is_overridden = True # Don't count this class
                                            
                                    if not is_overridden:
                                        class_counts[orig_name] += 1

            # 2. Add classes from ADDITIONAL_CLASSES
            for added_class in ADDITIONAL_CLASSES:
                class_date = added_class['Date']
                if class_date > today_date:
                    continue # Skip future classes
                
                is_in_past = False
                if class_date < today_date:
                    is_in_past = True
                elif class_date == today_date:
                    try:
                        # Need to parse the time from the 'Time' string
                        _, end_time_str = added_class['Time'].split('-')
                        class_end_dt = local_tz.localize(pd.to_datetime(f"{class_date.strftime('%Y-%m-%d')} {end_time_str}"))
                        is_in_past = class_end_dt < now_dt
                    except Exception:
                        is_in_past = False
                
                if is_in_past:
                    # Check if this class is a valid subject
                    norm_name = normalize_string(added_class['Subject'])
                    if norm_name in normalized_course_map:
                        orig_name = normalized_course_map[norm_name]
                        class_counts[orig_name] += 1
            
            # --- End of new logic ---
            
            if not class_counts:
                st.info("No past classes were found to calculate statistics.")
                return

            st.markdown("This shows the total number of sessions held *to date*, accounting for all schedule changes.")
            
            # --- Grouping Logic ---
            grouped_counts = defaultdict(dict)
            for full_name, count in class_counts.items():
                match = re.match(r"(.*?)\((.*)\)", full_name)
                if match:
                    course_name = match.group(1)
                    section_name = match.group(2).replace("'", "") # Clean up 'C -> C
                else:
                    course_name = full_name
                    section_name = "Main" # For subjects like 'BS'
                
                grouped_counts[course_name][section_name] = count
            
            # --- Display Logic ---
            sorted_courses = sorted(grouped_counts.keys())
            midpoint = len(sorted_courses) // 2 + (len(sorted_courses) % 2)
            col1, col2 = st.columns(2)

            with col1:
                for course_name in sorted_courses[:midpoint]:
                    st.markdown(f"**{course_name}**")
                    sections = grouped_counts[course_name]
                    for section_name in sorted(sections.keys()):
                        count = sections[section_name]
                        if section_name == "Main":
                            st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;Total Sessions: {count}")
                        else:
                            st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;Section {section_name}: {count} sessions")
                    st.markdown("") # Add a little space

            with col2:
                for course_name in sorted_courses[midpoint:]:
                    st.markdown(f"**{course_name}**")
                    sections = grouped_counts[course_name]
                    for section_name in sorted(sections.keys()):
                        count = sections[section_name]
                        if section_name == "Main":
                            st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;Total Sessions: {count}")
                        else:
                            st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;Section {section_name}: {count} sessions")
                    st.markdown("") # Add a little space
