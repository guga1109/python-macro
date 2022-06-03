import tkinter
import threading
import keyboard
import time
import pyautogui
from tkinter import filedialog as fd

def recordMacro():
    print('Recording macro...')

    newThread = threading.Thread(target=watchKeyPress)
    newThread.daemon = True
    newThread.start()
   
    while newThread.is_alive():
        time.sleep(1)
        position = str(pyautogui.position().x) + ', ' + str(pyautogui.position().y)
        listBox.insert('end', position)

    print('Recording stopped...')

def watchKeyPress():
    while True:
        if (keyboard.read_key() == 'q'):
            stop = True
            break
        elif (keyboard.read_key() == 'c'):
            listBox.insert('end', 'click')

def startRecordingThread(event):
    recordingThread = threading.Thread(target=recordMacro)
    recordingThread.daemon = True
    recordingThread.start()

def startMoving():
    numberOfItens = listBox.size()

    while True:
        for n in range(0, numberOfItens):
            if listBox.get(n) == 'click':
                pyautogui.click()
                continue
            else:
                x, y = listBox.get(n).split(', ') 
                pyautogui.moveTo(int(x), int(y), 1)

def saveFile():
    fileName = fd.asksaveasfilename(defaultextension='.txt', filetypes=[('text files', '*.txt')], title='Choose filename')
    numberOfItens = listBox.size()

    with open(fileName, 'w') as f:
        for n in range(0, numberOfItens):
            f.write(listBox.get(n) + '\n')

    print('File saved succesfully!\n')

def loadFile():
    fileName = fd.askopenfilename(defaultextension='.txt', filetypes=[('text files', '*.txt')], title='Choose file')

    with open(fileName, 'r') as f:
        listBox.delete(0, listBox.size())
        for line in f.readlines():
            listBox.insert('end', line)

def configureWidow():  
    window = tkinter.Tk()
    window.title('Macro')
    window.geometry('700x350')
    window.attributes('-topmost', True)
    
    menu = tkinter.Menu(window)
    fileMenu = tkinter.Menu(menu)
    fileMenu.add_command(label='Save', command=saveFile)
    fileMenu.add_command(label='Load', command=loadFile)

    menu.add_cascade(label='File', menu=fileMenu)
   
    global listBox
    listBox = tkinter.Listbox(window, width= 700, height= 300)
    listBox.grid(row=1, column=0)
    optionsMenu = tkinter.Menu(menu)
    optionsMenu.add_command(label='Record', command=lambda: startRecordingThread(None))
    optionsMenu.add_command(label='Start', command=startMoving)

    menu.add_cascade(label='Options', menu=optionsMenu)

    window.config(menu=menu)

    return window

window = configureWidow()
window.mainloop()
