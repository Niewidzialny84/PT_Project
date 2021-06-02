from enum import Enum
import json

class ProtocolVersion(Enum):
    V1 = 1

class Header(Enum):
    '''Enum of avaible headers for package with amount of arguments'''

    ACK = 0 #Acknowledment !
    ERR = 1 #Any type error !
    DIS = 2 #Disconnection !
    MSG = 3 #TODO: Message !
    LOG = 4 #Login !
    SES = 5 #Session !
    REG = 6 #Register !
    LIS = 7 #List of users !
    FRP = 8 #TODO: Forgot password !
    HIS = 9 #TODO: Returns a user history 
    UPD = 10 #TODO: Update speaking current user 
    CHP = 11 # Change password !
    CHM = 12 # Change mail !
    DEL = 13 # Remove account !

    '''
    | Version  | Type   | Payload Size |
    |----------|--------|--------------|
    | 2 bits   | 6 bits | 16 bits      |

    Header is 3 bytes long
    '''


class HeaderParser(object):
    @staticmethod
    def encode(header: Header, size: int):
        '''Header creator for internal protocol use'''

        version = str(format(ProtocolVersion.V1.value,'b').zfill(2)) 
        headerType = str(format(header.value,'b').zfill(6)) 

        byte1 = format(int((version+headerType),2),'x').zfill(2) 

        payloadSize = str(format(size,'x').zfill(4)) 
        
        return bytes.fromhex(byte1 + payloadSize)

    @staticmethod
    def decode(headerBytes):
        '''Header decoder for to know how more bytes are needed to read'''
        
        headerBytes = headerBytes.hex()

        byte1 = format(int(headerBytes[0:2],16),'b').zfill(8)
        version = int(byte1[0:2],2)
        headerType = Header(int(byte1[2:8],2))

        if version != ProtocolVersion.V1.value:
            raise ValueError('Invalid version')

        payloadSize = int(headerBytes[2:6],16)   

        return headerType,payloadSize

class Protocol(object):
    @staticmethod
    def encode(headerType: Header, **kwargs):
        '''Encoding data to return a specified header and data to be send'''

        data = ''
        msg = kwargs.get('msg',None)
        login = kwargs.get('login',None)
        password = kwargs.get('password',None)
        email = kwargs.get('email',None)

        if headerType == Header.ACK or headerType == Header.ERR or headerType == Header.DIS or  headerType == Header.DEL:
            data = {'msg': msg}
        elif headerType == Header.LOG:
            if login != None or password != None:
                data = {'login': login, 'password': password}
            else:
                raise TypeError('-LOG- Missing login or password')
        elif headerType == Header.REG:
            if login != None or password != None or email != None:
                data = {'login': login, 'password': password, 'email':email}
            else:
                raise TypeError('-REG- Missing login or password or email')
        elif headerType == Header.SES:
            session = kwargs.get('session',None)
            if session != None:
                data = {'session': session}
            else:
                raise TypeError('-SES- Missiong session id')
        elif headerType == Header.LIS:
            users = kwargs.get('users', [])
            if users != []:
                data = {'users': users}
            else:
                raise TypeError('-LIS- Missing users list')
        elif headerType == Header.CHM:
            if email != None:
                data = {'email': email}
            else:
                raise TypeError('-CHM- Missiong email')
        elif headerType == Header.CHP:
            if password != None:
                data = {'password': password}
            else:
                raise TypeError('-CHP- Missiong password')
        elif headerType == Header.MSG:
            reciever = kwargs.get('reciever', None)
            if reciever != None:
                data = {'msg': msg, 'reciever':reciever}
            else:
                raise TypeError('-MSG- Missiong reciver')
        elif headerType == Header.FRP:
            if login != None:
                data = {'login': login}
            else:
                raise TypeError('-FRP- Missing login')     
        elif headerType == Header.HIS:
            history = kwargs.get('history', [])  
            if history != []:
                data = {'history':history}
            else:
                raise TypeError('-HIS- Missing history')
        elif headerType == Header.UPD:
            reciever = kwargs.get('reciever',None)
            if reciever != None:
                data = {'reciver':reciever}
            else:
                raise TypeError('-UPD- Missing login')         

        encodedData = json.dumps(data).encode()
        header = HeaderParser.encode(headerType,len(encodedData))

        return header,encodedData

    @staticmethod
    def decode(data: str):
        '''Decoding data into dict array which should be used based on header'''

        return json.loads(data.decode())

