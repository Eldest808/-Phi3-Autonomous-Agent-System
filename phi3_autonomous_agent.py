#!/usr/bin/env python3
"""
Phi3 Autonomous Agent Controller
Bridges Ollama Phi3 to system commands and application control
Implements tool-use pattern for autonomous decision-making
"""

import json
import subprocess
import time
import re
from typing import Any, Dict, List, Optional
import requests
from datetime import datetime

# For application control
try:
    import pyautogui
    import mss
except ImportError:
    print("⚠️  Install optional dependencies: pip install pyautogui mss")
    pyautogui = None
    mss = None


class Phi3Agent:
    """Autonomous agent powered by Phi3 via Ollama"""
    
    def __init__(self, ollama_url: str = "http://localhost:11434", model: str = "phi3"):
        self.ollama_url = ollama_url
        self.model = model
        self.tools = self._define_tools()
        self.conversation_history = []
        self.max_iterations = 10
        self.iteration_count = 0
        
    def _define_tools(self) -> Dict[str, Any]:
        """Define available tools the agent can use"""
        return {
            "execute_command": {
                "description": "Execute a system shell command and get the output",
                "parameters": {
                    "command": "The shell command to execute (e.g., 'open -a mGBA' for Mac, 'start mGBA' for Windows, or 'mGBA' for Linux)",
                    "timeout": "How long to wait for command completion in seconds (default: 5)"
                }
            },
            "get_screenshot": {
                "description": "Take a screenshot to see the current state of the screen",
                "parameters": {}
            },
            "mouse_click": {
                "description": "Click the mouse at specified coordinates",
                "parameters": {
                    "x": "X coordinate (horizontal position)",
                    "y": "Y coordinate (vertical position)",
                    "button": "Mouse button: 'left', 'right', or 'middle' (default: 'left')"
                }
            },
            "mouse_move": {
                "description": "Move the mouse to specified coordinates",
                "parameters": {
                    "x": "X coordinate",
                    "y": "Y coordinate"
                }
            },
            "keyboard_press": {
                "description": "Press keyboard keys or type text",
                "parameters": {
                    "keys": "Key name or text to type (e.g., 'a', 'enter', 'backspace', or 'Hello World')"
                }
            },
            "keyboard_hotkey": {
                "description": "Press key combinations (e.g., Ctrl+C, Alt+Tab)",
                "parameters": {
                    "keys": "Keys to press together (e.g., 'ctrl,c' or 'alt,tab' or 'cmd,w')"
                }
            },
            "wait": {
                "description": "Wait/pause for a specified duration",
                "parameters": {
                    "seconds": "Number of seconds to wait"
                }
            },
            "get_running_processes": {
                "description": "Get list of currently running processes",
                "parameters": {}
            }
        }
    
    def _execute_tool(self, tool_name: str, tool_input: Dict) -> str:
        """Execute a tool and return the result"""
        try:
            if tool_name == "execute_command":
                return self._execute_command(
                    tool_input.get("command", ""),
                    tool_input.get("timeout", 5)
                )
            elif tool_name == "get_screenshot":
                return self._get_screenshot()
            elif tool_name == "mouse_click":
                return self._mouse_click(
                    tool_input.get("x", 0),
                    tool_input.get("y", 0),
                    tool_input.get("button", "left")
                )
            elif tool_name == "mouse_move":
                return self._mouse_move(tool_input.get("x", 0), tool_input.get("y", 0))
            elif tool_name == "keyboard_press":
                return self._keyboard_press(tool_input.get("keys", ""))
            elif tool_name == "keyboard_hotkey":
                return self._keyboard_hotkey(tool_input.get("keys", ""))
            elif tool_name == "wait":
                return self._wait(tool_input.get("seconds", 1))
            elif tool_name == "get_running_processes":
                return self._get_running_processes()
            else:
                return f"Unknown tool: {tool_name}"
        except Exception as e:
            return f"Error executing {tool_name}: {str(e)}"
    
    def _execute_command(self, command: str, timeout: int = 5) -> str:
        """Execute a shell command"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return f"Command executed. Output: {result.stdout if result.stdout else 'No output'}"
        except subprocess.TimeoutExpired:
            return f"Command timed out after {timeout} seconds"
    
    def _get_screenshot(self) -> str:
        """Get current screen state"""
        if not mss:
            return "Screenshot capability not available. Install mss: pip install mss"
        
        try:
            with mss.mss() as sct:
                monitor = sct.monitors[1]  # Primary monitor
                screenshot = sct.grab(monitor)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"/tmp/screenshot_{timestamp}.png"
                
                import PIL.Image
                img = PIL.Image.frombytes('RGB', screenshot.size, screenshot.rgb)
                img.save(filename)
                return f"Screenshot saved to {filename}. Screen size: {screenshot.size}"
        except Exception as e:
            return f"Screenshot failed: {str(e)}"
    
    def _mouse_click(self, x: int, y: int, button: str = "left") -> str:
        """Click the mouse"""
        if not pyautogui:
            return "Mouse control not available. Install pyautogui: pip install pyautogui"
        
        try:
            pyautogui.click(x, y, button=button)
            return f"Clicked at ({x}, {y}) with {button} button"
        except Exception as e:
            return f"Mouse click failed: {str(e)}"
    
    def _mouse_move(self, x: int, y: int) -> str:
        """Move the mouse"""
        if not pyautogui:
            return "Mouse control not available"
        
        try:
            pyautogui.moveTo(x, y, duration=0.5)
            return f"Mouse moved to ({x}, {y})"
        except Exception as e:
            return f"Mouse move failed: {str(e)}"
    
    def _keyboard_press(self, keys: str) -> str:
        """Press keyboard keys or type text"""
        if not pyautogui:
            return "Keyboard control not available"
        
        try:
            # Check if it's a special key or text
            special_keys = {'enter', 'tab', 'backspace', 'delete', 'space', 'escape',
                           'up', 'down', 'left', 'right', 'home', 'end', 'pageup', 'pagedown'}
            
            if keys.lower() in special_keys:
                pyautogui.press(keys.lower())
                return f"Pressed key: {keys}"
            else:
                pyautogui.typewrite(keys, interval=0.05)
                return f"Typed: {keys}"
        except Exception as e:
            return f"Keyboard input failed: {str(e)}"
    
    def _keyboard_hotkey(self, keys: str) -> str:
        """Press key combinations"""
        if not pyautogui:
            return "Keyboard control not available"
        
        try:
            key_list = [k.strip() for k in keys.split(',')]
            pyautogui.hotkey(*key_list)
            return f"Pressed hotkey: {keys}"
        except Exception as e:
            return f"Hotkey failed: {str(e)}"
    
    def _wait(self, seconds: float) -> str:
        """Wait for specified duration"""
        try:
            time.sleep(seconds)
            return f"Waited for {seconds} seconds"
        except Exception as e:
            return f"Wait failed: {str(e)}"
    
    def _get_running_processes(self) -> str:
        """Get list of running processes"""
        try:
            result = subprocess.run(
                "ps aux" if subprocess.os.name != 'nt' else "tasklist",
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )
            # Return just the first 20 lines to keep it concise
            lines = result.stdout.split('\n')[:20]
            return "Running processes:\n" + '\n'.join(lines)
        except Exception as e:
            return f"Failed to get processes: {str(e)}"
    
    def _parse_tool_calls(self, response: str) -> List[Dict[str, Any]]:
        """Extract tool calls from model response"""
        tool_calls = []
        
        # Look for tool calls in format: <tool>name</tool><input>{...}</input>
        tool_pattern = r'<tool>(\w+)</tool>\s*<input>(.*?)</input>'
        matches = re.findall(tool_pattern, response, re.DOTALL)
        
        for tool_name, tool_input_str in matches:
            try:
                tool_input = json.loads(tool_input_str)
                tool_calls.append({
                    "tool": tool_name,
                    "input": tool_input
                })
            except json.JSONDecodeError:
                # Try to parse as simple key=value format
                continue
        
        return tool_calls
    
    def _build_system_prompt(self) -> str:
        """Build the system prompt with tool definitions"""
        tools_description = "You have access to these tools:\n\n"
        
        for tool_name, tool_info in self.tools.items():
            tools_description += f"<tool>{tool_name}</tool>\n"
            tools_description += f"Description: {tool_info['description']}\n"
            if tool_info['parameters']:
                tools_description += "Parameters:\n"
                for param, desc in tool_info['parameters'].items():
                    tools_description += f"  - {param}: {desc}\n"
            tools_description += "\n"
        
        return f"""You are an autonomous agent powered by advanced reasoning. Your goal is to execute user commands and control applications.

{tools_description}

When you need to use a tool, format your response like this:
<tool>tool_name</tool>
<input>{{"parameter1": "value1", "parameter2": "value2"}}</input>

You can use multiple tools in sequence. After using tools, analyze the results and decide if you need more tools or if the task is complete.

Important:
- Always explain what you're doing
- Take screenshots to verify your actions
- Be systematic and thoughtful
- Report success or issues clearly
"""
    
    def run(self, user_input: str, verbose: bool = True) -> str:
        """Run the agent with a user command"""
        self.iteration_count = 0
        self.conversation_history = []
        
        if verbose:
            print(f"\n{'='*60}")
            print(f"User Command: {user_input}")
            print(f"{'='*60}\n")
        
        # Add user message
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })
        
        while self.iteration_count < self.max_iterations:
            self.iteration_count += 1
            
            if verbose:
                print(f"\n[Iteration {self.iteration_count}]")
            
            # Get response from Phi3
            response = self._call_ollama()
            
            if verbose:
                print(f"Agent Response:\n{response}\n")
            
            self.conversation_history.append({
                "role": "assistant",
                "content": response
            })
            
            # Check if there was an error
            if "Error" in response or "error" in response:
                if verbose:
                    print("\n✗ Task failed with error")
                return response
            
            # Parse and execute tools
            tool_calls = self._parse_tool_calls(response)
            
            if not tool_calls:
                # No more tools to call, task complete
                if verbose:
                    print("\n✓ Task completed")
                return response
            
            # Execute tools and collect results
            tool_results = []
            for tool_call in tool_calls:
                tool_name = tool_call["tool"]
                tool_input = tool_call["input"]
                
                if verbose:
                    print(f"  Executing: {tool_name}({tool_input})")
                
                result = self._execute_tool(tool_name, tool_input)
                tool_results.append(f"{tool_name}: {result}")
                
                if verbose:
                    print(f"  Result: {result}")
            
            # Add tool results to conversation
            self.conversation_history.append({
                "role": "user",
                "content": f"Tool Results:\n" + "\n".join(tool_results)
            })
        
        return "Max iterations reached"
    
    def _call_ollama(self) -> str:
        """Call the Ollama API with conversation history"""
        try:
            system_prompt = self._build_system_prompt()
            
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt}
                ] + self.conversation_history,
                "stream": False,
                "temperature": 0.7,
            }
            
            response = requests.post(
                f"{self.ollama_url}/api/chat",
                json=payload,
                timeout=180  # Increased from 60 to 180 seconds for slower systems
            )
            response.raise_for_status()
            
            result = response.json()
            return result.get("message", {}).get("content", "No response")
        
        except requests.exceptions.ConnectionError:
            return f"Error: Cannot connect to Ollama at {self.ollama_url}. Make sure Ollama is running."
        except Exception as e:
            return f"Error calling Ollama: {str(e)}"


def main():
    """Example usage"""
    agent = Phi3Agent(
        ollama_url="http://localhost:11434",
        model="phi3"
    )
    
    # Example commands
    examples = [
        "Open mGBA emulator",
        # "Open mGBA and load Pokemon Red from ~/Games/pokemon_red.gba",
        # "In mGBA, walk up 5 times then save the game",
    ]
    
    for command in examples:
        result = agent.run(command, verbose=True)
        print(f"\nFinal Result: {result}")
        time.sleep(2)


if __name__ == "__main__":
    main()
