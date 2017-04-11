from tkinter import *
import tkinter.messagebox as tm


username = ''
check = 0
# ------------Class for the login here. -


class LoginFrame(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.label_1 = Label(self, text= "Enter your name : ")
        self.entry_1 = Entry(self)
        self.label_1.grid(row = 3 , sticky=E)
        self.entry_1.grid(row=3, column=1)
        self.checkbox = Checkbutton(self, text="I am human", variable = var)
        self.checkbox.grid(columnspan=2)
        self.logbtn = Button(self, text="Login", command = self._login_btn_clicked)
        self.logbtn.grid(columnspan=2)
        self.pack()

    def _login_btn_clicked(self):
        global username, check
        username = self.entry_1.get()
        username = username.rstrip(' ')
        if(var.get() and len(username) >= 3):
            check = 1
            root.destroy()
        else:
            if(len(username) < 3 and not var.get()):
                tm._show('Nope', 'can\'t let u in sry')
            elif(len(username) < 3):
                tm._show('Error', 'len(name) should be > 3')
            else:
                tm._show('Error', 'prove to us u r human. pls')

root = Tk()
root.title('Login - PowerPuff Chat : Where life happens')
var = IntVar()
root.geometry("400x500")
root.resizable(width=FALSE, height=FALSE)
lf = LoginFrame(root)
root.mainloop()

# -------After login checked, the chat box starts from here.
username = username.title()
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost',5555))
s.sendall(str.encode('initSecName:'+ username))

def sendData(param):
    if param == '\n\n':
        EntryBox.delete(1.0,END)
        return
    if len(param) > 1:
        if '\n\n' in param:
            #strip both the carriage return and appened with only one.
            param =  param.rstrip('\n')
            param = param + '\n'
        EntryBox.delete(1.0, END)
        insertText(1, '>>' + param)
        s.sendall(str.encode(param))
        data = s.recv(4500)
        insertText(2, '>>' + data.decode('utf-8'))
        ChatLog.see(END)                  #this shows the END of the chatlog; auto scroll down

def insertText(num, param):
    ChatLog.config(state = NORMAL)
    if num == 1:
        ChatLog.insert(END, param, 'BLK')
    else:
        ChatLog.insert(END, param,'BLUE')
    ChatLog.config(state = DISABLED)

if check == 1:
    base = Tk()
    base.title('PowerPuff Chat Girls')
    base.geometry("400x500")
    base.resizable(width=FALSE, height=FALSE)

    #Create a Chat window
    ChatLog = Text(base, bd=0, bg="light grey", height="13", width="55", font="Arial",)
    ChatLog.insert(END, 'Welcome to the PowerPuff Chat, ' + username + '\n', 'INIT')   # THIS IS HERE <-----------------
    ChatLog.config(state = DISABLED)
    ChatLog.tag_config('INIT', foreground = 'red', justify = CENTER)
    ChatLog.tag_config('BLUE', foreground = 'blue', justify = LEFT)
    ChatLog.tag_config('BLK', foreground = 'black', justify = RIGHT)

    #Bind a scrollbar to the Chat window
    scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
    ChatLog['yscrollcommand'] = scrollbar.set

    #Create the box to enter message
    EntryBox = Text(base, bg="white",width="29", height="5", font="Arial")
    EntryBox.bind("<KeyRelease-Return>", lambda event: sendData(EntryBox.get(1.0, END)))

    #Create the Button to send message
    SendButton = Button(base, font=30, text="Send", width="11", height= 1,
                         bg="white", fg = 'navy blue', activebackground="#FACC2E", command=lambda: sendData(EntryBox.get(1.0, END)))

    #Place all components on the screen
    scrollbar.place(x=380,y=6, height=386)
    ChatLog.place(x=8, y=6, height=405, width=370)
    EntryBox.place(x=128, y=425, height=60, width=248)
    SendButton.place(x=6, y=425, height=60)

    base.mainloop()
