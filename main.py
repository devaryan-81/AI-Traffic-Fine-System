import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from src.vehicle_detection import detect_vehicles
from src.challan_generator import generate_challan
from src.database_manager import insert_violation_record
from src.license_plate_recognition import recognize_plate  # Optional if not using OCR
import os
import threading

class TrafficFineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Traffic Fine System")
        self.root.geometry("900x600")
        self.root.configure(bg="#1e1e1e")

        self.video_source = "videos/traffic.mp4"
        self.vid = cv2.VideoCapture(self.video_source)

        self.canvas = tk.Canvas(self.root, width=800, height=500)
        self.canvas.pack(pady=10)

        self.btn_frame = tk.Frame(self.root, bg="#1e1e1e")
        self.btn_frame.pack()

        self.start_btn = tk.Button(self.btn_frame, text="Start Detection", command=self.run_detection, bg="#444", fg="white")
        self.start_btn.grid(row=0, column=0, padx=10)

        self.select_btn = tk.Button(self.btn_frame, text="Select Video", command=self.select_video, bg="#444", fg="white")
        self.select_btn.grid(row=0, column=1, padx=10)

        self.log_box = tk.Text(self.root, height=6, width=100, bg="#222", fg="white")
        self.log_box.pack(pady=10)

    def select_video(self):
        path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi")])
        if path:
            print(f"[INFO] New video selected: {path}")
            self.video_source = path
            self.vid.release()
            self.vid = cv2.VideoCapture(self.video_source)
            self.run_detection()
            
    def process_violation(self, plate_region):
        from src.license_plate_recognition import recognize_plate

        plate = recognize_plate(plate_region)
        generate_challan(plate, "Lane Violation")
        insert_violation_record(plate, "Lane Violation")
        self.log_box.insert(tk.END, f"Violation Detected: {plate}\n")


    def run_detection(self):
        print("[INFO] Trying to read frame from:", self.video_source)
        ret, frame = self.vid.read()
        print("[DEBUG] Frame Read Status:", ret)

        if not ret:
            print("[WARNING] Could not read frame. Check video format or path.")
            return

        frame = cv2.resize(frame, (800, 500))
        print("[INFO] Frame resized")

        try:
            # Use fake vehicle detection (simulated boxes)
            detections = detect_vehicles(frame)
            violations = detections

            for (x, y, w, h) in violations:
                # Replace this with actual OCR if needed:
                plate = "DL10ABC123" 
                threading.Thread(target=self.process_violation, args=(frame[y:y+h, x:x+w],)).start()

                #plate = recognize_plate(frame[y:y+h, x:x+w])
                print(f"[INFO] Detected violation: {plate}")
                generate_challan(plate, "Lane Violation")
                insert_violation_record(plate, "Lane Violation")
                self.log_box.insert(tk.END, f"Violation Detected: {plate}\n")

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(Image.fromarray(frame))
            self.canvas.create_image(0, 0, anchor=tk.NW, image=img)
            self.root.image = img

        except Exception as e:
            print("[EXCEPTION] in run_detection:", e)

        self.root.after(30, self.run_detection)

if __name__ == "__main__":
    try:
        if not os.path.exists("videos/traffic.mp4"):
            print("\n[ERROR] Demo video not found. Please add it to the 'videos/' folder.\n")
        else:
            print("[INFO] Launching GUI...")
            root = tk.Tk()
            app = TrafficFineApp(root)
            root.mainloop()
    except Exception as e:
        print("[EXCEPTION] in main:", e)
