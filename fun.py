from datetime import datetime
from datetime import timedelta
import pytz

record_ex = {'recordID':'123', 'title':'上課','startDate':'2021-01-30', 'startSection':1, 'endDate':'2021-01-30', 'endSection':10,
'roomName':'TR313', 'building':'研揚大樓(TR)', 'participant':['茶是一種蔬菜湯','茶葉蛋',
'神棍局局長']}

record_ex2 = {'recordID':'456', 'title':'創業', 'startDate':'2021-02-01', 'startSection':1, 'endDate':'2021-01-31', 'endSection':10,
'roomName':'TR411', 'building':'研揚大樓(TR)', 'participant':['勞工',
'CEO','CTO','PM']}

records = [record_ex, record_ex2]

def get_current_time():
    taipei = pytz.timezone('Asia/Taipei')
    return datetime.strftime(datetime.now(taipei), "%Y-%m-%d")

  

def authentication(email:str, password:str):
    """
    check user iuformation
    """
    if email == None or password == None:
        return (False, None)
    elif password == "admin": #admin account
        print((True, "admin"))
        return (True, "admin")
    print((True, "normal"))

    return (True, "normal")

def search():
    return True

def get_record(id):
    for record in records:
        if record['recordId'] == id:
            return record

def register(data):
    return True


def modify_record(data):
    recordId = data['recordId']
    participants = []
    for i in range(int(data['counter'])):
        p = data.get('participant' + str(i))
        if  p != None and p != '':
            participants.append(data['participant' + str(i)])
    print(participants)
    participants = ",".join(participants)
    print(participants)

    return True
def delete_record(data):
    print(data)
    recordId = data['recordId']
    print("delete", recordId)
