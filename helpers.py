from flask import redirect, render_template, request, session
from functools import wraps

def require_login(f):
    """
    Decorate routes to require login.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def bail(errmsg, errcode):
    return render_template("error.html", errmsg=errmsg, errcode=errcode)