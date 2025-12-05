import streamlit as st
from datetime import datetime, timedelta

from data_utils import save_json, FILES
from ui_helpers import validate_nonempty, format_date, expand_notes

def page():
    st.title("✅ Action Tracking")
    st.markdown("Track actions from check-ins and 1-2-1s")

    tab1, tab2 = st.tabs(["➕ Add Action", "📋 Manage Actions"])
    actions = st.session_state.actions

    with tab1:
        with st.form("action_form"):
            col1, col2 = st.columns(2)
            with col1:
                member = st.selectbox("Team Member", st.session_state.team_members)
                action_text = st.text_input("Action")
                priority = st.selectbox("Priority", ["Low", "Medium", "High"])
            with col2:
                owner = st.selectbox("Owner", ["Manager", "Team Member", "Both"])
                due = st.date_input("Due Date", datetime.now() + timedelta(days=7))
                category = st.selectbox("Category", ["Development", "Performance", "Project", "Training", "Admin", "Other"])
            notes = st.text_area("Additional Notes (optional)", height=100)
            if st.form_submit_button("Create Action", use_container_width=True):
                valid = all([
                    validate_nonempty(member, "Team Member"),
                    validate_nonempty(action_text, "Action")
                ])
                if valid:
                    status = "Overdue" if due < datetime.now().date() else "Not Started"
                    new_action = {
                        'id': len(actions) + 1,
                        'team_member': member,
                        'action': action_text,
                        'priority': priority,
                        'owner': owner,
                        'due_date': due.isoformat(),
                        'category': category,
                        'notes': notes,
                        'status': status,
                        'created_at': datetime.now().isoformat(),
                        'updates': []
                    }
                    actions.append(new_action)
                    save_json(FILES['actions'], actions)
                    st.success(f"✅ Action created for {member}")
                    st.rerun()

    with tab2:
        # Update overdue status
        today = datetime.now().date()
        for action in actions:
            due = datetime.fromisoformat(action['due_date']).date()
            if action['status'] != 'Completed' and due < today:
                action['status'] = 'Overdue'

        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_member = st.selectbox("Team Member", ["All"] + st.session_state.team_members, key="action_filter")
        with col2:
            filter_status = st.selectbox("Status", ["All", "Not Started", "In Progress", "Overdue", "Completed"])
        with col3:
            filter_priority = st.selectbox("Priority", ["All", "High", "Medium", "Low"])

        filtered = actions.copy()
        if filter_member != "All":
            filtered = [a for a in filtered if a['team_member'] == filter_member]
        if filter_status != "All":
            filtered = [a for a in filtered if a['status'] == filter_status]
        if filter_priority != "All":
            filtered = [a for a in filtered if a['priority'] == filter_priority]

        if filtered:
            for action in sorted(filtered, key=lambda x: x['due_date']):
                status_emoji = {'Not Started': '⚪', 'In Progress': '🟡', 'Completed': '✅', 'Overdue': '🔴'}
                with st.expander(f"{status_emoji.get(action['status'], '⚪')} {action['team_member']} - {action['action']} (Due: {format_date(action['due_date'])})"):
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.markdown(f"**Action:** {action['action']}")
                        st.markdown(f"**Owner:** {action['owner']}")
                        st.markdown(f"**Category:** {action['category']}")
                        if action['notes']:
                            st.markdown(f"**Notes:** {action['notes']}")
                    with col2:
                        st.markdown(f"**Priority:** {action['priority']}")
                        st.markdown(f"**Due:** {format_date(action['due_date'])}")
                        st.markdown(f"**Status:** {action['status']}")
                    new_status = st.selectbox("Update Status", ["Not Started", "In Progress", "Completed"],
                        index=["Not Started", "In Progress", "Completed"].index(action['status'])
                            if action['status'] in ["Not Started", "In Progress", "Completed"] else 0,
                        key=f"status_{action['id']}")
                    update_note = st.text_input("Add Update (optional)", key=f"update_{action['id']}")
                    if st.button("Save Update", key=f"save_{action['id']}"):
                        action['status'] = new_status
                        if update_note:
                            action['updates'].append({'date': datetime.now().isoformat(), 'note': update_note})
                        save_json(FILES['actions'], actions)
                        st.success("Action updated!")
                        st.rerun()
                    expand_notes(action.get('updates', []))
        else:
            st.info("No actions found matching the filters")