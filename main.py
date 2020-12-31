from flask import Flask , render_template
from flask import request, url_for, flash, redirect, make_response

from fun import *

app = Flask(__name__)

buildings=['研揚大樓(TR)','第四教學大樓(T4)','綜合研究大樓(RB)','國際大樓(IB)','電資館(EE)']

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
        return render_template("search.html", building=buildings, date=request.form['date'])
        
    return render_template("search.html", building=buildings, date=get_current_time())
    
# @app.route('/search_result',methods=['POST','GET'])
# def search_result_page():
#     if not cookie_check():
#         return redirect(url_for('login_page'))

#     return render_template("search_result.html")

@app.route('/borrow',methods=['POST','GET'])
def borrow_page():
    if not cookie_check():
        return redirect(url_for('login_page'))
    return render_template("borrow.html")

@app.route('/record',methods=['POST','GET'])
def record_page():
    if not cookie_check():
        return redirect(url_for('login_page'))

    return render_template("record.html")


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