# Advanced Usage Guide - Game Automation with Phi3

This guide shows how to create specialized agents for complex tasks like game automation.

## Game Automation Architecture

When automating games like mGBA, you need a feedback loop:

```
User Command
    ↓
[Agent thinks about task]
    ↓
[Takes screenshot of game]
    ↓
[Analyzes game state]
    ↓
[Decides next action: movement, attack, interact, etc]
    ↓
[Executes action via keyboard/mouse]
    ↓
[Waits for game response]
    ↓
[Loop until task complete]
```

## Example 1: Basic Game Automation

```python
from phi3_autonomous_agent import Phi3Agent
import time

# Create agent optimized for game control
agent = Phi3Agent(
    ollama_url="http://localhost:11434",
    model="phi3"
)

# Task: Open mGBA and play a simple sequence
commands = [
    "Open mGBA emulator application",
    "Wait 3 seconds for it to fully load",
    "Take a screenshot to verify it opened",
]

for cmd in commands:
    print(f"\n>>> {cmd}")
    result = agent.run(cmd, verbose=True)
    print(f"Result: {result[:100]}...\n")
    time.sleep(2)
```

## Example 2: Pokemon Game Automation

```python
from phi3_autonomous_agent import Phi3Agent

agent = Phi3Agent()

# Step-by-step game progression
instructions = """
You are controlling Pokemon Red in mGBA. 
Here's what I need you to do:

1. Take a screenshot first to see the current game state
2. Move to the nearest grass patch (you can see green areas on the map)
3. Walk around in the grass 3-5 times
4. Wait for a wild Pokemon to appear
5. Take a screenshot when a Pokemon appears
6. If a battle starts, press 'a' to select fight
7. Continue pressing 'a' to use the default attack
8. Report when the battle is won or lost

Be methodical and take screenshots between actions to verify the game state.
"""

result = agent.run(instructions, verbose=True)
print(f"\nGame automation completed!")
print(f"Result: {result}")
```

## Example 3: Custom Game Agent Class

Create a specialized agent for a specific game:

```python
from phi3_autonomous_agent import Phi3Agent
import time

class PokemonGameAgent(Phi3Agent):
    """Specialized agent for Pokemon game automation"""
    
    def __init__(self):
        super().__init__(model="phi3")
        self.game_state = {
            "current_location": None,
            "pokemon_party": [],
            "items": [],
            "battles_won": 0
        }
    
    def _build_system_prompt(self):
        """Enhanced system prompt for Pokemon gameplay"""
        base_prompt = super()._build_system_prompt()
        
        pokemon_instructions = f"""

POKEMON GAMEPLAY CONTEXT:
Current Game State: {self.game_state}

When playing Pokemon:
- Press 'up', 'down', 'left', 'right' to move around
- Press 'a' to interact with people/Pokemon/items
- Press 'b' to go back/cancel
- In battles: 'a' selects attack, 'b' to switch Pokemon
- Press 's' to access start menu (save, items, etc)

Your goal is to play the game strategically:
1. Catch Pokemon to build your team
2. Train them by winning battles
3. Explore areas and gather items
4. Report your progress regularly

Always take screenshots to see the game state and plan your actions.
"""
        
        return base_prompt + pokemon_instructions
    
    def catch_pokemon(self):
        """High-level task: catch a Pokemon"""
        instructions = """
        1. Navigate to tall grass
        2. Walk around until a wild Pokemon appears
        3. Throw a Pokeball at it
        4. If it escapes, try again or use a different Pokeball
        5. Return when Pokemon is caught or inventory is empty
        """
        return self.run(instructions, verbose=True)
    
    def battle_trainer(self):
        """High-level task: battle a trainer"""
        instructions = """
        1. Navigate to a trainer
        2. Initiate battle by talking to them
        3. Use your strongest Pokemon
        4. Use super-effective moves when available
        5. Switch Pokemon if needed
        6. Win the battle
        7. Report the result
        """
        return self.run(instructions, verbose=True)
    
    def explore_area(self, area_name):
        """High-level task: explore a game area"""
        instructions = f"""
        Explore {area_name}:
        1. Map out the area by moving around
        2. Identify any Pokemon, trainers, or items
        3. Report what you find
        4. Look for anything valuable or rare
        5. Return to starting point
        """
        return self.run(instructions, verbose=True)


# Usage
if __name__ == "__main__":
    agent = PokemonGameAgent()
    
    # Open game
    agent.run("Open mGBA and load Pokemon Red", verbose=True)
    time.sleep(3)
    
    # Play the game
    result = agent.catch_pokemon()
    print(f"Catch result: {result}")
    
    time.sleep(3)
    
    result = agent.battle_trainer()
    print(f"Battle result: {result}")
    
    time.sleep(3)
    
    result = agent.explore_area("Viridian Forest")
    print(f"Exploration result: {result}")
```

## Example 4: Real-Time Game Feedback

Monitor agent performance and provide corrective instructions:

```python
from phi3_autonomous_agent import Phi3Agent
import time

agent = Phi3Agent()

# Start game automation
print("Starting game automation with real-time feedback...\n")

# Phase 1: Setup
print("[Phase 1] Opening game...")
agent.run("Open mGBA with Pokemon Red loaded", verbose=False)
time.sleep(3)

# Phase 2: Monitor and correct
max_attempts = 3
attempt = 1

while attempt <= max_attempts:
    print(f"\n[Phase 2, Attempt {attempt}] Attempting to catch Pokemon...")
    
    # Take screenshot for manual feedback
    result = agent.run(
        "Take a screenshot of the current game state",
        verbose=False
    )
    
    # You could analyze the screenshot here
    print("Screenshot taken. Proceeding with Pokemon catching...")
    
    # Attempt to catch
    catch_result = agent.run(
        """
        Walk into the tall grass.
        Walk around until a Pokemon appears.
        Throw a Pokeball and catch it.
        Report if successful.
        """,
        verbose=True
    )
    
    if "caught" in catch_result.lower() or "captured" in catch_result.lower():
        print("✓ Successfully caught Pokemon!")
        break
    else:
        print(f"✗ Attempt {attempt} failed. Retrying...")
        attempt += 1
        time.sleep(2)

if attempt > max_attempts:
    print("Could not catch Pokemon after multiple attempts")
```

## Example 5: Multi-Agent Coordination

Use multiple agents for different tasks:

```python
from phi3_autonomous_agent import Phi3Agent
import threading
import time

class MultiAgentGame:
    """Multiple agents working together"""
    
    def __init__(self):
        self.battle_agent = Phi3Agent(model="phi3")
        self.exploration_agent = Phi3Agent(model="phi3")
        self.results = {}
    
    def run_battle(self):
        """Agent 1: Focus on battles"""
        print("[Battle Agent] Starting battles...")
        result = self.battle_agent.run(
            "Enter the first Pokemon battle and win it",
            verbose=True
        )
        self.results["battle"] = result
    
    def run_exploration(self):
        """Agent 2: Focus on exploration"""
        print("[Explorer Agent] Starting exploration...")
        result = self.exploration_agent.run(
            "Explore the current area and find all items",
            verbose=True
        )
        self.results["exploration"] = result
    
    def run_parallel(self):
        """Run agents in parallel"""
        threads = [
            threading.Thread(target=self.run_battle),
            threading.Thread(target=self.run_exploration)
        ]
        
        for t in threads:
            t.start()
        
        for t in threads:
            t.join()
        
        return self.results


# Usage
multi_agent = MultiAgentGame()
results = multi_agent.run_parallel()
print(f"\nResults: {results}")
```

## Example 6: Task Decomposition

Break complex tasks into subtasks:

```python
from phi3_autonomous_agent import Phi3Agent

class TaskDecomposer:
    """Break down complex games tasks into subtasks"""
    
    @staticmethod
    def decompose_gym_challenge():
        """Decompose: Beat the first Pokemon gym"""
        return [
            {
                "name": "Travel to gym",
                "instructions": "Navigate to the first Pokemon gym"
            },
            {
                "name": "Enter gym",
                "instructions": "Enter the gym building"
            },
            {
                "name": "Solve gym puzzle",
                "instructions": "Complete any puzzles blocking the gym leader"
            },
            {
                "name": "Battle gym leader",
                "instructions": "Defeat the gym leader in battle"
            },
            {
                "name": "Claim badge",
                "instructions": "Accept the badge from the gym leader"
            }
        ]
    
    @staticmethod
    def execute_decomposed_task(tasks):
        """Execute a decomposed task sequence"""
        agent = Phi3Agent()
        
        for i, task in enumerate(tasks, 1):
            print(f"\n[Task {i}/{len(tasks)}] {task['name']}")
            print(f"Instructions: {task['instructions']}")
            
            result = agent.run(task['instructions'], verbose=True)
            
            if "failed" in result.lower() or "error" in result.lower():
                print(f"⚠️  Task failed. Retrying...")
                # Retry logic here
            else:
                print(f"✓ Task completed!")
            
            import time
            time.sleep(2)


# Usage
decomposer = TaskDecomposer()
tasks = decomposer.decompose_gym_challenge()
decomposer.execute_decomposed_task(tasks)
```

## Example 7: Game State Tracking

Track and maintain game state across commands:

```python
from phi3_autonomous_agent import Phi3Agent
import json

class GameStateTracker:
    """Track game state across agent commands"""
    
    def __init__(self):
        self.agent = Phi3Agent()
        self.state = {
            "location": "Unknown",
            "level": 1,
            "pokemon_party": [],
            "items": [],
            "badges": 0,
            "money": 0,
            "playtime_minutes": 0
        }
        self.history = []
    
    def update_state(self, key, value):
        """Update game state"""
        old_value = self.state.get(key)
        self.state[key] = value
        self.history.append({
            "timestamp": self._get_time(),
            "changed": key,
            "from": old_value,
            "to": value
        })
    
    def run_with_tracking(self, task):
        """Run task and track state changes"""
        print(f"State before: {json.dumps(self.state, indent=2)}")
        
        result = self.agent.run(task, verbose=True)
        
        # Parse result and update state
        # This is a simplified example
        if "caught" in result.lower():
            self.update_state("pokemon_party", 
                            self.state["pokemon_party"] + ["New Pokemon"])
        
        print(f"\nState after: {json.dumps(self.state, indent=2)}")
        return result
    
    def get_summary(self):
        """Get game progress summary"""
        return f"""
        Game Progress Summary:
        - Current Location: {self.state['location']}
        - Level: {self.state['level']}
        - Pokemon Caught: {len(self.state['pokemon_party'])}
        - Items: {self.state['items']}
        - Badges: {self.state['badges']}
        - Money: ${self.state['money']}
        - Total Playtime: {self.state['playtime_minutes']} minutes
        """
    
    @staticmethod
    def _get_time():
        from datetime import datetime
        return datetime.now().isoformat()


# Usage
tracker = GameStateTracker()
tracker.run_with_tracking("Enter first battle and win")
print(tracker.get_summary())
```

## Performance Tuning

### For Better Game Automation:

1. **Screenshot Frequency**
   ```python
   # Take screenshots more often for real-time feedback
   agent.run(
       "Take screenshot every action to verify the game state",
       verbose=True
   )
   ```

2. **Shorter Wait Times**
   ```python
   # Reduce wait times for faster gameplay
   "Execute quickly with minimal waiting between actions"
   ```

3. **Temperature Adjustment**
   - Lower temperature (0.3-0.5) = More consistent actions
   - Higher temperature (0.8+) = More creative problem-solving

4. **Custom Model Prompts**
   ```python
   class GameAgent(Phi3Agent):
       def _build_system_prompt(self):
           return """
           You are an expert game player. You:
           - Take screenshots to see state before acting
           - Plan multiple moves ahead
           - Remember the goal
           - Report progress clearly
           - Use optimal strategies
           """
   ```

## Debugging Tips

### Enable Detailed Logging

```python
import logging

logging.basicConfig(level=logging.DEBUG)

agent = Phi3Agent()
agent.run("your command", verbose=True)
```

### Save Screenshots for Analysis

```python
# Agent automatically saves screenshots to /tmp/screenshot_*.png
# Analyze them to understand what the agent sees
import os
screenshots = [f for f in os.listdir('/tmp') if f.startswith('screenshot')]
print(f"Found {len(screenshots)} screenshots")
```

### Monitor Tool Usage

```python
# Review which tools the agent uses
result = agent.run("your command")
print(agent.conversation_history)  # See all tool calls
```

## Next Steps

1. Start with simple game automation
2. Add custom tools for game-specific actions
3. Implement state tracking
4. Create specialized agent classes
5. Optimize performance for your game
6. Add error recovery mechanisms

---

These examples show the power of autonomous agents for complex tasks like game automation. Start simple and build up complexity gradually!
