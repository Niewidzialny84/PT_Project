import socket, ssl
import threading
from protocol import Header,HeaderParser,Protocol
import time
import os,hashlib

class Client(object):
    def __init__(self):
        self.is_Connected = False
        self.session = None

        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        self.context.check_hostname = False
        self.context.verify_mode=ssl.CERT_NONE
        self.context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.addr = ('127.0.0.1',7777)
        self.salt = None
        self.username = None
        self.password = None

        self.conn = self.context.wrap_socket(self.sock,server_hostname=self.addr[0])
        try:
            self.conn.connect(self.addr)
            self.is_Connected = True
            
        except Exception as err:
            print(err)
        

    def transfer(self,h,p):
        try:
            self.conn.send(h)
            self.conn.send(p)
        except socket.error as ex:
            print(ex)
    
    def passwordHash(self, password: str, salt=None):
        salt = salt or os.urandom(32)
        key = hashlib.pbkdf2_hmac('sha256',password.encode(),salt,10000)
        return (salt+key)

    def login(self,login: str, password: str):
        if self.username == None and self.password == None:
            self.username = login
            self.password = password

        if self.salt == None:
            h, p = Protocol.encode(Header.LOG,login=self.username,password='X')
        else:
            h, p = Protocol.encode(Header.LOG,login=self.username,password=self.passwordHash(self.password,self.salt).hex())
        self.transfer(h,p)

    def register(self,login: str, password: str, email: str):
        h, p = Protocol.encode(Header.REG,login=login,password=self.passwordHash(password).hex(),email=email)
        self.transfer(h,p)

    def password(self, password: str): 
        h, p = Protocol.encode(Header.CHP,password=self.passwordHash(password).hex())
        self.transfer(h,p)

    def mail(self, email: str): 
        h, p = Protocol.encode(Header.CHM,email=email)
        self.transfer(h,p)

    def delete(self): 
        h, p = Protocol.encode(Header.DEL,msg='Delete')
        self.transfer(h,p)

    def update(self, reciever: str): 
        h, p = Protocol.encode(Header.UPD,reciever=reciever)
        self.transfer(h,p)

    def message(self, reciever: str, msg: str): 
        h, p = Protocol.encode(Header.MSG,reciever=reciever,msg=msg)
        self.transfer(h,p)

    def forgot(self, login: str):
        h, p = Protocol.encode(Header.FRP,login=login)
        self.transfer(h,p)


    """
    def receive(self):
        try:
            r = self.conn.recv(3)
            if r != b'':
                headerType, size = HeaderParser.decode(r)
                data = Protocol.decode(self.conn.recv(size))

                if headerType == Header.SES:
                    self.session = data['session']
                    return str(data['session'])
                elif headerType == Header.LIS:
                    return data['users']
                elif headerType == Header.ERR:
                    return data['msg']

        except socket.error as ex:
                print(ex)
                return ex
    """

    def stop(self):
        h, p = Protocol.encode(Header.DIS, msg='Disconnect')
        self.transfer(h,p)
        self.is_Connected = False
        self.conn.close()
        #self.reciveThread.join()