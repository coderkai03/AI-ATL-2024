import pyautogui
import os
import time
import cv2
import numpy as np
from threading import Thread, Event
from queue import Queue

def capture_screen_continuously(screenshot_queue, stop_event, save_directory=None, interval=3):
    """
    Continuously captures the screen and saves it as 'screenshot.png'.

    Parameters:
    - save_directory (str): The directory where the screenshot will be saved.
                            If None, saves to the current working directory.
    - interval (float): Time interval between screenshots in seconds.

    Returns:
    - None
    """
    try:
        # Set save directory
        if save_directory is None:
            save_directory = os.getcwd()
        else:
            # Create the directory if it doesn't exist
            os.makedirs(save_directory, exist_ok=True)
        
        # Full path for the image file
        filepath = os.path.join(save_directory, "screenshot.png")
        
        print(f"Starting continuous screen capture. Press Ctrl+C to stop.")
        while not stop_event.is_set():
            # Capture the screenshot
            screenshot = pyautogui.screenshot()
            
            # Save the screenshot
            screenshot.save(filepath)
            
            # Add screenshot to queue for processing
            screenshot_queue.put(filepath)
            
            print(f"Screenshot saved at: {filepath}")
            time.sleep(interval)

    except KeyboardInterrupt:
        print("Screen capture stopped.")
    except Exception as e:
        print(f"An error occurred while capturing the screen: {e}")

def process_screenshots(screenshot_queue, stop_event, save_directory):
    # Use the Haar Cascade file from the specified location
    cascade_path = "./haar/haarcascade_frontalface_default.xml"
    
    if not os.path.exists(cascade_path):
        print(f"Error: Haar Cascade file not found at {cascade_path}")
        return

    face_cascade = cv2.CascadeClassifier(cascade_path)
    print(f"Using Haar Cascade file from: {cascade_path}")
    
    # Create the captured_faces directory
    captured_faces_dir = os.path.join(save_directory, "captured_faces")
    os.makedirs(captured_faces_dir, exist_ok=True)
    
    while not stop_event.is_set():
        if not screenshot_queue.empty():
            screenshot_path = screenshot_queue.get()
            img = cv2.imread(screenshot_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            
            if len(faces) > 0:
                # Choose the first detected face
                x, y, w, h = faces[0]
                face = img[y:y+h, x:x+w]
                
                # Save the cropped face in the captured_faces directory
                face_filename = f"face_{int(time.time())}.png"
                face_filepath = os.path.join(captured_faces_dir, face_filename)
                cv2.imwrite(face_filepath, face)
                print(f"Face detected and saved at: {face_filepath}")
        
        time.sleep(0.1)  # Small delay to prevent high CPU usage

if __name__ == "__main__":
    save_directory = "screenshots"
    os.makedirs(save_directory, exist_ok=True)
    
    screenshot_queue = Queue()
    stop_event = Event()
    
    # Start the screenshot capture thread
    capture_thread = Thread(target=capture_screen_continuously, 
                            args=(screenshot_queue, stop_event, save_directory))
    capture_thread.start()
    
    # Start the face detection thread
    process_thread = Thread(target=process_screenshots, 
                            args=(screenshot_queue, stop_event, save_directory))
    process_thread.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping threads...")
        stop_event.set()
        capture_thread.join()
        process_thread.join()
        print("Application stopped.")
