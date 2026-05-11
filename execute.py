#!/usr/bin/env python3
"""
Phi3 Autonomous Agent - Simple Command Executor
Type commands directly, agent executes them on your system
"""

import sys
from phi3_autonomous_agent import Phi3Agent

def main():
    """Simple command loop"""
    
    print("\n" + "="*70)
    print("  PHI3 AUTONOMOUS AGENT - COMMAND EXECUTOR")
    print("="*70)
    print("\nType commands for the agent to execute:")
    print("  Example: 'Open Notepad'")
    print("  Example: 'Take a screenshot'")
    print("  Example: 'Open VS Code'")
    print("  Type 'exit' to quit\n")
    print("-"*70 + "\n")
    
    agent = Phi3Agent(model="phi3")
    
    while True:
        try:
            # Get user input
            command = input("\n> Command: ").strip()
            
            if not command:
                continue
            
            if command.lower() == "exit":
                print("\nGoodbye!")
                break
            
            if command.lower() == "help":
                print("""
Available commands:
  - "Open [application]" - Open any application (Notepad, VS Code, etc)
  - "Take a screenshot" - Capture the desktop
  - "Click at X,Y" - Click mouse at coordinates
  - "Type [text]" - Type text on keyboard
  - "Press [key]" - Press keyboard key (enter, escape, etc)
  - "Open [app] and [action]" - Multi-step commands
                """)
                continue
            
            # Execute the command
            print(f"\n[Executing] {command}\n")
            result = agent.run(command, verbose=True)
            
            # Show result summary
            if "Error" in result or "error" in result:
                print(f"\n❌ Failed: {result}")
            else:
                print(f"\n✓ Command executed")
        
        except KeyboardInterrupt:
            print("\n\nInterrupted. Type 'exit' to quit properly.")
        except Exception as e:
            print(f"\n✗ Error: {e}")


if __name__ == "__main__":
    main()
