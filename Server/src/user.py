from logger import Logger
from protocol import Header,Protocol

import requests, json

class URL(object):
    local = 'http://127.0.0.1:5000/api/'
    remote = ''

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
        h,p = None,None

        if headerType == Header.LOG:
            r = requests.get(URL.local+'users', params={'username':data['login']})
            j = r.json()
            if r.status_code == 200 and j != {}:
                if data['password'] == j['password']:
                    h,p = Protocol.encode(Header.SES, session = self.uuid)
                    self.socket.send(h)
                    self.socket.send(p)
                    Logger.log('User logged in ('+str(data['login'])+')')
                    return UserLogged(self,j['id'],j['username'])
            
            h,p = Protocol.encode(Header.ERR, msg = 'Invalid login data')
            Logger.log('User login invalid data ')           
        elif headerType == Header.REG:
            r = requests.post(URL.local+'users', data=json.dumps({'username':data['login'], 'email': data['email'], 'password': data['password']}))
            if r.status_code == 201:
                h,p = Protocol.encode(Header.ACK, msg = 'Created Account')
                Logger.log('User registered ')
            elif r.status_code == 409:
                h,p = Protocol.encode(Header.ERR, msg = 'Account already exists')
                msg = r.json()['Message']
                Logger.log('User thats already exists creation try ('+str(data['login'])+')')
            else:
                h,p = Protocol.encode(Header.ERR, msg = 'Invalid register data')
                Logger.log('User register invalid data ')
        
        if h != None and p != None:
            self.socket.send(h)
            self.socket.send(p)
        return None


class UserLogged(User):
    def __init__(self, user: User, dbID, username):
        super().__init__(user.socket,user.address)
        self.uuid = user.uuid()
        self.dbID = dbID
        self.username = username

    def handle(self):
        return None
