from collections import deque, Counter

gesture_history = deque(maxlen=5)

THUMB_TIP = 4
INDEX_TIP = 8
MIDDLE_TIP = 12
RING_TIP = 16
PINKY_TIP = 20


# ---------------------------
# Finger checks
# ---------------------------

def is_index_open(landmarks):
    return landmarks[8][1] < landmarks[6][1]


def is_middle_open(landmarks):
    return landmarks[12][1] < landmarks[10][1]


def is_ring_open(landmarks):
    return landmarks[16][1] < landmarks[14][1]


def is_pinky_open(landmarks):
    return landmarks[20][1] < landmarks[18][1]


def is_thumb_open(landmarks):
    wrist = landmarks[0]
    thumb_tip = landmarks[4]
    index_mcp = landmarks[5]  # use hand size as reference so it works across resolutions
    hand_size = abs(index_mcp[1] - wrist[1])
    if hand_size == 0:
        return False
    return abs(thumb_tip[0] - wrist[0]) > hand_size * 0.3


# ---------------------------
# MAIN CLASSIFIER
# ---------------------------

def classify_gesture(landmarks):

    if len(landmarks) != 21:
        return "UNKNOWN"

    wrist = landmarks[0]
    thumb_tip = landmarks[THUMB_TIP]
    index_tip = landmarks[INDEX_TIP]

    thumb_dx = thumb_tip[0] - wrist[0]
    thumb_dy = thumb_tip[1] - wrist[1]

    palm_dx = index_tip[0] - wrist[0]
    palm_dy = index_tip[1] - wrist[1]

    thumb_open = is_thumb_open(landmarks)
    index_open = is_index_open(landmarks)
    middle_open = is_middle_open(landmarks)
    ring_open = is_ring_open(landmarks)
    pinky_open = is_pinky_open(landmarks)

    gesture = "UNKNOWN"

    # ---------------- STOP ----------------
    # All 5 fingers open, palm facing camera (vertical orientation)
    if (
        thumb_open and index_open and middle_open and
        ring_open and pinky_open and
        abs(palm_dy) > abs(palm_dx)
    ):
        gesture = "STOP"

    # ---------------- HELLO ----------------
    # All 5 fingers open, palm tilted sideways (horizontal orientation)
    elif (
        thumb_open and index_open and middle_open and
        ring_open and pinky_open and
        abs(palm_dx) > abs(palm_dy)
    ):
        gesture = "HELLO"

    # ---------------- YES ----------------
    # Thumbs up: thumb open + pointing upward, all fingers closed
    # Checked BEFORE HELP to avoid conflict
    elif (
        thumb_open and
        not index_open and not middle_open and
        not ring_open and not pinky_open and
        thumb_dy < 0  # thumb pointing up
    ):
        gesture = "YES"

    # ---------------- HELP ----------------
    # Closed fist with thumb extended SIDEWAYS (not upward)
    # abs(thumb_dx) > abs(thumb_dy) ensures thumb goes sideways, not up
    elif (
        not index_open and not middle_open and
        not ring_open and not pinky_open and
        thumb_open and abs(thumb_dx) > abs(thumb_dy)
    ):
        gesture = "HELP"

    # ---------------- NO ----------------
    # Peace sign: index + middle open, rest closed, no thumb
    elif (
        not thumb_open and index_open and middle_open and
        not ring_open and not pinky_open
    ):
        gesture = "NO"

    # ---------------- SMOOTHING ----------------
    gesture_history.append(gesture)
    most_common = Counter(gesture_history).most_common(1)[0][0]

    return most_common