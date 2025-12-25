import os
import time
import requests
import urllib.parse
import random
from datetime import datetime

# --- 1. CONFIGURATION ---
OUTPUT_DIR = r"c:\Users\Asus\Desktop\Katya\content\images"
MODEL = "flux"
NUM_IMAGES_TO_GENERATE = 10

# Ensure directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- 2. THE "KATYA" DNA ---
KATYA_BASE = (
    "Real amateur phone photo of Katya, 20yo Eastern European goth girl, pale skin, messy black wolf-cut hair. "
    "She has a sharp jawline, heavy messy graphic eyeliner, and looks slightly tired. "
    "The photo is taken with a direct, harsh camera flash that casts hard shadows behind her. "
    "Low quality JPEG, grainy ISO noise, unpolished, candid, slightly out of focus background. "
)

# --- 3. EXPANDED INGREDIENTS LISTS ---

LOCATIONS = [
    # Domestic / Messy
    "in a messy bedroom with clothes and vintage posters piled on the floor",
    "in a cluttered kitchen with dirty dishes and a box of pizza, 3am vibe",
    "sitting on the floor of a bathroom with harsh yellow lighting",
    "laying on an unmade bed with white sheets, staring at the ceiling",
    "in a dark living room illuminated only by the blue light of a TV screen",
    
    # Urban / Gritty
    "in a brutalist concrete stairwell with graffiti on the walls",
    "standing in a desolate parking lot at night under orange streetlights",
    "waiting at a lonely bus stop in the rain, glass reflection visible",
    "inside an empty subway car with flickering fluorescent lights",
    "leaning against a brick wall in a dark alleyway behind a club",
    "on a windy apartment balcony overlooking a foggy city skyline",
    "in a 24-hour laundromat with rows of washing machines behind her",
    "sitting on a curb outside a convenience store holding a plastic bag",
    
    # Social / Vibe
    "in a crowded techno club bathroom, very cramped",
    "in a thrift store changing room with unflattering overhead lighting",
    "inside a moving car at night, city lights streaking on the window",
    "in an elevator with mirrored walls and green fluorescent tint",
]

OUTFITS = [
    # Casual Goth
    "wearing an oversized vintage Korn band tee and ripped fishnets",
    "wearing a black skeleton-print zip-up hoodie and baggy cargo pants",
    "wearing a distressed knit sweater with holes and a silver chain necklace",
    "wearing mismatched plaid pajamas and fuzzy slippers",
    
    # Dressy / Alt
    "wearing a tight black vinyl dress that reflects the camera flash",
    "wearing a lace corset top and a long velvet skirt",
    "wearing a spiked leather jacket, mini skirt, and heavy platform boots",
    "wearing a sheer mesh top with a black bralette underneath",
    "wearing a faux-fur leopard print coat and big sunglasses (indoors)",
    "wearing a catholic schoolgirl style outfit with a loose tie and combat boots",
    
    # Accessories focused
    "wearing heavy silver rings on every finger and chipped black nail polish",
    "wearing big over-ear headphones around her neck and a choker",
]

ACTIONS = [
    # The "Cool/Bored" Poses
    "looking annoyed at the camera, hand raised to block the flash",
    "staring blankly into the distance, looking dissociated",
    "rolling her eyes dramatically",
    "slouching comfortably, looking totally relaxed and unposed",
    
    # Active / Candid
    "applying black lipstick using a compact mirror",
    "sipping from a can of Monster energy drink",
    "lighting a cigarette (flame illuminating face)",
    "exhaling smoke, obscuring part of the face",
    "fixing her messy hair, elbows up",
    "tying the laces of her heavy boots",
    "eating a slice of pizza messily",
    "holding a retro camcorder or digital camera",
    
    # Phone interaction
    "taking a mirror selfie with the phone covering her face completely",
    "scrolling on her phone, illuminated by the screen glow",
    "showing the middle finger to the camera playfully",
]

IMPERFECTIONS = [
    # Lighting Flaws
    "harsh direct flash creating a shadow directly behind her",
    "red-eye effect from the camera flash",
    "overexposed forehead due to strong flash",
    "lighting is dim and muddy, hard to see details",
    
    # Focus/Lens Flaws
    "image is slightly blurry due to motion (shutter drag)",
    "focus is on the background instead of her face (missed focus)",
    "lens is dirty/smudged creating a foggy glow around lights",
    "chromatic aberration (color fringing) on the edges of the photo",
    "thumb accidentally covering the bottom corner of the lens",
    
    # Composition Flaws
    "background is chaotic and cluttered with random objects",
    "dutch angle (camera tilted sideways)",
    "shot from a high angle (CCTV style)",
    "shot from a low unflattering angle",
]

# --- 4. SCENARIO GENERATOR ---

def generate_unique_prompt():
    loc = random.choice(LOCATIONS)
    outfit = random.choice(OUTFITS)
    action = random.choice(ACTIONS)
    flaw = random.choice(IMPERFECTIONS)
    
    # We combine them into a sentence, sometimes varying the order for natural language
    scenario = f"{action}, {loc}. {outfit}. {flaw}."
    return scenario

# --- 5. EXECUTION ---

def get_pollinations_url(prompt, seed):
    # 50% chance of Portrait (Phone), 25% Square (Insta), 25% Wide (Cinematic)
    aspect_choices = ["&width=768&height=1024", "&width=768&height=1024", "&width=1024&height=1024", "&width=1280&height=720"]
    dim_str = random.choice(aspect_choices)
    
    safe_prompt = urllib.parse.quote(prompt)
    return f"https://image.pollinations.ai/prompt/{safe_prompt}?nologo=true{dim_str}&seed={seed}&model={MODEL}"

def generate_feed():
    print(f"🚀 Spooling up EXPANDED Auto-Generator...")
    batch_id = int(time.time())

    for i in range(NUM_IMAGES_TO_GENERATE):
        scenario = generate_unique_prompt()
        full_prompt = f"{KATYA_BASE} {scenario}"
        seed = random.randint(10000, 99999)
        
        filename = f"katya_v2_{batch_id}_{i+1}.jpg"
        file_path = os.path.join(OUTPUT_DIR, filename)
        
        print(f"\n[{i+1}/{NUM_IMAGES_TO_GENERATE}] Generating...")
        print(f"   📝 Scenario: {scenario}")
        
        # RETRY LOOP: Tries 3 times before giving up
        max_retries = 3
        for attempt in range(max_retries):
            try:
                url = get_pollinations_url(full_prompt, seed)
                
                # CHANGED: Increased timeout from 30 to 120 seconds (2 minutes)
                r = requests.get(url, timeout=120)
                
                if r.status_code == 200:
                    with open(file_path, "wb") as f:
                        f.write(r.content)
                    print(f"   ✨ Saved: {filename}")
                    break # Success! Exit the retry loop
                else:
                    print(f"   ⚠️ Attempt {attempt+1} failed: Status {r.status_code}")
                    
            except requests.exceptions.Timeout:
                print(f"   ⚠️ Attempt {attempt+1} timed out (Server is busy). Retrying...")
            except Exception as e:
                print(f"   ⚠️ Attempt {attempt+1} error: {e}")
            
            # Wait a bit before retrying
            time.sleep(3)
            
        time.sleep(2)

if __name__ == "__main__":
    generate_feed()