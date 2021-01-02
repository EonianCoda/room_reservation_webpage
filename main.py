from flask import Flask , render_template
from flask import request, url_for, flash, redirect, make_response

from fun import *

app = Flask(__name__)

buildings=['研揚大樓(TR)','第四教學大樓(T4)','綜合研究大樓(RB)','國際大樓(IB)','電資館(EE)']

record_ex = {'recordId':'123', 'title':'上課','start_date':'2021-01-30', 'start_section':1, 'end_date':'2021-01-30', 'end_section':10,
'roomName':'TR313', 'building':'研揚大樓(TR)', 'participant':['茶是一種蔬菜湯','茶葉蛋',
'神棍局局長']}

record_ex2 = {'recordId':'456', 'title':'創業', 'start_date':'2021-02-01', 'start_section':1, 'end_date':'2021-01-31', 'end_section':10,
'roomName':'TR411', 'building':'研揚大樓(TR)', 'participant':['勞工',
'CEO','CTO','PM']}

records = [record_ex, record_ex2]

search_ex = {'building':'研揚大樓','roomName':'TR313','capacity':20,
'status':{1:(1,'電機系上課','咕你媽逼'), 10:(0, '投影機故障', 'admin')}}

search_ex2 = {'building':'研揚大樓','roomName':'TR414','capacity':30,
'status':{5:(1,'開會','Jerry'), 14:(0, '椅子壞掉', 'admin')}}

search_result = [search_ex, search_ex2]

def cookie_check():
    """
    check cookie's correctness
    """
    email = request.cookies.get("email")
    password = request.cookies.get('password')
    if authentication(email, password):
        return True
    return False

@app.route('/logout')
def logout():
    res = make_response(redirect(url_for("login_page")))
    res.set_cookie(key='email', value='', expires=0)
    res.set_cookie(key='password', value='', expires=0)
    return res


    return redirect(url_for('logout'))
@app.route('/login',methods=['POST','GET'])
def login_page():
    if cookie_check():
        return redirect(url_for('main_page'))
    return render_template("login.html")

@app.route('/search',methods=['POST','GET'])
def search_page():
    if not cookie_check():
        return redirect(url_for('login_page'))
    if request.method =='POST':
        return render_template("search.html", buildings=buildings, date=request.form['date'], result=search_result)
    print("template")
    return render_template("search.html", buildings=buildings, date=get_current_time(), result=None)
    
# @app.route('/search_result',methods=['POST','GET'])
# def search_result_page():
#     if not cookie_check():
#         return redirect(url_for('login_page'))

#     return render_template("search_result.html")

@app.route('/borrow',methods=['POST','GET'])
def borrow_page():
    if not cookie_check():
        return redirect(url_for('login_page'))
    return render_template("borrow.html", buildings=buildings)

@app.route('/record',methods=['POST','GET'])
def record_page():
    if not cookie_check():
        return redirect(url_for('login_page'))

    return render_template("record.html", records=records)

@app.route('/single_record',methods=['POST'])
def single_record_page():
    if not cookie_check():
        return redirect(url_for('login_page'))
    if request.method =='POST':
        return render_template("single_record.html",record=get_record(request.form['id']))
    
    return render_template("single_record.html")

@app.route('/', methods=['POST', 'GET'])
def main_page():
    #if cookie exists and user information is correct, then enter main page 
    if cookie_check():
        return render_template("main.html", user_name = request.cookies.get('email'))


    if request.method =='POST':
        #TODO encryption
        if authentication(request.form['email'], request.form['password']):
            resp = make_response(render_template("main.html"))
            #set cookie
            resp.set_cookie('email', request.form['email']) #TODO set age
            resp.set_cookie('password', request.form['password']) #TODO set age
            return resp
        #login fail
        else:
            return redirect(url_for('login_page'))
    else:
        return redirect(url_for('login_page'))
         
    
if __name__ == '__main__':
    app.debug = True
    app.secret_key = "test Key"
    app.run()