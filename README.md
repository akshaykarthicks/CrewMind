# 🎯 Goal Tracker Crew

An AI-powered goal setting and planning assistant built with CrewAI that helps you transform your aspirations into actionable, achievable plans.
<img width="1904" height="1064" alt="image" src="https://github.com/user-attachments/assets/d980d236-a76d-44af-b9c5-a3d4dffee9e8" />


![Goal Tracker Crew](https://img.shields.io/badge/AI-Powered-blue) ![CrewAI](https://img.shields.io/badge/CrewAI-Framework-green) ![Gemini](https://img.shields.io/badge/Gemini-1.5%20Flash-orange) ![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red)

## 🌟 Features

### 🤖 **Dual AI Agent System**
- **🎯 Goal Tracker Agent**: Transforms vague ideas into SMART goals with actionable milestones
- **📅 Planner Agent**: Creates realistic schedules that fit your lifestyle and commitments

### ✨ **Smart Goal Planning**
- **SMART Goal Creation**: Specific, Measurable, Achievable, Relevant, Time-bound
- **Personalized Scheduling**: Adapts to your available time and preferred schedule
- **Progress Monitoring**: Built-in tracking and accountability systems
- **Flexible Planning**: Accommodates existing commitments and constraints

### 🎨 **Beautiful Interface**
- **Streamlit Web App**: Interactive, user-friendly interface
- **Real-time Processing**: Watch AI agents work on your plan
- **Formatted Output**: Clean, readable goal plans with markdown formatting
- **Download Options**: Save your plans as markdown files

## 🚀 Quick Start

### Prerequisites
- Python 3.10+ 
- Gemini API Key from [Google AI Studio](https://makersuite.google.com/app/apikey)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd crewmind
   ```

2. **Install dependencies**
   ```bash
   pip install -e .
   ```

3. **Set up environment variables**
   ```bash
   # Create .env file
   echo "GOOGLE_API_KEY=your_gemini_api_key_here" > .env
   echo "GEMINI_API_KEY=your_gemini_api_key_here" >> .env
   ```

4. **Run the application**
   
   **Option 1: Streamlit Web App (Recommended)**
   ```bash
   streamlit run app.py
   ```
   
   **Option 2: Command Line Interface**
   ```bash
   python src/crewmind/main.py
   ```

## 🎯 How It Works

### 1. **Goal Input**
Tell the system what you want to achieve:
- Your specific goal
- Timeline for completion
- Available time commitment
- Current commitments and constraints
- Preferred working schedule

### 2. **AI Processing**
Two specialized agents collaborate:
- **Goal Tracker Agent** analyzes and structures your goal
- **Planner Agent** creates realistic schedules and action plans

### 3. **Personalized Plan**
Receive a comprehensive plan including:
- SMART goal breakdown
- Weekly and daily schedules
- Progress tracking framework
- Milestone checkpoints
- Accountability measures

## 📋 Example Usage

### Web Interface
1. Open `http://localhost:8501` after running `streamlit run app.py`
2. Fill in the goal setting form
3. Watch the AI agents create your plan
4. View results in organized tabs
5. Download your plan as markdown

### Command Line
```bash
python src/crewmind/main.py
```
Follow the interactive prompts to input your goal details.

## 🏗️ Project Structure

```
crewmind/
├── src/crewmind/           # Core application
│   ├── config/             # Agent and task configurations
│   │   ├── agents.yaml     # AI agent definitions
│   │   └── tasks.yaml      # Task specifications
│   ├── crew.py             # CrewAI crew orchestration
│   └── main.py             # CLI interface
├── app.py                  # Streamlit web interface
├── requirements.txt        # Python dependencies
├── pyproject.toml         # Project configuration
└── README.md              # This file
```

## ⚙️ Configuration

### Environment Variables
```env
# Required
GOOGLE_API_KEY=your_gemini_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here

# Optional
MODEL=gemini/gemini-1.5-flash
CREWAI_TELEMETRY_OPT_OUT=true
```

### Agent Configuration
The system uses template variables that are automatically filled with user input:
- `{{user_goal}}` - Your specific goal
- `{{timeline}}` - Achievement timeline
- `{{available_time}}` - Time commitment
- `{{current_commitments}}` - Existing obligations
- `{{preferred_schedule}}` - Preferred working times
- `{{goal_type}}` - Goal category
- `{{motivation_level}}` - Current motivation level

## 🎨 Features in Detail

### Goal Setting Form
- **Smart Validation**: Ensures required fields are completed
- **Helpful Tips**: SMART goal guidelines and examples
- **Advanced Options**: Difficulty level, accountability preferences
- **Category Selection**: Professional, Health, Education, Creative, etc.

### AI-Generated Plans
- **Structured Output**: Clear sections and formatting
- **Visual Progress**: Metrics and progress indicators
- **Actionable Steps**: Specific tasks with time estimates
- **Flexibility**: Buffer time and contingency plans

### Results Display
- **📋 Full Plan**: Complete AI-generated goal plan
- **📊 Plan Overview**: Structured breakdown with metrics
- **📅 Daily Schedule**: Calendar-style planning
- **💾 Download**: Markdown export with progress tracking

## 🛠️ Development

### Running Tests
```bash
# Test environment setup
python test_env.py

# Test API key
python test_api_key.py
```

### Project Commands
```bash
# Install in development mode
pip install -e .

# Run the crew directly
crewmind

# Run with custom inputs
python src/crewmind/main.py
```

## 🔧 Troubleshooting

### Common Issues

**1. API Key Errors**
```bash
# Test your API key
python test_api_key.py

# Set environment variables manually
export GOOGLE_API_KEY="your_key_here"
```

**2. Import Errors**
```bash
# Reinstall in development mode
pip install -e .
```

**3. Streamlit Issues**
```bash
# Run on different port
streamlit run app.py --server.port 8502
```

### Environment Setup
If you're having issues with environment variables:

**Windows (PowerShell):**
```powershell
$env:GOOGLE_API_KEY="your_key_here"
$env:GEMINI_API_KEY="your_key_here"
```

**Windows (CMD):**
```cmd
set GOOGLE_API_KEY=your_key_here
set GEMINI_API_KEY=your_key_here
```

## 📊 Example Output

The system generates comprehensive plans like:

```markdown
# 🎯 Goal Plan - Learn Python Programming

## Goal Details
- **Goal:** Learn Python programming and build 3 projects
- **Timeline:** 6 months
- **Available Time:** 2 hours per day, weekdays
- **Category:** Professional Development

## Weekly Schedule
### Monday - Friday
- **7:00-8:00 AM**: Python fundamentals study
- **8:00-9:00 AM**: Hands-on coding practice

## Milestones
1. **Month 1-2**: Python basics and syntax
2. **Month 3-4**: First project - Web scraper
3. **Month 5-6**: Advanced projects and portfolio
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **CrewAI**: Multi-agent AI framework
- **Google Gemini**: Advanced language model
- **Streamlit**: Interactive web interface
- **Community**: Contributors and users

## 📞 Support

- **Issues**: Report bugs and request features via GitHub Issues
- **Documentation**: Check the `/docs` folder for detailed guides
- **Community**: Join discussions in GitHub Discussions

---

**Ready to achieve your goals?** 🚀

Start by running `streamlit run app.py` and let AI help you create a personalized success plan!

## 🔗 Quick Links

- [Get Gemini API Key](https://makersuite.google.com/app/apikey)
- [CrewAI Documentation](https://docs.crewai.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Project Issues](https://github.com/your-repo/issues)

---

*Built with ❤️ using CrewAI and Gemini AI*
