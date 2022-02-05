#!/usr/bin/env python3
import os
from flask import Flask, flash, jsonify, redirect, render_template, request, session

app = Flask(__name__)

@app.route("/")
def index():
    """ Index """
    # render index
    return render_template("index.html")

if __name__ == "__main__":
  app.run()