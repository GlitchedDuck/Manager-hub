import streamlit as st
from datetime import datetime, timedelta

from data_utils import save_json, FILES
from ui_helpers import format_date, validate_nonempty, expand_notes

def page():
    st.title("📝 Check-in Notes")
    st.markdown("Record informal conversations between formal 1-2-1s")

    tab1, tab2 = st.tabs(["➕ Add Check-in", "📋 View Check-ins"])

    with tab1:
        st.subheader("Record a New Check-in")
        with st.form("checkin_form"):
            col1, col2 = st.columns(2)
            with col1:
                member = st.selectbox("Team Member", st.session_state.team_members)
                dt = st.date_input("Date", datetime.now())
                typ = st.selectbox("Type",
                    ["Quick Catch-up", "Progress Update", "Concern/Issue", "Wellbeing Check", "Training Discussion", "Other"]
                )
            with col2:
                tags = st.multiselect(
                    "Tags (optional)",
                    ["Performance", "Development", "Wellbeing", "Project", "Training", "Conflict", "Recognition"]
                )
                follow_up = st.checkbox("Requires Follow-up")
            notes = st.text_area("Notes", height=200)
            if st.form_submit_button("Save Check-in", use_container_width=True):
                if all([
                    validate_nonempty(member, "Team Member"),
                    validate_nonempty(typ, "Type"),
                    validate_nonempty(notes, "Notes")
                ]):
                    new_checkin = {
                        'id': len(st.session_state.checkins) + 1,
                        'team_member': member,
                        'date': dt.isoformat(),
                        'type': typ,
                        'notes': notes,
                        'tags': tags,
                        'follow_up': follow_up,
                        'created_at': datetime.now().isoformat()
                    }
                    st.session_state.checkins.append(new_checkin)
                    save_json(FILES['checkins'], st.session_state.checkins)
                    st.success(f"✅ Check-in recorded for {member}")
                    st.rerun()

    with tab2:
        st.subheader("All Check-ins")
        checkins = st.session_state.checkins
        for c in sorted(checkins, key=lambda x: x['date'], reverse=True):
            with st.expander(f"{c['team_member']} - {format_date(c['date'])} - {c['type']}"):
                st.write(c['notes'])
                if c.get('tags'):
                    st.markdown("**Tags:** " + ", ".join(c['tags']))
                if c.get('follow_up'):
                    st.warning("⚠️ Requires follow-up")
                expand_notes(c.get('notes', []))