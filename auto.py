import tkinter as tk
import pyautogui
import keyboard
import threading
import time

# Function to simulate typing
def auto_type_code(code: str, typing_speed: float):
    """Simulate typing the provided code with a typing speed interval in the active window."""
    pyautogui.typewrite(code, interval=typing_speed)  # interval controls typing speed

# Function to wait for the shortcut key and start typing when pressed
def wait_for_trigger_key(trigger_key: str, code: str, typing_speed: float):
    """Wait for the trigger key and then start typing the code in the active window."""
    print(f"Press {trigger_key} to start typing...")
    keyboard.wait(trigger_key)  # Wait for the trigger key (Numpad1)
    print(f"'{trigger_key}' pressed! Starting to type...")
    time.sleep(0.5)  # A short delay before typing begins
    auto_type_code(code, typing_speed)  # Start typing the code

# Function to be executed in a separate thread to allow key listening in the background
def start_typing_thread(trigger_key: str, code: str, typing_speed: float):
    """Start the typing process in a new thread to avoid blocking the GUI."""
    typing_thread = threading.Thread(target=wait_for_trigger_key, args=(trigger_key, code, typing_speed))
    typing_thread.daemon = True  # Daemon thread will close when the main program exits
    typing_thread.start()

# Main function for the GUI
def create_gui():
    # Create the main window
    window = tk.Tk()
    window.title("Auto Typer")

    # Create a text box where users can paste code
    label = tk.Label(window, text="Paste your code here:")
    label.pack(padx=10, pady=5)

    text_box = tk.Text(window, height=10, width=50)
    text_box.pack(padx=10, pady=5)

    # Create an entry box for typing speed (seconds between keystrokes)
    label_speed = tk.Label(window, text="Typing speed (seconds between keys):")
    label_speed.pack(padx=10, pady=5)

    speed_entry = tk.Entry(window)
    speed_entry.insert(0, "0.05")  # Default typing speed
    speed_entry.pack(padx=10, pady=5)

    # Set up a start button
    def start_typing():
        code = text_box.get("1.0", tk.END).strip()  # Get the code from the text box
        try:
            typing_speed = float(speed_entry.get())  # Get the typing speed
        except ValueError:
            typing_speed = 0.05  # Default to 0.05 if invalid input
        trigger_key = "s"  # The trigger key to start typing (Numpad1)
        start_typing_thread(trigger_key, code, typing_speed)

    start_button = tk.Button(window, text="Start Typing", command=start_typing)
    start_button.pack(padx=10, pady=20)

    # Run the Tkinter event loop
    window.mainloop()

if __name__ == "__main__":
    create_gui()
