import asyncio
import websockets
import requests
import pytesseract
import pyautogui
import cv2
import numpy as np
from PIL import Image
import json
import time
from collections import defaultdict

def capture_and_grouped_ocr():
    screenshot = pyautogui.screenshot()
    screen_width, screen_height = pyautogui.size()
    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    image_height, image_width = img.shape[:2]

    lines = defaultdict(list)

    for i in range(len(data['text'])):
        if int(data['conf'][i]) > 60:
            text = data['text'][i].strip()
            if text:
                block_num = data['block_num'][i]
                par_num = data['par_num'][i]
                line_num = data['line_num'][i]
                key = (block_num, par_num, line_num)

                lines[key].append({
                    "text": text,
                    "x": data['left'][i],
                    "y": data['top'][i],
                    "w": data['width'][i],
                    "h": data['height'][i]
                })

    grouped_regions = []
    for words in lines.values():
        full_text = " ".join([w["text"] for w in words])
        x = min(w["x"] for w in words)
        y = min(w["y"] for w in words)
        x2 = max(w["x"] + w["w"] for w in words)
        y2 = max(w["y"] + w["h"] for w in words)

        # Scale bounding box
        scaled_x = int(x * screen_width / image_width)
        scaled_y = int(y * screen_height / image_height)
        scaled_w = int((x2 - x) * screen_width / image_width)
        scaled_h = int((y2 - y) * screen_height / image_height)

        grouped_regions.append({
            "text": full_text,
            "left": scaled_x,
            "top": scaled_y,           # ✅ FIXED: correct key
            "width": scaled_w,
            "height": scaled_h
        })

    return grouped_regions, img

def draw_debug_image(original_img, regions, filename="debug_output.png"):
    for r in regions:
        x, y, w, h = r["left"], r["top"], r["width"], r["height"]
        cv2.rectangle(original_img, (x, y), (x + w, y + h), (0, 0, 255), 2)
    cv2.imwrite(filename, original_img)

async def send_ocr_regions():
    while True:
        try:
            regions, original_img = capture_and_grouped_ocr()
            print(f"[✓] Captured {len(regions)} grouped regions")

            # Send grouped regions to backend AI
            response = requests.post("http://localhost:5000/predict", json={"regions": regions})
            all_results = response.json().get("toxic_regions", [])

            # Only keep toxic regions (label_0)
            toxic_regions = [r for r in all_results if r.get("label") == "LABEL_0"]
            print(f"[✓] Filtered {len(toxic_regions)} toxic regions")

            draw_debug_image(original_img, toxic_regions, "debug_output.png")

            async with websockets.connect("ws://localhost:8765") as ws:
                await ws.send(json.dumps(toxic_regions))
                print("[✓] Sent toxic regions to WebSocket")

        except Exception as e:
            print(f"[x] Error: {e}")

        time.sleep(2)

if __name__ == "__main__":
    asyncio.run(send_ocr_regions())