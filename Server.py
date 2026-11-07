import socket
from threading import Thread

host = 'localhost'
port=9090

clients={}
addresses={}

sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))


def handle_clients(conn,address):

    name = conn.recv(1024).decode()
    welcome = "Welcome "+name+". You can type #quit if you ever want to leave the Chat Room"
    conn.recv(bytes(welcome, "utf8"))
    msg = name + "Has Recently joined the Chat Room"
    broadcast(bytes(msg, "utf8"))
    clients[conn]=name

    while True :

        msg = conn.recv(1024)
        if msg!=bytes("#quit", "utf8"):
            broadcast(msg, name+":")

        else:
            conn.send(bytes("#quit", "utf8"))
            conn.close()
            del clients[conn]
            broadcasts(bytes(name +"Has Left the CHat Room"))


def accept_client_connections():

    while True:
        client_conn,client_address= sock.accept()
        print(client_address," Has connected succefully ")
        client_conn.send("Welcome te the Chaty, Please type ypur name to continue".encode('utf8'))
        addresses[client_conn]=client_address

        Thread(target=handle_clients,args=(client_conn, client_address)).start()



if __name__=="__main__":
    sock.listen(5)
    print("The serve is running and is listening to clients requests")

    t1 = Thread(target=accept_client_connections)
    t1.start()
    t1.join()

