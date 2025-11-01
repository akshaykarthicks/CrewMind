#!/usr/bin/env python
import streamlit as st
import sys
import os
from datetime import datetime
import time
import re

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

# --- Page Configuration ---
st.set_page_config(
    page_title="🎯 GoalForge AI",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS ---
st.markdown(f"""
<style>
    /* --- General --- */
    .stApp {{
        background-color: #F0F2F6;
    }}
    h1, h2, h3, h4, h5, h6 {{
        color: #1E293B !important;
    }}
    .stMarkdown p, .stMarkdown div, .stMarkdown span, .stMarkdown li {{
        color: #475569 !important;
    }}

    /* --- Main Header --- */
    .main-header {{
        text-align: center;
        padding: 2.5rem 1rem;
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
        color: white;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 16px rgba(99, 102, 241, 0.2);
    }}
    .main-header h1 {{
        color: white !important;
        font-weight: 700;
    }}
    .main-header p {{
        color: rgba(255, 255, 255, 0.9) !important;
        font-size: 1.1rem;
    }}

    /* --- Cards & Containers --- */
    .card {{
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 1rem;
    }}
    .card-header {{
        font-size: 1.2rem;
        font-weight: 600;
        color: #334155;
        margin-bottom: 1rem;
        border-bottom: 2px solid #F1F5F9;
        padding-bottom: 0.75rem;
    }}
    
    /* --- Buttons --- */
    .stButton > button {{
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        border: none;
    }}
    .stButton > button[kind="primary"] {{
        background: linear-gradient(90deg, #6366F1 0%, #8B5CF6 100%);
        color: white;
    }}
    .stButton > button[kind="primary"]:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(99, 102, 241, 0.3);
    }}
    .stButton > button[kind="secondary"] {{
        background-color: #F1F5F9;
        color: #475569;
    }}

    /* --- Tabs --- */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 24px;
    }}
    .stTabs [data-baseweb="tab"] {{
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 8px;
        padding: 0 1rem;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }}

    /* --- Expander --- */
    .stExpander {{
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        box-shadow: none !important;
    }}

    /* --- Plan Display --- */
    .plan-section {{
        background: #F8FAFC;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #6366F1;
        margin: 1rem 0;
    }}
    .plan-section h3 {{
        color: #1E293B !important;
        margin-top: 0;
    }}
    .plan-section ul {{
        padding-left: 20px;
    }}
    .plan-section li {{
        margin-bottom: 0.5rem;
    }}
</style>
""", unsafe_allow_html=True)


def show_api_key_error():
    """Displays an error message if the API key is not found."""
    st.error("❌ **Gemini API Key Not Found!**")
    st.markdown("""
    **Please follow these steps to set up your API key:**
    1. Go to: [Google AI Studio](https://makersuite.google.com/app/apikey)
    2. Click **"Create API Key"**
    3. Copy the generated key.
    4. Create a file named `.env` in the `crewmind` folder.
    5. Add the following line to the `.env` file, replacing `YOUR_API_KEY` with your actual key:
       ```
       GEMINI_API_KEY=YOUR_API_KEY
       ```
    6. Save the file and refresh this page.
    """)
    st.stop()

def main():
    """Main function to run the Streamlit app."""
    # Check for API key
    if not (os.getenv('GOOGLE_API_KEY') or os.getenv('GEMINI_API_KEY')):
        show_api_key_error()

    # --- Header ---
    st.markdown("""
    <div class="main-header">
        <h1>🎯 GoalForge AI</h1>
        <p>Your personal AI-powered assistant for turning ambitions into achievements.</p>
    </div>
    """, unsafe_allow_html=True)

    # --- Sidebar ---
    with st.sidebar:
        st.image("image.png", width=100)
        st.header("Navigation")
        page = st.radio("Choose a page:", ["🚀 Set a New Goal", "📊 View Plan", "ℹ️ About"])

        if st.session_state.get('crew_result'):
            st.markdown("---")
            st.success("✅ Goal plan generated!")
            if st.button("🔄 Start New Goal", use_container_width=True):
                clear_session_state()
                st.rerun()

    # --- Page Routing ---
    if page == "🚀 Set a New Goal":
        show_goal_setting_page()
    elif page == "📊 View Plan":
        show_results_page()
    else:
        show_about_page()

def clear_session_state():
    """Clears relevant keys from the session state."""
    for key in ['crew_result', 'goal_inputs', 'show_results']:
        if key in st.session_state:
            del st.session_state[key]

def show_goal_setting_page():
    """Displays the page for users to input their goals."""
    st.header("🎯 Let's Forge Your Goal")
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        with st.form("goal_form"):
            st.markdown("<p class='card-header'>Tell us what you want to achieve</p>", unsafe_allow_html=True)

            user_goal = st.text_area(
                "**What is your primary goal?** *",
                placeholder="e.g., 'Become a proficient Python developer and land a job in tech'",
                height=100,
                help="Be specific! The more detail, the better the plan."
            )
            
            col1, col2 = st.columns(2)
            with col1:
                timeline = st.selectbox(
                    "**Timeline** *",
                    ["3 Months", "6 Months", "1 Year", "Custom"],
                    help="Select a realistic timeframe for your goal."
                )
                if timeline == "Custom":
                    timeline = st.text_input("Enter custom timeline:", placeholder="e.g., '8 weeks'")
            
            with col2:
                goal_type = st.selectbox(
                    "**Goal Category**",
                    ["Professional Development", "Health & Fitness", "Personal Growth", "Education", "Creative", "Financial", "Other"],
                    help="Categorizing helps tailor the plan."
                )

            st.markdown("<p class='card-header' style='margin-top: 2rem;'>Your Availability & Preferences</p>", unsafe_allow_html=True)
            
            col3, col4 = st.columns(2)
            with col3:
                available_time = st.text_input(
                    "**How much time can you commit?** *",
                    placeholder="e.g., '10 hours per week'",
                    help="Be realistic about your weekly time commitment."
                )
            with col4:
                preferred_schedule = st.selectbox(
                    "**When are you most productive?**",
                    ["Early morning (6-9 AM)", "Morning (9-12 PM)", "Afternoon (12-5 PM)", "Evening (5-8 PM)", "Night (8-11 PM)", "Flexible"],
                )

            with st.expander("🔧 Advanced Options"):
                motivation_level = st.select_slider(
                    "**Current motivation level**",
                    options=["Low", "Medium", "High", "Very High"],
                    value="High"
                )
                difficulty_preference = st.selectbox(
                    "**Preferred challenge level**",
                    ["Gentle start", "Moderate challenge", "Ambitious push"],
                    index=1
                )
                current_commitments = st.text_area(
                    "**Any existing commitments?** (optional)",
                    placeholder="e.g., 'Full-time job (9-5), family time on weekends'",
                    height=100
                )

            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button(
                "🚀 Forge My Plan",
                use_container_width=True,
                type="primary"
            )

            if submitted:
                if user_goal and timeline and available_time:
                    inputs = {
                        'user_goal': user_goal, 'timeline': timeline, 'available_time': available_time,
                        'current_commitments': current_commitments, 'preferred_schedule': preferred_schedule,
                        'goal_type': goal_type, 'motivation_level': motivation_level,
                        'difficulty_preference': difficulty_preference,
                        'current_year': str(datetime.now().year)
                    }
                    st.session_state.goal_inputs = inputs
                    st.session_state.show_results = True
                    run_crew_and_display_results(inputs)
                else:
                    st.error("⚠️ Please fill in all required fields marked with *")
        
        st.markdown('</div>', unsafe_allow_html=True)

def run_crew_and_display_results(inputs):
    """Runs the CrewAI process and handles the display of results."""
    st.header("🎉 Your Personalized Goal Plan")

    with st.spinner("🤖 AI agents are forging your personalized plan... This may take a moment."):
        try:
            crew = Crewmind().crew()
            result = crew.kickoff(inputs=inputs)
            
            st.session_state.crew_result = result
            
            st.success("✅ Success! Your personalized goal plan has been forged!")
            time.sleep(1)
            # Use a rerun to switch to the results view cleanly
            st.rerun()

        except Exception as e:
            st.error(f"❌ An error occurred while forging your plan: {str(e)}")
            st.warning("Please check your API key and try again.")

def show_results_page():
    """Displays the generated goal plan results."""
    st.header("📊 Your Forged Plan")

    if not st.session_state.get('crew_result'):
        st.info("🎯 No goal plan found. Please set a new goal first!")
        if st.button("➡️ Go to Goal Setting"):
            clear_session_state()
            st.rerun()
        return

    inputs = st.session_state.goal_inputs
    result = st.session_state.crew_result
    content = result.raw if hasattr(result, 'raw') else str(result)

    # --- Goal Summary ---
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("<p class='card-header'>🎯 Goal Summary</p>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    col1.metric("🎯 Goal", inputs['user_goal'][:30] + "...")
    col2.metric("⏰ Timeline", inputs['timeline'])
    col3.metric("📅 Commitment", inputs['available_time'])
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Results Tabs ---
    tab1, tab2, tab3 = st.tabs(["📋 Full Action Plan", "📅 Weekly Breakdown", "💡 Success Tips"])

    with tab1:
        display_formatted_plan(content)

    with tab2:
        display_weekly_breakdown(content)
        
    with tab3:
        display_success_tips(content)

    # --- Download Button ---
    st.markdown("---")
    st.subheader("💾 Download Your Plan")
    download_content = format_download_content(inputs, result)
    st.download_button(
        label="📄 Download Full Plan as Markdown",
        data=download_content,
        file_name=f"goal_plan_{datetime.now().strftime('%Y%m%d')}.md",
        mime="text/markdown",
        use_container_width=True
    )

def display_formatted_plan(content):
    """Parses and displays the AI-generated plan in a structured format."""
    st.markdown("### 🗺️ Your Roadmap to Success")
    
    # Simple regex to find sections (lines in all caps or ending with a colon)
    sections = re.split(r'\n(?=[A-Z\s]+:|\n[A-Z\s]{5,}\n)', content)
    
    for section in sections:
        section = section.strip()
        if not section:
            continue

        lines = section.split('\n')
        title = lines[0].strip().replace('**', '').replace(':', '').title()
        body = '\n'.join(lines[1:]).strip()

        if body:
            with st.expander(f"**{title}**", expanded=True):
                st.markdown(body, unsafe_allow_html=True)

def display_weekly_breakdown(content):
    """Extracts and displays a weekly breakdown from the plan."""
    st.markdown("### 🗓️ Your Week-by-Week Guide")
    
    # Regex to find "Week X" sections
    weekly_sections = re.findall(r'(Week\s*\d+.*?)(?=\nWeek\s*\d+|\Z)', content, re.DOTALL | re.IGNORECASE)

    if not weekly_sections:
        st.info("A detailed weekly breakdown was not explicitly found in the plan. The full plan provides a general timeline.")
        st.markdown(content)
        return

    for i, week_content in enumerate(weekly_sections):
        week_content = week_content.strip()
        # Extract the title more reliably
        title_match = re.match(r'(Week\s*\d+.*?)(\n|$)', week_content)
        title = title_match.group(1).strip().replace('**', '') if title_match else f"Week {i+1}"
        
        st.markdown(f'<div class="plan-section"><h3>{title}</h3>', unsafe_allow_html=True)
        
        # Display content as a list
        items = re.split(r'\n\s*[-*]\s*', week_content)
        if len(items) > 1:
            st.markdown("<ul>" + "".join(f"<li>{item.strip()}</li>" for item in items[1:] if item.strip()) + "</ul>", unsafe_allow_html=True)
        else:
            st.markdown(week_content)
            
        st.markdown('</div>', unsafe_allow_html=True)

def display_success_tips(content):
    """Extracts and displays success tips from the plan."""
    st.markdown("### ✨ Tips for Staying on Track")

    # Regex to find a "Success Tips" or similar section
    tips_match = re.search(r'(Success Tips|Staying Motivated|Key to Success.*?)(\n\n|\Z)', content, re.DOTALL | re.IGNORECASE)
    
    if tips_match:
        tips_section = tips_match.group(0)
        items = re.split(r'\n\s*[-*]\s*', tips_section)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        for item in items[1:]:
            if item.strip():
                st.markdown(f"💡 {item.strip()}")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No specific success tips section found. General advice is often included throughout the plan.")
        # Generic tips
        st.markdown("""
        - **Consistency is key:** Stick to your schedule as much as possible.
        - **Track your progress:** Seeing how far you've come is a great motivator.
        - **Don't be afraid to adjust:** This plan is a guide, not a rigid set of rules.
        - **Celebrate your wins:** Acknowledge your hard work along the way!
        """)

def format_download_content(inputs, result):
    """Formats the plan for a professional-looking markdown download."""
    content = result.raw if hasattr(result, 'raw') else str(result)
    
    download_template = f"""# 🎯 Personal Goal Achievement Plan

> Generated by GoalForge AI - Your personalized roadmap to success.

---

## 📋 Goal Overview

| Aspect                  | Details                                       |
|-------------------------|-----------------------------------------------|
| **🎯 Goal**             | {inputs['user_goal']}                         |
| **⏰ Timeline**         | {inputs['timeline']}                          |
| **📂 Category**         | {inputs['goal_type']}                         |
| **🕒 Time Commitment**   | {inputs['available_time']}                    |
| **📅 Preferred Schedule** | {inputs.get('preferred_schedule', 'Flexible')} |
| **⚡ Challenge Level**   | {inputs.get('difficulty_preference', 'Moderate')} |
| **🗓️ Date Generated**   | {datetime.now().strftime('%B %d, %Y')}        |

---

## 🤖 AI-Generated Action Plan

{content}

---

## 💡 Success Tips

- **Review this plan weekly** to stay on track and make adjustments.
- **Break down large tasks** into smaller, manageable steps.
- **Celebrate small wins** to maintain momentum and motivation.
- **Stay consistent**, even when you don't feel motivated. Progress over perfection.
- **Share your goal** with someone for accountability.

> **You've got this!** Believe in your ability to achieve this goal.
"""
    return download_template

def show_about_page():
    """Displays the 'About' page with information on the project."""
    st.header("ℹ️ About GoalForge AI")

    st.markdown("""
    <div class="card">
        <p class='card-header'>What is GoalForge AI?</p>
        <p>
            GoalForge AI is an intelligent assistant designed to help you transform your aspirations into actionable, 
            well-structured plans. Using a team of specialized AI agents, it analyzes your goal, timeline, and 
            preferences to create a personalized roadmap for success.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="card">
            <p class='card-header'>🤖 The AI Agents</p>
            <ul>
                <li><strong>🎯 Goal Tracker Agent:</strong> Defines SMART goals, establishes clear milestones, and sets up metrics for progress.</li>
                <li><strong>📅 Planner Agent:</strong> Creates a realistic, optimized schedule based on your availability and commitments.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
            <p class='card-header'>🎨 Technology Stack</p>
            <ul>
                <li><strong>CrewAI:</strong> For orchestrating the multi-agent AI system.</li>
                <li><strong>Gemini 1.5 Flash:</strong> The powerful language model driving the agents.</li>
                <li><strong>Streamlit:</strong> For the interactive and user-friendly web interface.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card" style="text-align: center;">
        <p class='card-header'>👨‍💻 Developer</p>
        <h3>Akshay Karthick S</h3>
        <p>AI Engineer & Full Stack Developer</p>
        <a href="https://akshaykarthicks.github.io/AKS/" target="_blank">
            <button>🌐 View Portfolio</button>
        </a>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
s
