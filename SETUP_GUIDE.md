# Phi3 Autonomous Agent - Complete Setup Guide

## Overview

This system bridges your local Ollama Phi3 model to system commands and application control, enabling truly autonomous operation. The agent can:

- ✅ Open and launch applications
- ✅ Execute system commands
- ✅ Control mouse and keyboard
- ✅ Take screenshots and analyze screen state
- ✅ Make autonomous decisions based on visual feedback
- ✅ Control games in emulators (like mGBA)
- ✅ Perform complex multi-step tasks

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│         Your Command / Web Dashboard                     │
└────────────────┬────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────┐
│      Phi3 Autonomous Agent (phi3_autonomous_agent.py)   │
│                                                          │
│  - Tool-use System (function calling)                   │
│  - Conversation Management                             │
│  - Iterative decision making                           │
└────────────────┬────────────────────────────────────────┘
                 │
       ┌─────────┼─────────┐
       │         │         │
┌──────▼─┐ ┌────▼──┐ ┌───▼──────┐
│ Ollama │ │System │ │Application│
│ Phi3  │ │Commands│ │Control   │
└────────┘ └───────┘ └──────────┘
```

## Prerequisites

### 1. Ollama with Phi3

Install Ollama from https://ollama.ai

Pull the Phi3 model:
```bash
ollama pull phi3
```

Verify it works:
```bash
ollama run phi3
```

Type `exit` to quit. Leave Ollama running in the background.

### 2. Python 3.8+

Check your Python version:
```bash
python3 --version
```

## Installation

### Step 1: Clone or Copy Files

Copy these files to your project directory:
- `phi3_autonomous_agent.py` - Core agent logic
- `phi3_web_dashboard.py` - Web interface (optional)
- `requirements.txt` - Python dependencies

### Step 2: Install Dependencies

```bash
# Create a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Verify Ollama Connection

```bash
# Test connection to Ollama
python3 -c "
import requests
try:
    r = requests.get('http://localhost:11434/api/tags')
    print('✓ Ollama is running')
    print('Available models:', r.json())
except:
    print('✗ Cannot connect to Ollama. Make sure it is running.')
"
```

## Usage

### Option 1: Command Line Usage

```python
from phi3_autonomous_agent import Phi3Agent

# Create agent
agent = Phi3Agent(
    ollama_url="http://localhost:11434",
    model="phi3"
)

# Run a command
result = agent.run("Open mGBA and load Pokemon Red")
print(result)
```

### Option 2: Web Dashboard (Recommended)

Start the web server:
```bash
python3 phi3_web_dashboard.py
```

Open browser to: **http://localhost:5000**

You'll see a beautiful terminal-style interface where you can:
1. Type commands
2. Watch the agent execute them in real-time
3. See tool usage and results
4. Access command history

### Option 3: Script with Multiple Commands

```python
from phi3_autonomous_agent import Phi3Agent
import time

agent = Phi3Agent()

commands = [
    "Open mGBA emulator",
    "Load Pokemon Red game file from ~/Games/pokemon_red.gba",
    "Walk to the first grass patch and catch a Pokemon",
]

for cmd in commands:
    print(f"\n>>> {cmd}")
    agent.run(cmd, verbose=True)
    time.sleep(2)
```

## Available Tools

The agent can use these tools (automatically):

### System Commands
```
execute_command(command, timeout=5)
  - Run any shell command
  - Example: "open -a mGBA" (Mac), "start mGBA" (Windows)
```

### Screen Control
```
get_screenshot()
  - Take a screenshot to see current state
  - Helps agent verify actions worked

mouse_click(x, y, button='left')
  - Click at coordinates
  - button: 'left', 'right', or 'middle'

mouse_move(x, y)
  - Move mouse to position

keyboard_press(keys)
  - Type text or press keys
  - Special keys: 'enter', 'tab', 'space', 'backspace', 'escape'
  - Example: keyboard_press('Hello') or keyboard_press('enter')

keyboard_hotkey(keys)
  - Press key combinations
  - Example: 'ctrl,s' or 'alt,tab' or 'cmd,w'
```

### Utility
```
wait(seconds)
  - Pause execution
  
get_running_processes()
  - List running applications
```

## Example Commands

### Opening Applications
```
"Open VS Code"
"Open Chrome and navigate to google.com"
"Launch the Spotify application"
```

### Game Automation
```
"Open mGBA and load Pokemon Red from ~/Games/pokemon_red.gba"
"Walk to the first grass patch in the game"
"Battle and catch the first wild Pokemon"
```

### System Tasks
```
"Create a file called test.txt with the text 'hello world'"
"List all running processes and find Firefox"
"Take a screenshot and describe what you see"
```

## How It Works (Advanced)

### Tool-Use System

The agent uses a structured tool format:

```xml
<tool>tool_name</tool>
<input>{"parameter": "value"}</input>
```

Example response from Phi3:
```
I need to open mGBA first.
<tool>execute_command</tool>
<input>{"command": "open -a mGBA"}</input>

Now let me wait for it to load.
<tool>wait</tool>
<input>{"seconds": 2}</input>

Let me take a screenshot to see the current state.
<tool>get_screenshot</tool>
<input>{}</input>
```

### Iterative Decision Making

1. **User Command** → Agent analyzes task
2. **Tool Execution** → Agent decides what tool to use
3. **Feedback Loop** → Agent sees results (screenshot, command output)
4. **Refinement** → Agent decides next steps or declares task complete
5. **Repeat** → Until max iterations or task complete

### System Prompt Engineering

The agent receives a detailed system prompt that:
- Defines all available tools
- Explains tool format
- Encourages systematic thinking
- Promotes result verification

## Customization

### Modify Available Tools

Edit `_define_tools()` in `phi3_autonomous_agent.py`:

```python
def _define_tools(self):
    return {
        "my_custom_tool": {
            "description": "What this tool does",
            "parameters": {
                "param1": "Description of param1"
            }
        }
        # ... add more tools
    }
```

Then implement in `_execute_tool()`:

```python
def _execute_tool(self, tool_name, tool_input):
    if tool_name == "my_custom_tool":
        return self._my_custom_tool(tool_input.get("param1"))
```

### Change Model

Switch to a different model:

```python
agent = Phi3Agent(model="phi3.5")  # or phi, mistral, neural-chat, etc.
```

### Adjust Temperature

More creative responses:
```python
# In _call_ollama(), modify:
payload["temperature"] = 1.0  # More creative
```

Lower values = more deterministic:
```python
payload["temperature"] = 0.3  # More focused
```

### Increase Max Iterations

For complex tasks:
```python
agent.max_iterations = 20  # Default is 10
```

## Troubleshooting

### "Cannot connect to Ollama"
- Make sure Ollama is running: `ollama run phi3`
- Check it's on `localhost:11434`
- Verify with: `curl http://localhost:11434/api/tags`

### Agent keeps looping
- Increase `max_iterations` if task is complex
- Adjust system prompt for clearer completion criteria
- Use simpler, more specific commands

### Poor task completion
- Make sure model has enough context: longer conversation history
- Use screenshots to help agent see results
- Break complex tasks into smaller steps

### "Module not found" errors
- Reinstall requirements: `pip install -r requirements.txt`
- Make sure virtual environment is activated
- Check Python version: `python3 --version`

### System control not working
- Install system control libraries:
  ```bash
  pip install pyautogui mss pillow
  ```
- On Linux, may need: `sudo apt-get install python3-tk`
- Disable mouse/keyboard in system settings if blocked

## Performance Tips

1. **Use Web Dashboard** - Better feedback than CLI
2. **Take Screenshots** - Helps agent verify actions
3. **Longer Thinking** - Let agent process results
4. **Simple Instructions** - Clear commands work better
5. **Add Waits** - Game/app loading takes time

Example with waits:
```
"Open mGBA, wait 3 seconds, then load Pokemon Red"
```

## Security Considerations

⚠️ **Important**: This agent has full system access

- Only run on trusted machines
- Don't expose web dashboard to internet without authentication
- Commands are executed with your user's permissions
- Be careful with what you ask it to do

For public use, add authentication:

```python
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    if username == "admin" and password == "your_password":
        return username

@app.route('/api/execute', methods=['POST'])
@auth.login_required
def api_execute():
    # ... rest of code
```

## Advanced Features

### Custom Tool Example: Browser Control

```python
def _open_url(self, url: str) -> str:
    """Open URL in default browser"""
    import webbrowser
    try:
        webbrowser.open(url)
        return f"Opened {url} in browser"
    except Exception as e:
        return f"Failed to open URL: {str(e)}"
```

Add to tools dict:
```python
"open_url": {
    "description": "Open a URL in the default web browser",
    "parameters": {"url": "The URL to open"}
}
```

Add to execute:
```python
elif tool_name == "open_url":
    return self._open_url(tool_input.get("url", ""))
```

## Next Steps

1. **Start Simple** - Test with basic commands first
2. **Experiment** - Try different task types
3. **Iterate** - Refine prompts based on results
4. **Expand** - Add custom tools for your needs
5. **Deploy** - Run as service for automation

## Resources

- Ollama: https://ollama.ai
- Phi3: https://huggingface.co/microsoft/phi-3
- PyAutoGUI: https://pyautogui.readthedocs.io
- Flask: https://flask.palletsprojects.com

## Support

For issues:
1. Check Ollama is running: `ollama run phi3`
2. Verify Python dependencies: `pip list`
3. Check system control permissions
4. Review error messages in console
5. Try simpler commands first

## License

This code is provided as-is for educational and personal use.

---

**Enjoy your autonomous agent! 🚀**
