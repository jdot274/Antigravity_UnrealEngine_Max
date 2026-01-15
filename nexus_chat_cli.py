import requests
import sys
import json

SERVER_URL = "http://localhost:3002/chat"

def chat():
    print("🛡️ ANTIGRAVITY_UNREALENGINE - NLP TERMINAL INTERFACE")
    print("------------------------------------------")
    print("Type your message to the Nexus AI (Type 'quit' to exit)")
    
    while True:
        user_input = input("\n👤 YOU: ")
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Shutting down NLP terminal link...")
            break
            
        try:
            response = requests.post(SERVER_URL, json={
                "message": user_input,
                "context": {
                    "source": "cli",
                    "system": "Antigravity Nexus V1.0.2"
                }
            })
            
            if response.status_code == 200:
                data = response.json()
                print(f"\n🤖 AI: {data['response']}")
            else:
                print(f"\n❌ Error: Server returned {response.status_code}")
                
        except Exception as e:
            print(f"\n❌ Connection Failed: Is the Nexus Bridge running on port 3002?")

if __name__ == "__main__":
    chat()
