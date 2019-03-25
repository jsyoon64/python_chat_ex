from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

def send(event=None):  # event is passed by binders.
    window = tkinter.Toplevel(top)
    id_button = tkinter.Button(top, text="test_id")
    button2 = tkinter.Button(top, text="Send", command=send)
    button2.pack()


def on_closing(event=None):
    pass


top = tkinter.Tk()
top.title("Chatter")
#top.protocol("WM_DELETE_WINDOW", on_closing)

button1 = tkinter.Button(top, text="Send", command=send)
button1.pack()

tkinter.mainloop()  # Starts GUI execution.