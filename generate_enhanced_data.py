"""
Enhanced sample data generator for Manager Hub & TAG Training POC
Includes training matrix, Sytner bookings, and learning resources
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

# Sample check-ins
sample_checkins = [
    {
        'id': 1,
        'team_member': 'Alice Johnson',
        'date': (datetime.now() - timedelta(days=2)).isoformat()[:10],
        'type': 'Training Discussion',
        'notes': 'Discussed progress on Python certification. Alice is doing well and should complete by end of quarter. Also talked about upcoming Sytner sales training.',
        'tags': ['Training', 'Development'],
        'follow_up': True,
        'created_at': (datetime.now() - timedelta(days=2)).isoformat()
    },
    {
        'id': 2,
        'team_member': 'Bob Smith',
        'date': (datetime.now() - timedelta(days=5)).isoformat()[:10],
        'type': 'Wellbeing Check',
        'notes': 'Bob mentioned feeling overwhelmed with balancing current role and new training requirements. Agreed to spread out training matrix items over longer period.',
        'tags': ['Wellbeing', 'Training'],
        'follow_up': True,
        'created_at': (datetime.now() - timedelta(days=5)).isoformat()
    },
    {
        'id': 3,
        'team_member': 'Carol Williams',
        'date': (datetime.now() - timedelta(days=7)).isoformat()[:10],
        'type': 'Progress Update',
        'notes': 'Carol completed leadership training ahead of schedule. Excellent feedback from facilitators. Ready to take on team lead responsibilities.',
        'tags': ['Performance', 'Recognition', 'Training'],
        'follow_up': False,
        'created_at': (datetime.now() - timedelta(days=7)).isoformat()
    }
]

# Sample actions
sample_actions = [
    {
        'id': 1,
        'team_member': 'Alice Johnson',
        'action': 'Complete final module of Python certification',
        'priority': 'High',
        'owner': 'Team Member',
        'due_date': (datetime.now() + timedelta(days=14)).isoformat()[:10],
        'category': 'Training',
        'notes': 'Link with training plan',
        'status': 'In Progress',
        'created_at': (datetime.now() - timedelta(days=10)).isoformat(),
        'updates': [
            {
                'date': (datetime.now() - timedelta(days=3)).isoformat(),
                'note': 'Completed module 4, starting final project'
            }
        ]
    },
    {
        'id': 2,
        'team_member': 'Bob Smith',
        'action': 'Review and prioritize training matrix items with manager',
        'priority': 'High',
        'owner': 'Both',
        'due_date': (datetime.now() + timedelta(days=5)).isoformat()[:10],
        'category': 'Development',
        'notes': 'Schedule 1-2-1 to discuss',
        'status': 'Not Started',
        'created_at': (datetime.now() - timedelta(days=5)).isoformat(),
        'updates': []
    },
    {
        'id': 3,
        'team_member': 'Carol Williams',
        'action': 'Submit expenses for leadership training',
        'priority': 'Medium',
        'owner': 'Team Member',
        'due_date': (datetime.now() + timedelta(days=7)).isoformat()[:10],
        'category': 'Admin',
        'notes': 'Course completed, need to claim £450',
        'status': 'Not Started',
        'created_at': (datetime.now() - timedelta(days=7)).isoformat(),
        'updates': []
    }
]

# Sample training plans
sample_training = [
    {
        'id': 1,
        'team_member': 'Alice Johnson',
        'course_name': 'Advanced Python for Data Analysis',
        'type': 'Online Course',
        'start_date': (datetime.now() - timedelta(days=45)).isoformat()[:10],
        'end_date': (datetime.now() + timedelta(days=14)).isoformat()[:10],
        'priority': 'High',
        'objectives': 'Gain advanced Python skills for data analysis tasks, including pandas, numpy, and data visualization',
        'business_case': 'Required for upcoming data analysis project. Will improve efficiency in monthly reporting.',
        'cost': 299.0,
        'approval_required': True,
        'approval_status': 'Approved',
        'status': 'In Progress',
        'progress': 85,
        'created_at': (datetime.now() - timedelta(days=45)).isoformat(),
        'notes': [
            {
                'date': (datetime.now() - timedelta(days=30)).isoformat(),
                'note': 'Completed first 3 modules ahead of schedule'
            },
            {
                'date': (datetime.now() - timedelta(days=10)).isoformat(),
                'note': 'Starting final capstone project'
            }
        ]
    },
    {
        'id': 2,
        'team_member': 'Bob Smith',
        'course_name': 'Time Management & Productivity',
        'type': 'Self-Study',
        'start_date': (datetime.now() - timedelta(days=5)).isoformat()[:10],
        'end_date': (datetime.now() + timedelta(days=25)).isoformat()[:10],
        'priority': 'Medium',
        'objectives': 'Learn effective prioritization and time management strategies',
        'business_case': 'Support for managing workload and reducing stress',
        'cost': 0.0,
        'approval_required': False,
        'approval_status': 'Approved',
        'status': 'In Progress',
        'progress': 15,
        'created_at': (datetime.now() - timedelta(days=5)).isoformat(),
        'notes': []
    },
    {
        'id': 3,
        'team_member': 'Carol Williams',
        'course_name': 'Leadership Fundamentals',
        'type': 'In-Person Training',
        'start_date': (datetime.now() - timedelta(days=21)).isoformat()[:10],
        'end_date': (datetime.now() - timedelta(days=18)).isoformat()[:10],
        'priority': 'High',
        'objectives': 'Develop core leadership competencies for team lead role',
        'business_case': 'Preparation for promotion to Team Lead position',
        'cost': 850.0,
        'approval_required': True,
        'approval_status': 'Approved',
        'status': 'Completed',
        'progress': 100,
        'created_at': (datetime.now() - timedelta(days=60)).isoformat(),
        'notes': [
            {
                'date': (datetime.now() - timedelta(days=18)).isoformat(),
                'note': 'Completed successfully. Excellent feedback from facilitator. Certificate received.'
            }
        ]
    }
]

# Training Matrix
sample_training_matrix = [
    {
        'id': 1,
        'team_member': 'Alice Johnson',
        'skill_name': 'Python Programming',
        'category': 'Technical',
        'required_level': 'Advanced',
        'current_level': 'Intermediate',
        'priority': 'High',
        'target_date': (datetime.now() + timedelta(days=30)).isoformat()[:10],
        'training_method': 'Online course + practical projects',
        'completed': False,
        'completion_date': None,
        'created_at': (datetime.now() - timedelta(days=60)).isoformat(),
        'notes': [
            {
                'date': (datetime.now() - timedelta(days=20)).isoformat(),
                'note': 'Good progress on certification course'
            }
        ]
    },
    {
        'id': 2,
        'team_member': 'Alice Johnson',
        'skill_name': 'SQL Database Management',
        'category': 'Technical',
        'required_level': 'Intermediate',
        'current_level': 'Basic',
        'priority': 'Medium',
        'target_date': (datetime.now() + timedelta(days=90)).isoformat()[:10],
        'training_method': 'Online tutorials + database project',
        'completed': False,
        'completion_date': None,
        'created_at': (datetime.now() - timedelta(days=60)).isoformat(),
        'notes': []
    },
    {
        'id': 3,
        'team_member': 'Alice Johnson',
        'skill_name': 'Data Visualization',
        'category': 'Technical',
        'required_level': 'Intermediate',
        'current_level': 'Intermediate',
        'priority': 'Low',
        'target_date': (datetime.now() - timedelta(days=5)).isoformat()[:10],
        'training_method': 'Self-study with Tableau',
        'completed': True,
        'completion_date': (datetime.now() - timedelta(days=5)).isoformat(),
        'created_at': (datetime.now() - timedelta(days=90)).isoformat(),
        'notes': [
            {
                'date': (datetime.now() - timedelta(days=5)).isoformat(),
                'note': 'Completed dashboard project successfully'
            }
        ]
    },
    {
        'id': 4,
        'team_member': 'Bob Smith',
        'skill_name': 'Sytner Product Range',
        'category': 'Product Knowledge',
        'required_level': 'Advanced',
        'current_level': 'Intermediate',
        'priority': 'High',
        'target_date': (datetime.now() + timedelta(days=60)).isoformat()[:10],
        'training_method': 'Sytner training + shadowing',
        'completed': False,
        'completion_date': None,
        'created_at': (datetime.now() - timedelta(days=30)).isoformat(),
        'notes': []
    },
    {
        'id': 5,
        'team_member': 'Bob Smith',
        'skill_name': 'Customer Service Excellence',
        'category': 'Soft Skills',
        'required_level': 'Advanced',
        'current_level': 'Advanced',
        'priority': 'Medium',
        'target_date': (datetime.now() - timedelta(days=10)).isoformat()[:10],
        'training_method': 'Workshop + mentoring',
        'completed': True,
        'completion_date': (datetime.now() - timedelta(days=10)).isoformat(),
        'created_at': (datetime.now() - timedelta(days=120)).isoformat(),
        'notes': []
    },
    {
        'id': 6,
        'team_member': 'Carol Williams',
        'skill_name': 'Team Leadership',
        'category': 'Leadership',
        'required_level': 'Intermediate',
        'current_level': 'Intermediate',
        'priority': 'High',
        'target_date': (datetime.now() - timedelta(days=18)).isoformat()[:10],
        'training_method': 'Leadership course',
        'completed': True,
        'completion_date': (datetime.now() - timedelta(days=18)).isoformat(),
        'created_at': (datetime.now() - timedelta(days=60)).isoformat(),
        'notes': [
            {
                'date': (datetime.now() - timedelta(days=18)).isoformat(),
                'note': 'Completed 3-day leadership workshop'
            }
        ]
    },
    {
        'id': 7,
        'team_member': 'Carol Williams',
        'skill_name': 'Conflict Resolution',
        'category': 'Soft Skills',
        'required_level': 'Advanced',
        'current_level': 'Basic',
        'priority': 'Medium',
        'target_date': (datetime.now() + timedelta(days=45)).isoformat()[:10],
        'training_method': 'Workshop + practice scenarios',
        'completed': False,
        'completion_date': None,
        'created_at': (datetime.now() - timedelta(days=30)).isoformat(),
        'notes': []
    },
    {
        'id': 8,
        'team_member': 'David Brown',
        'skill_name': 'CRM System',
        'category': 'Systems/Tools',
        'required_level': 'Expert',
        'current_level': 'Advanced',
        'priority': 'Medium',
        'target_date': (datetime.now() + timedelta(days=30)).isoformat()[:10],
        'training_method': 'Advanced CRM training',
        'completed': False,
        'completion_date': None,
        'created_at': (datetime.now() - timedelta(days=45)).isoformat(),
        'notes': []
    },
    {
        'id': 9,
        'team_member': 'David Brown',
        'skill_name': 'Project Management',
        'category': 'Leadership',
        'required_level': 'Intermediate',
        'current_level': 'None',
        'priority': 'High',
        'target_date': (datetime.now() + timedelta(days=90)).isoformat()[:10],
        'training_method': 'PMP certification course',
        'completed': False,
        'completion_date': None,
        'created_at': (datetime.now() - timedelta(days=20)).isoformat(),
        'notes': []
    }
]

# Sytner Training Bookings
sample_sytner_bookings = [
    {
        'id': 1,
        'team_member': 'Bob Smith',
        'course_name': 'Sytner Sales Excellence Programme',
        'location': 'Regional Centre',
        'start_date': (datetime.now() + timedelta(days=21)).isoformat()[:10],
        'end_date': (datetime.now() + timedelta(days=23)).isoformat()[:10],
        'cost': 650.0,
        'travel_required': True,
        'expenses_estimate': 200.0,
        'objectives': 'Master Sytner sales methodology and customer engagement strategies',
        'booking_ref': 'SYTN-2024-0342',
        'status': 'Booked',
        'attendance': None,
        'completion_date': None,
        'feedback': None,
        'created_at': (datetime.now() - timedelta(days=14)).isoformat()
    },
    {
        'id': 2,
        'team_member': 'Alice Johnson',
        'course_name': 'Digital Marketing Fundamentals',
        'location': 'Virtual',
        'start_date': (datetime.now() + timedelta(days=7)).isoformat()[:10],
        'end_date': (datetime.now() + timedelta(days=7)).isoformat()[:10],
        'cost': 195.0,
        'travel_required': False,
        'expenses_estimate': 0.0,
        'objectives': 'Learn digital marketing strategies for automotive sector',
        'booking_ref': 'SYTN-2024-0389',
        'status': 'Booked',
        'attendance': None,
        'completion_date': None,
        'feedback': None,
        'created_at': (datetime.now() - timedelta(days=5)).isoformat()
    },
    {
        'id': 3,
        'team_member': 'Carol Williams',
        'course_name': 'Advanced Leadership Workshop',
        'location': 'Head Office',
        'start_date': (datetime.now() - timedelta(days=21)).isoformat()[:10],
        'end_date': (datetime.now() - timedelta(days=18)).isoformat()[:10],
        'cost': 850.0,
        'travel_required': True,
        'expenses_estimate': 350.0,
        'objectives': 'Develop advanced leadership capabilities',
        'booking_ref': 'SYTN-2024-0298',
        'status': 'Completed',
        'attendance': 'Attended',
        'completion_date': (datetime.now() - timedelta(days=18)).isoformat(),
        'feedback': 'Excellent course. Very relevant content. Great networking opportunity with other team leads.',
        'created_at': (datetime.now() - timedelta(days=60)).isoformat()
    },
    {
        'id': 4,
        'team_member': 'David Brown',
        'course_name': 'Customer Experience Excellence',
        'location': 'Regional Centre',
        'start_date': (datetime.now() + timedelta(days=35)).isoformat()[:10],
        'end_date': (datetime.now() + timedelta(days=36)).isoformat()[:10],
        'cost': 450.0,
        'travel_required': True,
        'expenses_estimate': 180.0,
        'objectives': 'Learn strategies to improve customer satisfaction scores',
        'booking_ref': 'SYTN-2024-0401',
        'status': 'Booked',
        'attendance': None,
        'completion_date': None,
        'feedback': None,
        'created_at': (datetime.now() - timedelta(days=3)).isoformat()
    }
]

# Learning Resources
sample_learning_resources = [
    {
        'id': 1,
        'team_member': 'Alice Johnson',
        'title': 'Python for Data Analysis (O\'Reilly)',
        'type': 'Book',
        'provider': 'O\'Reilly Media',
        'cost': 45.99,
        'assigned_date': (datetime.now() - timedelta(days=50)).isoformat()[:10],
        'expiry_date': (datetime.now() + timedelta(days=315)).isoformat()[:10],
        'link_to_expenses': True,
        'description': 'Comprehensive guide to data analysis with Python, pandas, and numpy',
        'status': 'In Progress',
        'completion_date': None,
        'created_at': (datetime.now() - timedelta(days=50)).isoformat(),
        'notes': [
            {
                'date': (datetime.now() - timedelta(days=30)).isoformat(),
                'note': 'Completed first 6 chapters, very useful for current project'
            }
        ]
    },
    {
        'id': 2,
        'team_member': 'Alice Johnson',
        'title': 'LinkedIn Learning Premium',
        'type': 'License/Subscription',
        'provider': 'LinkedIn',
        'cost': 299.99,
        'assigned_date': (datetime.now() - timedelta(days=90)).isoformat()[:10],
        'expiry_date': (datetime.now() + timedelta(days=275)).isoformat()[:10],
        'link_to_expenses': True,
        'description': 'Annual subscription for professional development courses',
        'status': 'In Progress',
        'completion_date': None,
        'created_at': (datetime.now() - timedelta(days=90)).isoformat(),
        'notes': []
    },
    {
        'id': 3,
        'team_member': 'Bob Smith',
        'title': 'Getting Things Done (David Allen)',
        'type': 'Book',
        'provider': 'Amazon',
        'cost': 12.99,
        'assigned_date': (datetime.now() - timedelta(days=10)).isoformat()[:10],
        'expiry_date': (datetime.now() + timedelta(days=355)).isoformat()[:10],
        'link_to_expenses': False,
        'description': 'Productivity methodology book',
        'status': 'Not Started',
        'completion_date': None,
        'created_at': (datetime.now() - timedelta(days=10)).isoformat(),
        'notes': []
    },
    {
        'id': 4,
        'team_member': 'Carol Williams',
        'title': 'Leaders Eat Last (Simon Sinek)',
        'type': 'Book',
        'provider': 'Amazon',
        'cost': 14.99,
        'assigned_date': (datetime.now() - timedelta(days=65)).isoformat()[:10],
        'expiry_date': (datetime.now() + timedelta(days=300)).isoformat()[:10],
        'link_to_expenses': True,
        'description': 'Leadership philosophy and practices',
        'status': 'Completed',
        'completion_date': (datetime.now() - timedelta(days=20)).isoformat(),
        'created_at': (datetime.now() - timedelta(days=65)).isoformat(),
        'notes': [
            {
                'date': (datetime.now() - timedelta(days=20)).isoformat(),
                'note': 'Finished reading. Excellent insights on servant leadership. Highly recommend.'
            }
        ]
    },
    {
        'id': 5,
        'team_member': 'David Brown',
        'title': 'Project Management Professional (PMP) Prep Course',
        'type': 'Online Course',
        'provider': 'Udemy',
        'cost': 89.99,
        'assigned_date': (datetime.now() - timedelta(days=25)).isoformat()[:10],
        'expiry_date': (datetime.now() + timedelta(days=340)).isoformat()[:10],
        'link_to_expenses': True,
        'description': 'Preparation course for PMP certification exam',
        'status': 'In Progress',
        'completion_date': None,
        'created_at': (datetime.now() - timedelta(days=25)).isoformat(),
        'notes': [
            {
                'date': (datetime.now() - timedelta(days=10)).isoformat(),
                'note': 'Completed 35% of course material'
            }
        ]
    },
    {
        'id': 6,
        'team_member': 'David Brown',
        'title': 'Automotive Industry Conference 2024',
        'type': 'Conference',
        'provider': 'SMMT',
        'cost': 450.0,
        'assigned_date': (datetime.now() + timedelta(days=60)).isoformat()[:10],
        'expiry_date': (datetime.now() + timedelta(days=60)).isoformat()[:10],
        'link_to_expenses': True,
        'description': '2-day automotive industry conference covering latest trends and technology',
        'status': 'Not Started',
        'completion_date': None,
        'created_at': (datetime.now() - timedelta(days=15)).isoformat(),
        'notes': []
    }
]

# Write all data to JSON files
with open(DATA_DIR / 'checkins.json', 'w') as f:
    json.dump(sample_checkins, f, indent=2)

with open(DATA_DIR / 'actions.json', 'w') as f:
    json.dump(sample_actions, f, indent=2)

with open(DATA_DIR / 'training_plans.json', 'w') as f:
    json.dump(sample_training, f, indent=2)

with open(DATA_DIR / 'training_matrix.json', 'w') as f:
    json.dump(sample_training_matrix, f, indent=2)

with open(DATA_DIR / 'sytner_bookings.json', 'w') as f:
    json.dump(sample_sytner_bookings, f, indent=2)

with open(DATA_DIR / 'learning_resources.json', 'w') as f:
    json.dump(sample_learning_resources, f, indent=2)

print("✅ Enhanced sample data created successfully!")
print(f"   - {len(sample_checkins)} check-ins")
print(f"   - {len(sample_actions)} actions")
print(f"   - {len(sample_training)} training plans")
print(f"   - {len(sample_training_matrix)} training matrix items")
print(f"   - {len(sample_sytner_bookings)} Sytner training bookings")
print(f"   - {len(sample_learning_resources)} learning resources")
print("\nTotal training investment in demo data:")
training_cost = sum(t.get('cost', 0) for t in sample_training)
sytner_cost = sum(b['cost'] + b.get('expenses_estimate', 0) for b in sample_sytner_bookings)
resources_cost = sum(r['cost'] for r in sample_learning_resources)
print(f"   - Training Plans: £{training_cost:,.2f}")
print(f"   - Sytner Training: £{sytner_cost:,.2f}")
print(f"   - Learning Resources: £{resources_cost:,.2f}")
print(f"   - TOTAL: £{training_cost + sytner_cost + resources_cost:,.2f}")
print("\nRun 'streamlit run app_enhanced.py' to see the full TAG Training features!")
