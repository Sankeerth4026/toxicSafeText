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

