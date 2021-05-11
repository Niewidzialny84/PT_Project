from logger import Logger

class User(object):
    def __init__(self, conn, addr):
        super().__init__()

        self.address = addr
        self.socket = conn
        self.connected = True
        self.uuid = None

    def quit(self, message: str):
        self.connected = False
        self.socket.close()
        Logger.log('Client closed from:'+str(self.socket.getsockname()))

class UserLogged(User):
    def __init__(self, conn, addr):
        super().__init__(conn, addr)
