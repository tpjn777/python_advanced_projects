import socket
import sys
import tkinter as tk
from threading import Thread

HOST = '127.0.0.1'
PORT = 9090

# Name comes from the command line: python client2.py Sara
# If it's missing, ask in the terminal.
name = sys.argv[1] if len(sys.argv) > 1 else input("Your name: ").strip()
if not name:
    name = "Guest"


def receive():
    while True:
        try:
            msg = sock.recv(1024).decode("utf8")
        except OSError:
            break
        if not msg:
            break
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
        return

    if msg == "#quit":
        sock.close()
        window.destroy()


def on_quiting():
    my_msg.set("#quit")
    send()


window = tk.Tk()
window.title(f"Chat Room - {name}")
window.configure(bg="blue")
window.protocol("WM_DELETE_WINDOW", on_quiting)

message_frame = tk.Frame(window, bg="white")
message_frame.pack()

my_msg = tk.StringVar()

scroll_bar = tk.Scrollbar(message_frame)
msg_list = tk.Listbox(message_frame, height=20, width=70, bg="white",
                      yscrollcommand=scroll_bar.set)
scroll_bar.config(command=msg_list.yview)
scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
msg_list.pack(side=tk.LEFT, fill=tk.BOTH)

tk.Label(window, text="Enter the message", fg="yellow", bg="black",
         font="Arial").pack()

entry_field = tk.Entry(window, textvariable=my_msg, fg="red", width=50)
entry_field.bind("<Return>", send)
entry_field.pack()
entry_field.focus()

tk.Button(window, text="Send", font="Arial", command=send).pack()
tk.Button(window, text="Quit", font="Arial", command=on_quiting).pack()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
sock.send(name.encode("utf8"))  # register with the server automatically

Thread(target=receive, daemon=True).start()

window.mainloop()