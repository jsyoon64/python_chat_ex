"""Server for echo application."""

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

class Server:
    sock = socket(AF_INET,SOCK_STREAM)

    def __init__(self):
        self.sock.bind(('0.0.0.0',3000))
        self.sock.listen(1)

    #def ByteToStr(self, bytestr):
    #    return ''.join(chr(x) for x in bytestr)
    #
    #  그냥 bytestr.decode("utf-8")로 하면 됨
    #
    def handler(self, c, a):
        data = c.recv(1024)
        c.send(data)
        c.close()
        print("Model:"+data[0:6].decode("utf-8"), "ID:"+data[6:10].decode("utf-8"), end=" ")
        print("OP:0x{}".format(data[10]), "Dev:0x{}".format(data[11]), "Type:0x{}".format(data[12]), end=" ")
        if(data[13] != 0):
            print(data[14:].decode("utf-8"))
        else:
            print("HeartBeat")

    def run(self):
        while True:
            client, client_addr = self.sock.accept()
            cThread = Thread(args=(client, client_addr) , target=self.handler)
            cThread.daemon = True
            cThread.start()
            print(str(client_addr[0]) + ':' + str(client_addr[1]), ":", end='')

server = Server()

#ACCEPT_THREAD = Thread(target=server.run())
# 위처럼 하면 안됨
ACCEPT_THREAD = Thread(target=server.run)

ACCEPT_THREAD.start()
ACCEPT_THREAD.join()
server.sock.close()
