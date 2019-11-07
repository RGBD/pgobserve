from flask import Flask, escape, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('static', filename='index.html'))
