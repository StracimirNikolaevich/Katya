import os
import google.generativeai as genai
from dotenv import load_dotenv
import datetime

# Load environment variables
load_dotenv()

def generate_weekly_plan():
    print("📅 Generating Weekly Content Plan for Katya...")
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Error: GOOGLE_API_KEY not found.")
        return

    genai.configure(api_key=api_key)
    
    # Load Persona
    try:
        with open("content/planning/system_prompt.txt", "r", encoding="utf-8") as f:
            system_prompt = f.read().strip()
    except:
        system_prompt = "You are Katya, a cynical Eastern European art student."

    # Prompt for Content Strategy
    prompt = f"""
    You are {system_prompt}
    
    Task: Generate a 1-week content plan (7 days) for your social media (TikTok, Instagram, Snapchat).
    
    Constraints:
    - Stick to the "Doomer Girl / Eastern European Student" aesthetic.
    - TikToks should be viral trends adapted to this niche.
    - Instagram posts should be moody.
    - Snapchat stories should feel like "girlfriend experience" updates.
    
    Output Format:
    ## Day [Number]: [Theme]
    - **TikTok:** [Concept + Sound Suggestion]
    - **Instagram:** [Image Idea + Caption]
    - **Snapchat:** [Time of day + Photo description + Text]
    """

    # Try to use a valid model
    model_name = 'gemini-flash-latest'
    print(f"🤖 Using model: {model_name}")
    model = genai.GenerativeModel(model_name)
    
    try:
        response = model.generate_content(prompt)
        
        # Save to file
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
        filename = f"content/planning/WEEKLY_PLAN_{timestamp}.md"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# 📅 Weekly Content Plan ({timestamp})\n\n")
            f.write(response.text)
            
        print(f"✅ Plan generated successfully: {filename}")
        
    except Exception as e:
        print(f"❌ Error generating plan: {e}")

if __name__ == "__main__":
    generate_weekly_plan()
