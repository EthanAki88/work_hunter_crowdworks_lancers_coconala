# Windows Notification System

A Python script that provides multiple ways to send notifications on Windows.

## Features

- **Multiple notification methods**: Supports win10toast, winotify, and Windows API
- **Auto-detection**: Automatically finds the best available notification method
- **Command line interface**: Easy to use from command line
- **Demo mode**: Built-in demonstration of different notification types
- **No dependencies required**: Windows API method works without external libraries

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

Or install individual packages:
```bash
pip install win10toast
pip install winotify
```

## Usage

### 1. Run Demo (Recommended for first use)
```bash
python main.py
```

This will run a demonstration showing different types of notifications.

### 2. Command Line Usage
```bash
# Basic notification
python main.py "Title" "Message"

# Specify notification method
python main.py "Title" "Message" "winotify"
python main.py "Title" "Message" "win10toast"
python main.py "Title" "Message" "windows_api"
```

### 3. Programmatic Usage
```python
from main import send_notification

# Send a simple notification
send_notification("Hello!", "This is a test message")

# Send with specific method
send_notification("Reminder", "Time for a break!", method="winotify", duration=10)
```

## Available Methods

### 1. winotify (Recommended)
- Modern Windows 10/11 toast notifications
- Supports custom icons and audio
- Non-blocking notifications
- Install: `pip install winotify`

### 2. win10toast
- Traditional Windows 10 toast notifications
- Simple and reliable
- Install: `pip install win10toast`

### 3. Windows API (Built-in)
- Uses Windows MessageBox
- No external dependencies required
- Blocking (user must click OK)
- Works on all Windows versions

## Examples

### Time-based Reminder
```python
from main import send_notification
from datetime import datetime

current_time = datetime.now().strftime("%H:%M:%S")
send_notification("Current Time", f"The time is: {current_time}")
```

### Error Notification
```python
send_notification("Error Alert", "Something went wrong! Please check the logs.")
```

### Long-duration Reminder
```python
send_notification("Break Time", "Don't forget to take a break!", duration=30)
```

## Troubleshooting

### Notifications not appearing?
1. Check Windows notification settings
2. Ensure "Focus Assist" is not blocking notifications
3. Try different notification methods

### Import errors?
- Install required packages: `pip install win10toast winotify`
- The Windows API method works without any external dependencies

### Permission issues?
- Run as administrator if needed
- Check Windows security settings

## Notes

- The script automatically tries the best available notification method
- Toast notifications are non-blocking and appear in the notification area
- Windows API notifications are blocking and require user interaction
- Duration parameter only applies to toast notifications (win10toast/winotify) 