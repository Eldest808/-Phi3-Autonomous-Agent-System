#!/usr/bin/env python3
"""
Ollama Diagnostics - Test Phi3 Model and Connection
"""

import requests
import json
import time

def test_ollama_connection():
    """Test basic Ollama connection"""
    print("\n" + "="*70)
    print("TEST 1: Ollama Server Connection")
    print("="*70)
    
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        print(f"✓ Ollama is running (Status: {response.status_code})")
        
        data = response.json()
        models = data.get("models", [])
        print(f"✓ Found {len(models)} models:")
        for model in models:
            print(f"  - {model['name']}")
        
        return True
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to Ollama")
        print("  Make sure: ollama serve is running")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_phi3_availability():
    """Test if Phi3 model is available"""
    print("\n" + "="*70)
    print("TEST 2: Phi3 Model Availability")
    print("="*70)
    
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        data = response.json()
        models = [m['name'] for m in data.get("models", [])]
        
        phi_models = [m for m in models if 'phi' in m.lower()]
        
        if phi_models:
            print(f"✓ Phi models available: {phi_models}")
            return True
        else:
            print("✗ No Phi models found")
            print("  Run: ollama pull phi3")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_phi3_simple_chat():
    """Test simple chat with Phi3"""
    print("\n" + "="*70)
    print("TEST 3: Simple Chat with Phi3")
    print("="*70)
    
    try:
        print("Sending test message to Phi3...")
        
        payload = {
            "model": "phi3",
            "messages": [
                {"role": "user", "content": "Say 'hello world'"}
            ],
            "stream": False
        }
        
        response = requests.post(
            "http://localhost:11434/api/chat",
            json=payload,
            timeout=30
        )
        
        print(f"Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            message = data.get("message", {}).get("content", "")
            print(f"✓ Phi3 responded: {message[:100]}...")
            return True
        else:
            print(f"✗ Error Response: {response.status_code}")
            print(f"Details: {response.text[:200]}")
            return False
    
    except requests.exceptions.Timeout:
        print("✗ Timeout - Phi3 took too long to respond")
        print("  Possible causes:")
        print("  - Model is still loading")
        print("  - System is under heavy load")
        print("  - Model needs to be restarted")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_system_prompt():
    """Test with system prompt (like the agent uses)"""
    print("\n" + "="*70)
    print("TEST 4: Chat with System Prompt (Agent-style)")
    print("="*70)
    
    try:
        print("Sending agent-style message...")
        
        payload = {
            "model": "phi3",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant. Respond briefly."
                },
                {
                    "role": "user",
                    "content": "Open VS Code"
                }
            ],
            "stream": False,
            "temperature": 0.7
        }
        
        response = requests.post(
            "http://localhost:11434/api/chat",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            message = data.get("message", {}).get("content", "")
            print(f"✓ Response: {message[:150]}...")
            return True
        else:
            print(f"✗ Error: {response.status_code}")
            print(f"Details: {response.text[:200]}")
            return False
    
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_ollama_health():
    """Test Ollama health endpoint"""
    print("\n" + "="*70)
    print("TEST 5: Ollama Health Check")
    print("="*70)
    
    try:
        response = requests.get("http://localhost:11434/api/health", timeout=5)
        print(f"✓ Health Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✓ Ollama is healthy")
            return True
        else:
            print(f"⚠️  Health check returned: {response.status_code}")
            return False
    
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def suggest_fixes():
    """Suggest fixes based on test results"""
    print("\n" + "="*70)
    print("SUGGESTED FIXES")
    print("="*70)
    
    print("""
If Phi3 returns 500 errors:

1. RESTART OLLAMA:
   - Kill: Ctrl+C on ollama serve
   - Wait 5 seconds
   - Restart: ollama serve
   - Wait for "Listening on 127.0.0.1:11434"

2. RELOAD THE MODEL:
   - Run: ollama pull phi3
   - This re-downloads/verifies the model
   - Should fix corruption issues

3. CHECK SYSTEM RESOURCES:
   - Make sure you have at least 8GB RAM free
   - Close other heavy applications
   - Check disk space (need ~20GB for Phi3)

4. CLEAR CACHE:
   - Stop Ollama
   - On Windows: Delete %LOCALAPPDATA%\\Ollama\\cache
   - On Mac: Delete ~/.ollama/cache
   - On Linux: Delete ~/.ollama/cache
   - Restart Ollama and re-pull phi3

5. TRY A DIFFERENT MODEL:
   - ollama pull mistral
   - ollama pull neural-chat
   - ollama pull dolphin-mixtral

6. CHECK OLLAMA LOGS:
   - Ollama logs are in:
     * Windows: %LOCALAPPDATA%\\Ollama\\ollama.log
     * Mac: ~/.ollama/ollama.log
     * Linux: ~/.ollama/ollama.log
""")


def main():
    """Run all diagnostics"""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*15 + "OLLAMA DIAGNOSTICS - PHI3 TEST" + " "*23 + "║")
    print("╚" + "="*68 + "╝")
    
    results = []
    
    # Run tests
    results.append(("Ollama Connection", test_ollama_connection()))
    results.append(("Phi3 Available", test_phi3_availability()))
    results.append(("Simple Chat", test_phi3_simple_chat()))
    results.append(("System Prompt", test_system_prompt()))
    results.append(("Health Check", test_ollama_health()))
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name:.<40} {status}")
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    print(f"\nPassed: {passed}/{total}")
    
    if passed < total:
        suggest_fixes()
    else:
        print("\n✓ All tests passed! Your system is ready to use.")
    
    print("\n")


if __name__ == "__main__":
    main()
