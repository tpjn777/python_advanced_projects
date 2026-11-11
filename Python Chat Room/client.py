import socket
import tkinter as tk
from threading import Thread

HOST = '127.0.0.1'
PORT = 9090


def receive():
    while True:
        try:
            msg = sock.recv(1024).decode("utf8")
        except OSError:
            break  # socket closed
        if not msg:
            break  # server closed the connection
        msg_list.insert(tk.END, msg)
        msg_list.yview(tk.END)


def send(event=None):
    msg = my_msg.get().strip()
    if not msg:
        return
    my_msg.set("")
    try:
        sock.send(msg.encode("utf8"))
    except OSError:
        print("Could not send message; connection closed")
        return

    if msg == "#quit":
        sock.close()
        window.destroy()


def on_quiting():
    my_msg.set("#quit")
    send()


window = tk.Tk()
window.title("Tkinter Chat Room")
window.configure(bg="blue")
window.protocol("WM_DELETE_WINDOW", on_quiting)

message_frame = tk.Frame(window, height=110, width=100, bg="white")
message_frame.pack()

my_msg = tk.StringVar()
my_msg.set("")

scroll_bar = tk.Scrollbar(message_frame)
msg_list = tk.Listbox(message_frame, height=20, width=70, bg="white",
                      yscrollcommand=scroll_bar.set)
scroll_bar.config(command=msg_list.yview)
scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
msg_list.pack(side=tk.LEFT, fill=tk.BOTH)

label = tk.Label(window, text="Enter the message", fg="yellow", font="Arial", bg="black")
label.pack()

entry_field = tk.Entry(window, textvariable=my_msg, fg="red", width=50)
entry_field.bind("<Return>", send)
entry_field.pack()

send_button = tk.Button(window, text="Send", font="Arial", fg="black", command=send)
send_button.pack()

quit_button = tk.Button(window, text="Quit", font="Arial", fg="black", command=on_quiting)
quit_button.pack()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

Thread(target=receive, daemon=True).start()

window.mainloop()