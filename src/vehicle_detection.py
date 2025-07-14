# vehicle_detection.py – Simulated version for low-memory systems

def detect_vehicles(frame):
    print("[YOLO] Fake detection mode active.")
    return [
        (100, 200, 80, 40),  # box 1 (x, y, width, height)
        (300, 220, 100, 50)  # box 2
    ]
