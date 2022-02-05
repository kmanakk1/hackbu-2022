from flask import redirect, render_template, request, session
from functools import wraps

def bail(errmsg, errcode):
    return render_template("error.html", errmsg=errmsg, errcode=errcode)