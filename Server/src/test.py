import socket, ssl

import threading

from protocol import Header,HeaderParser,Protocol

import time

context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.check_hostname = False
context.verify_mode=ssl.CERT_NONE
context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

addr = ('127.0.0.1',7777)

conn = context.wrap_socket(sock,server_hostname=addr[0])

conn.connect(addr)


def transfer(h,p):
    conn.send(h)
    conn.send(p)

def login(login: str, password: str): 
    h, p = Protocol.encode(Header.LOG,login=login,password=password)
    transfer(h,p)


session = None

_login = 'multiEryk'
login(_login,'123')
    
headerType, size = HeaderParser.decode(conn.recv(3))
data = Protocol.decode(conn.recv(size))

if headerType == Header.SES:
    session = data['session']
    print(session)

    headerType, size = HeaderParser.decode(conn.recv(3))
    data = Protocol.decode(conn.recv(size))
    print(data['users'])
elif headerType == Header.ERR:
    print(data['msg'])

h, p = Protocol.encode(Header.DIS, msg='Disconnect')
transfer(h,p)

conn.close()

