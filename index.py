#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import random
import cgitb
import json
cgitb.enable()


def web_input():
    w = {}
    cl = os.getenv("CONTENT_LENGTH")
    if cl:
        data = sys.stdin.read(int(cl))
        for kv in data.split('&'):
            k, v = kv.split('=')
            w[k] = v
    return w


# check to see if there is a file
# load json into a var
# check file for first key name
# set this name to the 'u' var

# if no file exists we start from scratch, which happens after first submit of name, and answer
# set 'u' to d['user']
# use format_json to generate and return json structure

# this function : {'username': {'score': ['correct n', 'incorrect n']}}
def format_json(session):
    j = {}
    correct = 0
    incorrect = 0
    if session:
        u = session.keys()[0]
        correct = session[u]['score'][0]
        incorrect = session[u]['score'][1]
    elif 'user' in w:
        u = w['user']

    j[u] = {'score': [correct, incorrect]}

    return j



def save_data(data):
    with open('session/data.json', 'wb') as f:
        json.dump(data, f, indent = 4, sort_keys = True)


def read_data():
    try:
        with open('session/data.json') as f:
            session = json.load(f)
            return session
    except IOError:
        print "no session file exists"
        return False


notes = ['ding', 'dong', 'deng', 'dung', 'dang']
w = web_input()
first = not w  # POST calls should have some input vars so must be GET
choice_made = bool(w.get('choice'))  # 'choice' will be missing if no radio button was pressed
wrong = choice_made and w['note'] != w['choice']  # test user selection against stored correct answer
sd = read_data()
j = format_json(sd)
u = j.keys()[0] or "guest"

print "Content-Type: text/html"
print
print """<!DOCTYPE html>
<!--[if lt IE 7]>      <html class="no-js lt-ie9 lt-ie8 lt-ie7"> <![endif]-->
<!--[if IE 7]>         <html class="no-js lt-ie9 lt-ie8"> <![endif]-->
<!--[if IE 8]>         <html class="no-js lt-ie9"> <![endif]-->
<!--[if gt IE 8]><!--> <html class="no-js"> <!--<![endif]-->
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
        <title>Gamelan Note Tester</title>
        <meta name="description" content="">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <!--<link rel="stylesheet" href="css/normalize.min.css">-->
        <!--<link rel="stylesheet" href="css/app.css">-->

        <!--<script src="js/vendor/modernizr-2.6.2.min.js"></script>-->
    </head>
    <body>
"""

print "<div id='container'>"
# print read_data()
# print session

if wrong:
    note = w['note']
else:
    temp_notes = list(notes)
    if not first:
        temp_notes.remove(w['note'])
    note = random.choice(temp_notes)

#  audio player
print """
<audio src="audio/{0}.mp3" autoplay controls loop> # autoplay - removed for now for silence...hah
  <source src="audio/{0}.mp3" type="audio/mp3">
  <source src="audio/{0}.ogg" type="audio/ogg">
  <p>Your browser does not support the audio element.</p>
</audio>""".format(note)

#  form
print"""
<h3>Select which note just played and click the submit button.</h3>

<form action="" method="POST">
  <label for="user">User</label>
  <input type="text" name="user" value="">
  <input type="hidden" name="note" value="{0}"><br><br>
  """.format(note)

for n in notes:
    print """<label for="{0}">{1}</label>
    <input type="radio" name="choice" id="{0}" value="{0}"><br>""".format(n, n.capitalize())

print """<br><input type="submit" value='Submit Answer'>
</form>""".format(note)

print "</div>"

if first:

    # check to see if there is a first key in the json file, which represents the user
    # if 'user' in sd:
    #     print "Hello {}, would you like to continue from your last session?".format(sd['user'])
    #     j[sd['user']] = []
    # else:
    #     print "Start new game"

    print j
    
else:  # we only print a status on form submission
    if not choice_made:
        message = "Please select an answer"
    elif wrong:
        message = "Incorrect, try again"
        j[u]['score'][1] += 1
    else:
        message = "Correct"
        j[u]['score'][0] += 1

    print "<p><strong>{}</strong></p>".format(message)

    if 'user' in w:
        print '<p>Username is:', w['user'].capitalize() + "</p>"

    print "j: ", j
    print "correct: ", j[u]['score'][0]
    print "incorrect: ", j[u]['score'][1]
    save_data(j)


print """
    </body>
</html>
"""
