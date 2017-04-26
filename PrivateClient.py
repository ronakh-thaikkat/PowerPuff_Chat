import tkinter as tk
import socket
from tkinter import *
portPrivate = 5556
class PrivateFrame(Frame):
    def __init__(self, master):
        super().__init__(master)

        # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # s.connect(('localhost', portPrivate))

        global memList
        global rootHome
        self.master.geometry("400x500")
        self.master.resizable(width=FALSE, height=FALSE)
        self.master.title("PowerPuff Chat Girls")

        #TextArea
        self.ChatLog = Text(self, bd=0, bg="light grey", height="13", width="55", font="Arial")
        self.ChatLog.insert(END, 'Welcome to the Private PowerPuff Chat')
        self.ChatLog.config(state=DISABLED)
        self.ChatLog.tag_config('INIT', foreground='red', justify=CENTER)
        self.ChatLog.tag_config('BLUE', foreground='blue', justify=LEFT)
        self.ChatLog.tag_config('BLK', foreground='black', justify=RIGHT)

        #ScrollBar
        self.scrollbar = Scrollbar(self, command = self.ChatLog.yview, cursor="heart")
        self.ChatLog['yscrollcommand'] = self.scrollbar.set

        #EntryBox
        self.EntryBox = Text(self, bg="white", width="29", height="5", font="Arial")
        self.EntryBox.bind("<KeyRelease-Return>", lambda event: sendData(self.EntryBox.get(1.0, END)))

        #SendButton
        self.SendButton = Button(self, font=30, text="Send", width="11", height=1,
                            bg="white", fg='navy blue', activebackground="#FACC2E",  command=lambda: sendData(self.EntryBox.get(1.0, END)))

        #Place them on Screen
        self.scrollbar.place(x=380, y=6, height=386)
        self.ChatLog.place(x=8, y=6, height=405, width=370)
        self.EntryBox.place(x=128, y=425, height=60, width=248)
        self.SendButton.place(x=6, y=425, height=60)

        def sendData(param):
            if param == '\n\n':
                self.EntryBox.delete(1.0, END)
                return
            if len(param) > 1:
                if '\n\n' in param:
                    # strip both the carriage return and appened with only one.
                    param = param.rstrip('\n')
                    param = param + '\n'
                self.EntryBox.delete(1.0, END)
                insertText(1, '>>' + param)
                # s.sendall(str.encode(param))
                # data = s.recv(4500)
                # if 'privateInit' in data.decode('utf-8'):
                #     pass
                #
                # insertText(2, '>>' + data.decode('utf-8'))
                # self.ChatLog.see(END)  # this shows the END of the chatlog; auto scroll down

        def insertText(num, param):
            self.ChatLog.config(state=NORMAL)
            if num == 1:
                self.ChatLog.insert(END, param, 'BLK')
            else:
                self.ChatLog.insert(END, param, 'BLUE')
            self.ChatLog.config(state=DISABLED)