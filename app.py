        # --- AUTO-SCROLL TO TODAY'S TIMETABLE (robust polling) ---
        # `today_anchor_id` is set while rendering upcoming_dates (e.g. "date-card-3").
        # If not set, fallback to first upcoming card if that exists.
        target_id = None
        if 'today_anchor_id' in locals() and today_anchor_id:
            target_id = today_anchor_id
        elif upcoming_dates:
            # fallback to first upcoming card id used in rendering loop
            target_id = "date-card-0"

        if target_id and not st.session_state.get('auto_scrolled', False):
            # Poll the DOM until the element exists (max ~20 attempts => ~5 seconds)
            st.markdown(f"""
                <script>
                (function() {{
                    const id = "{target_id}";
                    let attempts = 0;
                    const maxAttempts = 20;
                    const iv = setInterval(() => {{
                        const el = window.parent.document.getElementById(id);
                        if (el) {{
                            el.scrollIntoView({{behavior: 'smooth', block: 'start'}});
                            clearInterval(iv);
                        }}
                        attempts++;
                        if (attempts >= maxAttempts) {{
                            clearInterval(iv);
                        }}
                    }}, 250); // check every 250ms
                }})();
                </script>
            """, unsafe_allow_html=True)
            st.session_state.auto_scrolled = True
