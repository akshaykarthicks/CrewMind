#!/usr/bin/env python
# SQLite workaround for cloud environments # for streamlit cloud 
try:
    __import__('pysqlite3')
    import sys as _sys
    _sys.modules['sqlite3'] = _sys.modules.pop('pysqlite3')
except ImportError:
    pass

import sys
import os
import warnings
from datetime import datetime
from dotenv import load_dotenv
from crewmind.crew import Crewmind

# Load environment variables from .env file
# Try to load from multiple possible locations
load_dotenv()  # Current directory
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '..', '.env'))  # crewmind/.env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '..', '..', '.env'))  # root .env

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Goal Tracker Crew - Main execution file
# This runs the crew locally with sample inputs for goal tracking and planning.
# For Streamlit frontend, use app.py instead.

def get_user_input():
    """
    Get goal information from user input.
    """
    print("🎯 Welcome to Goal Tracker Crew!")
    print("Let's help you set and plan your goal.\n")
    
    # Get user goal
    user_goal = input("What goal do you want to achieve? \n> ").strip()
    while not user_goal:
        user_goal = input("Please enter your goal: \n> ").strip()
    
    # Get timeline
    print("\nHow long do you want to take to achieve this goal?")
    timeline = input("Timeline (e.g., '3 months', '1 year'): \n> ").strip()
    while not timeline:
        timeline = input("Please enter a timeline: \n> ").strip()
    
    # Get available time
    print("\nHow much time can you dedicate to this goal?")
    available_time = input("Available time (e.g., '2 hours per day', '10 hours per week'): \n> ").strip()
    while not available_time:
        available_time = input("Please enter your available time: \n> ").strip()
    
    # Get current commitments (optional)
    print("\nWhat are your current commitments? (optional)")
    current_commitments = input("Current commitments (e.g., 'Full-time job, gym 3x/week'): \n> ").strip()
    
    # Get preferred schedule (optional)
    print("\nWhen do you prefer to work on your goals? (optional)")
    preferred_schedule = input("Preferred time (e.g., 'Early morning', 'Evenings'): \n> ").strip()
    
    # Get goal type
    print("\nWhat type of goal is this?")
    print("1. Professional Development")
    print("2. Health & Fitness") 
    print("3. Education")
    print("4. Personal Growth")
    print("5. Creative")
    print("6. Other")
    
    goal_type_map = {
        '1': 'professional development',
        '2': 'health & fitness',
        '3': 'education', 
        '4': 'personal growth',
        '5': 'creative',
        '6': 'other'
    }
    
    choice = input("Choose (1-6): \n> ").strip()
    goal_type = goal_type_map.get(choice, 'other')
    
    return {
        'user_goal': user_goal,
        'timeline': timeline,
        'available_time': available_time,
        'current_commitments': current_commitments,
        'preferred_schedule': preferred_schedule,
        'goal_type': goal_type,
        'current_year': str(datetime.now().year)
    }


def run():
    """
    Run the Goal Tracker Crew with user input.
    """
    # Check if API key is set
    api_key = os.getenv('GOOGLE_API_KEY') or os.getenv('GEMINI_API_KEY')
    if not api_key or api_key == 'YOUR_GEMINI_API_KEY_HERE':
        print("❌ ERROR: Gemini API key not found!")
        print("Please follow these steps:")
        print("1. Go to: https://makersuite.google.com/app/apikey")
        print("2. Create a new API key")
        print("3. Edit the .env file and replace YOUR_GEMINI_API_KEY_HERE with your actual key")
        print("4. Save the file and run again")
        return None
    
    try:
        # Get user input
        inputs = get_user_input()
        
        print("\n" + "="*60)
        print("🎯 GOAL SUMMARY")
        print("="*60)
        print(f"Goal: {inputs['user_goal']}")
        print(f"Timeline: {inputs['timeline']}")
        print(f"Available Time: {inputs['available_time']}")
        print(f"Goal Type: {inputs['goal_type'].title()}")
        if inputs['current_commitments']:
            print(f"Current Commitments: {inputs['current_commitments']}")
        if inputs['preferred_schedule']:
            print(f"Preferred Schedule: {inputs['preferred_schedule']}")
        print("="*60)
        
        # Confirm before proceeding
        confirm = input("\nProceed with creating your goal plan? (y/n): ").strip().lower()
        if confirm not in ['y', 'yes']:
            print("Goal planning cancelled.")
            return
        
        print("\n🤖 Starting Goal Tracker Crew...")
        print("This may take a few minutes...")
        print("-" * 50)
        
        # Run the crew
        result = Crewmind().crew().kickoff(inputs=inputs)
        
        print("\n" + "="*60)
        print("🎉 GOAL TRACKER CREW COMPLETED!")
        print("="*60)
        print("Your personalized goal plan has been created!")
        print("Check the generated daily_plan.md file for your detailed plan.")
        print("="*60)
        
        return result
        
    except KeyboardInterrupt:
        print("\n\nGoal planning interrupted by user.")
        return None
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
        return None


if __name__ == "__main__":
    run()

