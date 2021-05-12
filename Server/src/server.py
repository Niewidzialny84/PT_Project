import socket, threading, ssl
import os

from users import User
from logger import Logger


class UserContainer(object):
    def __init__(self):
        super().__init__()

        self.connections = []
        self.UUIDs = set()

    def add(self, user: User):
        self.connections.append(user)
        user.uuid = self.getID()
        
    def getID(self):
        for i in range(1000):
            if not self.UUIDs.issuperset(set([i])):
                self.UUIDs.add(i)
                return i

    def remove(self, user: User):
        self.connections.remove(user)
        self.UUIDs.remove(user.id)
    
    def remove(self, uuid: int):
        for x in self.connections:
            if x.id == uuid:
                self.remove(x)
                break
                

class Server(object):
    def __init__(self, ip: str, port: int):
        super().__init__()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((ip,port))

        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        self.context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
        self.context.set_ciphers('AES256+ECDH:AES256+EDH')
        self.context.load_cert_chain(certfile=str(os.path.dirname(os.path.abspath(__file__))+'/cert.pem'))

        self.innerAddr = self.sock.getsockname()

        self.running = True

        self.users = UserContainer()
    
    def run(self):
        self.sock.listen(100)
        self.context

        Logger.log("Running on: "+ str(self.sock.getsockname()))

        while self.running:
            try:
                c, addr = self.sock.accept()
                Logger.log('Connection from: '+str(addr))

                wrap = self.context.wrap_socket(c,server_side=True)

                user = User(wrap,addr) 
                self.users.add(user)

                threading.Thread(target=self.userHandler, args=(user,)).start()

                Logger.log('Encrypted connection from:'+str(addr))
            except socket.error:
                break

    def userHandler(self, user: User):
        while self.running and user.connected:
            try:
                data = user.socket.recv(1024)
                
                if data != '':
                    Logger.log('Recived'+str(data))
                    if isinstance(user,UserLogged):
                        print('handle logged')
                    else:
                        print('handle unnloged')
            except socket.error:
                self.users.remove(user)                
                user.quit()
                break

    def stop(self):
        self.running = False
        self.sock.close()


class ConsoleApp(object):
    def __init__(self,ip: str, port: int):
        super().__init__()

        self.server = Server(ip,port)

        self.thread = threading.Thread(target=self.server.run)

        Logger.log('Starting server')
        self.thread.start()

        self.run()

    def run(self):
        while True:
            command = str(input()).upper()
            if command == 'STOP':
                Logger.log('Stopping server...')
                self.server.stop()
                self.thread.join()
                break
        
        Logger.log('Stopped server')

app = ConsoleApp('',7777)
