import time, datetime, pytz 
import threading

class Logger(object):
    @staticmethod
    def log(text: str):
        threading.Thread(target=Logger._logtask,args=(text,)).start()

    @staticmethod
    def _logtask(text: str):
        t = '[ '+ datetime.datetime.now(pytz.timezone('Europe/Warsaw')).strftime("%Y-%m-%d %H:%M:%S")+' ]  '
        print(t+str(text))