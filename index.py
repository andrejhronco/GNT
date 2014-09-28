#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import random
import cgitb
import json
cgitb.enable()


notes = ['ding', 'dong', 'deng', 'dung', 'dang']

def web_input():
    w = {}
    cl = os.getenv("CONTENT_LENGTH")
    if cl:
        data = sys.stdin.read(int(cl))
        for kv in data.split('&'):
            k, v = kv.split('=')
            w[k] = v.lower()
    return w


sd = None
def read_data():
    global sd
    try:
        with open('session/data.json') as f:
            sd = json.load(f)
    except IOError:
        #print "no session file exists"
        sd = {}

def get_user(user):
    if sd == None:
        read_data()
    if user in sd:
        return sd[user]
    else:
        return { 'score' : [0,0] }

def save_data(user_name, user_data):
    sd[user_name] = user_data        # updates user data
    with open('session/data.json', 'w') as f:
        json.dump(sd, f, indent = 4, sort_keys = True)


w = web_input()
login = not w  # POST calls should have some input vars so must be GET

def login_page():
  #  form
    print """
    <h4>Sign in or play as guest</h4>
    <label for="user">Username</label>
    <input type="text" name="user" value=""><br>
    <br>
    <br>
    <input type="submit" value="Sign In">
    """


def note_test():
    guest = bool('user' in w and w['user'] == '')
    first_test = 'note' not in w
    choice_made = bool(w.get('choice'))  # 'choice' will be missing if no radio button was pressed
    wrong = choice_made and w['note'] != w['choice']  # test user selection against stored correct answer

    if 'user' in w and not guest:
        user_name = w['user']
        user_data = get_user(user_name)
    else:
        user_name = ''
        user_data = {}

    if wrong:
        note = w['note']   # same note
    else:
        temp_notes = list(notes)
        if not first_test:
            temp_notes.remove(w['note'])
        note = random.choice(temp_notes)
        
    print """
    <audio src="audio/{1}.mp3" {0} controls>
      <source src="audio/{1}.mp3" type="audio/mp3">
      <source src="audio/{1}.ogg" type="audio/ogg">
      <p>Your browser does not support the audio element.</p>
    </audio><br>""".format("" if login else "autoplay", note)

    #  form
    if user_name:
        print """<input type="hidden" name="user" value="{0}">""".format(user_name)
        print """<h4>Select which note just played and click the submit button.</h4>"""
    print """<input type="hidden" name="note" value="{0}">""".format(note)

    for n in notes:
        print """<label for="{0}">{1}</label>
        <input type="radio" name="choice" id="{0}" value="{0}"><br>""".format(n, n.capitalize())

    print '<br><input type="submit" value="Submit Answer">\n'

    if not choice_made:
        message = "Please select an answer"
    elif wrong:
        message = "Incorrect, try again"
        if not guest:
            user_data['score'][1] += 1
    else:
        message = "Correct"
        if not guest:
           user_data['score'][0] += 1

    print "<p><strong>{}</strong></p>".format(message)

    if 'user' in w and not guest:
        print '<p>Username is:', w['user'].capitalize() + " <a href='/index.py'>logout</a></p>"

    if not guest:
        save_data(user_name, user_data)
        print "<p>Correct: {}".format(user_data['score'][0]) + " / " + "Incorrect: {}".format(user_data['score'][1]) + "</p>"


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

print '<form action="" method="POST">'

if login:
    login_page()
else:
    note_test()
    
print '</form>'

print "</div>"

print """
    </body>
</html>
"""
