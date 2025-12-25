import os
import time
import requests
import urllib.parse
import random

# Ensure directory exists
output_dir = r"c:\Users\Asus\Desktop\Katya\content\images"
os.makedirs(output_dir, exist_ok=True)

# --- 1. CONFIGURATION ---
MODEL = "flux"
SEED = 42

# --- IMPROVED MASTER PROMPT: THE INFLUENCER AESTHETIC ---
# Changes made:
# 1. Added "curated social media feed aesthetic" to set the context.
# 2. Changed "Bored expression" to "cool, detached attitude" and "knowing gaze" 
#    (influencers know the camera is there).
# 3. Emphasized that the low-fidelity look is an intentional style choice.
KATYA_DESCRIPTION = (
    "An aesthetic film photograph from the curated social media feed of Katya, a 20-year-old Eastern European goth influencer. "
    "She has pale skin, a sharp jawline, heavy graphic eyeliner, and a trendy messy black wolf-cut hairstyle. "
    "She has a cool, detached attitude and a knowing gaze towards the camera. "
    "The image style is intentional low-fidelity 35mm film grain with direct flash, trendy and moody. "
)

# List of images to generate with INFLUENCER scenarios
images = [
    {
        "name": "01_profile_new_hair.jpg",
        # Scenario emphasizes a deliberate pose and showing off a feature (hair/makeup)
        "scenario": "A tightly framed portrait shot showing off her fresh wolf-cut hair and detailed makeup, posing confidently in her room with cool posters in the background. High contrast flash.",
        "aspect": "square" 
    },
    {
        "name": "02_ig_post_study_struggle.jpg",
        # Scenario changed to an "aesthetic mess" - relatable but styled content.
        "scenario": "A 'plandid' (planned candid) shot of Katya at a desk, looking dramatically stressed surrounded by aesthetically cluttered notes and a Monster energy can. 'The struggle is real' vibe, dimly lit.",
        "aspect": "portrait"
    },
    {
        "name": "03_ig_post_winter_fit_check.jpg",
        # Scenario changed to focus on the outfit ("fit check") and the pose.
        "scenario": "Full body outfit check pose standing in the snow, showcasing an oversized vintage fur coat, big platform boots, and a fur hat. The imposing concrete apartment building is the backdrop. Streetwear aesthetic.",
        "aspect": "portrait"
    },
    {
        "name": "04_story_mirror_ootd.jpg",
        # Crucial update: Added details about the phone itself and the "OOTD" pose.
        "scenario": "A mirror selfie showing today's outfit (OOTD). She is holding up a modern iPhone with a sticker-covered case, obscuring part of her face. Wearing fishnets and a pleated skirt. The mirror is grimy for aesthetic effect.",
        "aspect": "story" 
    },
    {
        "name": "05_story_moody_vibes.jpg",
        # Focus on the "vibe" and atmospheric lighting.
        "scenario": "Atmospheric moody shot on a balcony at night, smoking a cigarette, side profile looking out at city lights. Wind blowing hair, very grainy film look, emphasizing lonely city vibes.",
        "aspect": "story"
    },
    {
        "name": "06_tiktok_cover_club_makeup.jpg",
        # Intense close-up meant to stop scrolling on a feed.
        "scenario": "Intense close-up face shot under flashing red and blue club lights, showing sweat and heavy goth makeup design. Looking down the lens. High energy feel.",
        "aspect": "story"
    },
    {
        "name": "07_main_feed_gritty_aesthetic.jpg",
        # A stylized, deliberate fashion shot in a gritty location.
        "scenario": "A stylized fashion pose standing in a brutalist concrete hallway. The harsh overhead fluorescent light flickers, casting long shadows. She is posing coolly against the wall, looking nonchalant.",
        "aspect": "portrait"
    }
]

# --- 2. GENERATION LOGIC (Unchanged from previous version) ---

def get_pollinations_url(prompt, aspect, seed):
    dims = {
        "square": "&width=1024&height=1024",
        "portrait": "&width=768&height=1024",
        "story": "&width=720&height=1280",
    }
    dim_str = dims.get(aspect, "&width=1024&height=1024")
    safe_prompt = urllib.parse.quote(prompt)
    return f"https://image.pollinations.ai/prompt/{safe_prompt}?nologo=true{dim_str}&seed={seed}&model={MODEL}"

def download_image(name, scenario, seed):
    full_prompt = f"{KATYA_DESCRIPTION} {scenario}"
     
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
         
    file_path = os.path.join(output_dir, name)
     
    print(f"\n📸 Generating Influencer Post: {name}")
    print(f"   Scenario: {scenario[:60]}...")
 
    try:
        # Get aspect from the image dict
        aspect = None
        for img in images:
            if img['name'] == name:
                aspect = img['aspect']
                break
        
        if not aspect:
            aspect = "square"  # Default fallback
            
        poly_url = get_pollinations_url(full_prompt, aspect, seed)
        r = requests.get(poly_url, timeout=45)
        if r.status_code == 200 and len(r.content) > 0:
            with open(file_path, "wb") as f:
                f.write(r.content)
            print(f"   ✨ Posted to feed: {file_path}")
        else:
            print(f"   ❌ Upload failed: Status {r.status_code}")
             
    except Exception as e:
        print(f"   ❌ Error: {e}")
 
# --- 3. MAIN LOOP ---
if __name__ == "__main__":
    print("🚀 Spooling up influencer feed generation...")
    print(f"📝 Vibe check: {KATYA_DESCRIPTION[:60]}...")
     
    for img in images:
        download_image(img['name'], img['scenario'], SEED)
        time.sleep(random.uniform(1.5, 3.5))
 
    print(f"\n🎉 Feed generation complete. Check folder: {output_dir}")