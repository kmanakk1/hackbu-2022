#!/usr/bin/env python3
from flask import Flask, flash, url_for, jsonify, redirect, render_template, request, session, Blueprint
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from flask_login import login_user, logout_user, login_required, current_user
from tempfile import mkdtemp
import os

# custom imports
from helpers import bail, valid_filename, rand_str, date_str
from initialize import create_app, db
from models import Assignment, Answer

UPLOAD_DIR = "static/uploads/"

# main blueprint
main = Blueprint('main', __name__)

@main.route("/", methods=['GET', 'POST'])
def index():
    # render index
    search = request.args.get("search")
    textresults = ""
    if search:
        # do search
        dbresults = Assignment.query.filter(Assignment.name.like('%' + search + '%'))
    else:
        dbresults = Assignment.query
    for assign in dbresults:
        textresults = textresults + f"""
            <div class="assignment-card">
            <span><a href="/assign?id={assign.id}"><h4 class="assignment-card-link">{assign.name}</h4></a></span><br>
            <span>{assign.course}</span><br>
            <span>{assign.prof}</span><br>
            <span>{assign.date}</span><br>
            </div>
        """
    return render_template("homepage.html", results=textresults)

@main.route("/profile")
@login_required
def profile():
    return "Welcome, " + current_user.email + "!"

@main.route("/addassignment", methods=['GET', 'POST'])
@login_required
def addassignment():
    if(request.method == 'GET'):
        return render_template("addassignment.html")
    else:
        user = current_user.email
        a_name = request.form.get("name")
        a_course = request.form.get("class")
        a_prof = request.form.get("instructor")
        a_date = date_str(request.form.get("end-date"))

        # File upload
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for('main.addassignment'))
        file = request.files['file']
        
        if file.filename == '':
            flash('No selected file')
            return redirect(url_for('main.addassignment'))
        if file and valid_filename(file.filename):
            origfilen = secure_filename(file.filename)
            filename = rand_str(16) + "." + origfilen.split(".")[-1]
            file.save(os.path.join(UPLOAD_DIR, filename))
        #filename="doesnotexist.pdf"
        newAssignment = Assignment(user=user, name=a_name, course=a_course, prof=a_prof, date=a_date, file=filename)
        db.session.add(newAssignment)
        db.session.commit()
        return redirect(url_for('main.index', name=filename))

@main.route("/assign", methods=['GET'])
def assign():
    id = request.args.get("id")
    answers = ""
    if id:
        a = Assignment.query.filter_by(id=id).first()
        # get comments/answers
        dbresults = Answer.query.filter_by(assignment=id)
        for ans in dbresults:
            answers = answers + f"""
                <div class="answer-card">
                <span><h4 class="assignment-card-link">{ans.user}</h4></a></span><br>
                <span><form action="/vote" method="POST">
                <input type="hidden" value="{ans.id}" name="id"/>
                <input type="hidden" value="{id}" name="qid"/>
                <input type="submit" name="vote" value="Up"/>: {ans.upvote}, <input type="submit" name="vote" value="Down"/>: {ans.downvote}</span><br>
                </form>
                <span>{ans.response}</span><br>
                </div>
            """
        return render_template("assignmentpage.html", id=id, name=a.name, course=a.course, prof=a.prof,\
                 date=a.date, file="/" + UPLOAD_DIR + a.file, answers=answers)
    return bail("Invalid assignment", 404)

@main.route("/vote", methods=['GET', 'POST'])
@login_required
def vote():
    id = request.form.get("id")
    qid = request.form.get("qid")

    vote = request.form['submit_button']
    if id:
        ans = Answer.query.filter_by(id=id).first()
        if vote == "Up":
            ans.upvote += 1
        elif vote == "Down":
            ans.downvote += 1
        db.session.commit()
    return redirect(f"/assign?id={qid}")

@main.route("/post", methods=['GET', 'POST'])
@login_required
def post():
    id = request.form.get("assignid")
    response = request.form.get("answer")
    email = current_user.email
    if id:
        newPost = Answer(user=email, assignment=id, response=response)
        db.session.add(newPost)
        db.session.commit()
    return redirect(f"/assign?id={id}")

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
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    app.run()