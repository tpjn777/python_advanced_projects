import socket
from threading import Thread, Lock

HOST = 'localhost'
PORT = 9090

clients = {}
addresses = {}
lock = Lock()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((HOST, PORT))


def broadcast(msg, prefix=""):
    """Send msg (bytes) to every connected client, with an optional text prefix."""
    data = prefix.encode("utf8") + msg
    with lock:
        targets = list(clients)
    for c in targets:
        try:
            c.send(data)
        except OSError:
            pass  # that client is gone; its own thread will clean up


def handle_clients(conn, address):
    try:
        name = conn.recv(1024).decode("utf8").strip()
        if not name:
            return

        welcome = f"Welcome {name}. You can type #quit if you ever want to leave the Chat Room"
        conn.send(welcome.encode("utf8"))

        with lock:
            clients[conn] = name
        broadcast(f"{name} has recently joined the Chat Room".encode("utf8"))

        while True:
            msg = conn.recv(1024)
            if not msg or msg == b"#quit":
                break
            broadcast(msg, name + ": ")
    except OSError:
        pass
    finally:
        with lock:
            name = clients.pop(conn, None)
            addresses.pop(conn, None)
        try:
            conn.send(b"#quit")
        except OSError:
            pass
        conn.close()
        if name:
            broadcast(f"{name} has left the Chat Room".encode("utf8"))


def accept_client_connections():
    while True:
        client_conn, client_address = sock.accept()
        print(client_address, "has connected successfully")
        client_conn.send("Welcome to the Chat, please type your name to continue".encode("utf8"))
        with lock:
            addresses[client_conn] = client_address
        Thread(target=handle_clients, args=(client_conn, client_address), daemon=True).start()


if __name__ == "__main__":
    sock.listen(5)
    print("The server is running and listening for client requests")

    t1 = Thread(target=accept_client_connections)
    t1.start()
    t1.join()