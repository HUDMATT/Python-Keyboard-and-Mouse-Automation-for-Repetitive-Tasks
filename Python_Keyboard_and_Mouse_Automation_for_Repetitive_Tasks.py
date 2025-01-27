from pynput.mouse import Listener as MouseListener, Button, Controller as MouseController
from pynput.keyboard import Listener as KeyboardListener, Key, Controller as KeyboardController
import time
import threading
import sys

mouse = MouseController()
keyboard = KeyboardController()

actions = []
recording = False
stop_flag = False

print("\n\n\nThis program will record any keyboard and mouse actions you perform to automate repetitive tasks\n\nTo start recording press F9\n\nTo stop recording press F9\n\nTo replay actions press F10\n\nTo stop performing recorded actions press 'esc'\n")

def on_click(x, y, button, pressed):
    global recording
    if recording:
        action = ('click', (x, y), button.name, pressed)
        actions.append(action)
        print(f"Recorded action: {action}")

def on_press(key):
    global stop_flag, recording
    if key == Key.esc:
        print("Exiting program...")
        sys.exit()  # Exit the program
    elif key == Key.f9:
        recording = not recording
        if recording:
            print("Recording started. Perform the actions you want to record.")
            time.sleep(0.5)  # Small delay to avoid recording the F9 key release
        else:
            print("Recording stopped.")
    elif key == Key.f10:
        print("Starting to perform recorded actions...")
        time.sleep(0.5)  # Small delay to avoid recording the F10 key press
        perform_actions(actions)
    else:
        if recording:
            action = ('press', key.char if hasattr(key, 'char') else key.name)
            actions.append(action)
            print(f"Recorded action: {action}")

def on_release(key):
    if recording:
        action = ('release', key.char if hasattr(key, 'char') else key.name)
        actions.append(action)
        print(f"Recorded action: {action}")

def perform_actions(actions):
    global stop_flag
    while not stop_flag:
        for action in actions:
            if stop_flag:
                break
            if action[0] == 'click':
                _, (x, y), button, pressed = action
                mouse.position = (x, y)
                if pressed:
                    mouse.press(Button[button])
                else:
                    mouse.release(Button[button])
            elif action[0] == 'press':
                _, key = action
                keyboard.press(Key[key] if key in Key.__members__ else key)
            elif action[0] == 'release':
                _, key = action
                keyboard.release(Key[key] if key in Key.__members__ else key)
            time.sleep(0.1)  # Small delay between actions
    print("Program stopped")

def start_listeners():
    with MouseListener(on_click=on_click) as mouse_listener, KeyboardListener(on_press=on_press, on_release=on_release) as keyboard_listener:
        mouse_listener.join()
        keyboard_listener.join()

# Start the listeners in a separate thread
listener_thread = threading.Thread(target=start_listeners)
listener_thread.start()

# Main loop to check for stop_flag
while True:
    if stop_flag:
        break
    time.sleep(0.1)



