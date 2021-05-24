import socket, ssl

import threading

from protocol import Header,HeaderParser,Protocol

import time

class Client(object):
    def __init__(self):
        super().__init__()    
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        self.context.check_hostname = False
        self.context.verify_mode=ssl.CERT_NONE
        self.context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.addr = ('127.0.0.1',7777)

        self.conn = self.context.wrap_socket(self.sock,server_hostname=self.addr[0])

        self.conn.connect(self.addr)

        self.running = True
        self.session = None

        self.reciveThread = threading.Thread(target=self.loop)
        self.reciveThread.start()

        self._login = 'multiEryk'
        self.login(self._login,'123c')
    
    def loop(self):
        while self.running:
            try:
                r = self.conn.recv(3)
                print(r)
                if r != b'':
                    headerType, size = HeaderParser.decode(r)
                    data = Protocol.decode(self.conn.recv(size))

                    if headerType == Header.SES:
                        self.session = data['session']
                        print(self.session)
                    elif headerType == Header.LIS:
                        print(data['users'])
                    elif headerType == Header.ERR:
                        print(data['msg'])
            except socket.error as ex:
                print(ex)

    

    def login(self, login: str, password: str): 
        h, p = Protocol.encode(Header.LOG,login=login,password=password)
        self.transfer(h,p)

    def transfer(self,h,p):
        self.conn.send(h)
        self.conn.send(p)
    
    def stop(self):
        self.running = False
        self.conn.setblocking(False)
        self.conn.close()
        self.reciveThread.join()

c = Client()
time.sleep(3)
c.stop()