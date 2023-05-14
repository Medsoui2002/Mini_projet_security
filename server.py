from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s s'est connecté." % client_address)
        client.send(
            bytes("Salutations de la grotte! Tapez maintenant votre nom et appuyez sur Entrée !", "utf8"))
        addresses[client] = client_address
        HANDLE_THREAD = Thread(target=handle_client, args=(client,))
        HANDLE_THREAD.start()


def handle_client(client):
    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Bienvenu %s! Si jamais vous voulez quitter, tapez {quit} pour quitter.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s a rejoint la discussion!" % name
    broadcast(bytes(msg, "utf8"))
    clientsNames[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name+": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clientsNames[client]
            broadcast(bytes("%s à quitté la discussion." % name, "utf8"))
            break


def broadcast(msg, prefix=""):

    print("Tous les clients connectés: ",  clientsNames.values())
    for sock in clientsNames:
        print("sock: ", sock)
        sock.send(bytes(prefix, "utf8") + msg)


clientsNames = {}
addresses = {}
HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Attente de connexion...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()

    ACCEPT_THREAD.join()
    SERVER.close()
