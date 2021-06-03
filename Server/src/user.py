from logger import Logger
from protocol import Header,HeaderParser,Protocol

from mail import sendRecoveryMail

import requests, json, hashlib, os, socket, threading ,time

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
                    u2 = bytes.fromhex(j['password'])
                    u1 = self.passwordHash(data['password'], u2[:32])

                    if u1[32:] == u2[32:]:
                        h,p = Protocol.encode(Header.SES, session = self.uuid)
                        self.transfer(h,p)
                        Logger.log('User logged in ('+str(data['login'])+')')
                        return UserLogged(self,j['id'],j['username'])
                
                h,p = Protocol.encode(Header.ERR, msg = 'Invalid login data')
                Logger.log('User login invalid data '+ str(self.address))           
            elif headerType == Header.REG:
                r = requests.post(URL.local+'users', json={'username':data['login'], 'email': data['email'], 'password': self.passwordHash(data['password']).hex()})
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
                ru = requests.get(URL.local+'users', params={'username':data['login']})
                j = ru.json()
                if ru.status_code == 200:
                    if j != {}:
                        mail = j['email']
                        r = requests.post('https://molly.ovh:5050/token/'+data['login'])
                        j2 = r.json()
                        token = j2['token']
                        threading.Thread(target=sendRecoveryMail,params=(data['login'],token,)).start()
                        Logger.log('FRP send')

                    h,p = Protocol.encode(Header.ACK, msg = 'Send recovery mail')
                    Logger.log('FRP used')
                else:
                    h,p = Protocol.encode(Header.ERR, msg = 'Error occured')
                    Logger.log('FRP error')
            elif headerType == Header.DIS:
                raise socket.error(data['msg'])
                
            if h != None and p != None:
                self.transfer(h,p)
        return None

    def transfer(self,h,p):
        try:
            self.socket.send(h)
            self.socket.send(p)
        except Exception as ex:
            pass
    
    def passwordHash(self, password: str, salt=None):
        salt = salt or os.urandom(32)
        key = hashlib.pbkdf2_hmac('sha256',password.encode(),salt,10000)
        return (salt+key)


class UserLogged(User):
    def __init__(self, user: User, dbID, username):
        super().__init__(user.socket,user.address)
        self.uuid = user.uuid
        self.dbID = dbID
        self.username = username

        self.usersThread = threading.Thread(target=self.userListUpdateThread)
        self.usersThread.start()

        self.reciever = None
        self.historyThread = threading.Thread(target=self.historyUpdateThread)
        self.historyThread.start()

    def __repr__(self):
        return str(self.address)+' '+str(self.uuid)+' '+self.username

    def userListUpdateThread(self):
        while self.connected:
            r = requests.get(URL.local+'users')
            
            l = []
            for x in r.json():
                if x['username'] != self.username:
                    l.append(x['username'])

            if l != []:
                h,p = Protocol.encode(Header.LIS, users = l)
                self.transfer(h,p)

            time.sleep(10)

    def historyUpdateThread(self):
        while self.connected:
            if self.reciever != None:
                r = requests.get(URL.local+'history-manager',params={'first_username':self.username,'second_username':self.reciever})

                if r.status_code == 200:
                    history = []
                    for x in r.json():
                        history.append('['+str(x['date'])+'] '+str(x['username'])+': '+str(x['content']))

                    if history != []:
                        if len(history) > 200:
                            history.reverse()
                            history = history[:200]
                            history.reverse()
                        h,p = Protocol.encode(Header.HIS, history = history)
                        self.transfer(h,p)

                time.sleep(0.5)

    def handle(self):
        r = self.socket.recv(3)
        if r != b'':
            headerType, size = HeaderParser.decode(r)
            data = Protocol.decode(self.socket.recv(size))
            h,p = None,None

            if headerType == Header.DIS:
                raise socket.error('Disconnect')
            elif headerType == Header.MSG:
                historyID = self.checkHistory(self.username,data['reciever'])
                if historyID != None:
                    r = requests.post(URL.local+'history-manager', json={'history_id':historyID, 'username':self.username, 'content': data['msg']})      
            elif headerType == Header.DEL:
                r = requests.delete(URL.local+'users', params={'username':self.username})

                if r.status_code == 200:
                    h,p = Protocol.encode(Header.ACK, msg = 'Deletion succesfull')
                else:
                    h,p = Protocol.encode(Header.ERR, msg = 'Deletion failed')
            elif headerType == Header.CHP:
                r = requests.patch(URL.local+'users', json=({'password':self.passwordHash(data['password']).hex()}), params={'username':self.username})

                if r.status_code == 200:
                    h,p = Protocol.encode(Header.ACK, msg = 'Change password succesfull')
                else:
                    h,p = Protocol.encode(Header.ERR, msg = 'Change password failed')
            elif headerType == Header.CHM:
                r = requests.patch(URL.local+'users', json=({'email':data['email']}) ,params={'username':self.username})

                if r.status_code == 200:
                    h,p = Protocol.encode(Header.ACK, msg = 'Change mail succesfull')
                else:
                    h,p = Protocol.encode(Header.ERR, msg = 'Change mail failed')
            elif headerType == Header.UPD:
                self.reciever = data['reciever']
                if self.reciever != None:
                    self.checkHistory(self.username,self.reciever)

            if h != None and p != None:
                self.transfer(h,p)
                
        return None

    def checkHistory(self, u1, u2):
        r = requests.get(URL.local+'history-manager/historyID', params={'first_username': u1, 'second_username': u2})

        if r.status_code == 200:
            historyID = r.json()['history_id']

            return historyID
        elif r.status_code == 404:
            r = requests.post(URL.local+'history-manager', json={'first_username': u1, 'second_username': u2})
            if r.status_code == 201:
                r = requests.get(URL.local+'history-manager/historyID', params={'first_username': u1, 'second_username': u2})
                historyID = r.json()['history_id']

                return historyID
            return None
        return None