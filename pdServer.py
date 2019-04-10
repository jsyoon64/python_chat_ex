"""Server for pd application."""

from socket import AF_INET, socket, SOCK_STREAM
import select
import threading
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
                ready_to_read, ready_to_write, in_error = \
                    select.select([c, ], [c, ], [], 2)
            except select.error:
                c.shutdown(2) # 0 = done receiving, 1 = done sending, 2 = both
                c.close()
                break

            if len(ready_to_read) > 0:
                data = c.recv(1024)
                if not data:
                    c.shutdown(2)  # 0 = done receiving, 1 = done sending, 2 = both
                    c.close()
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
                    #print('3',ctrClients)
                    for sock1 in ctrClients:
                        #print(sock1)
                        sock1.send(data1)

                    self.StatusSet(id, data[10])
                    print(data[0:6].decode("utf-8"), id, end=" ")
                    print("OP:0x{:x}".format(data[10]), "Dev:0x{:x}".format(data[11]), "Type:0x{:x}".format(data[12]), end=" ")
                    if(data[13] != 0):
                        print(data[14:].decode("utf-8"))
                    else:
                        print("HeartBeat")

    def run(self):
        while True:
            client, client_addr = self.sock.accept()
            cThread = threading.Thread(args=(client, client_addr) , target=self.handler)
            #cThread.daemon = True
            cThread.start()
            print(str(threading.active_count())+','+str(client_addr[0]) + ':' + str(client_addr[1]), end=' ')

class CtrServer:
    sock = socket(AF_INET,SOCK_STREAM)

    def __init__(self):
        self.sock.bind(('0.0.0.0',3100))
        self.sock.listen(1)

    def handler(self, c, a):
        # 함수 내에서 global 변수를 접근 하는 경우 정확하게 명시 필요
        # 즉 local 변수가 아니라는
        global ctrClients

        while True:
            try:
                ready_to_read, ready_to_write, in_error = \
                    select.select([c, ], [c, ], [], 2)
            except select.error:
                del ctrClients[c]
                #print('1',ctrClients)
                c.shutdown(2) # 0 = done receiving, 1 = done sending, 2 = both
                c.close()
                break
            if len(ready_to_read) > 0:
                try:
                    data = c.recv(1024)
                except:
                    del ctrClients[c]
                    #print('2',ctrClients)
                    c.shutdown(2)  # 0 = done receiving, 1 = done sending, 2 = both
                    c.close()
                    break

                if not data:
                    del ctrClients[c]
                    #print('2',ctrClients)
                    c.shutdown(2)  # 0 = done receiving, 1 = done sending, 2 = both
                    c.close()
                    break
                else :
                    # 제어 값 수신 처리 필요
                    #print(data.decode("utf-8"))
                    #print(data[0:10].decode("utf-8"))
                    id = data[6:10].decode("utf-8")
                    if(id in clientLists.keys()):
                        clientLists[id]['CTR'] = data

    def run(self):
        global ctrClients
        while True:
            client, client_addr = self.sock.accept()
            ctrClients[client] = client_addr[0]
            cThread = threading.Thread(args=(client, client_addr) , target=self.handler)
            #cThread.daemon = True
            cThread.start()
            print('ctrServer '+str(client_addr[0]) + ':' + str(client_addr[1]), " connected!")


server = Server()
ctrserver = CtrServer()
ACCEPT_THREAD = threading.Thread(target=server.run)
ACCEPT_THREAD1 = threading.Thread(target=ctrserver.run)
ACCEPT_THREAD.start()
ACCEPT_THREAD1.start()
ACCEPT_THREAD.join()
ACCEPT_THREAD1.join()
server.sock.close()
CtrServer.sock.close()
