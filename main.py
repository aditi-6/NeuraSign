import sys
import cv2
import mediapipe as mp
from gesture_classifier import classify_gesture
from hand_detection import HandDetector


mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
 
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
 
cap = cv2.VideoCapture(0)
detector = HandDetector()

window_name = "Sign Language Translator"

try:
    while True:
        success, frame = cap.read()
        if not success:
            break
 
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
 
        results = hands.process(rgb_frame)
 
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
 
                mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS
                )
 
                landmarks = []
                h, w, c = frame.shape
 
                for lm in hand_landmarks.landmark:
                    landmarks.append((int(lm.x * w), int(lm.y * h)))

                event = detector.detect_event(landmarks)
                if event is None:
                    continue
                gesture = classify_gesture(landmarks)
 
                # Background box behind text for readability
                text = f"Sign: {gesture}"
                (text_w, text_h), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
                cv2.rectangle(frame, (40, 20), (60 + text_w, 65), (0, 0, 0), -1)
 
                cv2.putText(
                    frame,
                    text,
                    (50, 55),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )
 
        cv2.imshow(window_name, frame)
 
        key = cv2.waitKey(1) & 0xFF
 
        # Exit via Q or window close
        if key == ord('q'):
            break
 
        if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
            break
 
finally:
    cap.release()
    cv2.destroyAllWindows()
    sys.exit()
