#!/usr/bin/env python3
""" Created on Fri Dec 14 10:21:05 2018 @author: jklhj """

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()