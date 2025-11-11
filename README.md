# toxicSafeText

⚠️ **Status:** Experimental project — works partially, not perfect yet.

---

## 🧠 Overview
**toxicSafeText** is an experimental desktop app that detects toxic or unsafe text on your screen using **OCR** and **AI-based text classification**, then **blurs those regions** in real time to create a safer viewing experience.

It combines:
- 🧩 **Python backend** – handles OCR and toxicity detection  
- ⚡ **WebSocket communication** – sends detection results live  
- 💻 **Electron + React frontend** – creates an overlay that blurs toxic text  

---

## 🚧 Current Problem

The project runs, but there’s a major issue:

When the app blurs toxic text, the **next screenshot includes the blur overlay**, so the AI no longer detects toxic words.  
It then **unblurs the region**, causing a *blink / flicker effect* (blur → unblur → blur again).

### Why this happens
The screen capture process includes the overlay itself. Since the blurred overlay hides the toxic words, the next frame shows “no toxicity,” which resets the blur.

---

## 🔧 Possible Fixes / Ideas
If you want to help make it work:
- Exclude overlay from screenshots  
  → In Electron, try `mainWindow.setContentProtection(true)`
- Capture only the background (using Windows Desktop Duplication API)
- Cache toxic regions to avoid instantly unblurring  
- Run detection every few seconds instead of continuously  

If you manage to fix it — much appreciated ❤️

---

## ⚙️ How to Run (Experimental)
> Tested mainly on **Windows** during development.

1. **Clone the repo**
   ```bash
   git clone https://github.com/Sankeerth4026/toxicSafeText.git
   cd toxicSafeText
### 2️⃣ Capture only the desktop layer (Platform API)

Use APIs that let you capture **only the desktop background**, excluding overlay windows like your blur layer.

**For example:**
- 🪟 **Windows:** Use the **Desktop Duplication API** (DirectX) to directly capture the desktop frame buffer instead of the rendered display.  
- 🍎 **macOS:** Use the **CGDisplayStream API**.
- 🐧 **Linux:** Consider libraries like **XComposite** or **PipeWire**.

These APIs allow you to grab the screen content *beneath* overlay windows, preventing your own overlay from being captured — effectively solving the blur-unblur feedback loop.

---

### 3️⃣ Cache toxic regions

Don’t unblur immediately after a single clean detection — add stability by caching previously toxic regions.

**Approach:**
- Maintain a list of “active toxic regions.”  
- If an area was toxic recently, keep it blurred for a few more frames (e.g., 5–10 seconds).  
- Only remove the blur if it remains clean for multiple scans.  

This prevents flicker and makes the app look smoother overall

###4️⃣ Slow or timed detection cycle

Instead of continuous frame-by-frame OCR scanning, you can run the detection process at controlled intervals.

**Recommended approach:**
- Run OCR + toxicity detection every **2–3 seconds** instead of continuously.
- Optionally, trigger detection only when the screen content has changed (using image diffing or screen events).

**Benefits:**
- Reduces CPU and GPU load ⚙️  
- Prevents flickering caused by rapid re-rendering ⚡  
- Makes blurring behavior smoother and more stable ✅  

---

### 5️⃣ Differential or masked detection

Optimize performance by detecting toxicity only in **changed** regions of the screen.

**Implementation ideas:**
- Store the previous screenshot.  
- Compare it with the new one using pixel difference.  
- Run OCR only on regions where the difference exceeds a threshold.  

This ensures:
- No redundant OCR on static areas.  
- Fewer false detections from overlay blur.  
- Smoother real-time updates.

---

## 🪜 Step 5: Project Setup & Usage

### 🧰 Prerequisites
- Python ≥ 3.9  
- Node.js ≥ 18  
- Tesseract OCR installed on your system  
- Electron + React dependencies installed  

---

### ⚙️ Backend Setup (Python)

```bash
cd backend
pip install -r requirements.txt
python server.py
```

### 💻 Frontend Setup (Electron + React)

```bash
cd frontend
npm install
npm start
```
## 🪜 Step 6: Folder Structure (Example)
```bash
toxicSafeText/
├── backend/
│ ├── server.py
│ ├── detector.py
│ ├── ocr.py
│ └── requirements.txt
├── frontend/
│ ├── public/
│ │ └── main.js
│ ├── src/
│ │ ├── App.jsx
│ │ └── components/
│ └── package.json
└── README.md
```

🗂️ **Explanation:**
- **backend/** → Handles OCR, toxicity detection, and WebSocket communication.  
- **frontend/** → Electron + React overlay app that applies the blur in real time.  
- **requirements.txt** → Python dependencies.  
- **package.json** → Electron/React dependencies.  

---

## 🪜 Step 7: Known Issues

| Issue | Description |
|-------|-------------|
| ⚠️ Self-blur feedback | Overlay window appears in screenshots, causing an infinite blur–unblur loop. |
| 💤 Slow OCR | Frame-by-frame OCR is resource-intensive and may cause lag. |
| 🔁 WebSocket instability | Occasional disconnections interrupt blur synchronization. |
| 🖥️ Multi-monitor support | Coordinates can misalign across screens; unstable in multi-monitor setups. |

🧩 *These are known problems — fixes and contributions are welcome!*

---

## 🪜 Step 8: Related Projects

- 🧠 **toxicSafeText** — this initial prototype  
- 🧩 **toxicSafe2 / toxicSafe3 / toxicSafe4** — incremental test versions experimenting with bug fixes and refinements  
- 💻 **toxicSafeScreen** — advanced Electron + Python build combining text + image detection, packaged for Windows  

---

## 🪜 Step 9: Contributing

💡 **How you can help:**
- Fix the screen-capture feedback loop.  
- Optimize OCR to use less CPU.  
- Add image-based or multi-monitor detection.  
- Improve backend ↔ frontend synchronization.

If you manage to stabilize the blur overlay or improve frame detection, please open a **Pull Request (PR)** — your contribution will be credited and appreciated ❤️  

---

## 💬 Final Notes

This project was a **learning experiment** exploring:
- Real-time OCR text recognition  
- Toxicity classification using AI models  
- Desktop overlays and blur rendering  
- Integration between Python backends and Electron frontends  

It’s not perfect, but it’s a solid foundation for anyone curious about **AI-driven screen filtering and safety tools**.

⭐ *If you build upon or fix this project, please credit this repo — every improvement helps make it better!*


