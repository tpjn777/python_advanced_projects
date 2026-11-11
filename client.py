import tkinter
import socket
from tkinter import *
from threading import Thread

def receive():
    while True:
        try:
            msg = sock.recv(1024).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except:
            print("There is an Error Receiving the message")

def send():
    msg = my_msg.get()
    my_msg.set("")
    sock.send(bytes(msg,"utf8"))

    if msg =='#quit':
        sock.close()
        window.close()


def on_quiting():
    msg = my_msg.set("#quit")

window = Tk()
window.title("tinker Chat Room")
window.configure(bg="blue")

message_frame= Frame(window, height=110, width=100, bg='white')
message_frame.pack()

my_msg=StringVar()
my_msg.set("")

scroll_bar = Scrollbar(message_frame)
msg_list = Listbox(message_frame, height=20, width=70, bg="white",yscrollcommand=scroll_bar.set)
scroll_bar.pack(side=RIGHT, fill=Y)
msg_list.pack(side=LEFT, fill=BOTH)
msg_list.pack()

label = Label(window, text="Enter the message", fg="yellow", font ='Aeria', bg='black' )
label.pack()

entry_field= Entry(window, textvariable=my_msg,fg='red', width=50)
entry_field.pack()

send_button = Button(window, text="send", font="Aerial", fg='white',command=send)
send_button.pack()

quit_button = Button(window, text="send", font="Aerial", fg='white',command=on_quiting)
quit_button.pack()

Host = '127.0.0.1'
Port=3000

sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((Host, Port))


receive_Thread = Thread(target=receive)
receive_Thread.start()