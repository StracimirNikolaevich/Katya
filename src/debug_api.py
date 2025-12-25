import requests
import time

url = "https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=cat&image_size=square"

print("Requesting...")
r = requests.get(url)
print(f"Status: {r.status_code}")
print(f"Headers: {r.headers}")
print(f"Content Length: {len(r.content)}")

# Check if it looks like the placeholder (approx 176KB)
if 176000 < len(r.content) < 177000:
    print("⚠️  Received likely placeholder image.")

print("\nWaiting 15 seconds...")
time.sleep(15)

print("Requesting again...")
r2 = requests.get(url)
print(f"Status: {r2.status_code}")
print(f"Content Length: {len(r2.content)}")
