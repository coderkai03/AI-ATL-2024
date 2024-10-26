import pyautogui
import os
import time

def capture_screen_continuously(save_directory=None, interval=1):
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
        while True:
            # Capture the screenshot
            screenshot = pyautogui.screenshot()
            
            # Save the screenshot
            screenshot.save(filepath)
            
            print(f"Screenshot saved at: {filepath}")
            time.sleep(interval)

    except KeyboardInterrupt:
        print("Screen capture stopped.")
    except Exception as e:
        print(f"An error occurred while capturing the screen: {e}")

if __name__ == "__main__":
    # Example usage:
    # Continuously capture and save the screenshot in the current directory
    capture_screen_continuously()

    # To specify a different directory and capture interval, uncomment and modify the line below:
    # capture_screen_continuously(save_directory="path/to/save", interval=0.5)