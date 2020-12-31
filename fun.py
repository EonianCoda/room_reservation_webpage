from datetime import datetime
import pytz

def getTime():
    taipei = pytz.timezone('Asia/Taipei')
    return datetime.now(taipei)

def authentication(email:str, password:str):
    """
    check user iuformation
    """
    if email == None or password == None:
        return False
    return True

def search():
    return True