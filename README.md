# Python Keylogger with Audio, Clipboard, and Screenshot Capture

This project is a multi-functional keylogger built using Python. It captures:
- Keystrokes
- System & clipboard information
- Microphone audio
- Screenshots

All captured data is encrypted and optionally emailed.

## Features
- Records keystrokes and stores them in a log file
- Captures clipboard content
- Records microphone audio
- Takes a screenshot of the screen
- Sends all logs and screenshots via email
- Encrypts sensitive logs with Fernet

## Requirements
- Python 3.10+
- Modules:
  - `sounddevice`
  - `pynput`
  - `cryptography`
  - `scipy`
  - `Pillow`
  - `requests`
  - `pywin32`

Install all dependencies:
```bash
pip install -r requirements.txt
