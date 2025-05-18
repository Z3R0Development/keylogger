from pynput import keyboard
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from sys import argv
import pygetwindow as gw
import datetime, random

def currentTime(format=None):
    time = datetime.datetime.now()
    h = time.hour
    m = time.minute

    if format is None:
        return f"{h:02}:{m:02}"
    if format == 'int':
        return int(h),int(m)
    if format == 'date':
        tmp = time.strftime("%Y")+'.'+time.strftime("%m")+'.'+time.strftime("%d")
        return tmp
    if format == 'datetime':
        tmp = time.strftime("%Y")+'.'+time.strftime("%m")+'.'+time.strftime("%d")+' - '+f"{h:02}:{m:02}"
        return tmp
    
def futureTime(interval, format=None):
    tmpH,tmpM = currentTime('int')
    tmpM += int(interval)

    totalMin = tmpH * 60 + tmpM
    tmpH = (totalMin // 60) % 24
    tmpM = totalMin % 60
    
    if format is None:
        return f"{tmpH:02}:{tmpM:02}"
    if format == 'int':
        return [tmpH,tmpM]
    
def checkFlag(timeArr):
    tmpH, tmpM = currentTime('int')
    futureH = timeArr[0]
    futureM = timeArr[1]

    currentMins = tmpH * 60 + tmpM
    futureMins = futureH * 60 + futureM
    if futureMins < currentMins: futureMins+=24*60

    return currentMins >= futureMins

def genStr(len):
    dict = 'abcdefghijklmnopqrstuvwxyz1234567890()-_,.'
    tmp = ''
    for i in range(int(len)):
        tmp += random.choice(dict)
    return tmp + '.cfd'

def save(data):
    dt = currentTime('datetime')
    title = genStr(16)
    imprinted = dt + '\n' + data
    encoded,key,iv = encryptAES(imprinted.encode())

    with open(title, 'wb') as f:
        f.write(iv)
        f.write(key)
        f.write(encoded)
    f.close()

def readLog():
    with open(argv[1],'rb') as f:
        iv = f.read(16)
        key = f.read(16)
        ciphertext = f.read()
    print(decryptAES(ciphertext,key,iv))

def encryptAES(data):
    padded = pad(data,16)
    key = get_random_bytes(16)
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(padded)
    return ciphertext,key,iv

def decryptAES(data,key,iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    message = cipher.decrypt(data)
    return message.decode()