from datetime import datetime
import pytz

search_ex = {"CR_ID":0, 'building':'研揚大樓','roomName':'TR313','capacity':20,
'status':{1:(1,'電機系上課','咕你媽逼'), 10:(0, '投影機故障', 'admin')}}

search_ex2 = {"CR_ID":1, 'building':'研揚大樓','roomName':'TR414','capacity':30,
'status':{5:(1,'開會','Jerry'), 14:(0, '椅子壞掉', 'admin')}}

search_result = [search_ex, search_ex2]

record_ex = {'recordID':'123', 'title':'上課','startDate':'2021-01-30', 'startSection':1, 'endDate':'2021-01-30', 'endSection':10,
'roomName':'TR-313', 'building':'研揚大樓(TR)', 'participant':['茶是一種蔬菜湯','茶葉蛋',
'神棍局局長']}

record_ex2 = {'recordID':'456', 'title':'創業', 'startDate':'2021-02-01', 'startSection':1, 'endDate':'2021-01-31', 'endSection':10,
'roomName':'TR-411', 'building':'研揚大樓(TR)', 'participant':[]}

records = [record_ex, record_ex2]

user_ex1={"userID":0,"userName":"wacky","nickName":"OwO","password":"hahaha","email":"chenghan0516@gmail.com","identity":0,"banned":False}
user_ex2={"userID":0,"userName":"hello","nickName":"OwO","password":"hahaha","email":"chenghan0516@gmail.com","identity":0,"banned":True}


search_single1 = {1:(1,'電機系上課','咕你媽逼'), 10:(0, '投影機故障', 'admin')}
search_single2 = {3:(1,'電機系上課','咕你媽逼'), 10:(0, '投影機故障', 'admin')}
search_single3 = {3:(1,'電機系上課','咕你媽逼'), 10:(0, '投影機故障', 'admin')}
search_single4 = {3:(1,'電機系上課','咕你媽逼'), 10:(0, '投影機故障', 'admin')}
search_single5 = {3:(1,'電機系上課','咕你媽逼'), 10:(0, '故障', 'admin')}
search_single6 = {9:(1,'電機系上課','你好'), 10:(0, '投影機故障', 'admin')}
search_single7 = {3:(1,'電機系上課','WackilySmiley'), 10:(0, '投影機故障', 'admin')}

search_single_ex = {'CR_ID':1,'building':'研揚大樓','roomName':'TR313','capacity':20, 'status':[search_single1,search_single2,
search_single3,search_single4,search_single5,search_single6,search_single7]}

borrow_search_ex = {'building':'研揚大樓','roomName':'TR-414','capacity':30}
borrow_search_ex2 = {'building':'第四研究大樓','roomName':'T4-414','capacity':20}
borrow_search_ex3 = {'building':'貝殼廳','roomName':'T4-314','capacity':90}
borrow_search_exs = [borrow_search_ex, borrow_search_ex2, borrow_search_ex3]

def borrow(data, borrow_type):
    if borrow_type == "borrow":
        if data['title'] == 'error':
            return False
        return True

    elif borrow_type == "ban":
        if data['title'] == "error":
            return False
        return True

def search_for_borrow(data):
    return borrow_search_exs 

def get_record(recordID):
    return record_ex
def register(data):
    if data['userName'] == "error":
        return False
    return True

def search():
    return True

def cookie_authentication(email:str, password:str):
    """
    check user iuformation for cookie
    """
    if email == None or password == None:
        return (False, None)
    elif password == "admin": #admin account
        print((True, "admin"))
        return (True, "admin")
    print((True, "normal"))

    return (True, "normal")

def authentication(email:str, password:str):
    """
    check user iuformation for login
    """
    print("驗證" , email, password)
    if email == "error@gamil.com": #信箱錯誤
        return (1, None)
    elif password == "error": #密碼錯誤
        return (2, None)
    return (0, "咕你媽逼") #(status, username)


def getUserData(userName):
    if userName == "wacky":
        return (True, user_ex1)
    elif userName == "hello":
        return (True, user_ex2)
    else:
        return (False, None)


def get_search_result(data):
    return search_result

def get_single_result(CR_ID, start_date):
    return search_single_ex

def get_current_time():
    taipei = pytz.timezone('Asia/Taipei')
    return datetime.strftime(datetime.now(taipei), "%Y-%m-%d")


def modify_record(data):
    recordID = data['recordID']
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
    recordID = data['recordID']
    print("delete", recordID)
