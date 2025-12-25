import os
import time
import requests
import urllib.parse

# Ensure directory exists
output_dir = r"c:\Users\Asus\Desktop\Katya\content\images"
os.makedirs(output_dir, exist_ok=True)

# --- 1. CONSISTENCY CONFIGURATION ---
# We use a strict "Master Prompt" to keep her looking the same.
KATYA_DESCRIPTION = (
    "photo of a 20 year old eastern european goth girl named Katya, "
    "pale skin, messy black wolf-cut hair with bangs, sharp jawline, heavy black eyeliner, "
    "bored expression, beautiful face, realistic, "
    "wearing oversized black clothes, "
    "grainy 35mm flash photography style, high detail, 8k, raw photo"
)

# List of images to generate
images = [
    {
        "name": "profile_pic.jpg",
        "scenario": "close up portrait, sitting in cluttered dorm room, posters on wall, night time",
        "aspect": "square" 
    },
    {
        "name": "ig_post_1_study.jpg",
        "scenario": "sitting at messy desk, piles of notes, open textbooks, monster energy drink can, looking stressed, head in hands, dark room",
        "aspect": "portrait" # 3:4
    },
    {
        "name": "ig_post_2_outdoor.jpg",
        "scenario": "standing outside in snow, wearing thick oversized fur coat and fur hat, background is tall concrete panel apartment building, grey sky",
        "aspect": "portrait"
    },
    {
        "name": "ig_post_3_mirror_selfie.jpg",
        "scenario": "mirror selfie, wearing fishnets and black skirt, holding phone covering face, dark room, messy background, dirty mirror",
        "aspect": "story" # 9:16
    },
    {
        "name": "tiktok_cover_balcony.jpg",
        "scenario": "leaning on balcony railing, smoking cigarette, night time, city lights in distance, concrete building, wind blowing hair, side profile",
        "aspect": "story"
    },
    {
        "name": "tiktok_cover_rave.jpg",
        "scenario": "close up face, heavy goth makeup, black lipstick, choker, neon lights reflecting on face, dark club atmosphere, sweaty, intense look",
        "aspect": "story"
    },
    {
        "name": "katya_main_portrait.jpg",
        "scenario": "standing in a dimly lit concrete apartment block hallway, full body shot",
        "aspect": "portrait"
    }
]

# --- 2. GENERATION LOGIC ---

def get_pollinations_url(prompt, aspect):
    # Fallback AI: Pollinations.ai (Free, fast, good consistency via seed)
    # Width/Height mapping
    dims = {
        "square": "&width=1024&height=1024",
        "portrait": "&width=768&height=1024",
        "story": "&width=720&height=1280"
    }
    dim_str = dims.get(aspect, "&width=1024&height=1024")
    # We use a fixed seed '42' to try and keep the face consistent across different prompts
    return f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?nologo=true{dim_str}&seed=42&model=flux"

def download_image(name, scenario, aspect):
    full_prompt = f"{KATYA_DESCRIPTION}, {scenario}"
    file_path = os.path.join(output_dir, name)
    
    print(f"\n🖼️  Generating: {name}")
    print(f"   Prompt: ...{scenario}")

    # --- STRATEGY: FALLBACK AI (Pollinations - Fast, Reliable) ---
    print("   🔸 Attempt 1: Pollinations (Fast, No Waiting)...")
    try:
        poly_url = get_pollinations_url(full_prompt, aspect)
        r = requests.get(poly_url)
        
        if r.status_code == 200 and len(r.content) > 10000:
            with open(file_path, "wb") as f:
                f.write(r.content)
            print(f"   ✅ Success (Pollinations)")
            return
        else:
            print(f"   ❌ Pollinations failed: {r.status_code}")
            
    except Exception as e:
        print(f"   ❌ Pollinations Error: {e}")

# --- 3. MAIN LOOP ---
print("🚀 Starting Consistent Character Generation...")
print("📝 Master Prompt Loaded (Ensuring Katya looks the same)")

for img in images:
    download_image(img['name'], img['scenario'], img['aspect'])
    # Small cool-down between images
    time.sleep(2)

print("\n✨ All images processed.")
