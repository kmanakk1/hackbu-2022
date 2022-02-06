from flask import redirect, render_template, request, session
from functools import wraps
from datetime import datetime
import string    
import random
VALID_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def bail(errmsg, errcode):
    return render_template("error.html", errmsg=errmsg, errcode=errcode)

def valid_filename(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in VALID_EXTENSIONS

def rand_str(len):  
    rand = ''.join(random.choices(string.ascii_uppercase + string.digits, k = len))
    return rand

def date_str(str):
    if str:
        return datetime.fromisoformat(str)