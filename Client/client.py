import socket, ssl
import threading
from protocol import Header,HeaderParser,Protocol
import time

class Client(object):
    def __init__(self):
        self.is_Connected = False

        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        self.context.check_hostname = False
        self.context.verify_mode=ssl.CERT_NONE
        self.context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.addr = ('127.0.0.1',7777)

        self.conn = self.context.wrap_socket(self.sock,server_hostname=self.addr[0])
        try:
            self.conn.connect(self.addr)
            self.is_Connected = True
            
        except Exception as err:
            print(err)

    def transfer(self,h,p):
        self.conn.send(h)
        self.conn.send(p)

    def login(self,login: str, password: str): 
        h, p = Protocol.encode(Header.LOG,login=login,password=password)
        self.transfer(h,p)

    def receive(self):
        self.headerType, self.size = HeaderParser.decode(self.conn.recv(3))
        self.data = Protocol.decode(self.conn.recv(self.size))

        if self.headerType == Header.SES:
            session = self.data['session']
            print(session)

            self.headerType, self.size = HeaderParser.decode(self.conn.recv(3))
            self.data = Protocol.decode(self.conn.recv(self.size))
            print(self.data['users'])
        elif self.headerType == Header.ERR:
            print(self.data['msg'])

    def kill(self):
        h, p = Protocol.encode(Header.DIS, msg='Disconnect')
        self.transfer(h,p)
        self.conn.close()