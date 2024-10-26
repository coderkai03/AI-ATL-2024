import pyautogui
import os
import time
import cv2
import numpy as np
from threading import Thread, Event
from queue import Queue
import face_recognition
import requests


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

def classify_faces(stop_event, save_directory):
    known_faces_dir = "./known_faces"
    captured_faces_dir = os.path.join(save_directory, "captured_faces")
    
    # Load known faces
    known_faces = []
    known_names = []
    for person_name in os.listdir(known_faces_dir):
        person_dir = os.path.join(known_faces_dir, person_name)
        if os.path.isdir(person_dir):
            for image_name in os.listdir(person_dir):
                image_path = os.path.join(person_dir, image_name)
                image = cv2.imread(image_path)
                rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                encodings = face_recognition.face_encodings(rgb_image)
                if encodings:
                    known_faces.append(encodings[0])
                    known_names.append(person_name)
    
    print(f"Loaded {len(known_faces)} known faces")
    
    while not stop_event.is_set():
        for filename in os.listdir(captured_faces_dir):
            if filename.endswith(".png"):
                face_path = os.path.join(captured_faces_dir, filename)
                face_image = cv2.imread(face_path)
                rgb_face = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
                face_encodings = face_recognition.face_encodings(rgb_face)
                
                if face_encodings:
                    matches = face_recognition.compare_faces(known_faces, face_encodings[0])
                    name = "Unknown"
                    
                    if True in matches:
                        first_match_index = matches.index(True)
                        name = known_names[first_match_index]
                    
                    print(f"Face in {filename} classified as: {name}")
                    url = 'https://magicloops.dev/api/loop/run/ac4ff616-19cb-48b3-9b77-8256af33232e'
                    params = {"name": name}
                    response = requests.get(url, params=params)
                    responseJson = response.json()
                    print(f"STATUS: {responseJson['status']}")
                    print(f"OUTPUT: {responseJson['loopOutput']}")
                    #TODO PLEASE ACTUALLY USE THE OUTPUT THX RIAN/BILL
                    # Move the classified face to a new directory
                    classified_dir = os.path.join(save_directory, "classified_faces", name)
                    os.makedirs(classified_dir, exist_ok=True)
                    new_path = os.path.join(classified_dir, filename)
                    os.rename(face_path, new_path)
                
                time.sleep(0.1)  # Small delay to prevent high CPU usage
        
        time.sleep(1)  # Check for new faces every second

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
    
    # Start the face classification thread
    classify_thread = Thread(target=classify_faces,
                             args=(stop_event, save_directory))
    classify_thread.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping threads...")
        stop_event.set()
        capture_thread.join()
        process_thread.join()
        classify_thread.join()
        print("Application stopped.")
