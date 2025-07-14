import cv2

LANE_LINE_Y = 400  # Adjust if needed

def detect_lane_violations(frame, detections):
    violations = []
    cv2.line(frame, (0, LANE_LINE_Y), (frame.shape[1], LANE_LINE_Y), (0, 0, 255), 2)

    for (x, y, w, h) in detections:
        bottom_y = y + h
        if bottom_y > LANE_LINE_Y:
            violations.append((x, y, w, h))
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        else:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return violations
