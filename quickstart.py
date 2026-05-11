#!/usr/bin/env python3
"""
Quick Start Examples for Phi3 Autonomous Agent
Run this to test the agent with various commands
"""

import sys
import time
from phi3_autonomous_agent import Phi3Agent


def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


def test_basic_commands():
    """Test basic system commands"""
    print_section("Test 1: Basic System Commands")
    
    agent = Phi3Agent()
    
    # Test 1: List processes
    print("Testing: Get running processes...")
    result = agent.run(
        "List all currently running processes",
        verbose=True
    )
    print(f"\nResult: {result[:200]}...")  # First 200 chars
    time.sleep(2)


def test_app_opening():
    """Test opening applications"""
    print_section("Test 2: Opening Applications")
    
    agent = Phi3Agent()
    
    # Platform-specific commands
    import platform
    os_type = platform.system()
    
    if os_type == "Darwin":  # macOS
        cmd = "Open the Calculator application"
    elif os_type == "Windows":
        cmd = "Open Notepad"
    else:  # Linux
        cmd = "Open a text editor"
    
    print(f"Testing: {cmd}...")
    result = agent.run(cmd, verbose=True)
    print(f"\nResult: {result}")
    time.sleep(3)


def test_screenshot():
    """Test screenshot capability"""
    print_section("Test 3: Taking Screenshots")
    
    agent = Phi3Agent()
    
    print("Testing: Take a screenshot and describe what you see...")
    result = agent.run(
        "Take a screenshot of the current desktop and describe what you see",
        verbose=True
    )
    print(f"\nResult: {result}")
    time.sleep(2)


def test_game_automation():
    """Test game automation example"""
    print_section("Test 4: Game Automation Example (mGBA)")
    
    agent = Phi3Agent()
    
    print("Testing: Open mGBA emulator...")
    print("(This example shows the structure for game automation)")
    
    # Note: This is a test of the structure
    # In real use, you would have an actual game ROM
    command = """
    1. Open mGBA emulator
    2. Check if a game is loaded
    3. Report back what you see
    """
    
    result = agent.run(command, verbose=True)
    print(f"\nResult: {result}")
    time.sleep(2)


def interactive_mode():
    """Run in interactive mode"""
    print_section("Interactive Mode")
    print("Enter commands for the Phi3 agent to execute")
    print("Type 'exit' to quit, 'help' for examples\n")
    
    agent = Phi3Agent()
    
    examples = {
        "help": [
            "Example commands:",
            "  - 'Open VS Code'",
            "  - 'Take a screenshot'",
            "  - 'List all running applications'",
            "  - 'Open Calculator'",
            "  - 'Check if Chrome is running'",
        ]
    }
    
    while True:
        try:
            cmd = input("\n> Enter command: ").strip()
            
            if cmd.lower() == "exit":
                print("Goodbye!")
                break
            elif cmd.lower() == "help":
                for line in examples["help"]:
                    print(line)
            elif cmd:
                print(f"\nExecuting: {cmd}")
                result = agent.run(cmd, verbose=True)
                print(f"\n✓ Completed")
        
        except KeyboardInterrupt:
            print("\nInterrupted. Type 'exit' to quit")
        except Exception as e:
            print(f"Error: {e}")


def show_menu():
    """Show main menu"""
    print("\n" + "="*70)
    print("  PHI3 AUTONOMOUS AGENT - QUICK START TESTS")
    print("="*70)
    print("\nSelect a test to run:\n")
    print("  1. Basic System Commands")
    print("  2. Open Applications")
    print("  3. Take Screenshots")
    print("  4. Game Automation Example (mGBA)")
    print("  5. Interactive Mode")
    print("  6. Run All Tests")
    print("  0. Exit")
    print("\n" + "-"*70)


def main():
    """Main menu"""
    
    # Check Ollama connection first
    print_section("Checking Ollama Connection")
    
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=3)
        if response.status_code == 200:
            data = response.json()
            models = data.get("models", [])
            if models:
                print("✓ Ollama is running!")
                print(f"✓ Available models: {len(models)}")
                
                # Check for phi3 or similar models
                model_names = [m['name'] for m in models]
                phi_models = [m for m in model_names if 'phi' in m.lower()]
                
                print("\nAll models:")
                for model in model_names:
                    print(f"  - {model}")
                
                if phi_models:
                    print(f"\n✓ Phi models found: {phi_models}")
                else:
                    print("\n⚠️  No Phi models detected")
                    print("   Make sure you have Phi3 installed:")
                    print("   Run: ollama pull phi3")
                    return
            else:
                print("⚠️  Ollama is running but no models found")
                print("   Run: ollama pull phi3")
                return
        else:
            print("✗ Cannot connect to Ollama")
            return
    except Exception as e:
        print(f"✗ Ollama connection error: {e}")
        print("\nMake sure Ollama is running:")
        print("  1. Download from https://ollama.ai")
        print("  2. Run: ollama serve")
        print("  3. In another terminal: ollama pull phi3")
        return
    
    # Ollama check passed, proceed with main menu
    print("\n✓ All systems ready! You can now run tests.\n")
    
    # Main loop
    while True:
        show_menu()
        choice = input("\nEnter choice (0-6): ").strip()
        
        if choice == "1":
            test_basic_commands()
        elif choice == "2":
            test_app_opening()
        elif choice == "3":
            test_screenshot()
        elif choice == "4":
            test_game_automation()
        elif choice == "5":
            interactive_mode()
        elif choice == "6":
            test_basic_commands()
            test_app_opening()
            test_screenshot()
            test_game_automation()
        elif choice == "0":
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(0)
