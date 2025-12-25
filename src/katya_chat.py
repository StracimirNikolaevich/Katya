import os
import sys
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def load_system_prompt():
    try:
        with open("content/planning/system_prompt.txt", "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        print("Error: system_prompt.txt not found in content/planning/")
        return "You are Katya."

def chat_with_katya():
    print("❄️ Initializing Katya AI (Free Edition)... ❄️")
    
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        print("\n⚠️  WARNING: GOOGLE_API_KEY not found.")
        print("1. Go to https://aistudio.google.com/app/apikey (It is 100% FREE)")
        print("2. Create a key and paste it in a .env file: GOOGLE_API_KEY=your_key_here")
        print("3. Or paste it right here to start now:")
        api_key = input("Enter Google API Key: ").strip()
        if not api_key:
            print("No key provided. Exiting.")
            return

    try:
        genai.configure(api_key=api_key)
        
        # Load the personality
        system_prompt = load_system_prompt()
        print(f"\nSystem Prompt Loaded: {system_prompt[:50]}...\n")
        
        # Initialize the model
        model_name = "gemini-flash-latest"
        print(f"🤖 Connecting to model: {model_name}")
        model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=system_prompt
        )
        
        chat = model.start_chat(history=[])
        
        print("--- Start chatting with Katya (type 'exit' to quit) ---")
        print("(Connected to Google Gemini Free Tier)")

        while True:
            user_input = input("\nYou: ")
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("\nKatya: Whatever. Don't freeze out there. ❄️")
                break

            try:
                response = chat.send_message(user_input)
                print(f"\nKatya: {response.text}")
            except Exception as e:
                print(f"\nError: {e}")
                print("Make sure your API key is valid and you have internet access.")

    except Exception as e:
        print(f"\nCritical Error: {e}")

if __name__ == "__main__":
    chat_with_katya()
