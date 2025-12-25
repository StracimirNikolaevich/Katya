import os
print("Starting script...")
from PIL import Image, ImageDraw, ImageFont, ImageFilter
print("Imports successful")

# Directories
input_dir = r"c:\Users\Asus\Desktop\Katya\content\images"
output_dir = r"c:\Users\Asus\Desktop\Katya\content\ready_to_post"
os.makedirs(output_dir, exist_ok=True)

# Configuration for posts (Image + Text Overlay)
posts = [
    {
        "base_image": "tiktok_cover_balcony.jpg",
        "text": "POV: You fell in love\nwith the girl from the bloc.",
        "subtext": "(Good luck)",
        "output_name": "video1_slide1.jpg"
    },
    {
        "base_image": "ig_post_1_study.jpg",
        "text": "It's -10 degrees and\nI have an 8am lecture.",
        "subtext": "",
        "output_name": "video1_slide2.jpg"
    },
    {
        "base_image": "profile_pic.jpg",
        "text": "Don't talk to me.",
        "subtext": "",
        "output_name": "video1_slide3.jpg"
    },
    {
        "base_image": "ig_post_2_outdoor.jpg",
        "text": "What you think dating\nan Eastern European girl is like:",
        "subtext": "",
        "output_name": "video2_slide1.jpg"
    },
    {
        "base_image": "ig_post_3_mirror_selfie.jpg",
        "text": "Me bullying you because\nyou didn't text back.",
        "subtext": "",
        "output_name": "video2_slide2.jpg"
    },
     {
        "base_image": "ig_post_1_study.jpg",
        "text": "Me at university...",
        "subtext": "",
        "output_name": "video3_slide1.jpg"
    },
    {
        "base_image": "tiktok_cover_rave.jpg",
        "text": "...vs. Me at the rave.",
        "subtext": "",
        "output_name": "video3_slide2.jpg"
    }
]

def add_tiktok_text(image, text, subtext=""):
    draw = ImageDraw.Draw(image)
    width, height = image.size
    
    # Simple font logic (try to find a system font, fallback to default)
    try:
        # Arial Bold is standard for memes/social media
        font_size = int(width * 0.08) # Dynamic size
        font = ImageFont.truetype("arialbd.ttf", font_size)
        sub_font = ImageFont.truetype("arial.ttf", int(font_size * 0.7))
    except:
        font = ImageFont.load_default()
        sub_font = ImageFont.load_default()

    # Calculate Text Position (Centered, slightly lower than middle for "subtitle" look or top for "POV")
    # Let's do standard "POV text" at the top-middle
    
    # Helper to draw text with outline (classic meme/subtitle look)
    def draw_text_with_outline(x, y, text, font):
        # Thick black outline
        outline_width = 3
        for adj in range(-outline_width, outline_width+1):
             for adj2 in range(-outline_width, outline_width+1):
                 draw.text((x+adj, y+adj2), text, font=font, fill="black", anchor="mm")
        # White text
        draw.text((x, y), text, font=font, fill="white", anchor="mm")

    # Draw Main Text
    text_y = height * 0.3
    draw_text_with_outline(width/2, text_y, text, font)

    # Draw Subtext
    if subtext:
        subtext_y = text_y + font_size * 1.5
        draw_text_with_outline(width/2, subtext_y, subtext, sub_font)

    return image

def process_images():
    print("🎨 Processing images into TikTok slides...")
    
    for post in posts:
        input_path = os.path.join(input_dir, post['base_image'])
        output_path = os.path.join(output_dir, post['output_name'])
        
        if os.path.exists(input_path):
            try:
                with Image.open(input_path) as img:
                    # 1. Resize/Crop to 9:16 for TikTok if needed (Portrait)
                    target_ratio = 9/16
                    current_ratio = img.width / img.height
                    
                    if current_ratio > target_ratio:
                        # Too wide, crop width
                        new_width = int(img.height * target_ratio)
                        offset = (img.width - new_width) // 2
                        img = img.crop((offset, 0, offset + new_width, img.height))
                    else:
                        # Too tall (rare) or close enough, just resize
                        pass
                        
                    img = img.resize((1080, 1920), Image.Resampling.LANCZOS)
                    
                    # 2. Add Grain/Filter (Doomer aesthetic)
                    # Simple noise or darkening
                    # Let's just slightly darken it to make text pop
                    # (Skipping complex noise for now to keep it clean)
                    
                    # 3. Add Text
                    img = add_tiktok_text(img, post['text'], post['subtext'])
                    
                    img.save(output_path, quality=95)
                    print(f"✅ Generated: {post['output_name']}")
            except Exception as e:
                print(f"❌ Error processing {post['base_image']}: {e}")
        else:
            print(f"⚠️ Missing base image: {post['base_image']}")

if __name__ == "__main__":
    process_images()
