"""Server for pd application."""

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import pickle

def_control = {'PDxx':{'PA':0,'PB':0,'LED':0,'STYLE':0, 'CTR':'X'}}
clientLists = {}
ctrClients = {}
fieldPA = 0x01
fieldPB = 0x02
fieldLED = 0x10
fieldSTYLE = 0x60

class Server:
    sock = socket(AF_INET,SOCK_STREAM)

    def __init__(self):
        self.sock.bind(('0.0.0.0',4000))
        self.sock.listen(1)

    def StatusSet(self,id, val):
        #value_when_true if condition else value_when_false
        clientLists[id]['PA'] = 1 if ((val & fieldPA) == fieldPA) else 0
        clientLists[id]['PB'] = 1 if ((val & fieldPB) == fieldPB) else 0
        clientLists[id]['LED'] = 1 if ((val & fieldLED) == fieldLED) else 0
        clientLists[id]['STYLE'] = (val & fieldSTYLE) >> 5

    def handler(self, c, a):
        while True:
            data = c.recv(1024)
            if not data:
                break
            else :
                if(data[6:10].decode("utf-8") not in clientLists):
                    clientLists[data[6:10].decode("utf-8")] = def_control['PDxx'].copy()

                self.StatusSet(data[6:10].decode("utf-8"), data[10])

                # 응답 part이므로 제어 메시지 송신 부분
                if(clientLists[data[6:10].decode("utf-8")]['CTR'] == 'X'):
                    c.send(data)
                else:
                    c.send(bytes(clientLists[data[6:10].decode("utf-8")]['CTR'], 'utf-8'))
                    clientLists[data[6:10].decode("utf-8")]['CTR'] = 'X'
                #c.close()

                for sock in ctrClients:
                    data1 = pickle.dumps(clientLists)
                    sock.send(data1)

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
            print('Server '+str(client_addr[0]) + ':' + str(client_addr[1]), ":", end='')

class CtrServer:
    sock = socket(AF_INET,SOCK_STREAM)

    def __init__(self):
        self.sock.bind(('0.0.0.0',4100))
        self.sock.listen(1)

    def handler(self, c, a):
        while True:
            data = c.recv(1024)
            if not data:
                break

            # TODO
            # 제어 값 수신 처리 필요
            print(data.decode("utf-8"))
            #clientLists['PD01']['CTR'] = 'AAAAAAAAAAAA'

    def run(self):
        while True:
            client, client_addr = self.sock.accept()
            ctrClients[client] = client_addr[0]
            cThread = Thread(args=(client, client_addr) , target=self.handler)
            cThread.daemon = True
            cThread.start()
            print('ctrServer '+str(client_addr[0]) + ':' + str(client_addr[1]), ":", end='')


server = Server()
ctrserver = CtrServer()
ACCEPT_THREAD = Thread(target=server.run)
ACCEPT_THREAD1 = Thread(target=ctrserver.run)
ACCEPT_THREAD.start()
ACCEPT_THREAD1.start()
ACCEPT_THREAD.join()
ACCEPT_THREAD1.join()
server.sock.close()
CtrServer.sock.close()
