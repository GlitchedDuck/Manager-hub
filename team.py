import streamlit as st
from data_utils import save_json, FILES
from ui_helpers import validate_nonempty

def page():
    st.title("👥 Team Members")
    st.subheader("Add or Remove Team Members")
    team = st.session_state.team_members
    st.write(f"Current: {', '.join(team)}")
    new_name = st.text_input("Add Team Member")
    if st.button("Add"):
        if validate_nonempty(new_name, "Name") and new_name not in team:
            team.append(new_name)
            save_json(FILES['team_members'], team)
            st.success(f"Added {new_name}")
            st.rerun()
    del_name = st.selectbox("Remove Member", [""] + team)
    if st.button("Remove") and del_name:
        st.session_state.team_members = [m for m in team if m != del_name]
        save_json(FILES['team_members'], st.session_state.team_members)
        st.success(f"Removed {del_name}")
        st.rerun()