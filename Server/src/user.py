from logger import Logger
from protocol import Header,Protocol

import requests

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

    def handle(self):
        headerType, size = Header.decode(self.socket.recv(3))
        data = Protocol.decode(self.socket.recv(size))

        if headerType == Header.LOG:
            return UserLogged(self)
        elif headerType == Header.REG:
            Logger.log('User registered ')
        return None


class UserLogged(User):
    def __init__(self, user: User, dbID):
        super().__init__(user.socket,user.address)
        self.uuid = user.uuid()
        self.dbID = dbID

    def handle(self):
        return None
