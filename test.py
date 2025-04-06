import requests

# Sample test cases
test_texts = [
    "You're amazing and doing great work!",
    "This is the worst thing ever.",
    "You idiot!",
    "Go to settings",
    "x",
    "I hope you die!",
    "lol",
    "Shut up and leave me alone.",
    "You piece of trash!",
    "Okay"
]

# Simulate regions as in OCR
test_regions = [{
    "text": text,
    "x": 100,
    "y": 100 + i * 60,
    "width": 200,
    "height": 50
} for i, text in enumerate(test_texts)]

# Send to backend
response = requests.post("http://localhost:5000/predict", json={"regions": test_regions})
result = response.json()

# Print all results
print("\n🔍 All Regions:")
for region in result.get("all_regions", []):
    print(f"→ Label: {region['label']} | Score: {region['score']:.4f} | Text: {region['text']}")

print("\n🚨 Toxic Regions (LABEL_0 with score > 0.95):")
for region in result.get("toxic_regions", []):
    print(f"❗ {region['text']} (score: {region['score']:.4f})")
