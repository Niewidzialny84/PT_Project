import socket, threading, ssl,time, datetime, pytz

class User(object):
    def __init__(self, conn, addr):
        super().__init__()

        self.address = addr
        self.socket = conn

class UserLogged(User):
    def __init__(self, conn, addr):
        super().__init__(conn, addr)

class Logger(object):
    @staticmethod
    def log(text: str):
        threading.Thread(target=Logger._logtask,args=(text,)).start()

    @staticmethod
    def _logtask(text: str):
        t = '[ '+ datetime.datetime.now(pytz.timezone('Europe/Warsaw')).strftime("%Y-%m-%d %H:%M:%S")+' ]  '
        print(t+str(text))

class Server(object):
    def __init__(self, ip: str, port: int):
        super().__init__()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((ip,port))

        #self.context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        #self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        self.context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
        self.context.set_ciphers('AES256+ECDH:AES256+EDH')

        self.innerAddr = self.sock.getsockname()

        self.running = True
    
    def run(self):
        self.sock.listen(100)
        self.context

        Logger.log("Running on: "+ str(self.sock.getsockname()))

        while self.running:
            try:
                c, addr = self.sock.accept()
                Logger.log('Connection from: '+str(addr))

                wrap = self.context.wrap_socket(c,server_side=True)
                #wrap = ssl.SSLSocket(c)

                user = User(wrap,addr)

                threading.Thread(target=self.userHandler, args=(user,)).start()
            except socket.error:
                break

    def userHandler(self, user: User):
        while self.running:
            try:
                data = user.socket.recv(1024)
            except socket.error:
                user.socket.close()
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
