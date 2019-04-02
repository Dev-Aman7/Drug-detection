import serial
import time# if you have not already done so
from flask import Flask,render_template,make_response, request, current_app  
from flask import request
from flask import json
from datetime import timedelta  
from functools import update_wrapper

ser = serial.Serial('com16', 9600)
app = Flask(__name__)


def crossdomain(origin=None, methods=None, headers=None, max_age=21600, attach_to_all=True, automatic_options=True):  
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, str):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, str):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator




@app.route("/")
def api_root():
    return  render_template('index.html')

@app.route('/temp',methods=['POST','GET'])
@crossdomain(origin='*')
def temp():
    content = request.form['cmd']
    print(content)  
    content1=request.form['key']
    print(content1)
    retval=""
    if(content=="write"):
        a="one"
        x=""
        ser.write(a.encode('utf-8'))
        while x!="end":
            #print("kkk")
            t2=ser.readline().strip().decode("utf-8")
            x=t2;
            if "Card UID:" in t2:
                retval+=t2[9:21]
                #retval.replace(" ", "")

            print(t2)
            if(t2=="tryagain"):
                ser.write("one".encode('utf-8'))
            #print(type(t2))
            if(t2=="type"):
               # print("hii")
                ser.write(content1.encode('utf-8'))
    else:
        print("in")
        x=""
        a="two"
        ser.write(a.encode('utf-8'))
        while x!="end":
            #print("infunc")
            t2=ser.readline().strip().decode("utf-8")
            if "Card UID:" in t2:
                retval=t2[9:]
            if "Name:" in t2:
                retval=retval+"~" + t2[5:]
                
            #print(t2)
            x=t2;
            if(t2=="tryagain"):
                #print("in1")
                ser.write(a.encode('utf-8'))
            print(t2)
    str(retval).replace(" ", "")
    return retval
    #print("jj")
    
if __name__=='__main__':
    app.run(debug=True)
    x,y=temp()
    print('came')
    print(x,y)
    
