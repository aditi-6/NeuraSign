import numpy as np

class HandDetector:
    def __init__(self):
        self.prev_landmarks = None
        self.THRESHOLD = 0.05
        self.event_count = 0

    def detect_event(self, landmarks):
        if self.prev_landmarks is None:
            self.prev_landmarks = landmarks
            return None

        curr = np.array(landmarks, dtype=float)
        prev = np.array(self.prev_landmarks, dtype=float)

        delta = np.mean(np.linalg.norm(curr - prev, axis=1))

        self.prev_landmarks = landmarks

        if delta > self.THRESHOLD:
            self.event_count += 1
            return landmarks

        return None
