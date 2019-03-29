"""Server for pd application."""

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import pickle
import sys

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
        self.sock.bind(('0.0.0.0',3000))
        self.sock.listen(1)

    def StatusSet(self,id, val):
        global clientLists
        #global clientLists
        #value_when_true if condition else value_when_false
        if(id in clientLists):
            clientLists[id]['PA'] = 1 if ((val & fieldPA) == fieldPA) else 0
            clientLists[id]['PB'] = 1 if ((val & fieldPB) == fieldPB) else 0
            clientLists[id]['LED'] = 1 if ((val & fieldLED) == fieldLED) else 0
            clientLists[id]['STYLE'] = (val & fieldSTYLE) >> 5

    def handler(self, c, a):
        global clientLists, def_control, ctrClients
        id = ''

        while True:
            try:
                data = c.recv(1024)
                #print(len(data), data)
                if(len(data) < 13):
                    continue
            except:
                if(id !=''):
                    del clientLists[id]
                break
            else:
                if not data:
                    sys.exit()
                    break
                else :
                    id = data[6:10].decode("utf-8")
                    if(id not in clientLists):
                        clientLists[id] = def_control['PDxx'].copy()

                    # 응답 part이므로 제어 메시지 송신 부분
                    if(clientLists[id]['CTR'] == 'X'):
                        c.send(data)
                    else:
                        c.send(clientLists[id]['CTR'])
                        clientLists[id]['CTR'] = 'X'
                    #c.close()

                    data1 = pickle.dumps(clientLists)
                    for sock1 in ctrClients:
                        #print(sock1)
                        sock1.send(data1)

                    self.StatusSet(id, data[10])
                    print("Model:"+data[0:6].decode("utf-8"), "ID:"+ id, end=" ")
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
        # 함수 내에서 global 변수를 접근 하는 경우 정확하게 명시 필요
        # 즉 local 변수가 아니라는
        global ctrClients

        while True:
            try:
                data = c.recv(1024)
            except:
                ctrClients.clear()
                sys.exit()
                break
            else:
                if not data:
                    ctrClients.clear()
                    break
                # 제어 값 수신 처리 필요
                #print(data.decode("utf-8"))
                #print(data[0:10].decode("utf-8"))
                clientLists['PD01']['CTR'] = data

    def run(self):
        global ctrClients
        while True:
            client, client_addr = self.sock.accept()
            ctrClients[client] = client_addr[0]
            cThread = Thread(args=(client, client_addr) , target=self.handler)
            #cThread.daemon = True
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
