import socket
import threading

HOST = 'localhost'
PORT = 45555

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
    server.bind((HOST,PORT))
except socket.error as e:
    print(str(e))

server.listen()

clients,names= [],[]

def broadcast(msg):
    for client in clients:
        client.send(msg)

def handle(client):
    while True:
        try:
            msg = client.recv(1024)
            print(f'{names[clients.index(client)]} has sent a msg')
            broadcast(msg)
        except:
            target_index = clients.index(client)
            clients.remove(client)
            client.close()
            rname = names[target_index]
            names.remove(rname)
            break

def receive():
    while True:

        client,address = server.accept()
        print(f"connected with {address[0]} : {address[1]}!")

        client.send('NAME:'.encode('utf-8'))
        name = client.recv(1024)

        names.append(name)
        clients.append(client)

        print(f"{name} connected the server")

        broadcast(f"{name} connected the chat \n".encode('utf-8'))
        client.send('connected to the chat'.encode('utf-8'))

        thread = threading.Thread(target=handle,args=(client,))
        thread.start()

print('--->  WAITING FOR CONNECTIONS.....')
receive()


