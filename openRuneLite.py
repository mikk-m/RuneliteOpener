import subprocess
import time
import pygetwindow as gw
import pyautogui


def wait_for_new_window(title, moved_windows, timeout=20):
    # Wait for a new window with the title
    start_time = time.time()
    while time.time() - start_time < timeout:
        windows = gw.getWindowsWithTitle(title)
        for window in windows:
            if window not in moved_windows:
                return window
        time.sleep(1)
    return None

def focus_window(window):
    # Bring the window to the foreground and focus on it
    if window:
        window.activate()
        time.sleep(1)
        # Click within the window to focus it
        x, y = window.topleft
        pyautogui.click(x + 10, y + 10)

def resize_and_position_window(window, screen_width, screen_height, position, taskbar_height):
    if window:
        focus_window(window)
        new_width = int(screen_width * 0.5 * 1.05)
        new_height = int(screen_height * 0.5 * 1.05)
        window.resizeTo(new_width, new_height)

        x, y = position
        if x == 'right':
            # Adjust for the invisible edge on the right side
            new_x = screen_width - new_width + 10
        else:
            new_x = -10

        if y == 'bottom':
            new_y = screen_height - new_height - taskbar_height + 10
        else:
            new_y = -10 

        window.moveTo(new_x, new_y)
    else:
        print("Window not found.")


def open_exe(num, exe_path, window_title, screen_width, screen_height, positions, taskbar_height):
    moved_windows = []
    for i in range(num):
        subprocess.Popen(exe_path)
        time.sleep(10)  # Launcher load time, can be edited

        window = wait_for_new_window(window_title, moved_windows)
        if window:
            moved_windows.append(window)
            if i < len(positions):
                resize_and_position_window(window, screen_width, screen_height, positions[i], taskbar_height)

def main():
    exe_path = "" # Path to your runelite executable
    num = int(input("How many instances do you want to open? "))
    
    window_title = "RuneLite"

    screen_width, screen_height = 2560, 1440 # Change per your resolution
    taskbar_height = 40

    positions = [('right', 'top'), ('right', 'bottom'), ('left', 'bottom'), ('left', 'top')]

    open_exe(num, exe_path, window_title, screen_width, screen_height, positions, taskbar_height)

if __name__ == "__main__":
    main()
