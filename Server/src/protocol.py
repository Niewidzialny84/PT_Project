from enum import Enum

class ProtocolVersion(Enum):
    V1 = 1

class Header(Enum):
    '''Enum of avaible headers for package with amount of arguments'''

    ACK = 0 #Acknowledment
    ERR = 1 #Any type error
    DIS = 2#Disconnection
    MSG = 3 #Message max 512 bytes
    LOG = 4 #Login
    SES = 5 #Session
    REG = 6, #Register
    LIS = 7 #List of users

    '''
    | Version  | Type   | Payload Size |
    |----------|--------|--------------|
    | 2 bits   | 6 bits | 16 bits      |

    Header is 3 bytes long
    '''

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
    def encode(headerType: Header, data: str,**kwargs):

        #TODO: Create special encoding depending on the heder type

        encodedData = data.encode()
        header = Header.encode(headerType,len(encodedData))

        return header,encodedData

    @staticmethod
    def decode(data: str):
        
        #TODO: Add special decoding

        return data.decode()

