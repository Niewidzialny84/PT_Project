import socket, ssl

class Client(object):
    def __init__(self):
        super().__init__()

        #self.context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)      
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        self.context.check_hostname = False
        self.context.verify_mode=ssl.CERT_NONE
        self.context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.addr = ('127.0.0.1',7777)

        self.s = self.context.wrap_socket(self.sock,server_hostname=self.addr[0])
        print(ssl.OPENSSL_VERSION)
        self.s.connect(self.addr)

        self.send('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        print(str(self.s))

        self.s.close()


Client()