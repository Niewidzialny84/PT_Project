def transfer(h,p):
    conn.send(h)
    conn.send(p)

def login(login: str, password: str): 
    h, p = Protocol.encode(Header.LOG,login=login,password=password)
    transfer(h,p)