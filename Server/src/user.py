from logger import Logger
from protocol import Header,HeaderParser,Protocol

import requests, json, socket

class URL(object):
    local = 'http://127.0.0.1:5000/api/'
    remote = 'http://molly.ovh:5000/api/'

class User(object):
    def __init__(self, conn, addr):
        super().__init__()

        self.address = addr
        self.socket = conn
        self.connected = True
        self.uuid = None

    def __repr__(self):
        return str(self.address)+' '+str(self.uuid)

    def quit(self, message: str):
        self.connected = False
        self.socket.close()
        Logger.log('Client closed from:'+str(self.address)+' '+str(message))

    def handle(self):
        r = self.socket.recv(3)
        if r != b'':
            headerType, size = HeaderParser.decode(r)
            data = Protocol.decode(self.socket.recv(size))
            h,p = None,None

            if headerType == Header.LOG:
                r = requests.get(URL.local+'users', params={'username':data['login']})
                j = r.json()
                if r.status_code == 200 and j != {}:
                    #TODO handle password encoding
                    if data['password'] == j['password']:
                        h,p = Protocol.encode(Header.SES, session = self.uuid)
                        self.transfer(h,p)
                        Logger.log('User logged in ('+str(data['login'])+')')
                        return UserLogged(self,j['id'],j['username'])
                
                h,p = Protocol.encode(Header.ERR, msg = 'Invalid login data')
                Logger.log('User login invalid data '+ str(self.address))           
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
            elif headerType == Header.FRP:
                #TODO: handle the forgot password function
                print('lol he forgot password')
            elif headerType == Header.DIS:
                raise socket.error(data['msg'])
                
            if h != None and p != None:
                self.transfer(h,p)
        return None

    def transfer(self,h,p):
        self.socket.send(h)
        self.socket.send(p)


class UserLogged(User):
    def __init__(self, user: User, dbID, username):
        super().__init__(user.socket,user.address)
        self.uuid = user.uuid
        self.dbID = dbID
        self.username = username
        r = requests.get(URL.local+'users')
        
        l = []
        for x in r.json():
            if x['username'] != self.username:
                l.append(x['username'])
        h,p = Protocol.encode(Header.LIS, users = l)
        self.transfer(h,p)

    def __repr__(self):
        return str(self.address)+' '+str(self.uuid)+' '+self.username

    def handle(self):
        r = self.socket.recv(3)
        if r != b'':
            headerType, size = HeaderParser.decode(r)
            data = Protocol.decode(self.socket.recv(size))
            h,p = None,None

            if headerType == Header.DIS:
                raise socket.error('Disconnect')
            elif headerType == Header.MSG:
                #TODO create single message handling and adding to database
                r = requests.post(URL.local+'history-manager', data=json.dumps({'first_username': self.username, 'second_username': data['reciver']}))
            elif headerType == Header.HIS:
                #TODO: create sending of history to client
                print('abc')
            elif headerType == Header.DEL:
                r = requests.delete(URL.local+'users', params={'username':self.username})

                if r.status_code == 200:
                    h,p = Protocol.encode(Header.ACK, msg = 'Deletion succesfull')
                else:
                    h,p = Protocol.encode(Header.ERR, msg = 'Deletion failed')
            elif headerType == Header.CHP:
                r = requests.patch(URL.local+'users', data=json.dumps({'password':data['password']}), params={'username':self.username})

                if r.status_code == 200:
                    h,p = Protocol.encode(Header.ACK, msg = 'Change password succesfull')
                else:
                    h,p = Protocol.encode(Header.ERR, msg = 'Change password failed')
            elif headerType == Header.CHM:
                r = requests.patch(URL.local+'users', data=json.dumps({'email':data['email']}) ,params={'username':self.username})

                if r.status_code == 200:
                    h,p = Protocol.encode(Header.ACK, msg = 'Change mail succesfull')
                else:
                    h,p = Protocol.encode(Header.ERR, msg = 'Change mail failed')
            elif headerType == Header.UPD:
                print('any update')

            if h != None and p != None:
                self.transfer(h,p)
                
        return None

