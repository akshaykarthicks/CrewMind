#!/usr/bin/env python
import streamlit as st
import sys
import os
from datetime import datetime
import time
import re
import pandas as pd

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
    page_title="🎯 CrewMind AI",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS ---
st.markdown(f"""
<style>
    /* --- General --- */
    .stApp {{
        background: #F5F5F5;
        background-attachment: fixed;
    }}
    
    /* Main content area */
    .main .block-container {{
        padding-top: 2rem;
        max-width: 1200px;
    }}
    
    h1, h2, h3, h4, h5, h6 {{
        color: #000000 !important;
    }}

    /* --- Main Header --- */
    .main-header {{
        text-align: center;
        padding: 3rem 2rem;
        background: #000000;
        color: white;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
    }}
    .main-header h1 {{
        color: white !important;
        font-weight: 700;
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }}
    .main-header p {{
        color: #FFFFFF !important;
        font-size: 1.25rem;
    }}

    /* --- Cards & Containers --- */
    .card {{
        background: white;
        padding: 2rem;
        border-radius: 16px;
        border: 2px solid #E0E0E0;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
        margin-bottom: 1.5rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }}
    .card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.12);
        border-color: #000000;
    }}
    .card-header {{
        font-size: 1.4rem;
        font-weight: 700;
        color: #000000;
        margin-bottom: 1.5rem;
        border-bottom: 3px solid #E0E0E0;
        padding-bottom: 1rem;
    }}
    
    /* --- Form Styling --- */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {{
        background-color: #FAFAFA !important;
        border: 2px solid #D0D0D0 !important;
        border-radius: 10px !important;
        padding: 0.75rem !important;
        transition: all 0.3s ease !important;
        color: #000000 !important;
    }}
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus {{
        border-color: #000000 !important;
        box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.1) !important;
        background-color: white !important;
    }}
    
    /* --- Buttons --- */
    .stButton > button {{
        border-radius: 12px;
        padding: 0.875rem 2rem;
        font-weight: 600;
        font-size: 1.05rem;
        transition: all 0.3s ease;
        border: 2px solid #000000;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }}
    .stButton > button[kind="primary"] {{
        background: #000000;
        color: white;
    }}
    .stButton > button[kind="primary"]:hover {{
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.25);
        background: #1a1a1a;
    }}
    .stButton > button[kind="secondary"] {{
        background-color: white;
        color: #000000;
        border: 2px solid #000000;
    }}
    .stButton > button[kind="secondary"]:hover {{
        background-color: #000000;
        color: white;
    }}

    /* --- Tabs --- */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        background-color: #E8E8E8;
        padding: 0.5rem;
        border-radius: 12px;
    }}
    .stTabs [data-baseweb="tab"] {{
        height: 50px;
        background-color: transparent;
        border-radius: 10px;
        padding: 0 1.5rem;
        font-weight: 600;
        color: #666666;
        transition: all 0.3s ease;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: white !important;
        color: #000000 !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }}

    /* --- Expander --- */
    .stExpander {{
        background-color: white;
        border: 2px solid #D0D0D0 !important;
        border-radius: 12px !important;
        margin-bottom: 1rem;
    }}
    .stExpander:hover {{
        border-color: #000000 !important;
    }}

    /* --- Plan Display --- */
    .plan-section {{
        background: #FAFAFA;
        padding: 1.75rem;
        border-radius: 12px;
        border-left: 5px solid #000000;
        margin: 1.25rem 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }}
    .plan-section h3 {{
        color: #000000 !important;
        margin-top: 0;
        font-size: 1.3rem;
    }}
    .plan-section ul {{
        padding-left: 20px;
    }}
    .plan-section li {{
        margin-bottom: 0.75rem;
        color: #333333;
    }}
    
    /* --- Results Section --- */
    .results-container {{
        background: white;
        padding: 2.5rem;
        border-radius: 20px;
        border: 2px solid #E0E0E0;
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.1);
        margin-top: 2rem;
        animation: slideUp 0.5s ease;
    }}
    
    @keyframes slideUp {{
        from {{
            opacity: 0;
            transform: translateY(30px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    /* --- Metrics --- */
    [data-testid="stMetricValue"] {{
        font-size: 1.5rem;
        font-weight: 700;
        color: #000000;
    }}
    
    /* --- Sidebar --- */
    [data-testid="stSidebar"] {{
        background: #000000;
    }}
    [data-testid="stSidebar"] .stRadio > label {{
        color: #FFFFFF !important;
        font-weight: 600;
    }}
    [data-testid="stSidebar"] h2 {{
        color: #FFFFFF !important;
    }}
    [data-testid="stSidebar"] p {{
        color: #FFFFFF !important;
    }}
    [data-testid="stSidebar"] * {{
        color: #FFFFFF !important;
    }}
    
    /* --- Additional text colors --- */
    .stMarkdown p,{{
        color: #ffffff   !important;
        
    }}
    .stMarkdown div, .stMarkdown span, .stMarkdown li {{
        color: #000000  !important;
    }}
    
    label {{
        color: #000000 !important;
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
        <h1>🎯 CrewMind AI</h1>
        <p>Your personal AI-powered assistant for turning ambitions into achievements.</p>
    </div>
    """, unsafe_allow_html=True)

    # --- Sidebar ---
    with st.sidebar:
        st.header("Navigation")
        page = st.radio("Choose a page:", ["🚀 Goal Planner", "ℹ️ About"])

        if st.session_state.get('crew_result'):
            st.markdown("---")
            st.success("✅ Plan Generated!")
            if st.button("🔄 New Goal", use_container_width=True, key="sidebar_new"):
                clear_session_state()
                st.rerun()

    # --- Page Routing ---
    if page == "🚀 Goal Planner":
        show_goal_setting_page()
    else:
        show_about_page()

def clear_session_state():
    """Clears relevant keys from the session state."""
    for key in ['crew_result', 'goal_inputs', 'show_results']:
        if key in st.session_state:
            del st.session_state[key]

def show_goal_setting_page():
    """Displays the page for users to input their goals."""
    
    # Show form only if no results yet
    if not st.session_state.get('show_results'):
        st.header("🎯 Set Your Goal")
        
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
                    accountability_preference = st.selectbox(
                        "**Accountability style**",
                        ["Self-accountability", "Friend/family support", "Public commitment", "Regular check-ins", "No preference"],
                        index=0,
                        help="How do you prefer to stay accountable?"
                    )
                    current_commitments = st.text_area(
                        "**Any existing commitments?** (optional)",
                        placeholder="e.g., 'Full-time job (9-5), family time on weekends'",
                        height=100
                    )

                st.markdown("<br>", unsafe_allow_html=True)
                submitted = st.form_submit_button(
                    "🚀 Generate My Plan",
                    use_container_width=True,
                    type="primary"
                )

                if submitted:
                    if user_goal and timeline and available_time:
                        inputs = {
                            'user_goal': user_goal, 'timeline': timeline, 'available_time': available_time,
                            'current_commitments': current_commitments if current_commitments else 'None', 
                            'preferred_schedule': preferred_schedule,
                            'goal_type': goal_type, 'motivation_level': motivation_level,
                            'difficulty_preference': difficulty_preference,
                            'accountability_preference': accountability_preference,
                            'current_year': str(datetime.now().year)
                        }
                        st.session_state.goal_inputs = inputs
                        st.session_state.show_results = True
                        st.rerun()
                    else:
                        st.error("⚠️ Please fill in all required fields marked with *")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Show results inline if they exist
    if st.session_state.get('show_results'):
        if not st.session_state.get('crew_result'):
            run_crew_and_display_results(st.session_state.goal_inputs)
        else:
            display_inline_results()

def run_crew_and_display_results(inputs):
    """Runs the CrewAI process and handles the display of results."""
    st.header("🎉 Generating Your Plan")

    with st.spinner("🤖 AI agents are creating your personalized plan... This may take a moment."):
        try:
            crew = Crewmind().crew()
            result = crew.kickoff(inputs=inputs)
            
            st.session_state.crew_result = result
            st.success("✅ Success! Your personalized goal plan is ready!")
            time.sleep(0.5)
            st.rerun()

        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            st.warning("Please check your API key and try again.")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✏️ Edit Inputs", use_container_width=True):
                    st.session_state.show_results = False
                    st.rerun()
            with col2:
                if st.button("🔄 Try Again", use_container_width=True, type="primary"):
                    del st.session_state['crew_result']
                    st.rerun()

def display_inline_results():
    """Displays the generated goal plan inline on the same page."""
    inputs = st.session_state.goal_inputs
    result = st.session_state.crew_result
    content = result.raw if hasattr(result, 'raw') else str(result)

    st.markdown('<div class="results-container">', unsafe_allow_html=True)
    
    # Header with action buttons
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.header("📊 Your Personalized Plan")
    with col2:
        if st.button("✏️ Edit Goal", type="secondary", use_container_width=True, key="edit_goal_btn"):
            st.session_state.show_results = False
            del st.session_state['crew_result']
            st.rerun()
    with col3:
        if st.button("🔄 New Goal", type="secondary", use_container_width=True, key="new_goal_btn"):
            clear_session_state()
            st.rerun()
    
    # Goal Summary Card
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("<p class='card-header'>🎯 Goal Overview</p>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    col1.metric("Goal", inputs['goal_type'])
    col2.metric("Timeline", inputs['timeline'])
    col3.metric("Commitment", inputs['available_time'])
    
    with st.expander("View Full Goal Details", expanded=False):
        st.markdown(f"**Your Goal:** {inputs['user_goal']}")
        st.markdown(f"**Preferred Schedule:** {inputs['preferred_schedule']}")
        st.markdown(f"**Challenge Level:** {inputs['difficulty_preference']}")
        if inputs['current_commitments'] != 'None':
            st.markdown(f"**Commitments:** {inputs['current_commitments']}")
    st.markdown('</div>', unsafe_allow_html=True)

    # Results Tabs
    tab1, tab2, tab3 = st.tabs(["📋 Action Plan", "📅 Weekly Schedule", "💡 Success Tips"])

    with tab1:
        display_formatted_plan(content)

    with tab2:
        display_weekly_breakdown(content)
        
    with tab3:
        display_success_tips(content)

    # Download Button
    st.markdown("---")
    download_content = format_download_content(inputs, result)
    st.download_button(
        label="📄 Download Complete Plan",
        data=download_content,
        file_name=f"CrewMind_Plan_{datetime.now().strftime('%Y%m%d')}.md",
        mime="text/markdown",
        use_container_width=True,
        type="primary"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)



def display_formatted_plan(content):
    """Parses and displays the AI-generated plan in a structured, concise format."""
    st.markdown("#### Plan Overview")
    
    # Clean up the content - remove excessive whitespace and newlines
    content = re.sub(r'\n{3,}', '\n\n', content)
    content = re.sub(r'\s{2,}', ' ', content)
    
    # Split by common section markers (headers, numbered sections, bold text)
    # Look for patterns like: "##", "**", numbered lists, or ALL CAPS headings
    sections = re.split(r'\n(?=\*\*[^*]+\*\*:|\n#+\s|\n[A-Z][A-Z\s]{4,}:|\n\d+\.\s+[A-Z])', content)
    
    if len(sections) == 1:
        # If no clear sections found, try splitting by double newlines
        sections = [s.strip() for s in content.split('\n\n') if s.strip()]
    
    for section in sections:
        section = section.strip()
        if len(section) < 10:  # Skip very short sections
            continue

        lines = [l.strip() for l in section.split('\n') if l.strip()]
        if not lines:
            continue
            
        # Extract title from first line
        first_line = lines[0]
        title = first_line
        
        # Clean up title - remove markdown, emojis, extra formatting
        title = re.sub(r'^#+\s*', '', title)  # Remove markdown headers
        title = re.sub(r'\*\*([^*]+)\*\*', r'\1', title)  # Remove bold, keep text
        title = re.sub(r'^[-*•]\s*', '', title)  # Remove list markers
        title = re.sub(r':\s*$', '', title)  # Remove trailing colon
        title = title.strip()
        
        # Limit title length
        if len(title) > 60:
            title = title[:57] + "..."
        
        # Get body (rest of the lines)
        body_lines = lines[1:] if len(lines) > 1 else []
        
        # Clean and shorten body text
        body = '\n'.join(body_lines)
        
        # Remove excessive markdown formatting
        body = re.sub(r'\*\*([^*]+)\*\*', r'**\1**', body)  # Keep only essential bold
        body = re.sub(r'_{2,}', '', body)  # Remove underlines
        body = re.sub(r'#{3,}', '##', body)  # Limit header depth
        
        # Limit paragraph length - split long paragraphs
        sentences = re.split(r'([.!?]\s+)', body)
        if len(''.join(sentences)) > 500:
            # Keep only first few sentences if too long
            body = ''.join(sentences[:6]) + "..."
        
        if title and body:
            with st.expander(f"**{title}**", expanded=False):
                st.markdown(body, unsafe_allow_html=True)
        elif title:
            # If no body, just show title as a small note
            st.caption(f"• {title}")

def display_weekly_breakdown(content):
    """Extracts and displays all weekly schedule tables from the plan."""
    st.markdown("#### 📅 Weekly Schedule")

    # Find all occurrences of "Week X" sections
    weekly_sections = re.findall(r'(\#\#\#\s*Week\s*\d+.*?)(?=\n\#\#\#\s*Week|\Z)', content, re.DOTALL | re.IGNORECASE)

    if weekly_sections:
        for section in weekly_sections:
            st.markdown(section)
    else:
        # A simpler regex to find tables if the above fails
        tables = re.findall(r'(\|.*\|)', content)
        if tables:
            st.markdown("\n".join(tables))
        else:
            st.info("📅 No weekly schedule tables found in the output.")
            st.text(content)

def display_success_tips(content):
    """Extracts and displays success tips from the plan in a concise format."""
    st.markdown("#### Tips & Best Practices")

    # Regex to find tips section - look for various patterns
    tips_patterns = [
        r'(Success\s+Tips?[^\n]*\n.*?)(?=\n\*\*[A-Z]|\n##|\Z)',
        r'(Tips?\s+(?:for|to)[^\n]*\n.*?)(?=\n\*\*[A-Z]|\n##|\Z)',
        r'(Staying\s+Motivated[^\n]*\n.*?)(?=\n\*\*[A-Z]|\n##|\Z)',
        r'(Key\s+(?:to|Success)[^\n]*\n.*?)(?=\n\*\*[A-Z]|\n##|\Z)'
    ]
    
    tips_section = None
    for pattern in tips_patterns:
        tips_match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if tips_match:
            tips_section = tips_match.group(1)
            break
    
    if tips_section:
        # Extract bullet points
        items = re.findall(r'[-*•]\s+([^\n]+)', tips_section)
        if not items:
            items = re.findall(r'\d+[.)]\s+([^\n]+)', tips_section)
        
        if items:
            for item in items[:8]:  # Limit to 8 tips
                item_clean = re.sub(r'\*\*([^*]+)\*\*', r'**\1**', item.strip())  # Keep bold
                item_clean = re.sub(r'\s+', ' ', item_clean)  # Normalize whitespace
                if len(item_clean) > 120:  # Shorten long tips
                    item_clean = item_clean[:117] + "..."
                st.markdown(f"• {item_clean}")
        else:
            # Show text content, shortened
            tips_text = re.sub(r'\n{2,}', '\n', tips_section)
            tips_text = re.sub(r'\s+', ' ', tips_text[:400])
            if len(tips_section) > 400:
                tips_text += "..."
            st.markdown(tips_text)
    else:
        # Show concise default tips
        st.markdown("""
        • **Stay consistent** with your schedule
        • **Track progress** regularly  
        • **Adjust when needed** - plans are flexible
        • **Celebrate small wins** to maintain momentum
        """)

def format_download_content(inputs, result):
    """Formats the plan for a professional-looking markdown download."""
    content = result.raw if hasattr(result, 'raw') else str(result)
    
    download_template = f"""# 🎯 Personal Goal Achievement Plan

> Generated by CrewMind AI - Your personalized roadmap to success.

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
    st.header("ℹ️ About CrewMind AI")

    st.markdown("""
    <div class="card">
        <p class='card-header'>What is CrewMind AI?</p>
        <p>
            CrewMind AI is an intelligent assistant designed to help you transform your aspirations into actionable, 
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

