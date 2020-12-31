from datetime import datetime
import pytz

def get_current_time():
    taipei = pytz.timezone('Asia/Taipei')
    return datetime.strftime(datetime.now(taipei), "%Y-%m-%d")

def authentication(email:str, password:str):
    """
    check user iuformation
    """
    if email == None or password == None:
        return False
    return True

def search():
    return True