import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json
import os
from pathlib import Path

# Page config
st.set_page_config(
    page_title="Manager Hub & TAG Training",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize data directory
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

# Initialize session state for data persistence
if 'checkins' not in st.session_state:
    st.session_state.checkins = []
if 'actions' not in st.session_state:
    st.session_state.actions = []
if 'training_plans' not in st.session_state:
    st.session_state.training_plans = []
if 'training_matrix' not in st.session_state:
    st.session_state.training_matrix = []
if 'sytner_bookings' not in st.session_state:
    st.session_state.sytner_bookings = []
if 'learning_resources' not in st.session_state:
    st.session_state.learning_resources = []
if 'team_members' not in st.session_state:
    st.session_state.team_members = ['Alice Johnson', 'Bob Smith', 'Carol Williams', 'David Brown']

# Load data from JSON files if they exist
def load_data():
    try:
        files = {
            'checkins': 'checkins.json',
            'actions': 'actions.json',
            'training_plans': 'training_plans.json',
            'training_matrix': 'training_matrix.json',
            'sytner_bookings': 'sytner_bookings.json',
            'learning_resources': 'learning_resources.json'
        }
        
        for key, filename in files.items():
            file_path = DATA_DIR / filename
            if file_path.exists():
                with open(file_path, 'r') as f:
                    st.session_state[key] = json.load(f)
    except Exception as e:
        st.error(f"Error loading data: {e}")

# Save data to JSON files
def save_data():
    try:
        files = {
            'checkins': 'checkins.json',
            'actions': 'actions.json',
            'training_plans': 'training_plans.json',
            'training_matrix': 'training_matrix.json',
            'sytner_bookings': 'sytner_bookings.json',
            'learning_resources': 'learning_resources.json'
        }
        
        for key, filename in files.items():
            with open(DATA_DIR / filename, 'w') as f:
                json.dump(st.session_state[key], f, indent=2)
    except Exception as e:
        st.error(f"Error saving data: {e}")

# Load data on startup
load_data()

# Sidebar navigation
st.sidebar.title("👥 Manager Hub & TAG Training")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    [
        "📊 Dashboard",
        "📝 Check-in Notes", 
        "✅ Actions",
        "🎓 TAG Training Hub",
        "📋 Training Matrix",
        "🏢 Sytner Training",
        "📚 Learning Resources",
        "📈 Reports"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Quick Stats")
total_actions = len([a for a in st.session_state.actions if a['status'] != 'Completed'])
overdue_actions = len([a for a in st.session_state.actions if a['status'] == 'Overdue'])
active_training = len([t for t in st.session_state.training_plans if t['status'] == 'In Progress'])
upcoming_sytner = len([s for s in st.session_state.sytner_bookings 
                       if datetime.fromisoformat(s['start_date']).date() >= datetime.now().date()
                       and s['status'] != 'Completed'])

st.sidebar.metric("Active Actions", total_actions)
st.sidebar.metric("Overdue Actions", overdue_actions, delta=-overdue_actions if overdue_actions > 0 else 0)
st.sidebar.metric("Active Training", active_training)
st.sidebar.metric("Upcoming Sytner", upcoming_sytner)
# ============================================
# DASHBOARD PAGE
# ============================================
if page == "📊 Dashboard":
    st.title("📊 Manager Dashboard")
    st.markdown("### Your Team Overview")
    
    # Key metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Team Members", len(st.session_state.team_members))
    
    with col2:
        recent_checkins = len([c for c in st.session_state.checkins 
                              if (datetime.now() - datetime.fromisoformat(c['date'])).days <= 7])
        st.metric("Check-ins (7d)", recent_checkins)
    
    with col3:
        st.metric("Active Actions", total_actions)
    
    with col4:
        st.metric("Active Training", active_training)
    
    with col5:
        st.metric("Sytner Bookings", upcoming_sytner)
    
    st.markdown("---")
    
    # Two column layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔔 Recent Check-ins")
        if st.session_state.checkins:
            sorted_checkins = sorted(st.session_state.checkins, 
                                   key=lambda x: x['date'], reverse=True)[:5]
            for checkin in sorted_checkins:
                with st.expander(f"{checkin['team_member']} - {checkin['date']}"):
                    st.write(f"**Type:** {checkin['type']}")
                    st.write(checkin['notes'])
        else:
            st.info("No check-ins recorded yet")
        
        st.subheader("📚 Recent Learning Activity")
        if st.session_state.learning_resources:
            recent_resources = sorted(st.session_state.learning_resources,
                                    key=lambda x: x.get('assigned_date', ''), reverse=True)[:3]
            for resource in recent_resources:
                status_emoji = "✅" if resource['status'] == 'Completed' else "📖"
                st.markdown(f"{status_emoji} **{resource['team_member']}** - {resource['title']}")
                st.caption(f"Type: {resource['type']}")
        else:
            st.info("No learning resources assigned yet")
    
    with col2:
        st.subheader("⚠️ Actions Requiring Attention")
        if st.session_state.actions:
            priority_actions = [a for a in st.session_state.actions 
                              if a['status'] in ['Not Started', 'Overdue']]
            priority_actions = sorted(priority_actions, key=lambda x: x['due_date'])[:5]
            
            if priority_actions:
                for action in priority_actions:
                    status_color = "🔴" if action['status'] == 'Overdue' else "🟡"
                    st.markdown(f"{status_color} **{action['team_member']}** - {action['action']}")
                    st.caption(f"Due: {action['due_date']} | Priority: {action['priority']}")
            else:
                st.success("All actions are on track!")
        else:
            st.info("No actions tracked yet")
        
        st.subheader("🏢 Upcoming Sytner Training")
        if st.session_state.sytner_bookings:
            upcoming = [s for s in st.session_state.sytner_bookings
                       if datetime.fromisoformat(s['start_date']).date() >= datetime.now().date()
                       and s['status'] != 'Completed']
            upcoming = sorted(upcoming, key=lambda x: x['start_date'])[:3]
            
            if upcoming:
                for booking in upcoming:
                    st.markdown(f"📅 **{booking['team_member']}** - {booking['course_name']}")
                    st.caption(f"Date: {booking['start_date']} | Location: {booking['location']}")
            else:
                st.info("No upcoming Sytner training")
        else:
            st.info("No Sytner training booked yet")
    
    st.markdown("---")
    
    # Training Matrix Overview
    st.subheader("📋 Training Matrix Completion Overview")
    if st.session_state.training_matrix:
        matrix_data = []
        for member in st.session_state.team_members:
            member_matrix = [m for m in st.session_state.training_matrix if m['team_member'] == member]
            if member_matrix:
                completed = len([m for m in member_matrix if m['completed']])
                total = len(member_matrix)
                percentage = (completed / total * 100) if total > 0 else 0
                matrix_data.append({
                    'Team Member': member,
                    'Completed': completed,
                    'Total': total,
                    'Progress': f"{percentage:.0f}%"
                })
        
        if matrix_data:
            df = pd.DataFrame(matrix_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Visual progress bars
            for item in matrix_data:
                completed = item['Completed']
                total = item['Total']
                percentage = (completed / total * 100) if total > 0 else 0
                st.progress(percentage / 100, text=f"{item['Team Member']}: {completed}/{total} skills")
    else:
        st.info("No training matrix data yet")
      # ============================================
# CHECK-IN NOTES PAGE
# ============================================
elif page == "📝 Check-in Notes":
    st.title("📝 Check-in Notes")
    st.markdown("Record informal check-ins and conversations between formal 1-2-1s")
    
    tab1, tab2 = st.tabs(["➕ Add Check-in", "📋 View Check-ins"])
    
    with tab1:
        st.subheader("Record a New Check-in")
        
        with st.form("checkin_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                team_member = st.selectbox("Team Member", st.session_state.team_members)
                checkin_date = st.date_input("Date", datetime.now())
                checkin_type = st.selectbox(
                    "Type",
                    ["Quick Catch-up", "Progress Update", "Concern/Issue", "Wellbeing Check", "Training Discussion", "Other"]
                )
            
            with col2:
                tags = st.multiselect(
                    "Tags (optional)",
                    ["Performance", "Development", "Wellbeing", "Project", "Training", "Conflict", "Recognition"]
                )
                follow_up = st.checkbox("Requires Follow-up")
            
            notes = st.text_area("Notes", height=200, 
                                placeholder="Record key points from your conversation...")
            
            submitted = st.form_submit_button("Save Check-in", use_container_width=True)
            
            if submitted:
                new_checkin = {
                    'id': len(st.session_state.checkins) + 1,
                    'team_member': team_member,
                    'date': checkin_date.isoformat(),
                    'type': checkin_type,
                    'notes': notes,
                    'tags': tags,
                    'follow_up': follow_up,
                    'created_at': datetime.now().isoformat()
                }
                st.session_state.checkins.append(new_checkin)
                save_data()
                st.success(f"✅ Check-in recorded for {team_member}")
                st.rerun()
    
    with tab2:
        st.subheader("Check-in History")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_member = st.selectbox("Filter by Team Member", ["All"] + st.session_state.team_members)
        with col2:
            filter_type = st.selectbox("Filter by Type", ["All", "Quick Catch-up", "Progress Update", "Concern/Issue", "Wellbeing Check", "Training Discussion", "Other"])
        with col3:
            filter_days = st.selectbox("Time Period", ["Last 7 days", "Last 30 days", "Last 90 days", "All Time"])
        
        filtered_checkins = st.session_state.checkins.copy()
        
        if filter_member != "All":
            filtered_checkins = [c for c in filtered_checkins if c['team_member'] == filter_member]
        
        if filter_type != "All":
            filtered_checkins = [c for c in filtered_checkins if c['type'] == filter_type]
        
        if filter_days != "All Time":
            days_map = {"Last 7 days": 7, "Last 30 days": 30, "Last 90 days": 90}
            days = days_map[filter_days]
            cutoff_date = datetime.now() - timedelta(days=days)
            filtered_checkins = [c for c in filtered_checkins 
                               if datetime.fromisoformat(c['date']) >= cutoff_date]
        
        if filtered_checkins:
            sorted_checkins = sorted(filtered_checkins, key=lambda x: x['date'], reverse=True)
            st.markdown(f"**{len(sorted_checkins)} check-in(s) found**")
            
            for checkin in sorted_checkins:
                with st.expander(f"{'🔔' if checkin.get('follow_up') else '📝'} {checkin['team_member']} - {checkin['date']} - {checkin['type']}"):
                    st.write(checkin['notes'])
                    if checkin.get('tags'):
                        st.markdown("**Tags:** " + ", ".join(checkin['tags']))
                    if checkin.get('follow_up'):
                        st.warning("⚠️ Requires follow-up")
        else:
            st.info("No check-ins found matching the filters")

# ============================================
# ACTIONS PAGE
# ============================================
elif page == "✅ Actions":
    st.title("✅ Action Tracking")
    st.markdown("Track actions and follow-ups from check-ins and 1-2-1s")
    
    tab1, tab2 = st.tabs(["➕ Add Action", "📋 Manage Actions"])
    
    with tab1:
        with st.form("action_form"):
            col1, col2 = st.columns(2)
            with col1:
                action_member = st.selectbox("Team Member", st.session_state.team_members)
                action_text = st.text_input("Action")
                action_priority = st.selectbox("Priority", ["Low", "Medium", "High"])
            with col2:
                action_owner = st.selectbox("Owner", ["Manager", "Team Member", "Both"])
                action_due = st.date_input("Due Date", datetime.now() + timedelta(days=7))
                action_category = st.selectbox("Category", ["Development", "Performance", "Project", "Training", "Admin", "Other"])
            
            action_notes = st.text_area("Additional Notes (optional)", height=100)
            submitted = st.form_submit_button("Create Action", use_container_width=True)
            
            if submitted:
                status = "Overdue" if action_due < datetime.now().date() else "Not Started"
                new_action = {
                    'id': len(st.session_state.actions) + 1,
                    'team_member': action_member,
                    'action': action_text,
                    'priority': action_priority,
                    'owner': action_owner,
                    'due_date': action_due.isoformat(),
                    'category': action_category,
                    'notes': action_notes,
                    'status': status,
                    'created_at': datetime.now().isoformat(),
                    'updates': []
                }
                st.session_state.actions.append(new_action)
                save_data()
                st.success(f"✅ Action created for {action_member}")
                st.rerun()
    
    with tab2:
        for action in st.session_state.actions:
            if action['status'] != 'Completed':
                due_date = datetime.fromisoformat(action['due_date']).date()
                if due_date < datetime.now().date():
                    action['status'] = 'Overdue'
        
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_action_member = st.selectbox("Team Member", ["All"] + st.session_state.team_members, key="action_filter")
        with col2:
            filter_status = st.selectbox("Status", ["All", "Not Started", "In Progress", "Overdue", "Completed"])
        with col3:
            filter_priority = st.selectbox("Priority", ["All", "High", "Medium", "Low"])
        
        filtered_actions = st.session_state.actions.copy()
        if filter_action_member != "All":
            filtered_actions = [a for a in filtered_actions if a['team_member'] == filter_action_member]
        if filter_status != "All":
            filtered_actions = [a for a in filtered_actions if a['status'] == filter_status]
        if filter_priority != "All":
            filtered_actions = [a for a in filtered_actions if a['priority'] == filter_priority]
        
        if filtered_actions:
            sorted_actions = sorted(filtered_actions, key=lambda x: x['due_date'])
            st.markdown(f"**{len(sorted_actions)} action(s) found**")
            
            for action in sorted_actions:
                status_emoji = {'Not Started': '⚪', 'In Progress': '🟡', 'Completed': '✅', 'Overdue': '🔴'}
                with st.expander(f"{status_emoji.get(action['status'], '⚪')} {action['team_member']} - {action['action']} (Due: {action['due_date']})"):
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.markdown(f"**Action:** {action['action']}")
                        st.markdown(f"**Owner:** {action['owner']}")
                        st.markdown(f"**Category:** {action['category']}")
                        if action['notes']:
                            st.markdown(f"**Notes:** {action['notes']}")
                    with col2:
                        st.markdown(f"**Priority:** {action['priority']}")
                        st.markdown(f"**Due:** {action['due_date']}")
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
                        save_data()
                        st.success("Action updated!")
                        st.rerun()
        else:
            st.info("No actions found matching the filters")
          # ============================================
# TAG TRAINING HUB PAGE
# ============================================
elif page == "🎓 TAG Training Hub":
    st.title("🎓 TAG Training Hub (Training and Guidance)")
    st.markdown("Comprehensive training management for your team")
    
    tab1, tab2, tab3 = st.tabs(["➕ Create Plan", "📋 Manage Plans", "📊 Team Overview"])
    
    with tab1:
        st.subheader("Create Individual Training Plan")
        
        with st.form("training_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                training_member = st.selectbox("Team Member", st.session_state.team_members)
                course_name = st.text_input("Training/Course Name")
                training_type = st.selectbox(
                    "Type",
                    ["Online Course", "In-Person Training", "Certification", "Mentoring", 
                     "Self-Study", "Sytner Training", "On-the-Job", "Other"]
                )
                start_date = st.date_input("Start Date", datetime.now())
            
            with col2:
                priority = st.selectbox("Priority", ["Low", "Medium", "High"], key="training_priority")
                end_date = st.date_input("Target Completion", datetime.now() + timedelta(days=90))
                cost = st.number_input("Estimated Cost (£)", min_value=0.0, step=50.0, value=0.0)
                approval_required = st.checkbox("Requires Manager Approval")
            
            objectives = st.text_area("Learning Objectives", height=100,
                placeholder="What skills or knowledge should be gained from this training?")
            
            business_case = st.text_area("Business Case / Justification", height=80,
                placeholder="How does this training support role requirements or career development?")
            
            submitted = st.form_submit_button("Create Training Plan", use_container_width=True)
            
            if submitted:
                new_training = {
                    'id': len(st.session_state.training_plans) + 1,
                    'team_member': training_member,
                    'course_name': course_name,
                    'type': training_type,
                    'start_date': start_date.isoformat(),
                    'end_date': end_date.isoformat(),
                    'priority': priority,
                    'objectives': objectives,
                    'business_case': business_case,
                    'cost': cost,
                    'approval_required': approval_required,
                    'approval_status': 'Pending' if approval_required else 'Approved',
                    'status': 'Not Started',
                    'progress': 0,
                    'created_at': datetime.now().isoformat(),
                    'notes': []
                }
                st.session_state.training_plans.append(new_training)
                save_data()
                st.success(f"✅ Training plan created for {training_member}")
                st.rerun()
    
    with tab2:
        st.subheader("Manage Training Plans")
        
        col1, col2 = st.columns(2)
        with col1:
            filter_training_member = st.selectbox("Filter by Team Member", ["All"] + st.session_state.team_members, key="training_filter")
        with col2:
            filter_training_status = st.selectbox("Filter by Status", ["All", "Not Started", "In Progress", "Completed", "Cancelled"])
        
        filtered_training = st.session_state.training_plans.copy()
        if filter_training_member != "All":
            filtered_training = [t for t in filtered_training if t['team_member'] == filter_training_member]
        if filter_training_status != "All":
            filtered_training = [t for t in filtered_training if t['status'] == filter_training_status]
        
        if filtered_training:
            total_cost = sum(t.get('cost', 0) for t in filtered_training)
            st.info(f"📊 {len(filtered_training)} training plan(s) | Total Cost: £{total_cost:,.2f}")
            
            for training in filtered_training:
                status_emoji = {'Not Started': '⚪', 'In Progress': '🟡', 'Completed': '✅', 'Cancelled': '❌'}
                approval_badge = ""
                if training.get('approval_required'):
                    if training.get('approval_status') == 'Pending':
                        approval_badge = " 🟡 Pending Approval"
                    elif training.get('approval_status') == 'Approved':
                        approval_badge = " ✅ Approved"
                    elif training.get('approval_status') == 'Rejected':
                        approval_badge = " ❌ Rejected"
                
                with st.expander(f"{status_emoji.get(training['status'], '⚪')} {training['team_member']} - {training['course_name']}{approval_badge}"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"**Course:** {training['course_name']}")
                        st.markdown(f"**Type:** {training['type']}")
                        st.markdown(f"**Objectives:** {training['objectives']}")
                        if training.get('business_case'):
                            st.markdown(f"**Business Case:** {training['business_case']}")
                    
                    with col2:
                        st.markdown(f"**Priority:** {training['priority']}")
                        st.markdown(f"**Start:** {training['start_date']}")
                        st.markdown(f"**End:** {training['end_date']}")
                        st.markdown(f"**Cost:** £{training.get('cost', 0):,.2f}")
                    
                    if training.get('approval_required') and training.get('approval_status') == 'Pending':
                        st.markdown("---")
                        st.markdown("**Manager Approval Required**")
                        col_approve, col_reject = st.columns(2)
                        with col_approve:
                            if st.button("✅ Approve", key=f"approve_{training['id']}", use_container_width=True):
                                training['approval_status'] = 'Approved'
                                save_data()
                                st.success("Training approved!")
                                st.rerun()
                        with col_reject:
                            if st.button("❌ Reject", key=f"reject_{training['id']}", use_container_width=True):
                                training['approval_status'] = 'Rejected'
                                save_data()
                                st.error("Training rejected")
                                st.rerun()
                    
                    st.markdown("---")
                    st.markdown("**Progress Tracking:**")
                    new_progress = st.slider("Completion %", 0, 100, training['progress'], key=f"progress_{training['id']}")
                    
                    new_training_status = st.selectbox("Status", ["Not Started", "In Progress", "Completed", "Cancelled"],
                        index=["Not Started", "In Progress", "Completed", "Cancelled"].index(training['status']),
                        key=f"training_status_{training['id']}")
                    
                    training_note = st.text_input("Add Note", key=f"training_note_{training['id']}")
                    
                    if st.button("Update Training", key=f"update_training_{training['id']}"):
                        training['progress'] = new_progress
                        training['status'] = new_training_status
                        if training_note:
                            training['notes'].append({'date': datetime.now().isoformat(), 'note': training_note})
                        save_data()
                        st.success("Training updated!")
                        st.rerun()
                    
                    if training.get('notes'):
                        st.markdown("**Notes:**")
                        for note in training['notes']:
                            st.caption(f"{note['date']}: {note['note']}")
        else:
            st.info("No training plans found")
    
    with tab3:
        st.subheader("Team Training Overview")
        
        if st.session_state.training_plans:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                total_plans = len(st.session_state.training_plans)
                st.metric("Total Plans", total_plans)
            with col2:
                in_progress = len([t for t in st.session_state.training_plans if t['status'] == 'In Progress'])
                st.metric("In Progress", in_progress)
            with col3:
                completed = len([t for t in st.session_state.training_plans if t['status'] == 'Completed'])
                st.metric("Completed", completed)
            with col4:
                total_investment = sum(t.get('cost', 0) for t in st.session_state.training_plans)
                st.metric("Total Investment", f"£{total_investment:,.0f}")
            
            st.markdown("---")
            
            training_data = []
            for member in st.session_state.team_members:
                member_training = [t for t in st.session_state.training_plans if t['team_member'] == member]
                if member_training:
                    total = len(member_training)
                    in_prog = len([t for t in member_training if t['status'] == 'In Progress'])
                    completed = len([t for t in member_training if t['status'] == 'Completed'])
                    avg_progress = sum(t['progress'] for t in member_training) / total if total > 0 else 0
                    
                    training_data.append({
                        'Team Member': member,
                        'Total Plans': total,
                        'In Progress': in_prog,
                        'Completed': completed,
                        'Avg Progress': f"{avg_progress:.0f}%"
                    })
            
            if training_data:
                df = pd.DataFrame(training_data)
                st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No training plans to display")

# ============================================
# TRAINING MATRIX PAGE
# ============================================
elif page == "📋 Training Matrix":
    st.title("📋 Training Matrix")
    st.markdown("Track required skills and competencies for each team member")
    
    tab1, tab2, tab3 = st.tabs(["➕ Add Skills", "✅ Track Progress", "📊 Matrix View"])
    
    with tab1:
        st.subheader("Add Skills to Training Matrix")
        
        with st.form("matrix_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                matrix_member = st.selectbox("Team Member", st.session_state.team_members, key="matrix_member")
                skill_name = st.text_input("Skill/Competency Name")
                skill_category = st.selectbox("Category", 
                    ["Technical", "Soft Skills", "Leadership", "Product Knowledge", 
                     "Systems/Tools", "Compliance", "Safety", "Other"])
            
            with col2:
                required_level = st.selectbox("Required Level", ["Basic", "Intermediate", "Advanced", "Expert"])
                current_level = st.selectbox("Current Level", ["None", "Basic", "Intermediate", "Advanced", "Expert"])
                priority = st.selectbox("Priority", ["Low", "Medium", "High"], key="matrix_priority")
            
            target_date = st.date_input("Target Completion Date", datetime.now() + timedelta(days=90))
            training_method = st.text_input("Training Method", placeholder="e.g., Online course, shadowing, certification")
            
            submitted = st.form_submit_button("Add to Matrix", use_container_width=True)
            
            if submitted:
                completed = (current_level == required_level)
                new_matrix_item = {
                    'id': len(st.session_state.training_matrix) + 1,
                    'team_member': matrix_member,
                    'skill_name': skill_name,
                    'category': skill_category,
                    'required_level': required_level,
                    'current_level': current_level,
                    'priority': priority,
                    'target_date': target_date.isoformat(),
                    'training_method': training_method,
                    'completed': completed,
                    'completion_date': datetime.now().isoformat() if completed else None,
                    'created_at': datetime.now().isoformat(),
                    'notes': []
                }
                st.session_state.training_matrix.append(new_matrix_item)
                save_data()
                st.success(f"✅ Skill added to {matrix_member}'s training matrix")
                st.rerun()
    
    with tab2:
        st.subheader("Update Skill Progress")
        
        filter_matrix_member = st.selectbox("Select Team Member", st.session_state.team_members, key="matrix_progress_filter")
        
        member_matrix = [m for m in st.session_state.training_matrix if m['team_member'] == filter_matrix_member]
        
        if member_matrix:
            for skill in member_matrix:
                status_emoji = "✅" if skill['completed'] else "🔄"
                with st.expander(f"{status_emoji} {skill['skill_name']} ({skill['category']})"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**Skill:** {skill['skill_name']}")
                        st.markdown(f"**Category:** {skill['category']}")
                        st.markdown(f"**Required Level:** {skill['required_level']}")
                        st.markdown(f"**Training Method:** {skill['training_method']}")
                    
                    with col2:
                        st.markdown(f"**Current Level:** {skill['current_level']}")
                        st.markdown(f"**Priority:** {skill['priority']}")
                        st.markdown(f"**Target Date:** {skill['target_date']}")
                        if skill['completed']:
                            st.success(f"✅ Completed: {skill['completion_date']}")
                    
                    st.markdown("---")
                    new_current_level = st.selectbox("Update Current Level",
                        ["None", "Basic", "Intermediate", "Advanced", "Expert"],
                        index=["None", "Basic", "Intermediate", "Advanced", "Expert"].index(skill['current_level']),
                        key=f"level_{skill['id']}")
                    
                    mark_complete = st.checkbox("Mark as Completed", value=skill['completed'], key=f"complete_{skill['id']}")
                    skill_note = st.text_input("Add Note", key=f"skill_note_{skill['id']}")
                    
                    if st.button("Update Skill", key=f"update_skill_{skill['id']}"):
                        skill['current_level'] = new_current_level
                        skill['completed'] = mark_complete
                        if mark_complete and not skill.get('completion_date'):
                            skill['completion_date'] = datetime.now().isoformat()
                        if skill_note:
                            skill['notes'].append({'date': datetime.now().isoformat(), 'note': skill_note})
                        save_data()
                        st.success("Skill updated!")
                        st.rerun()
                    
                    if skill.get('notes'):
                        st.markdown("**Notes:**")
                        for note in skill['notes']:
                            st.caption(f"{note['date']}: {note['note']}")
        else:
            st.info(f"No skills in training matrix for {filter_matrix_member}")
    
    with tab3:
        st.subheader("Complete Training Matrix View")
        
        if st.session_state.training_matrix:
            matrix_data = []
            for item in st.session_state.training_matrix:
                matrix_data.append({
                    'Team Member': item['team_member'],
                    'Skill': item['skill_name'],
                    'Category': item['category'],
                    'Current': item['current_level'],
                    'Required': item['required_level'],
                    'Priority': item['priority'],
                    'Target': item['target_date'],
                    'Status': '✅ Complete' if item['completed'] else '🔄 In Progress'
                })
            
            df = pd.DataFrame(matrix_data)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                filter_member = st.selectbox("Filter Team Member", ["All"] + st.session_state.team_members, key="matrix_view_filter")
            with col2:
                filter_category = st.selectbox("Filter Category", ["All", "Technical", "Soft Skills", "Leadership", 
                    "Product Knowledge", "Systems/Tools", "Compliance", "Safety", "Other"])
            with col3:
                filter_status = st.selectbox("Filter Status", ["All", "Completed", "In Progress"])
            
            filtered_df = df.copy()
            if filter_member != "All":
                filtered_df = filtered_df[filtered_df['Team Member'] == filter_member]
            if filter_category != "All":
                filtered_df = filtered_df[filtered_df['Category'] == filter_category]
            if filter_status == "Completed":
                filtered_df = filtered_df[filtered_df['Status'] == '✅ Complete']
            elif filter_status == "In Progress":
                filtered_df = filtered_df[filtered_df['Status'] == '🔄 In Progress']
            
            st.dataframe(filtered_df, use_container_width=True, hide_index=True)
            
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                "📥 Download Matrix as CSV",
                csv,
                "training_matrix.csv",
                "text/csv",
                use_container_width=True
            )
        else:
            st.info("No training matrix data to display")
          # ============================================
# SYTNER TRAINING PAGE
# ============================================
elif page == "🏢 Sytner Training":
    st.title("🏢 Sytner Training Bookings")
    st.markdown("Manage Sytner-specific training courses and bookings")
    
    tab1, tab2 = st.tabs(["➕ Book Training", "📋 Manage Bookings"])
    
    with tab1:
        st.subheader("Book Sytner Training")
        
        with st.form("sytner_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                sytner_member = st.selectbox("Team Member", st.session_state.team_members, key="sytner_member")
                sytner_course = st.text_input("Course Name", placeholder="e.g., Sales Excellence Programme")
                sytner_location = st.selectbox("Location", 
                    ["Head Office", "Regional Centre", "Virtual", "On-site", "External Venue", "Other"])
                start_date = st.date_input("Start Date", datetime.now() + timedelta(days=14), key="sytner_start")
            
            with col2:
                end_date = st.date_input("End Date", datetime.now() + timedelta(days=14), key="sytner_end")
                cost = st.number_input("Course Cost (£)", min_value=0.0, step=100.0, value=0.0, key="sytner_cost")
                travel_required = st.checkbox("Travel/Accommodation Required")
                expenses_estimate = st.number_input("Estimated Expenses (£)", min_value=0.0, step=50.0, value=0.0, 
                    disabled=not travel_required)
            
            course_objectives = st.text_area("Course Objectives", height=80)
            booking_ref = st.text_input("Booking Reference (optional)")
            
            submitted = st.form_submit_button("Book Training", use_container_width=True)
            
            if submitted:
                new_booking = {
                    'id': len(st.session_state.sytner_bookings) + 1,
                    'team_member': sytner_member,
                    'course_name': sytner_course,
                    'location': sytner_location,
                    'start_date': start_date.isoformat(),
                    'end_date': end_date.isoformat(),
                    'cost': cost,
                    'travel_required': travel_required,
                    'expenses_estimate': expenses_estimate if travel_required else 0,
                    'objectives': course_objectives,
                    'booking_ref': booking_ref,
                    'status': 'Booked',
                    'attendance': None,
                    'completion_date': None,
                    'feedback': None,
                    'created_at': datetime.now().isoformat()
                }
                st.session_state.sytner_bookings.append(new_booking)
                save_data()
                st.success(f"✅ Sytner training booked for {sytner_member}")
                st.rerun()
    
    with tab2:
        st.subheader("Manage Sytner Training Bookings")
        
        if st.session_state.sytner_bookings:
            col1, col2 = st.columns(2)
            with col1:
                filter_sytner_member = st.selectbox("Filter by Team Member", 
                    ["All"] + st.session_state.team_members, key="sytner_filter")
            with col2:
                filter_sytner_status = st.selectbox("Filter by Status", 
                    ["All", "Booked", "In Progress", "Completed", "Cancelled"])
            
            filtered_bookings = st.session_state.sytner_bookings.copy()
            if filter_sytner_member != "All":
                filtered_bookings = [b for b in filtered_bookings if b['team_member'] == filter_sytner_member]
            if filter_sytner_status != "All":
                filtered_bookings = [b for b in filtered_bookings if b['status'] == filter_sytner_status]
            
            if filtered_bookings:
                total_cost = sum(b['cost'] + b.get('expenses_estimate', 0) for b in filtered_bookings)
                st.info(f"📊 {len(filtered_bookings)} booking(s) | Total Cost: £{total_cost:,.2f}")
                
                for booking in filtered_bookings:
                    status_emoji = {'Booked': '📅', 'In Progress': '🔄', 'Completed': '✅', 'Cancelled': '❌'}
                    
                    with st.expander(f"{status_emoji.get(booking['status'], '📅')} {booking['team_member']} - {booking['course_name']} ({booking['start_date']})"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown(f"**Course:** {booking['course_name']}")
                            st.markdown(f"**Location:** {booking['location']}")
                            st.markdown(f"**Dates:** {booking['start_date']} to {booking['end_date']}")
                            st.markdown(f"**Objectives:** {booking['objectives']}")
                        
                        with col2:
                            st.markdown(f"**Status:** {booking['status']}")
                            st.markdown(f"**Cost:** £{booking['cost']:,.2f}")
                            if booking['travel_required']:
                                st.markdown(f"**Expenses:** £{booking.get('expenses_estimate', 0):,.2f}")
                            if booking.get('booking_ref'):
                                st.markdown(f"**Booking Ref:** {booking['booking_ref']}")
                        
                        st.markdown("---")
                        
                        new_status = st.selectbox("Update Status", 
                            ["Booked", "In Progress", "Completed", "Cancelled"],
                            index=["Booked", "In Progress", "Completed", "Cancelled"].index(booking['status']),
                            key=f"sytner_status_{booking['id']}")
                        
                        if new_status == "Completed":
                            attendance = st.radio("Attendance", ["Attended", "Partial", "Did Not Attend"], 
                                key=f"attendance_{booking['id']}")
                            feedback = st.text_area("Course Feedback", key=f"feedback_{booking['id']}")
                        
                        if st.button("Update Booking", key=f"update_sytner_{booking['id']}"):
                            booking['status'] = new_status
                            if new_status == "Completed":
                                booking['completion_date'] = datetime.now().isoformat()
                                if 'attendance' in locals():
                                    booking['attendance'] = attendance
                                if 'feedback' in locals():
                                    booking['feedback'] = feedback
                            save_data()
                            st.success("Booking updated!")
                            st.rerun()
                        
                        if booking['travel_required'] and booking['status'] == 'Completed':
                            st.info("💷 Remember to submit expenses claim for travel/accommodation")
        else:
            st.info("No Sytner training bookings yet")

# ============================================
# LEARNING RESOURCES PAGE
# ============================================
elif page == "📚 Learning Resources":
    st.title("📚 Learning Resources")
    st.markdown("Track books, licenses, courses, and other learning materials")
    
    tab1, tab2 = st.tabs(["➕ Add Resource", "📋 Manage Resources"])
    
    with tab1:
        st.subheader("Add Learning Resource")
        
        with st.form("resource_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                resource_member = st.selectbox("Assign to", st.session_state.team_members, key="resource_member")
                resource_title = st.text_input("Title/Name")
                resource_type = st.selectbox("Type", 
                    ["Book", "Online Course", "License/Subscription", "Certification", 
                     "Conference", "Video Course", "Other"])
                provider = st.text_input("Provider/Publisher", placeholder="e.g., Udemy, O'Reilly, LinkedIn Learning")
            
            with col2:
                cost = st.number_input("Cost (£)", min_value=0.0, step=10.0, value=0.0, key="resource_cost")
                purchase_date = st.date_input("Purchase/Assignment Date", datetime.now())
                expiry_date = st.date_input("Expiry Date (if applicable)", datetime.now() + timedelta(days=365))
                link_to_expenses = st.checkbox("Linked to Expense Claim")
            
            description = st.text_area("Description/Purpose", height=80)
            
            submitted = st.form_submit_button("Add Resource", use_container_width=True)
            
            if submitted:
                new_resource = {
                    'id': len(st.session_state.learning_resources) + 1,
                    'team_member': resource_member,
                    'title': resource_title,
                    'type': resource_type,
                    'provider': provider,
                    'cost': cost,
                    'assigned_date': purchase_date.isoformat(),
                    'expiry_date': expiry_date.isoformat(),
                    'link_to_expenses': link_to_expenses,
                    'description': description,
                    'status': 'Not Started',
                    'completion_date': None,
                    'created_at': datetime.now().isoformat(),
                    'notes': []
                }
                st.session_state.learning_resources.append(new_resource)
                save_data()
                st.success(f"✅ Learning resource added for {resource_member}")
                st.rerun()
    
    with tab2:
        st.subheader("Manage Learning Resources")
        
        if st.session_state.learning_resources:
            col1, col2 = st.columns(2)
            with col1:
                filter_resource_member = st.selectbox("Filter by Team Member", 
                    ["All"] + st.session_state.team_members, key="resource_filter")
            with col2:
                filter_resource_type = st.selectbox("Filter by Type", 
                    ["All", "Book", "Online Course", "License/Subscription", "Certification", 
                     "Conference", "Video Course", "Other"])
            
            filtered_resources = st.session_state.learning_resources.copy()
            if filter_resource_member != "All":
                filtered_resources = [r for r in filtered_resources if r['team_member'] == filter_resource_member]
            if filter_resource_type != "All":
                filtered_resources = [r for r in filtered_resources if r['type'] == filter_resource_type]
            
            if filtered_resources:
                total_investment = sum(r['cost'] for r in filtered_resources)
                st.info(f"📊 {len(filtered_resources)} resource(s) | Total Investment: £{total_investment:,.2f}")
                
                for resource in filtered_resources:
                    status_emoji = {'Not Started': '📚', 'In Progress': '📖', 'Completed': '✅'}
                    
                    with st.expander(f"{status_emoji.get(resource['status'], '📚')} {resource['team_member']} - {resource['title']} ({resource['type']})"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown(f"**Title:** {resource['title']}")
                            st.markdown(f"**Type:** {resource['type']}")
                            st.markdown(f"**Provider:** {resource['provider']}")
                            st.markdown(f"**Description:** {resource['description']}")
                        
                        with col2:
                            st.markdown(f"**Status:** {resource['status']}")
                            st.markdown(f"**Cost:** £{resource['cost']:,.2f}")
                            st.markdown(f"**Assigned:** {resource['assigned_date']}")
                            st.markdown(f"**Expires:** {resource['expiry_date']}")
                            if resource['link_to_expenses']:
                                st.markdown("💷 **Linked to Expenses**")
                        
                        st.markdown("---")
                        
                        new_resource_status = st.selectbox("Update Status",
                            ["Not Started", "In Progress", "Completed"],
                            index=["Not Started", "In Progress", "Completed"].index(resource['status']),
                            key=f"resource_status_{resource['id']}")
                        
                        resource_note = st.text_input("Add Note", key=f"resource_note_{resource['id']}")
                        
                        if st.button("Update Resource", key=f"update_resource_{resource['id']}"):
                            resource['status'] = new_resource_status
                            if new_resource_status == 'Completed' and not resource.get('completion_date'):
                                resource['completion_date'] = datetime.now().isoformat()
                            if resource_note:
                                resource['notes'].append({'date': datetime.now().isoformat(), 'note': resource_note})
                            save_data()
                            st.success("Resource updated!")
                            st.rerun()
                        
                        if resource.get('notes'):
                            st.markdown("**Notes:**")
                            for note in resource['notes']:
                                st.caption(f"{note['date']}: {note['note']}")
        else:
            st.info("No learning resources tracked yet")
          # ============================================
# REPORTS PAGE
# ============================================
elif page == "📈 Reports":
    st.title("📈 Reports & Analytics")
    st.markdown("Comprehensive reporting across all training and development activities")
    
    report_period = st.selectbox("Report Period", ["Last 30 days", "Last 90 days", "Last 6 months", "All Time"])
    
    days_map = {"Last 30 days": 30, "Last 90 days": 90, "Last 6 months": 180, "All Time": 999999}
    days = days_map[report_period]
    cutoff_date = datetime.now() - timedelta(days=days)
    
    st.markdown("---")
    
    # Team Activity Overview
    st.subheader("Team Activity Overview")
    
    activity_data = []
    for member in st.session_state.team_members:
        checkins = len([c for c in st.session_state.checkins 
                       if c['team_member'] == member and datetime.fromisoformat(c['date']) >= cutoff_date])
        actions = len([a for a in st.session_state.actions if a['team_member'] == member])
        training_plans = len([t for t in st.session_state.training_plans 
                             if t['team_member'] == member and t['status'] == 'In Progress'])
        matrix_items = len([m for m in st.session_state.training_matrix 
                           if m['team_member'] == member and not m['completed']])
        
        activity_data.append({
            'Team Member': member,
            'Check-ins': checkins,
            'Active Actions': actions,
            'Training Plans': training_plans,
            'Matrix Items': matrix_items
        })
    
    if activity_data:
        df = pd.DataFrame(activity_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Training Investment Summary
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Training Investment")
        training_cost = sum(t.get('cost', 0) for t in st.session_state.training_plans)
        sytner_cost = sum(b['cost'] + b.get('expenses_estimate', 0) for b in st.session_state.sytner_bookings)
        resources_cost = sum(r['cost'] for r in st.session_state.learning_resources)
        total_cost = training_cost + sytner_cost + resources_cost
        
        st.metric("Training Plans", f"£{training_cost:,.2f}")
        st.metric("Sytner Training", f"£{sytner_cost:,.2f}")
        st.metric("Learning Resources", f"£{resources_cost:,.2f}")
        st.metric("Total Investment", f"£{total_cost:,.2f}")
    
    with col2:
        st.subheader("Completion Metrics")
        
        if st.session_state.training_plans:
            total_plans = len(st.session_state.training_plans)
            completed_plans = len([t for t in st.session_state.training_plans if t['status'] == 'Completed'])
            completion_rate = (completed_plans / total_plans * 100) if total_plans > 0 else 0
            st.metric("Training Plans", f"{completed_plans}/{total_plans}", f"{completion_rate:.0f}%")
        
        if st.session_state.training_matrix:
            total_matrix = len(st.session_state.training_matrix)
            completed_matrix = len([m for m in st.session_state.training_matrix if m['completed']])
            matrix_rate = (completed_matrix / total_matrix * 100) if total_matrix > 0 else 0
            st.metric("Matrix Skills", f"{completed_matrix}/{total_matrix}", f"{matrix_rate:.0f}%")
        
        if st.session_state.sytner_bookings:
            total_sytner = len(st.session_state.sytner_bookings)
            completed_sytner = len([s for s in st.session_state.sytner_bookings if s['status'] == 'Completed'])
            sytner_rate = (completed_sytner / total_sytner * 100) if total_sytner > 0 else 0
            st.metric("Sytner Courses", f"{completed_sytner}/{total_sytner}", f"{sytner_rate:.0f}%")
    
    st.markdown("---")
    
    # Export Section
    st.subheader("📥 Export Data")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("Export Check-ins", use_container_width=True):
            if st.session_state.checkins:
                df = pd.DataFrame(st.session_state.checkins)
                csv = df.to_csv(index=False)
                st.download_button("Download CSV", csv, "checkins_export.csv", "text/csv")
    
    with col2:
        if st.button("Export Training Plans", use_container_width=True):
            if st.session_state.training_plans:
                df = pd.DataFrame(st.session_state.training_plans)
                csv = df.to_csv(index=False)
                st.download_button("Download CSV", csv, "training_plans_export.csv", "text/csv")
    
    with col3:
        if st.button("Export Matrix", use_container_width=True):
            if st.session_state.training_matrix:
                df = pd.DataFrame(st.session_state.training_matrix)
                csv = df.to_csv(index=False)
                st.download_button("Download CSV", csv, "training_matrix_export.csv", "text/csv")
    
    with col4:
        if st.button("Export Sytner", use_container_width=True):
            if st.session_state.sytner_bookings:
                df = pd.DataFrame(st.session_state.sytner_bookings)
                csv = df.to_csv(index=False)
                st.download_button("Download CSV", csv, "sytner_training_export.csv", "text/csv")

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("Manager Hub & TAG Training v2.0")
st.sidebar.caption("Built with Streamlit")
