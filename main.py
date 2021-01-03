from flask import Flask , render_template
from flask import request, url_for, flash, redirect, make_response

from admin import *
from system import *
import datetime

app = Flask(__name__)

buildings=['研揚大樓(TR)','第四教學大樓(T4)','綜合研究大樓(RB)','國際大樓(IB)','電資館(EE)']

record_ex = {'recordID':'123', 'title':'上課','startDate':'2021-01-30', 'startSection':1, 'endDate':'2021-01-30', 'endSection':10,
'roomName':'TR-313', 'building':'研揚大樓(TR)', 'participant':['茶是一種蔬菜湯','茶葉蛋',
'神棍局局長']}

record_ex2 = {'recordID':'456', 'title':'創業', 'startDate':'2021-02-01', 'startSection':1, 'endDate':'2021-01-31', 'endSection':10,
'roomName':'TR-411', 'building':'研揚大樓(TR)', 'participant':[]}

records = [record_ex, record_ex2]

weekdays= ['一', '二', '三', '四','五','六','日']

def cookie_check():
    """
    check cookie's correctness
    """
    email = request.cookies.get("email")
    password = request.cookies.get('password')
    return cookie_authentication(email, password)

@app.route('/logout')
def logout():
    res = make_response(redirect(url_for("login_page")))
    res.set_cookie(key='email', value='', expires=0)
    res.set_cookie(key='password', value='', expires=0)
    return res

@app.route('/register',methods=['POST','GET'])
def register_page():
    if cookie_check()[0]:
        return redirect(url_for('main_page'))

    if request.method == 'POST':
        if register(request.form):
            #註冊成功
            return render_template("register.html", message="register_success")
        else:
            #註冊失敗
            return render_template("register.html", message="register_error")
        
    return render_template("register.html")

@app.route('/login',methods=['POST','GET'])
def login_page():
    if cookie_check()[0]:
        return redirect(url_for('main_page'))
    if request.method =='POST':
        #TODO encryption
        login_status = authentication(request.form['email'], request.form['password'])
        #login fail
        if login_status[0]: 
            if login_status[0] == 1: #email error
                return render_template("login.html", message="email_error")
            elif login_status[0] == 2: #password error
                return render_template("login.html", message="password_error")
        #login success
        else:
            resp = make_response(render_template("main.html", admin=cookie_authentication(request.form['email'], request.form['password'])[1]))
            #set cookie
            resp.set_cookie('email', request.form['email']) 
            resp.set_cookie('password', request.form['password'])
            resp.set_cookie('userName', login_status[1])
            return resp
    return render_template("login.html", message=None)

@app.route('/search',methods=['POST','GET'])
def search_page():
    check = cookie_check()
    if not check[0]:
        return redirect(url_for('login_page'))
    if request.method =='POST':
        result = get_search_result(request.form)
        return render_template("search.html", buildings=buildings, date=request.form['date'], result=result, admin = check[1])
    return render_template("search.html", buildings=buildings, date=get_current_time(), result=None, admin = check[1])
    
@app.route('/borrow',methods=['POST','GET'])
def borrow_page():
    check = cookie_check()
    if not check[0]:
        return redirect(url_for('login_page'))
    if request.method == "POST":

        result = borrow(request.form, request.form['borrow_type'])
        if request.form['borrow_type'] == "borrow":
            if result: 
                message="borrow_success"
            else:
                message="borrow_fail"

        elif request.form['borrow_type'] == "ban":
            if result: 
                message="ban_success"
            else:
                message="ban_fail"
        return render_template("borrow.html", buildings=buildings, admin=check[1], message=message)
      

    return render_template("borrow.html", buildings=buildings, admin=check[1])

@app.route('/borrow_search',methods=['POST','GET'])
def borrow_search_page():
    check = cookie_check()
    if not check[0]:
        return redirect(url_for('login_page'))

    if request.method == "POST":
        result = search_for_borrow(request.form)
        return render_template("borrow_search.html", result=result)

    return render_template("borrow_search.html")


@app.route('/record',methods=['POST','GET'])
def record_page():
    check = cookie_check()
    if not check[0]:
        return redirect(url_for('login_page'))

    return render_template("record.html", userName = request.cookies['userName'], records=records, admin = check[1])

@app.route('/single_record',methods=['POST'])
def single_record_page():
    check = cookie_check()
    if not check[0]:
        return redirect(url_for('login_page'))
    if request.method =='POST':
        if request.form['postType'] == 'get':
            print('get')
            return render_template("single_record.html",record=get_record(request.form['recordID']), admin = check[1])
        elif request.form['postType'] == 'modify':
            modify_record(request.form)
            return redirect(url_for('record_page'))
        elif request.form['postType'] == 'delete':
            delete_record(request.form)
            return redirect(url_for('record_page'))
    return redirect(url_for('main_page'))

@app.route('/', methods=['POST', 'GET'])
def main_page():
    check = cookie_check()
    #if cookie exists and user information is correct, then enter main page 
    if check[0]:
        return render_template("main.html", user_name = request.cookies.get('email'), admin=check[1])
    return redirect(url_for('login_page'))

@app.route('/account_management', methods=['POST', 'GET'])
def account_management_page():
    #if cookie exists and user information is correct, then enter main page 
    check = cookie_check()
    if check[0] and check[1] == "admin":
        if request.method == "POST":
            print(request.form)
            if request.form['postType'] == "search":
                result = getUserData(request.form['userName'])
                if result[0]:
                    return render_template("account_management.html", user = result[1], admin=check[1])
                else:
                    return render_template("account_management.html", user = result[1], admin=check[1], message = "error")
            elif request.form['postType'] == "delete":
                result = deleteAccount(request.form['userID'])
                if result:
                    result = "delete_success"
                else:
                    result = "delete_fail"
                return render_template("account_management.html", user = None, admin=check[1], message = result)

            elif request.form['postType'] == "ban":
                result = banAccount(request.form['userID'])
                if result:
                    result = "ban_success"
                else:
                    result = "ban_fail"
                return render_template("account_management.html", user = None, admin=check[1], message = result)

            elif request.form['postType'] == "unban":
                result = unBanAccount(request.form['userID'])
                if result:
                    result = "unban_success"
                else:
                    result = "unban_fail"
                return render_template("account_management.html", user = None, admin=check[1], message = result)
        return render_template("account_management.html", user = None, admin=check[1])
    else:
        return redirect(url_for('login_page'))
      
@app.route('/search_single',methods=['POST','GET'])
def search_single_page():
    check = cookie_check()
    if not check[0]:
        return redirect(url_for('login_page'))
    if request.method =='POST':
        classroom_data = get_single_result(request.form['CR_ID'], request.form['start_date'])
        start_date = request.form['start_date']
        
        start_date = datetime.datetime(int(start_date.split('-')[0]), 
                                        int(start_date.split('-')[1]),
                                        int(start_date.split('-')[2]))
        dates = [start_date]
        dates_weekdays = []
        for i in range(1,7):
            dates.append(start_date + datetime.timedelta(i))
        for i in range(7):
            dates_weekdays.append(weekdays[dates[i].weekday()])
            dates[i] = datetime.datetime.strftime(dates[i], "%Y-%m-%d")
            
        print(dates, dates_weekdays)
        return render_template("search_single.html",classroom = search_single_ex,
                                                    dates = dates,
                                                    dates_weekdays = dates_weekdays,
                                                    admin = check[1])
    return redirect(url_for('main_page'))
if __name__ == '__main__':
    app.debug = True
    app.secret_key = "test Key"
    app.run()