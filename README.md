# -Phi3-Autonomous-Agent-System
A Python bridge that connects Phi3 to your computer

Core Files:

phi3_autonomous_agent.py (500+ lines)

Main agent engine with tool-use system
8 autonomous control tools (keyboard, mouse, screenshots, commands, etc.)
Iterative decision-making loop
Conversation history management
Ready to import and use


phi3_web_dashboard.py (400+ lines)

Beautiful, professional web UI
Command input with history
Real-time agent monitoring
Terminal-style interface with green-on-black theme
Quick command buttons

quickstart.py

Interactive testing tool
5 different test scenarios
Menu-driven interface
Good for learning the system

Documentation:

README.md - Quick reference guide
SETUP_GUIDE.md - Complete 500-line setup & configuration manual
ADVANCED_GUIDE.md - Game automation examples, custom agents, state tracking
requirements.txt - All dependencies

Quick Start (Just 5 Minutes)
Step 1: Install Ollama & Phi3
bash# Download from https://ollama.ai
ollama pull phi3
ollama run phi3  # Keep this running
Step 2: Setup (in new terminal)
bashpython3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
Step 3: Run the Web Dashboard
bashpython3 phi3_web_dashboard.py
Then open http://localhost:5000 in your browser

🎮 What It Can Do
For mGBA Specifically:
"Open mGBA emulator"
"Open mGBA and load Pokemon Red"
"Walk around in the grass until a Pokemon appears"
"Catch a wild Pokemon"
"Battle and defeat a trainer"
"Navigate through Viridian Forest"
Any Application:
"Open VS Code"
"Launch Spotify and play music"
"Open Chrome and go to google.com"
"Open Calculator and solve 2+2"
System Tasks:
"Create a new file called test.txt"
"List all running processes"
"Take a screenshot and describe it"
"Find all PDF files in Downloads"

🔧 How It Works
The agent uses a tool-use system (function calling):

You give a command → "Open mGBA and load Pokemon Red"
Agent thinks → "I need to execute a command first"
Agent uses tools →

   <tool>execute_command</tool>
   <input>{"command": "open -a mGBA"}</input>

Sees result → Waits, then takes a screenshot
Analyzes state → "mGBA is open, now I need to load the ROM"
Uses more tools → Keyboard/mouse control to load file
Verifies → Takes another screenshot to confirm
Repeats → Until task is complete


🛠️ Available Tools (Automatic)
ToolWhat It Doesexecute_commandRun shell commands (open, start, etc.)get_screenshotSee what's on screenmouse_clickClick at (x, y) coordinateskeyboard_pressType text or press keyskeyboard_hotkeyPress Ctrl+C, Alt+Tab, etc.mouse_moveMove cursorwaitPause for N secondsget_running_processesSee running apps
The agent decides which tools to use automatically!

💡 Three Ways to Use It
Option A: Web Dashboard (Best)
bashpython3 phi3_web_dashboard.py
# Open http://localhost:5000
# Type commands in the browser
Option B: Python Script
pythonfrom phi3_autonomous_agent import Phi3Agent

agent = Phi3Agent()
agent.run("Open mGBA and load Pokemon Red")
Option C: Interactive Testing
bashpython3 quickstart.py
# Menu-driven testing interface

Example: Playing a Game
pythonfrom phi3_autonomous_agent import Phi3Agent
import time

agent = Phi3Agent()

# These run sequentially, agent sees results
tasks = [
    "Open mGBA emulator",
    "Load Pokemon Red ROM",
    "Walk into the tall grass 5 times",
    "Wait for a wild Pokemon to appear",
    "Throw a Pokeball to catch it",
    "Save the game",
]

for task in tasks:
    print(f"\nExecuting: {task}")
    result = agent.run(task, verbose=True)
    print(f"Result: {result}")
    time.sleep(2)

🔄 The Feedback Loop
This is what makes it truly autonomous:
┌─ Agent takes screenshot
│
├─ Agent analyzes what it sees
│
├─ Agent plans next action
│
├─ Agent executes action (keyboard/mouse/command)
│
├─ Agent waits for response
│
├─ Agent takes another screenshot
│
└─ Repeat until task complete!

⚙️ Customization
Change Model:
pythonagent = Phi3Agent(model="phi3.5")
Custom Tools:
pythonclass MyAgent(Phi3Agent):
    def _define_tools(self):
        tools = super()._define_tools()
        tools["browser_open"] = {
            "description": "Open a URL in browser",
            "parameters": {"url": "The URL"}
        }
        return tools
Game-Specific Agent:
pythonclass PokemonAgent(Phi3Agent):
    def catch_pokemon(self):
        return self.run("Find and catch a wild Pokemon")
    
    def battle_trainer(self):
        return self.run("Initiate and win a trainer battle")

agent = PokemonAgent()
agent.catch_pokemon()
See ADVANCED_GUIDE.md for 7 detailed examples!

📋 File Organization
your-project/
├── phi3_autonomous_agent.py      # Core engine
├── phi3_web_dashboard.py         # Web UI
├── quickstart.py                 # Testing tool
├── requirements.txt              # Dependencies
├── README.md                      # Quick ref
├── SETUP_GUIDE.md               # Detailed setup
└── ADVANCED_GUIDE.md            # Advanced usage

🚀 Next Steps

Install everything → Follow SETUP_GUIDE.md
Run the dashboard → python3 phi3_web_dashboard.py
Test it → "Open VS Code" or "Take a screenshot"
Explore games → Try mGBA commands
Customize → Add your own tools/prompts
Deploy → Run as background service


⚠️ Important Notes
✅ Works with: Any Ollama model (phi3, phi3.5, mistral, neural-chat, etc.)
✅ Cross-platform: Windows, macOS, Linux
✅ Full autonomy: Agent makes decisions without user intervention
⚠️ System access: Has full permission to run commands - only use on trusted machines
📚 Well documented: 1500+ lines of documentation included

🎓 To Learn More

SETUP_GUIDE.md - Detailed installation, troubleshooting, customization
ADVANCED_GUIDE.md - Game automation, specialized agents, multi-agent systems
Code comments - Both Python files are heavily commented
