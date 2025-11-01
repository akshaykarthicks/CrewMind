#!/usr/bin/env python
import streamlit as st
import sys
import os
from datetime import datetime
import time

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# SQLite workaround for cloud environments
try:
    __import__('pysqlite3')
    import sys as _sys
    _sys.modules['sqlite3'] = _sys.modules.pop('pysqlite3')
except ImportError:
    pass

from crewmind.crew import Crewmind

# Page configuration
st.set_page_config(
    page_title="🎯 Goal Tracker Crew",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .goal-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .goal-summary-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        color: white;
    }
    .goal-summary-card h3 {
        color: white !important;
        margin-bottom: 15px;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    }
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        margin: 0.5rem 0;
    }
    .metric-card .metric-label {
        color: #2c3e50 !important;
        font-weight: 600;
    }
    .metric-card .metric-value {
        color: #34495e !important;
        font-size: 1.2em;
        font-weight: bold;
    }
    .plan-section {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 10px 0;
    }
    .schedule-day {
        background: #e8f4fd;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #2196F3;
        margin: 10px 0;
    }
    .milestone-item {
        background: #fff3cd;
        padding: 10px;
        border-radius: 6px;
        border-left: 3px solid #ffc107;
        margin: 5px 0;
    }
    
    /* Ensure all text is visible */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: #2c3e50 !important;
    }
    .stMarkdown p, .stMarkdown div, .stMarkdown span {
        color: #34495e !important;
    }
    
    /* Fix for metric text visibility */
    [data-testid="metric-container"] {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
    }
    [data-testid="metric-container"] > div {
        color: #2c3e50 !important;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Check API key first
    api_key = os.getenv('GOOGLE_API_KEY') or os.getenv('GEMINI_API_KEY')
    if not api_key or api_key == 'YOUR_GEMINI_API_KEY_HERE':
        st.error("❌ **Gemini API Key Not Found!**")
        st.markdown("""
        **Please follow these steps to set up your API key:**
        
        1. Go to: https://makersuite.google.com/app/apikey
        2. Click "Create API Key"
        3. Copy the generated key
        4. Edit the `.env` file in the crewmind folder
        5. Replace `YOUR_GEMINI_API_KEY_HERE` with your actual key
        6. Save the file and refresh this page
        """)
        st.stop()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎯 Goal Tracker Crew</h1>
        <p>AI-powered goal setting and planning assistant</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar for navigation
    with st.sidebar:
        st.header("📋 Navigation")
        page = st.selectbox(
            "Choose a page:",
            ["🎯 Goal Tracker", "ℹ️ About"]
        )
        
        # Show current session info if available
        if st.session_state.get('crew_result'):
            st.markdown("---")
            st.markdown("### 📊 Current Session")
            st.success("✅ Goal plan created!")
            if st.button("🔄 Start New Goal", use_container_width=True):
                # Clear session state
                st.session_state.show_results = False
                for key in ['crew_result', 'goal_inputs', 'current_inputs']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()

    if page == "🎯 Goal Tracker":
        show_goal_setting_page()
    else:
        show_about_page()

def show_goal_setting_page():
    st.header("🎯 Set Your Goal")
    
    # Add some helpful tips
    with st.expander("💡 Tips for Setting Effective Goals"):
        st.markdown("""
        **Make your goal SMART:**
        - **Specific**: Clearly define what you want to achieve
        - **Measurable**: Include metrics to track progress
        - **Achievable**: Set realistic expectations
        - **Relevant**: Align with your values and priorities
        - **Time-bound**: Set a clear deadline
        
        **Examples of good goals:**
        - "Learn Python programming and build 3 web applications in 6 months"
        - "Run a 10K race in under 50 minutes within 4 months"
        - "Read 24 books this year (2 per month)"
        """)
    
    # Goal input form
    with st.form("goal_form"):
        # Goal Details Section
        st.markdown("### 📝 Goal Details")
        
        user_goal = st.text_area(
            "What do you want to achieve? *",
            placeholder="e.g., Learn Python programming and build 3 projects",
            height=100,
            help="Be as specific as possible about what you want to accomplish"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            timeline = st.selectbox(
                "Timeline *",
                ["1 month", "3 months", "6 months", "1 year", "Custom"],
                help="How long do you want to take to achieve this goal?"
            )
            
            if timeline == "Custom":
                timeline = st.text_input("Enter custom timeline:", placeholder="e.g., 8 weeks")
        
        with col2:
            goal_type = st.selectbox(
                "Goal Category",
                ["Professional Development", "Health & Fitness", "Personal Growth", 
                 "Education", "Creative", "Financial", "Other"],
                help="This helps us provide more targeted advice"
            )
        
        # Schedule Details Section
        st.markdown("### ⏰ Schedule Details")
        
        col3, col4 = st.columns(2)
        
        with col3:
            available_time = st.text_input(
                "Available time per day/week *",
                placeholder="e.g., 2 hours per day, weekdays",
                help="How much time can you realistically dedicate?"
            )
            
            preferred_schedule = st.selectbox(
                "Preferred time to work on goals",
                ["Early morning (6-9 AM)", "Morning (9-12 PM)", "Afternoon (12-5 PM)", 
                 "Evening (5-8 PM)", "Night (8-11 PM)", "Flexible"],
                help="When are you most productive?"
            )
        
        with col4:
            current_commitments = st.text_area(
                "Current commitments (optional)",
                placeholder="e.g., Full-time job 9-5, gym 3x per week",
                height=100,
                help="Help us work around your existing schedule"
            )
            
            motivation_level = st.select_slider(
                "Current motivation level",
                options=["Low", "Medium", "High", "Very High"],
                value="High",
                help="This helps us tailor the plan intensity"
            )
        
        # Additional preferences
        with st.expander("🔧 Advanced Options"):
            difficulty_preference = st.selectbox(
                "Preferred challenge level",
                ["Gentle start", "Moderate challenge", "Ambitious push"],
                index=1
            )
            
            accountability_preference = st.multiselect(
                "Accountability preferences",
                ["Daily check-ins", "Weekly reviews", "Progress milestones", "Reminder notifications"],
                default=["Weekly reviews", "Progress milestones"]
            )
        
        # Submit button with better styling
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button(
            "🚀 Create My Personalized Goal Plan", 
            use_container_width=True,
            type="primary"
        )
        
        if submitted:
            if user_goal and timeline and available_time:
                # Add the new fields to the inputs
                enhanced_inputs = {
                    'user_goal': user_goal,
                    'timeline': timeline,
                    'available_time': available_time,
                    'current_commitments': current_commitments,
                    'preferred_schedule': preferred_schedule,
                    'goal_type': goal_type,
                    'motivation_level': motivation_level,
                    'difficulty_preference': difficulty_preference,
                    'accountability_preference': ', '.join(accountability_preference)
                }
                # Store inputs in session state for display
                st.session_state.current_inputs = enhanced_inputs
                st.session_state.show_results = True
            else:
                st.error("⚠️ Please fill in the required fields marked with *")
    
    # Show results on the same page if form was submitted
    if st.session_state.get('show_results', False) and st.session_state.get('current_inputs'):
        st.markdown("---")
        display_goal_results(st.session_state.current_inputs)

def display_goal_results(inputs):
    """Display goal results on the same page"""
    
    st.header("🎉 Your Personalized Goal Plan")
    
    # Show goal summary
    st.markdown("""
    <div class="goal-summary-card">
        <h3 style="color: white; margin-bottom: 15px;">🎯 Your Goal Summary</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("🎯 Goal", inputs['user_goal'][:30] + "..." if len(inputs['user_goal']) > 30 else inputs['user_goal'])
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("⏰ Timeline", inputs['timeline'])
        st.markdown("</div>", unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("📅 Available Time", inputs['available_time'])
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Progress indicators
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Initialize crew
        status_text.text("🤖 Initializing Goal Tracker Crew...")
        progress_bar.progress(10)
        time.sleep(1)
        
        crew = Crewmind().crew()
        
        # Run the crew
        status_text.text("🎯 Goal Tracker Agent is analyzing your goal...")
        progress_bar.progress(30)
        
        with st.spinner("🤖 AI agents are working on your personalized plan..."):
            result = crew.kickoff(inputs=inputs)
        
        progress_bar.progress(100)
        status_text.text("✅ Goal plan created successfully!")
        
        # Store results in session state
        st.session_state.crew_result = result
        st.session_state.goal_inputs = inputs
        
        # Success message
        st.success("🎉 Success! Your personalized goal plan has been created!")
        
        # Display results immediately
        display_results_tabs(inputs, result)
        
        # Add action buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔄 Create New Goal", use_container_width=True):
                # Clear session state
                st.session_state.show_results = False
                if 'crew_result' in st.session_state:
                    del st.session_state.crew_result
                if 'goal_inputs' in st.session_state:
                    del st.session_state.goal_inputs
                if 'current_inputs' in st.session_state:
                    del st.session_state.current_inputs
                st.rerun()
        
        with col2:
            # Download button
            download_content = format_download_content(inputs, result)
            st.download_button(
                label="📄 Download Plan",
                data=download_content,
                file_name=f"goal_plan_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                mime="text/markdown",
                use_container_width=True
            )
        
        with col3:
            if st.button("📊 View Analytics", use_container_width=True):
                st.info("Analytics feature coming soon!")
        
    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")
        progress_bar.progress(0)
        status_text.text("❌ Failed to create goal plan")


def display_results_tabs(inputs, result):
    """Display results in tabs on the same page"""
    
    # Results tabs
    tab1, tab2, tab3 = st.tabs(["📋 Full Plan", "📊 Plan Overview", "📅 Daily Schedule"])
    
    with tab1:
        st.subheader("🤖 AI-Generated Goal Plan")
        
        # Get the result content
        if hasattr(result, 'raw'):
            content = result.raw
        else:
            content = str(result)
        
        # Display in a nice container
        with st.container():
            st.markdown("""
            <div class="plan-section">
            """, unsafe_allow_html=True)
            
            # Parse and display the content nicely
            display_formatted_plan(content)
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    with tab2:
        st.subheader("📊 Goal Plan Overview")
        display_plan_overview(inputs, result)
    
    with tab3:
        st.subheader("📅 Your Daily Schedule")
        display_daily_schedule(result)


def run_goal_tracker_crew(user_goal, timeline, available_time, current_commitments, preferred_schedule, goal_type, 
                         motivation_level="High", difficulty_preference="Moderate challenge", accountability_preference=""):
    """Run the Goal Tracker Crew with user inputs"""
    
    # Prepare inputs
    inputs = {
        'user_goal': user_goal,
        'timeline': timeline,
        'available_time': available_time,
        'current_commitments': current_commitments,
        'preferred_schedule': preferred_schedule,
        'goal_type': goal_type.lower(),
        'motivation_level': motivation_level,
        'difficulty_preference': difficulty_preference,
        'accountability_preference': accountability_preference,
        'current_year': str(datetime.now().year)
    }
    
    # Show goal summary
    st.markdown("""
    <div class="goal-summary-card">
        <h3 style="color: #2c3e50; margin-bottom: 15px;">🎯 Your Goal Summary</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="metric-card">
        """, unsafe_allow_html=True)
        st.metric("🎯 Goal", user_goal[:30] + "..." if len(user_goal) > 30 else user_goal)
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card">
        """, unsafe_allow_html=True)
        st.metric("⏰ Timeline", timeline)
        st.markdown("</div>", unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card">
        """, unsafe_allow_html=True)
        st.metric("📅 Available Time", available_time)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Progress indicators
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Initialize crew
        status_text.text("🤖 Initializing Goal Tracker Crew...")
        progress_bar.progress(10)
        time.sleep(1)
        
        crew = Crewmind().crew()
        
        # Run the crew
        status_text.text("🎯 Goal Tracker Agent is analyzing your goal...")
        progress_bar.progress(30)
        
        with st.spinner("🤖 AI agents are working on your personalized plan..."):
            result = crew.kickoff(inputs=inputs)
        
        progress_bar.progress(100)
        status_text.text("✅ Goal plan created successfully!")
        
        # Store results in session state
        st.session_state.crew_result = result
        st.session_state.goal_inputs = inputs
        
        # Success message
        st.markdown("""
        <div class="success-message">
            <h3>🎉 Success! Your personalized goal plan has been created!</h3>
            <p>Check the "View Results" page to see your detailed plan.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Auto-switch to results page
        time.sleep(2)
        st.rerun()
        
    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")
        progress_bar.progress(0)
        status_text.text("❌ Failed to create goal plan")

def show_results_page():
    st.header("📊 Your Goal Plan Results")
    
    if 'crew_result' in st.session_state and 'goal_inputs' in st.session_state:
        inputs = st.session_state.goal_inputs
        result = st.session_state.crew_result
        
        # Goal summary
        st.markdown("""
        <div class="goal-summary-card">
            <h3 style="color: #2c3e50; margin-bottom: 15px;">🎯 Goal Summary</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Goal:** {inputs['user_goal']}")
            st.write(f"**Timeline:** {inputs['timeline']}")
            st.write(f"**Category:** {inputs['goal_type'].title()}")
        
        with col2:
            st.write(f"**Available Time:** {inputs['available_time']}")
            st.write(f"**Preferred Schedule:** {inputs['preferred_schedule']}")
            st.write(f"**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        # Results tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📋 Full Plan", "📊 Plan Overview", "📅 Daily Schedule", "💾 Download"])
        
        with tab1:
            st.subheader("🤖 AI-Generated Goal Plan")
            
            # Get the result content
            if hasattr(result, 'raw'):
                content = result.raw
            else:
                content = str(result)
            
            # Display in a nice container
            with st.container():
                st.markdown("""
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 4px solid #667eea;">
                """, unsafe_allow_html=True)
                
                # Parse and display the content nicely
                display_formatted_plan(content)
                
                st.markdown("</div>", unsafe_allow_html=True)
        
        with tab2:
            st.subheader("📊 Goal Plan Overview")
            display_plan_overview(inputs, result)
        
        with tab3:
            st.subheader("📅 Your Daily Schedule")
            display_daily_schedule(result)
        
        with tab4:
            st.subheader("💾 Download Your Plan")
            
            # Prepare download content
            download_content = format_download_content(inputs, result)
            
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    label="📄 Download as Markdown",
                    data=download_content,
                    file_name=f"goal_plan_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                    mime="text/markdown",
                    use_container_width=True
                )
            
            with col2:
                # Preview of download content
                if st.button("👀 Preview Download", use_container_width=True):
                    st.text_area("Download Preview:", download_content, height=300)
        
        # Action buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Create New Goal", use_container_width=True):
                # Clear session state
                if 'crew_result' in st.session_state:
                    del st.session_state.crew_result
                if 'goal_inputs' in st.session_state:
                    del st.session_state.goal_inputs
                st.rerun()
        
        with col2:
            if st.button("📧 Share Plan", use_container_width=True):
                st.info("Copy the download link or use the download button to share your plan!")
    
    else:
        st.info("🎯 No goal plan found. Please create a goal first!")
        if st.button("➡️ Go to Goal Setting", use_container_width=True):
            st.rerun()

def display_formatted_plan(content):
    """Display the AI-generated plan in a nicely formatted way"""
    
    # Split content into sections
    sections = content.split('\n\n')
    
    for section in sections:
        if not section.strip():
            continue
            
        lines = section.strip().split('\n')
        first_line = lines[0].strip()
        
        # Check if it's a header (starts with # or is all caps)
        if first_line.startswith('#'):
            st.markdown(first_line)
        elif first_line.isupper() and len(first_line) > 5:
            st.markdown(f"### {first_line}")
        elif ':' in first_line and len(lines) > 1:
            # It's a section with details
            st.markdown(f"**{first_line}**")
            for line in lines[1:]:
                if line.strip():
                    if line.strip().startswith('-') or line.strip().startswith('*'):
                        st.markdown(line)
                    else:
                        st.write(line)
        else:
            # Regular content
            st.markdown(section)
        
        st.write("")  # Add spacing


def display_plan_overview(inputs, result):
    """Display a structured overview of the goal plan"""
    
    # Goal metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            label="🎯 Goal Type",
            value=inputs['goal_type'].title()
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            label="⏰ Timeline",
            value=inputs['timeline']
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            label="📅 Time Commitment",
            value=inputs['available_time']
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Goal breakdown
    st.markdown("---")
    st.subheader("🎯 Goal Breakdown")
    
    # Extract key information from the result
    content = result.raw if hasattr(result, 'raw') else str(result)
    
    # Try to extract milestones or key points
    milestones = extract_milestones(content)
    if milestones:
        for i, milestone in enumerate(milestones, 1):
            with st.expander(f"📍 Milestone {i}: {milestone[:50]}..."):
                st.write(milestone)
    
    # Progress tracking section
    st.markdown("---")
    st.subheader("📊 Progress Tracking")
    
    # Create a simple progress visualization
    progress_cols = st.columns(4)
    stages = ["Planning", "Foundation", "Implementation", "Completion"]
    
    for i, (col, stage) in enumerate(zip(progress_cols, stages)):
        with col:
            st.metric(
                label=stage,
                value="0%",
                help=f"Track your progress in the {stage.lower()} phase"
            )


def display_daily_schedule(result):
    """Display the daily schedule in a calendar-like format"""
    
    content = result.raw if hasattr(result, 'raw') else str(result)
    
    # Check if daily_plan.md was created
    if os.path.exists("daily_plan.md"):
        with open("daily_plan.md", "r", encoding='utf-8') as f:
            daily_plan = f.read()
        
        st.markdown("### 📅 Generated Daily Plan")
        with st.container():
            st.markdown("""
            <div style="background-color: #e8f4fd; padding: 15px; border-radius: 8px; border-left: 4px solid #2196F3;">
            """, unsafe_allow_html=True)
            st.markdown(daily_plan)
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        # Extract schedule information from the main content
        schedule_info = extract_schedule_info(content)
        
        if schedule_info:
            st.markdown("### 📅 Recommended Schedule")
            for day, activities in schedule_info.items():
                with st.expander(f"📆 {day}"):
                    for activity in activities:
                        st.write(f"• {activity}")
        else:
            st.info("📝 Daily schedule will be generated based on your goal plan. Check the Full Plan tab for detailed scheduling recommendations.")


def extract_milestones(content):
    """Extract milestones from the content"""
    milestones = []
    lines = content.split('\n')
    
    for line in lines:
        line = line.strip()
        if any(keyword in line.lower() for keyword in ['milestone', 'phase', 'step', 'stage']):
            if len(line) > 10 and not line.startswith('#'):
                milestones.append(line)
    
    return milestones[:5]  # Return first 5 milestones


def extract_schedule_info(content):
    """Extract schedule information from content"""
    schedule = {}
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    lines = content.split('\n')
    current_day = None
    
    for line in lines:
        line = line.strip()
        
        # Check if line contains a day
        for day in days:
            if day.lower() in line.lower():
                current_day = day
                schedule[day] = []
                break
        
        # If we have a current day and the line looks like an activity
        if current_day and line and not line.startswith('#'):
            if any(time_word in line.lower() for time_word in ['am', 'pm', 'morning', 'afternoon', 'evening']):
                schedule[current_day].append(line)
    
    return schedule


def format_download_content(inputs, result):
    """Format content for download"""
    content = result.raw if hasattr(result, 'raw') else str(result)
    
    download_content = f"""# 🎯 Goal Plan - {inputs['user_goal']}

## 📋 Goal Details
- **Goal:** {inputs['user_goal']}
- **Timeline:** {inputs['timeline']}
- **Category:** {inputs['goal_type'].title()}
- **Available Time:** {inputs['available_time']}
- **Current Commitments:** {inputs.get('current_commitments', 'None specified')}
- **Preferred Schedule:** {inputs.get('preferred_schedule', 'Flexible')}
- **Created:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## 🤖 AI-Generated Plan

{content}

---

## 📊 Progress Tracking

### Milestones Checklist
- [ ] Planning Phase Complete
- [ ] Foundation Established  
- [ ] Implementation Started
- [ ] Mid-point Review
- [ ] Final Push
- [ ] Goal Achieved! 🎉

### Weekly Review Questions
1. What progress did I make this week?
2. What challenges did I face?
3. What adjustments do I need to make?
4. What are my priorities for next week?

---

*Generated by Goal Tracker Crew - Your AI-powered goal achievement assistant*
"""
    
    return download_content


def show_about_page():
    st.header("ℹ️ About Goal Tracker Crew")
    
    # Developer Card
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 15px; margin: 2rem 0; box-shadow: 0 8px 16px rgba(0,0,0,0.1);">
        <div style="text-align: center; color: white;">
            <h2 style="color: white; margin-bottom: 1rem;">👨‍💻 Developer</h2>
            <h3 style="color: white; margin-bottom: 0.5rem;">Akshay Karthick S</h3>
            <p style="color: rgba(255,255,255,0.9); margin-bottom: 1.5rem; font-size: 1.1rem;">AI Engineer & Full Stack Developer</p>
            <a href="https://akshaykarthicks.github.io/AKS/" target="_blank" style="background: white; color: #667eea; padding: 12px 24px; border-radius: 25px; text-decoration: none; font-weight: bold; display: inline-block; transition: all 0.3s ease;">
                🌐 View Portfolio
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Project Overview
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 What is Goal Tracker Crew?
        
        An AI-powered assistant that transforms your aspirations into actionable, achievable plans using two specialized AI agents working in harmony.
        
        ### 🤖 AI Agents
        
        **🎯 Goal Tracker Agent**
        - Defines SMART goals with clear milestones
        - Monitors progress and provides feedback
        
        **📅 Planner Agent**
        - Creates realistic schedules
        - Optimizes time based on your constraints
        """)
    
    with col2:
        st.markdown("""
        ### ✨ Key Features
        
        - **Smart Goal Setting**: Transform ideas into actionable goals
        - **Personalized Planning**: Custom schedules for your lifestyle
        - **Progress Tracking**: Monitor your advancement
        - **Flexible Scheduling**: Adapts to your commitments
        - **Downloadable Plans**: Take your roadmap anywhere
        
        ### 🎨 Technology Stack
        
        - **CrewAI**: Multi-agent AI framework
        - **Gemini 1.5 Flash**: Advanced language model
        - **Streamlit**: Interactive web interface
        """)
    
    # Call to Action
    st.markdown("""
    ---
    <div style="text-align: center; padding: 2rem; background: #f8f9fa; border-radius: 10px; margin: 2rem 0;">
        <h3 style="color: #2c3e50; margin-bottom: 1rem;">Ready to achieve your goals?</h3>
        <p style="color: #34495e; margin-bottom: 1.5rem;">Let our AI agents help you create a personalized plan for success!</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()