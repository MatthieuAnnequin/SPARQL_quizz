#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 16:20:05 2023

@author: valentin
"""

from flask import Flask, render_template

from main import get_question

app = Flask(__name__)

@app.route("/")
def index():
    try:
        current_question = get_question()
    except:
        current_question ={
               'question': 'Fail',
                'optionA': '',
                'optionB': '',
                'optionC': '',
                'optionD': '',
                'correctOption': "optionD"
            }
    print(current_question)
    return render_template('index.html', currentQuestion = current_question)


@app.route("/fail")
def fail():
    return render_template('loser.html')


@app.route("/success")
def win():
    return render_template('winner.html')



if __name__ == '__main__':
    app.run(debug=True)