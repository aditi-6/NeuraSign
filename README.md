# NeuraSign — Real-Time Gesture Translator
 
Built in 24 hours. Runs on a laptop. No glove required.
 
---
 
## What is this?
 
NeuraSign translates hand gestures into text and speech in real time, using just a webcam. It works on a custom vocabulary of 5 predefined gestures, no external dataset needed.
 
No hardware. No wearables. No sensor array soldered at 3am.
 
The interesting part is how it processes video. Instead of analyzing every single frame, it takes inspiration from neuromorphic computing — it only wakes up and does work when your hand actually moves. Idle hand = idle CPU. The system fires on change, not on time.
 
Your brain does not process your entire visual field every millisecond. It reacts to movement. We did the same thing in software.
 
---
 
## Supported Gestures
 
| Gesture | Hand Pose |
|---------|-----------|
| STOP    | Open palm, facing camera, all 5 fingers extended |
| YES     | Thumbs up, other fingers closed |
| NO      | Index and middle finger up, rest closed |
| HELLO   | Open palm, slight sideways tilt |
| HELP    | Closed fist, thumb extended laterally |
 
---
 
## How It Works
 
```
Webcam → Hand Landmarks → Event Detection → Gesture Classifier → Text + Speech
        (OpenCV)         (MediaPipe)       (spike threshold)    (ML model)
```
 
**Hand Detection** — OpenCV grabs the webcam feed. MediaPipe extracts 21 landmarks from the hand — fingertips, knuckles, wrist. This runs every frame.
 
**Event-Driven Spike Logic** — The system compares landmark positions between frames using Euclidean distance. If the delta is below threshold, nothing happens. If it crosses the threshold, a spike fires and the classifier runs. Stationary hand = zero processing. New gesture = one classification.
 
**Gesture Recognition** — Takes the 21 landmark coordinates and determines what sign is being made. Checks finger states (open/closed), relative positions, and joint angles. Returns a gesture label with smoothing over the last 5 frames.
 
**Output** — Detected gesture displayed on screen with a running count of total events fired vs frames captured.
 
---
 
## Tech Stack
 
- Python 3.11
- OpenCV — webcam capture and display
- MediaPipe 0.10.21 — hand landmark detection
- NumPy — delta calculation and landmark math
- Windows Speech Synthesis — offline text-to-speech via subprocess
---
 
## Setup
 
```bash
git clone https://github.com/aditi-6/NeuraSign.git
cd NeuraSign
py -3.11 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```
 
Point your webcam at your hand.
 
---
 
## Project Structure
 
```
NeuraSign/
├── main.py                  # Entry point, ties everything together
├── hand_detection.py        # Event-driven spike logic, delta threshold
├── gesture_classifier.py    # Finger state logic, gesture labeling
├── requirements.txt
└── README.md
```
 
---
 
## The Neuromorphic Angle
 
Standard video processing runs inference on every frame — 30 classifications per second even when nothing is happening.
 
Our approach uses event-driven spike logic. A threshold check compares the Euclidean distance of key landmarks between frames. If movement is below the threshold, classification is skipped entirely. If it crosses the threshold, the system fires — runs the classifier and updates output.
 
On a static hand, we process approximately 0 frames per second. On an active gesture, we process only the frames that matter.
 
This maps directly to how Spiking Neural Networks work — neurons fire only when input crosses a threshold. We implemented this as a software approximation without specialized neuromorphic hardware.
 
---
 
## Limitations
 
- Works best with plain background and decent lighting
- Supports 5 predefined gestures — vocabulary can be extended by defining new finger-state rules
- Neuromorphic implementation is a software approximation, not spiking hardware
- Single hand only
---
 
## Team
 
Built at Neuronex 2026 — 13-06-2026
 
| Member              | Module                                              |
|---------------------|-----------------------------------------------------|
| Aditi Jha           | Hand Detection, Landmark Extraction, Event-Driven Spike Logic |
| Gauri Nandana M     | Gesture Recognition                                 |
| Vidushi Kesharwani  | UI, Text-to-Speech Output                           |
 
---
 
## Future Scope
 
- Expanded gesture vocabulary beyond current 5
- Dynamic gesture support for motion-based signs
- Actual neuromorphic hardware deployment — Intel Loihi, BrainScaleS
- Mobile-first version
 
