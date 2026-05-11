# 🚀 Phi3 Autonomous Agent - Complete System

Transform your local Phi3 LLM into a fully autonomous system that can execute commands, control applications, and play games.

## 📦 What You Get

This complete package includes:

```
phi3_autonomous_agent.py      - Core agent engine with tool-use system
phi3_web_dashboard.py         - Beautiful web UI for control
quickstart.py                 - Interactive testing tool
SETUP_GUIDE.md               - Complete installation & setup
ADVANCED_GUIDE.md            - Game automation & advanced usage
requirements.txt             - Python dependencies
```

## ⚡ Quick Start (5 minutes)

### 1. Install Ollama & Phi3
```bash
# Download from https://ollama.ai
ollama pull phi3
ollama run phi3  # Leave running
```

### 2. Setup Python
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run It
```bash
# Web Dashboard (Recommended)
python3 phi3_web_dashboard.py
# Open http://localhost:5000

# OR Interactive Quickstart
python3 quickstart.py

# OR In Python script
from phi3_autonomous_agent import Phi3Agent
agent = Phi3Agent()
agent.run("Open mGBA emulator")
```

## 🎮 What It Can Do

### ✅ System Control
- Open applications and software
- Execute shell commands
- Navigate file systems
- Manage processes

### ✅ Application Control
- Control mouse and keyboard
- Click, type, hotkeys
- Interact with any application
- Play games in emulators

### ✅ Autonomous Decision Making
- See current state via screenshots
- Analyze what's on screen
- Plan next steps intelligently
- Adapt to changing conditions
- Complete complex multi-step tasks

### ✅ Real-World Examples

**Open an app:**
```
"Open VS Code"
"Launch Spotify"
"Open mGBA emulator"
```

**Game automation:**
```
"Open Pokemon Red in mGBA and catch a wild Pokemon"
"Navigate to the first gym and battle the trainer"
"Walk around Viridian Forest and catch 3 Pokemon"
```

**System tasks:**
```
"Create a new file called test.txt with content 'hello'"
"Take a screenshot and describe what you see"
"Find and open all .pdf files in my Downloads"
```

## 🏗️ Architecture

```
┌─────────────────────────────────┐
│   Your Command or Web UI        │
└──────────────┬──────────────────┘
               │
┌──────────────▼──────────────────┐
│   Phi3 Agent (phi3_autonomous_  │
│       agent.py)                 │
├─────────────────────────────────┤
│  • Tool-use system              │
│  • Conversation management      │
│  • Iterative decision making    │
└──────────────┬──────────────────┘
               │
     ┌─────────┼─────────┐
     │         │         │
┌────▼──┐ ┌───▼──┐ ┌───▼────┐
│ Ollama│ │System│ │ App    │
│ Phi3  │ │Cmds  │ │Control │
└───────┘ └──────┘ └────────┘
```

## 🔧 Configuration

### Change Model
```python
agent = Phi3Agent(model="phi3.5")  # or phi, mistral, neural-chat
```

### Adjust Verbosity
```python
agent.run("command", verbose=True)   # See all details
agent.run("command", verbose=False)  # Silent mode
```

### Control Iterations
```python
agent.max_iterations = 20  # Allow more steps for complex tasks
```

### Customize Tools
Add your own tools by extending the `Phi3Agent` class:

```python
from phi3_autonomous_agent import Phi3Agent

class CustomAgent(Phi3Agent):
    def _define_tools(self):
        tools = super()._define_tools()
        tools["my_tool"] = {
            "description": "What it does",
            "parameters": {"param": "description"}
        }
        return tools
    
    def _execute_tool(self, tool_name, tool_input):
        if tool_name == "my_tool":
            return self._my_tool_impl(tool_input)
        return super()._execute_tool(tool_name, tool_input)
    
    def _my_tool_impl(self, params):
        # Your implementation
        return "result"
```

## 📊 Available Tools

The agent can use these tools automatically:

| Tool | Purpose |
|------|---------|
| `execute_command` | Run shell commands |
| `get_screenshot` | Capture screen state |
| `mouse_click` | Click at coordinates |
| `mouse_move` | Move mouse |
| `keyboard_press` | Type or press keys |
| `keyboard_hotkey` | Key combinations (Ctrl+S) |
| `wait` | Pause execution |
| `get_running_processes` | List running apps |

## 💡 Usage Patterns

### Pattern 1: Simple Commands
```python
agent = Phi3Agent()
result = agent.run("Open Chrome and google.com")
```

### Pattern 2: Multi-Step Tasks
```python
tasks = [
    "Open mGBA emulator",
    "Load Pokemon Red ROM",
    "Save the game",
]

for task in tasks:
    agent.run(task)
    time.sleep(2)
```

### Pattern 3: Specialized Agents
```python
class GameAgent(Phi3Agent):
    def play_game(self):
        return self.run("Play and win a Pokemon battle")

agent = GameAgent()
result = agent.play_game()
```

### Pattern 4: State Tracking
```python
agent = Phi3Agent()
state = {
    "game": "Pokemon Red",
    "level": 1,
    "pokemon": []
}

result = agent.run("Catch a Pokemon")
state["pokemon"].append("Pikachu")
```

## 🐛 Troubleshooting

### Ollama Not Connecting
```bash
# Check Ollama is running
curl http://localhost:11434/api/tags

# If not working:
ollama serve  # Start Ollama server
```

### Python Module Errors
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Check Python version
python3 --version  # Need 3.8+
```

### System Control Not Working
```bash
# Install optional packages
pip install pyautogui mss pillow

# Linux may need:
sudo apt-get install python3-tk
```

### Agent Not Completing Tasks
- Use simpler, clearer instructions
- Add screenshots to task instructions
- Increase `max_iterations`
- Check Ollama response quality

## 📈 Performance Tips

1. **Use Web Dashboard** - Better feedback than CLI
2. **Take Screenshots** - Helps agent understand state
3. **Be Specific** - Clear instructions = better results
4. **Add Timing** - Use `wait()` for app loading
5. **Test First** - Start with simple commands
6. **Monitor Output** - Watch what agent does

## 🔒 Security Notes

⚠️ **Important**: This system has full system access

- Only run on trusted machines
- Don't expose web dashboard publicly without auth
- Commands execute with your user permissions
- Be careful what you ask it to do

To add authentication:
```python
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()
```

## 📚 Documentation

- **SETUP_GUIDE.md** - Complete installation instructions
- **ADVANCED_GUIDE.md** - Game automation & advanced patterns
- **phi3_autonomous_agent.py** - Main agent code (well commented)
- **phi3_web_dashboard.py** - Web interface code

## 🎯 Common Tasks

### Open an Application
```python
agent.run("Open [app name]")
```

### Take a Screenshot
```python
agent.run("Take a screenshot and describe what you see")
```

### Play a Game
```python
agent.run("Open mGBA with Pokemon Red and catch a wild Pokemon")
```

### Control Applications
```python
agent.run("Click on the save button then press Ctrl+S")
```

### Automate Workflows
```python
agent.run("""
1. Open Excel
2. Create a new spreadsheet
3. Add headers: Name, Email, Phone
4. Save as contacts.xlsx
""")
```

## 🚀 Next Steps

1. **Start Simple** - Test with basic commands
2. **Explore Tools** - Try different capabilities
3. **Customize** - Add your own tools
4. **Automate** - Build workflows
5. **Deploy** - Run as background service

## 🤝 Contributing

To extend the system:
1. Add new tools to `_define_tools()`
2. Implement tool handlers in `_execute_tool()`
3. Update system prompt in `_build_system_prompt()`
4. Test with `quickstart.py`

## 📝 Examples

See **ADVANCED_GUIDE.md** for:
- Pokemon game automation
- Custom game agents
- Multi-agent coordination
- Task decomposition
- Game state tracking
- Performance optimization

## ⚙️ Requirements

- Python 3.8+
- Ollama + Phi3 model
- ~2GB RAM minimum
- Network connection (localhost:11434)

Optional:
- pyautogui, mss, pillow (for system control)
- Flask, Flask-CORS (for web dashboard)

## 📊 System Stats

- **Response Time**: ~2-5 seconds per iteration
- **Max Iterations**: 10 (configurable)
- **Token Context**: Full conversation history
- **Model**: Phi3 (7B parameters)

## 🎓 Learning Resources

- Ollama: https://ollama.ai
- Phi3 Paper: https://huggingface.co/microsoft/phi-3
- PyAutoGUI: https://pyautogui.readthedocs.io/
- Flask: https://flask.palletsprojects.com/

## 🤝 Support

For issues:
1. Check Ollama is running: `ollama run phi3`
2. Verify dependencies: `pip list | grep -E "requests|flask|pyautogui"`
3. Test connection: `python3 -c "import requests; print(requests.get('http://localhost:11434/api/tags').json())"`
4. Try simple commands first
5. Check error messages in console

## 📄 License

This code is provided as-is for educational and personal use.

---

## 🎉 Ready to Get Started?

```bash
# 1. Ensure Ollama is running
ollama run phi3

# 2. Install dependencies (in new terminal)
pip install -r requirements.txt

# 3. Start the dashboard
python3 phi3_web_dashboard.py

# 4. Open browser
# http://localhost:5000

# 5. Give it a command!
# "Open VS Code"
# "Take a screenshot"
# "Open mGBA"
```

**Enjoy your autonomous agent! 🚀**

For detailed setup: See **SETUP_GUIDE.md**
For advanced usage: See **ADVANCED_GUIDE.md**
For testing: Run `python3 quickstart.py`
