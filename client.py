import socket

host='localhost'
port=9090

sock=socket.socker(socket.AF_INET, socket.SOCK_STREAM)
sock.connet((host,port))

message = sock.recv(1024)

while message:
    print("message:" , message.decode)
    message=sock.recv(1024)
    
sock.close()

