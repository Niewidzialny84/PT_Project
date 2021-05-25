import socket, ssl
import threading
from protocol import Header,HeaderParser,Protocol
import time

class Client(object):
    def __init__(self):
        isConnected = False

        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.check_hostname = False
        context.verify_mode=ssl.CERT_NONE
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        addr = ('127.0.0.1',7777)

        conn = context.wrap_socket(sock,server_hostname=addr[0])
        try:
            conn.connect(addr)
            isConnected = True
        except Exception as err:
            print(err)

Client()