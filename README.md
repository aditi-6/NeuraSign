# NeuraSign — Real-Time Gesture Translator


Built in 24 hours. Runs on a laptop. No glove required.

## What is this?

NeuraSign translates hand gestures into text and speech — in real time, using just a webcam. It works on a custom vocabulary of 5 predefined gestures, no external dataset needed.

No hardware. No wearables. No sensor array soldered at 3am.

The interesting part is how it processes video. Instead of analyzing every single frame (which is wasteful and slow), it takes inspiration from neuromorphic computing — it only wakes up and does work when your hand actually moves. Idle hand = idle CPU. The system fires on change, not on time.

Think of it like this: your brain doesn't process your entire visual field every millisecond. It reacts to movement. We did the same thing in software.


# Supported Gestures

🖐️ STOP :Open palm, facing camera All 5 fingers extended

👍 YES Thumbs up Thumb out, others closed

✌️ NOPeace signIndex + middle up, rest closed

👋 HELLO Open palm, slight tiltSimilar to STOP but sideways


🆘 HELP Closed fist, thumb to sideFist + thumb extended laterally


## How it works

Webcam → Hand Landmarks → Delta Detection → Gesture Classifier → Text + Speech
           (MediaPipe)      (neuromorphic        (ML model)
                             spike logic)

## Three modules, three people:

1. Hand Detection — OpenCV grabs the webcam feed. MediaPipe extracts 21 landmarks from your hand (fingertips, knuckles, wrist — the works). This runs every frame.

2. Gesture Recognition — Takes those 21 landmark coordinates and figures out what sign you're making. Checks finger states (open/closed), angles between joints, relative positions. Returns a gesture label.

3. Event-Driven Logic + UI — Here's the neuromorphic bit. The system compares landmark positions between frames and only triggers classification when the delta crosses a threshold. Stationary hand? Nothing happens. New gesture? Spike fires, classifier runs, output updates. The dashboard shows the detected sign, live video feed, and a running count of frames captured vs. frames actually processed.


## Tech Stack


Python 3.10+
OpenCV — webcam capture, display
MediaPipe — hand landmark detection
scikit-learn / NumPy — gesture classifier
pyttsx3 — text-to-speech (offline, no API key needed)
Tkinter / OpenCV window — UI



## Setup

bashgit clone https://github.com/yourteam/neurasign.git
cd neurasign
pip install -r requirements.txt
python main.py

That's it. Point your webcam at your hand.


## Project Structure

neurasign/
├── main.py                  # Entry point, ties everything together
├── detection/
│   └── hand_tracker.py      # MediaPipe setup, landmark extraction
├── recognition/
│   └── gesture_classifier.py  # Finger state logic, gesture labeling
├── output/
│   └── voice_output.py      # TTS + text display
├── ui/
│   └── dashboard.py         # Live feed, stats, detected sign display
├── requirements.txt
└── README.md
-------------------------------------------------------------------------

## The Neuromorphic Angle :

Standard video processing = run inference on every frame = 30 classifications/second even when nothing's happening.

Our approach = event-driven spike logic. A threshold check compares the Euclidean distance of key landmarks between frames. If the movement is below the threshold, we skip classification entirely. If it crosses the threshold, we "fire" — run the classifier, update output.

Result: on a static hand, we process ~0 frames per second. On an active gesture, we process only the frames that matter.

This maps directly to how Spiking Neural Networks (SNNs) work — neurons fire only when input crosses a threshold. We implemented this as a software approximation without specialized neuromorphic hardware.


## Limitations (we're honest people) :

Works best with a plain background and decent lighting
Currently supports 5 predefined gestures — vocabulary can be extended by defining new finger-state rules
The "neuromorphic" implementation is a software approximation, not actual spiking hardware
One hand only for now


## Team :

Built at Neuronex'26 — 13-06-26

## MemberModule
Aditi Jha : Hand Detection + Landmark Extraction
Gauri Nandana M : Gesture Recognition (the AI bit)
Vidushi Kesharwani : Event Logic + UI + TTS


## Future Scope: 

Expanded gesture vocabulary (beyond the current 5)
Dynamic gesture support (motion-based signs like "THANK YOU")
Actual neuromorphic hardware deployment (Intel Loihi, BrainScaleS)
Mobile-first version
