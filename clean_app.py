#!/usr/bin/env python
"""
Script to clean up the app.py file by removing duplicate functions
"""

def clean_app_file():
    """Clean up the app.py file"""
    
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the start of the old run_goal_tracker_crew function
    start_marker = "def run_goal_tracker_crew(user_goal, timeline, available_time, current_commitments, preferred_schedule, goal_type,"
    end_marker = "if __name__ == \"__main__\":"
    
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)
    
    if start_idx != -1 and end_idx != -1:
        # Keep everything before the old function and everything from main onwards
        cleaned_content = content[:start_idx] + content[end_idx:]
        
        with open('app.py', 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
        
        print("✅ App.py cleaned successfully!")
        print(f"Removed {end_idx - start_idx} characters of duplicate code")
    else:
        print("❌ Could not find the markers to clean the file")

if __name__ == "__main__":
    clean_app_file()