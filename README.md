# 🥽 Beat Saber Lite 🎶 (No VR Required)

A rhythm-based action game clone of Beat Saber built entirely with **Python**, using **OpenCV** and **PyGame**. Slash the falling blocks in sync with music — all controlled via **your webcam**, no VR gear needed.

---

## 🔧 Features

- 🎮 Real-time hand tracking via webcam using OpenCV
- 🔺 Directional slicing (left, right, up, down) based on hand motion
- 🧠 Custom beatmap system to sync blocks with your own `.mp3` music
- 🩸 Health, combo, and scoring system
- 🧪 Debug fallback block mode
- 🔊 Integrated sound effects and background music
- 🐍 100% Python – no Unity, no VR, no external hardware

---

## 📁 Project Structure

📦 BeatSaberLite
├── main.py # Game entry point
├── arm_tracker.py # Hand tracking logic (OpenCV-based)
├── game_logic.py # Block management, scoring, collisions
├── assets/
│ ├── song.mp3 # Music file (user can replace)
│ ├── hit.wav # Hit sound effect
│ └── beatmap.json # Block spawn timings/directions
├── README.md # This file
└── requirements.txt # Python dependencies


---

## 🛠 Installation & Setup

### 1. Clone this repo

git clone https://github.com/yourusername/beat-saber-lite.git
cd beat-saber-lite
2. Create a virtual environment (optional but recommended)
bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
3. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
▶️ Run the Game
bash
Copy
Edit
python main.py
🎵 Customizing Music + Beatmap
Replace assets/song.mp3 with your own music file (same name).

Then update assets/beatmap.json with the beat times and directions:

json
Copy
Edit
[
  { "time": 2.5, "x": 150, "direction": "down" },
  { "time": 4.8, "x": 300, "direction": "left" }
]
Direction can be: "up", "down", "left", "right"

📷 Requirements
A working webcam

Good lighting for better tracking

Bright colored gloves/stickers (optional for better detection)

✅ Dependencies
Python 3.10+

OpenCV

PyGame

Numpy

Install via:

bash
Copy
Edit
pip install opencv-python pygame numpy
