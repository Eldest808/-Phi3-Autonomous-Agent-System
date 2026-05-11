#!/usr/bin/env python3
"""
Web Dashboard for Phi3 Autonomous Agent
Provides a UI for sending commands and monitoring agent activity
"""

from flask import Flask, render_template_string, request, jsonify
from flask_cors import CORS
import json
import threading
import time
from phi3_autonomous_agent import Phi3Agent
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Global agent instance
agent = None
agent_lock = threading.Lock()
last_output = ""
is_running = False


# HTML/CSS for the dashboard
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Phi3 Autonomous Agent</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Courier New', monospace;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #00ff00;
            min-height: 100vh;
            padding: 20px;
            overflow-x: hidden;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        header {
            text-align: center;
            margin-bottom: 40px;
            border-bottom: 2px solid #00ff00;
            padding-bottom: 20px;
        }

        h1 {
            font-size: 2.5em;
            text-shadow: 0 0 10px #00ff00;
            margin-bottom: 10px;
            letter-spacing: 2px;
        }

        .status-badge {
            display: inline-block;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
            margin-top: 10px;
        }

        .status-badge.idle {
            background: #1a472a;
            color: #00aa00;
        }

        .status-badge.running {
            background: #472a1a;
            color: #ff6600;
            animation: pulse 1s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }

        .main-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 30px;
        }

        .panel {
            background: rgba(0, 0, 0, 0.5);
            border: 2px solid #00ff00;
            padding: 20px;
            border-radius: 8px;
            backdrop-filter: blur(10px);
        }

        .panel h2 {
            color: #00ff00;
            margin-bottom: 20px;
            font-size: 1.3em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .input-group {
            margin-bottom: 20px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            color: #00ff00;
            font-weight: bold;
        }

        input[type="text"],
        select,
        textarea {
            width: 100%;
            padding: 12px;
            border: 1px solid #00ff00;
            background: rgba(0, 20, 0, 0.8);
            color: #00ff00;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            font-size: 0.95em;
        }

        input[type="text"]:focus,
        select:focus,
        textarea:focus {
            outline: none;
            box-shadow: 0 0 10px #00ff00;
            background: rgba(0, 40, 0, 0.9);
        }

        textarea {
            resize: vertical;
            min-height: 100px;
        }

        .button-group {
            display: flex;
            gap: 10px;
            margin-top: 20px;
        }

        button {
            flex: 1;
            padding: 12px;
            background: linear-gradient(135deg, #00ff00, #00aa00);
            color: #000;
            border: none;
            border-radius: 4px;
            font-weight: bold;
            cursor: pointer;
            font-family: 'Courier New', monospace;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: all 0.3s ease;
        }

        button:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 8px 15px rgba(0, 255, 0, 0.3);
        }

        button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        button.secondary {
            background: linear-gradient(135deg, #ff6600, #ff4400);
        }

        .output-panel {
            grid-column: 1 / -1;
        }

        .output {
            background: rgba(0, 0, 0, 0.8);
            border: 1px solid #00ff00;
            border-radius: 4px;
            padding: 15px;
            min-height: 400px;
            max-height: 600px;
            overflow-y: auto;
            font-size: 0.85em;
            line-height: 1.6;
            white-space: pre-wrap;
            word-break: break-word;
        }

        .output-line {
            margin-bottom: 5px;
        }

        .output-line.info {
            color: #00ff00;
        }

        .output-line.error {
            color: #ff4444;
        }

        .output-line.warning {
            color: #ffaa00;
        }

        .output-line.success {
            color: #00ff00;
            font-weight: bold;
        }

        .output-line.tool {
            color: #00aaff;
        }

        .command-history {
            max-height: 250px;
            overflow-y: auto;
        }

        .history-item {
            padding: 10px;
            margin-bottom: 8px;
            background: rgba(0, 40, 0, 0.5);
            border-left: 3px solid #00ff00;
            cursor: pointer;
            border-radius: 2px;
            transition: all 0.2s;
        }

        .history-item:hover {
            background: rgba(0, 60, 0, 0.7);
            transform: translateX(5px);
        }

        .history-time {
            font-size: 0.8em;
            color: #00aa00;
            margin-bottom: 4px;
        }

        .history-command {
            font-size: 0.9em;
        }

        @media (max-width: 1024px) {
            .main-grid {
                grid-template-columns: 1fr;
            }
        }

        /* Scrollbar styling */
        ::-webkit-scrollbar {
            width: 10px;
        }

        ::-webkit-scrollbar-track {
            background: rgba(0, 0, 0, 0.3);
        }

        ::-webkit-scrollbar-thumb {
            background: #00ff00;
            border-radius: 5px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: #00aa00;
        }

        .quick-commands {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-top: 15px;
        }

        .quick-btn {
            padding: 10px;
            font-size: 0.85em;
            background: rgba(0, 255, 0, 0.1);
            border: 1px solid #00ff00;
            color: #00ff00;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.2s;
        }

        .quick-btn:hover {
            background: rgba(0, 255, 0, 0.2);
            transform: scale(1.05);
        }

        .loading-indicator {
            display: none;
            text-align: center;
            margin: 20px 0;
        }

        .spinner {
            display: inline-block;
            width: 30px;
            height: 30px;
            border: 3px solid rgba(0, 255, 0, 0.3);
            border-radius: 50%;
            border-top-color: #00ff00;
            animation: spin 1s linear infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>⚙️ PHI3 AUTONOMOUS AGENT</h1>
            <p>Ollama-powered autonomous system control</p>
            <div class="status-badge idle" id="statusBadge">
                🟢 IDLE
            </div>
        </header>

        <div class="main-grid">
            <div class="panel">
                <h2>Command Input</h2>
                <div class="input-group">
                    <label for="command">Enter Command:</label>
                    <textarea id="command" placeholder="e.g., 'Open mGBA and load Pokemon Red'"></textarea>
                </div>
                <div class="input-group">
                    <label for="model">Model:</label>
                    <input type="text" id="model" value="phi3" placeholder="phi3, phi3.5, etc">
                </div>
                <div class="button-group">
                    <button onclick="executeCommand()">Execute</button>
                    <button class="secondary" onclick="clearOutput()">Clear</button>
                </div>
                
                <h2 style="margin-top: 30px; margin-bottom: 15px;">Quick Commands</h2>
                <div class="quick-commands">
                    <button class="quick-btn" onclick="setCommand('Open mGBA emulator')">Open mGBA</button>
                    <button class="quick-btn" onclick="setCommand('Take a screenshot')">Screenshot</button>
                    <button class="quick-btn" onclick="setCommand('List running processes')">List Apps</button>
                    <button class="quick-btn" onclick="setCommand('Open VS Code')">Open VS Code</button>
                </div>
            </div>

            <div class="panel">
                <h2>Command History</h2>
                <div class="command-history" id="history">
                    <p style="color: #00aa00; opacity: 0.7;">No history yet...</p>
                </div>
            </div>

            <div class="panel output-panel">
                <h2>Agent Output</h2>
                <div class="loading-indicator" id="loadingIndicator">
                    <div class="spinner"></div>
                    <p>Agent is thinking...</p>
                </div>
                <div class="output" id="output">
                    <div class="output-line info">> Waiting for command...</div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let commandHistory = [];

        async function executeCommand() {
            const command = document.getElementById('command').value.trim();
            const model = document.getElementById('model').value;

            if (!command) {
                alert('Please enter a command');
                return;
            }

            // Add to history
            const timestamp = new Date().toLocaleTimeString();
            commandHistory.unshift({ time: timestamp, command: command });
            updateHistory();

            // Update UI
            const statusBadge = document.getElementById('statusBadge');
            statusBadge.textContent = '🔴 RUNNING';
            statusBadge.className = 'status-badge running';
            document.getElementById('loadingIndicator').style.display = 'block';

            // Clear previous output
            const output = document.getElementById('output');
            output.innerHTML = `<div class="output-line info">> Executing: ${command}</div>`;

            try {
                const response = await fetch('/api/execute', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ command: command, model: model })
                });

                const data = await response.json();
                
                if (data.success) {
                    displayOutput(data.output);
                } else {
                    output.innerHTML += `<div class="output-line error">Error: ${data.error}</div>`;
                }
            } catch (error) {
                output.innerHTML += `<div class="output-line error">Connection error: ${error.message}</div>`;
            } finally {
                statusBadge.textContent = '🟢 IDLE';
                statusBadge.className = 'status-badge idle';
                document.getElementById('loadingIndicator').style.display = 'none';
            }
        }

        function displayOutput(text) {
            const output = document.getElementById('output');
            output.innerHTML = '';

            const lines = text.split('\n');
            lines.forEach(line => {
                const div = document.createElement('div');
                div.className = 'output-line';

                if (line.includes('Error') || line.includes('error')) {
                    div.className += ' error';
                } else if (line.includes('Warning') || line.includes('warning')) {
                    div.className += ' warning';
                } else if (line.includes('✓') || line.includes('success')) {
                    div.className += ' success';
                } else if (line.includes('[') && line.includes(']')) {
                    div.className += ' tool';
                } else {
                    div.className += ' info';
                }

                div.textContent = line;
                output.appendChild(div);
            });

            output.scrollTop = output.scrollHeight;
        }

        function updateHistory() {
            const historyDiv = document.getElementById('history');
            historyDiv.innerHTML = '';

            commandHistory.slice(0, 10).forEach(item => {
                const div = document.createElement('div');
                div.className = 'history-item';
                div.innerHTML = `
                    <div class="history-time">${item.time}</div>
                    <div class="history-command">${item.command}</div>
                `;
                div.onclick = () => setCommand(item.command);
                historyDiv.appendChild(div);
            });
        }

        function setCommand(cmd) {
            document.getElementById('command').value = cmd;
            document.getElementById('command').focus();
        }

        function clearOutput() {
            document.getElementById('output').innerHTML = '<div class="output-line info">> Ready for next command...</div>';
        }

        // Allow Enter key to execute
        document.getElementById('command').addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'Enter') {
                executeCommand();
            }
        });
    </script>
</body>
</html>
"""


@app.route('/')
def dashboard():
    """Serve the dashboard"""
    return render_template_string(DASHBOARD_HTML)


@app.route('/api/execute', methods=['POST'])
def api_execute():
    """API endpoint to execute a command"""
    global agent, is_running
    
    data = request.json
    command = data.get('command', '')
    model = data.get('model', 'phi3')
    
    if not command:
        return jsonify({'success': False, 'error': 'No command provided'})
    
    if is_running:
        return jsonify({'success': False, 'error': 'Agent is already running'})
    
    def run_agent():
        global agent, is_running, last_output
        is_running = True
        
        try:
            # Initialize agent if needed or if model changed
            with agent_lock:
                if agent is None or agent.model != model:
                    agent = Phi3Agent(model=model)
                else:
                    agent.model = model
            
            # Run the command
            output = agent.run(command, verbose=True)
            last_output = output
        
        except Exception as e:
            last_output = f"Error: {str(e)}"
        
        finally:
            is_running = False
    
    # Run agent in background thread
    thread = threading.Thread(target=run_agent)
    thread.daemon = True
    thread.start()
    
    # Wait a bit for agent to start producing output
    time.sleep(0.5)
    
    # For now, return placeholder - in production use WebSocket
    return jsonify({
        'success': True,
        'output': f"Command started: {command}\n\nAgent is processing...\n(Check console for live updates)"
    })


@app.route('/api/status', methods=['GET'])
def api_status():
    """Get current agent status"""
    return jsonify({
        'running': is_running,
        'output': last_output
    })


def main():
    """Start the web server"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║        Phi3 Autonomous Agent - Web Dashboard             ║
    ║        Open http://localhost:5000 in your browser        ║
    ║                                                           ║
    ║        Make sure Ollama is running:                      ║
    ║        $ ollama run phi3                                 ║
    ║                                                           ║
    ║        Optional: Install for better control:             ║
    ║        $ pip install pyautogui mss pillow                ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    app.run(debug=False, host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()
