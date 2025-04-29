import tkinter as tk
from tkinter import ttk, filedialog
import cv2
import numpy as np
from PIL import Image, ImageTk
import os
from datetime import datetime

class CameraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Camera Application")
        self.root.configure(bg='#2C3E50')
        
        # Initialize camera
        self.cap = cv2.VideoCapture(0)
        self.recording = False
        self.output_video = None
        self.frames = []  # Store frames during recording
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Enhanced Style configuration
        style = ttk.Style()
        style.configure('Capture.TButton',
                       background='#27AE60',
                       foreground='white',
                       padding=15,
                       font=('Arial', 12, 'bold'))
        
        style.configure('Record.TButton',
                       background='#E74C3C',
                       foreground='white',
                       padding=15,
                       font=('Arial', 12, 'bold'))
        
        style.configure('Quit.TButton',
                       background='#95A5A6',
                       foreground='white',
                       padding=15,
                       font=('Arial', 12, 'bold'))
        
        # Create video frame with border
        self.video_frame = tk.Label(self.main_frame, relief="solid", borderwidth=2)
        self.video_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        
        # Button Frame for better organization
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.grid(row=1, column=0, columnspan=3, pady=10)
        
        # Enhanced Buttons with better spacing and styling
        self.capture_btn = tk.Button(
            self.button_frame,
            text="📸 Take Photo",
            command=self.capture_photo,
            bg='#27AE60',
            fg='white',
            font=('Arial', 12, 'bold'),
            relief='raised',
            width=15,
            height=2
        )
        self.capture_btn.grid(row=0, column=0, padx=10)
        
        self.record_btn = tk.Button(
            self.button_frame,
            text="🎥 Start Recording",
            command=self.toggle_recording,
            bg='#E74C3C',
            fg='white',
            font=('Arial', 12, 'bold'),
            relief='raised',
            width=15,
            height=2
        )
        self.record_btn.grid(row=0, column=1, padx=10)
        
        self.quit_btn = tk.Button(
            self.button_frame,
            text="❌ Quit",
            command=self.quit_app,
            bg='#95A5A6',
            fg='white',
            font=('Arial', 12, 'bold'),
            relief='raised',
            width=15,
            height=2
        )
        self.quit_btn.grid(row=0, column=2, padx=10)
        
        # Enhanced Status label
        self.status_label = tk.Label(
            self.main_frame,
            text="Ready to use",
            font=('Arial', 11, 'bold'),
            bg='#2C3E50',
            fg='#ECF0F1',
            pady=10
        )
        self.status_label.grid(row=2, column=0, columnspan=3, pady=10)
        
        # Create output directory
        self.output_dir = "camera_output"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Start video stream
        self.update_frame()
    
    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Store the original frame for recording
            if self.recording:
                self.frames.append(frame.copy())
            
            # Convert frame for display
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_pil = Image.fromarray(frame_rgb)
            frame_pil = frame_pil.resize((640, 480))
            frame_tk = ImageTk.PhotoImage(image=frame_pil)
            
            self.video_frame.imgtk = frame_tk
            self.video_frame.configure(image=frame_tk)
        
        self.root.after(10, self.update_frame)
    
    def capture_photo(self):
        ret, frame = self.cap.read()
        if ret:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(self.output_dir, f"photo_{timestamp}.jpg")
            cv2.imwrite(filename, frame)
            self.status_label.config(text=f"Photo saved: {filename}")
            
            # Provide visual feedback
            self.capture_btn.config(relief='sunken')
            self.root.after(100, lambda: self.capture_btn.config(relief='raised'))
    
    def toggle_recording(self):
        if not self.recording:
            # Start recording
            self.frames = []  # Clear previous frames
            self.recording = True
            self.record_btn.config(
                text="⏹️ Stop Recording",
                bg='#C0392B'
            )
            self.status_label.config(text="Recording in progress...")
        else:
            # Stop recording and save video
            self.recording = False
            if self.frames:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = os.path.join(self.output_dir, f"video_{timestamp}.mp4")
                
                # Get the dimensions of the first frame
                height, width = self.frames[0].shape[:2]
                
                # Initialize video writer with H264 codec
                fourcc = cv2.VideoWriter_fourcc(*'avc1')
                out = cv2.VideoWriter(filename, fourcc, 30.0, (width, height))
                
                # Write frames to video file
                for frame in self.frames:
                    out.write(frame)
                
                # Release video writer
                out.release()
                self.frames = []  # Clear frames
                
                self.status_label.config(text=f"Video saved: {filename}")
            
            self.record_btn.config(
                text="🎥 Start Recording",
                bg='#E74C3C'
            )
    
    def quit_app(self):
        if self.recording:
            self.toggle_recording()
        self.cap.release()
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root)
    root.mainloop()