#!/usr/bin/env python3
"""
Windows Notification System
Provides multiple ways to send notifications on Windows
"""

import time
import sys
from datetime import datetime

def send_notification_win10toast(title, message, duration=5):
    """
    Send notification using win10toast library
    Requires: pip install win10toast
    """
    try:
        from win10toast import ToastNotifier
        toaster = ToastNotifier()
        toaster.show_toast(title, message, duration=duration, threaded=True)
        print(f"Notification sent via win10toast: {title} - {message}")
        return True
    except ImportError:
        print("win10toast not installed. Install with: pip install win10toast")
        return False
    except Exception as e:
        print(f"Error sending notification with win10toast: {e}")
        return False

def send_notification_winotify(title, message, duration=5):
    """
    Send notification using winotify library
    Requires: pip install winotify
    """
    try:
        from winotify import Notification, audio
        toast = Notification(
            app_id="Python Notification",
            title=title,
            msg=message,
            duration=str(duration),
            icon=""
        )
        toast.set_audio(audio.Default, loop=False)
        toast.show()
        print(f"Notification sent via winotify: {title} - {message}")
        return True
    except ImportError:
        print("winotify not installed. Install with: pip install winotify")
        return False
    except Exception as e:
        print(f"Error sending notification with winotify: {e}")
        return False

def send_notification_windows_api(title, message):
    """
    Send notification using Windows API (ctypes)
    No external dependencies required
    """
    try:
        import ctypes
        from ctypes import wintypes
        
        # Load the Windows API
        user32 = ctypes.windll.user32
        kernel32 = ctypes.windll.kernel32
        
        # Define the MessageBox function
        MessageBoxW = user32.MessageBoxW
        MessageBoxW.argtypes = [wintypes.HWND, wintypes.LPCWSTR, wintypes.LPCWSTR, wintypes.UINT]
        MessageBoxW.restype = wintypes.INT
        
        # Show the message box
        result = MessageBoxW(None, message, title, 0x40)  # 0x40 = MB_ICONINFORMATION
        print(f"Notification sent via Windows API: {title} - {message}")
        return True
    except Exception as e:
        print(f"Error sending notification with Windows API: {e}")
        return False

def send_notification(title, message, method="auto", duration=5):
    """
    Send notification using the specified method or auto-detect the best available
    
    Args:
        title (str): Notification title
        message (str): Notification message
        method (str): "win10toast", "winotify", "windows_api", or "auto"
        duration (int): Duration in seconds (for toast notifications)
    """
    if method == "auto":
        # Try winotify first (more modern), then win10toast, then Windows API
        if send_notification_winotify(title, message, duration):
            return True
        elif send_notification_win10toast(title, message, duration):
            return True
        else:
            return send_notification_windows_api(title, message)
    elif method == "win10toast":
        return send_notification_win10toast(title, message, duration)
    elif method == "winotify":
        return send_notification_winotify(title, message, duration)
    elif method == "windows_api":
        return send_notification_windows_api(title, message)
    else:
        print(f"Unknown method: {method}")
        return False

def demo_notifications():
    """Demonstrate different types of notifications"""
    print("=== Windows Notification Demo ===\n")
    
    # Test 1: Simple notification
    print("1. Sending simple notification...")
    send_notification("Hello!", "This is a test notification from Python!")
    time.sleep(2)
    
    # Test 2: Time-based notification
    print("\n2. Sending time-based notification...")
    current_time = datetime.now().strftime("%H:%M:%S")
    send_notification("Current Time", f"The current time is: {current_time}")
    time.sleep(2)
    
    # Test 3: Reminder notification
    print("\n3. Sending reminder notification...")
    send_notification("Reminder", "Don't forget to take a break!", duration=10)
    time.sleep(2)
    
    # Test 4: Error notification
    print("\n4. Sending error notification...")
    send_notification("Error Alert", "Something went wrong! Please check the logs.")
    time.sleep(2)
    
    print("\n=== Demo completed ===")

def main():
    """Main function to handle command line arguments or run demo"""
    if len(sys.argv) > 1:
        # Command line usage: python main.py "Title" "Message" [method]
        title = sys.argv[1]
        message = sys.argv[2] if len(sys.argv) > 2 else "No message provided"
        method = sys.argv[3] if len(sys.argv) > 3 else "auto"
        
        success = send_notification(title, message, method)
        if not success:
            print("Failed to send notification with any available method")
    else:
        # Run demo if no arguments provided
        demo_notifications()

if __name__ == "__main__":
    main() 