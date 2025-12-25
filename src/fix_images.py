import os
import time
import requests

# Ensure directory exists
output_dir = r"c:\Users\Asus\Desktop\Katya\content\images"
os.makedirs(output_dir, exist_ok=True)

# Image configurations
images = [
    {
        "name": "profile_pic.jpg",
        "prompt": "(flash photography:1.2), (grainy film:1.1), 1girl, pale skin, messy black hair with bangs, heavy eyeliner, septum piercing, wearing oversized black hoodie, sitting in cluttered dorm room, posters on wall, night time, russian doomer aesthetic, detailed face, looking at viewer, bored expression, 35mm",
        "size": "square_hd"
    },
    {
        "name": "ig_post_1_study.jpg",
        "prompt": "1girl, sitting at messy desk, piles of notes, open textbooks, monster energy drink can, looking stressed, head in hands, dark room, single desk lamp, gloomy atmosphere, russian doomer aesthetic, grainy film, flash photography",
        "size": "square"
    },
    {
        "name": "ig_post_2_outdoor.jpg",
        "prompt": "1girl, standing outside in snow, wearing thick oversized fur coat and fur hat, background is tall concrete panel apartment building, brutalist architecture, grey sky, cold atmosphere, full body shot, looking away, cinematic",
        "size": "portrait_4_3"
    },
    {
        "name": "ig_post_3_mirror_selfie.jpg",
        "prompt": "mirror selfie, 1girl, wearing fishnets and black skirt, holding phone covering face, dark room, messy background, flash photography, dirty mirror, aesthetic, grunge style, cool tones",
        "size": "portrait_16_9"
    },
    {
        "name": "tiktok_cover_balcony.jpg",
        "prompt": "1girl, leaning on balcony railing, smoking cigarette, night time, city lights in distance, concrete building, wind blowing hair, melancholic mood, cinematic lighting, side profile, russian doomer style",
        "size": "portrait_16_9"
    },
    {
        "name": "tiktok_cover_rave.jpg",
        "prompt": "1girl, close up face, heavy goth makeup, black lipstick, choker, neon lights reflecting on face, dark club atmosphere, sweaty, intense look, flash photography, party vibe",
        "size": "portrait_16_9"
    },
    {
        "name": "katya_main_portrait.jpg",
        "prompt": "alternative goth eastern european girl, pale skin, heavy eyeliner, wolf cut black hair, wearing fishnets and oversized hoodie, standing in a dimly lit concrete apartment block hallway, grainy film photography, flash, 35mm, doomer aesthetic, detailed face, looking at viewer, masterpiece, high quality",
        "size": "portrait_4_3"
    }
]

base_url = "https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image"

print("🔄 Starting Smart Download (with retries)...")

for img in images:
    print(f"\n🖼️  Processing {img['name']}...")
    
    url = f"{base_url}?prompt={requests.utils.quote(img['prompt'])}&image_size={img['size']}"
    
    # Attempt 1: Trigger Generation
    print("   Triggering generation...")
    r1 = requests.get(url)
    
    # Wait for generation (The API likely needs time)
    print("   Waiting 10 seconds for server to generate...")
    time.sleep(10)
    
    # Attempt 2: Download Real Image
    print("   Downloading result...")
    r2 = requests.get(url)
    
    if r2.status_code == 200:
        file_path = os.path.join(output_dir, img['name'])
        
        # Check size - placeholders are usually small (<15KB)
        content_length = len(r2.content)
        print(f"   File size: {content_length} bytes")
        
        if content_length < 20000:
            print("   ⚠️  Warning: File seems small (possible placeholder). Waiting 10s more and retrying...")
            time.sleep(10)
            r3 = requests.get(url)
            with open(file_path, "wb") as f:
                f.write(r3.content)
            print(f"   Saved (Retry): {file_path}")
        else:
            with open(file_path, "wb") as f:
                f.write(r2.content)
            print(f"   Saved: {file_path}")
    else:
        print(f"   ❌ Failed: Status {r2.status_code}")

print("\n✅ Download sequence complete.")
