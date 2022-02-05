#!/usr/bin/env python3
from flask import Flask, flash, jsonify, redirect, render_template, request, session, Blueprint
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
from tempfile import mkdtemp
import sqlite3

# user-made imports
from helpers import require_login, bail
from initialize import create_app, db

# Database stuff
#dbconn = sqlite3.connect("assignments.sqlite")
#db = dbconn.cursor()

# main blueprint
main = Blueprint('main', __name__)

@main.route("/")
def index():
    """ Index """
    # render index
    return render_template("index.html")

@main.route("/profile")
def profile():
    return "Profile"

def errorhandler(e):
    # Handle Errors
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return bail(e.name, e.code)

app = create_app()

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__ == "__main__":
    db.create_all(app=create_app()) # create and initialize database
    app.run()