from colorama import Cursor
from flask import Flask,redirect,request,render_template
import string
import random
import sqlite3

app=Flask(__name__)

class values:
    lurl=""
    surl=""
    ran=""
a=values()

def rand():
    chars=string.ascii_uppercase + string.digits
    c=""
    for i in range(0,5):
        d=random.choice(chars)
        c=c+d
    a.ran=c

def shorturl():
    rand()
    a.surl=a.ran
    print(a.surl)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/short',methods = ['POST', 'GET'])
def short():
    if request.method == 'POST':
      a.lurl = request.form['long']
      print(a.lurl)
      shorturl()
      g="("+"\""+a.lurl+"\""+","+"\""+a.surl+"\""+")"
      x="insert into urls values"+g
      print(x)
    try:
        con=sqlite3.connect('url.db')
        cursor=con.cursor()
        x="insert into urls values"+g
        cursor.execute(x)
        con.commit()
        con.close()
    except:
        print("not able to connect to db")
    return ""+a.surl

@app.route('/<sturl>')
def find(sturl):
    con=sqlite3.connect('url.db')
    cursor=con.cursor()
    m="select longurl from urls where shorturl="+"\""+sturl+"\""
    cursor.execute(m)
    q=str(cursor.fetchone())
    con.close()
    b1=str(q)
    b2=b1.replace('(','')
    b3=b2.replace("'",'')
    b4=b3.replace(')','')
    print(b4)
    
    return redirect(b4)

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')