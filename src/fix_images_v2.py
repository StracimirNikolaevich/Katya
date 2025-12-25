import os
import time
import requests

# Ensure directory exists
output_dir = r"c:\Users\Asus\Desktop\Katya\content\images"
os.makedirs(output_dir, exist_ok=True)

# Image configurations
images = [
    {
        "name": "katya_main_portrait.jpg",
        "prompt": "alternative goth eastern european girl, pale skin, heavy eyeliner, wolf cut black hair, wearing fishnets and oversized hoodie, standing in a dimly lit concrete apartment block hallway, grainy film photography, flash, 35mm, doomer aesthetic, detailed face, looking at viewer, masterpiece, high quality",
        "size": "portrait_4_3"
    },
    {
        "name": "profile_pic.jpg",
        "prompt": "(flash photography:1.2), (grainy film:1.1), 1girl, pale skin, messy black hair with bangs, heavy eyeliner, septum piercing, wearing oversized black hoodie, sitting in cluttered dorm room, posters on wall, night time, russian doomer aesthetic, detailed face, looking at viewer, bored expression, 35mm",
        "size": "square_hd"
    },
     {
        "name": "tiktok_cover_balcony.jpg",
        "prompt": "1girl, leaning on balcony railing, smoking cigarette, night time, city lights in distance, concrete building, wind blowing hair, melancholic mood, cinematic lighting, side profile, russian doomer style",
        "size": "portrait_16_9"
    }
]

base_url = "https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image"
placeholder_size = 176626 # The size of the "Generating..." image

def download_image_persistent(img_config):
    name = img_config['name']
    prompt = img_config['prompt']
    size = img_config['size']
    
    print(f"\n🖼️  Target: {name}")
    url = f"{base_url}?prompt={requests.utils.quote(prompt)}&image_size={size}"
    
    start_time = time.time()
    max_wait = 120 # Wait up to 2 minutes
    
    attempts = 0
    while (time.time() - start_time) < max_wait:
        attempts += 1
        try:
            response = requests.get(url)
            if response.status_code == 200:
                content_len = len(response.content)
                
                # Check if it's the placeholder
                # We assume anything close to 176KB is the placeholder
                if 176000 < content_len < 177000:
                    print(f"   [Attempt {attempts}] Still generating... (Size: {content_len}) - Waiting 5s")
                    time.sleep(5)
                else:
                    # SUCCESS! Size is different
                    file_path = os.path.join(output_dir, name)
                    with open(file_path, "wb") as f:
                        f.write(response.content)
                    print(f"   ✅ SUCCESS! Downloaded real image ({content_len} bytes)")
                    return True
            else:
                print(f"   ❌ Error: Status {response.status_code}")
                time.sleep(5)
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")
            time.sleep(5)
            
    print(f"   ⚠️  Timed out after {max_wait} seconds. Could not get real image.")
    return False

print("🔄 Starting Persistent Download Sequence...")
for img in images:
    download_image_persistent(img)

print("\nSequence complete.")
