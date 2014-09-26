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


def get_user(user):
    if user in sd:
        return { user : sd[user] }
    else:
        return { user : { 'score' : [0,0] }}


def read_data(): # need help with how to handle if there isn't a file
    try:
        with open('session/data.json') as f:
            session = json.load(f)
            return session
    except IOError:
        print "no session file exists"
        return False


def save_data(data):
    with open('session/data.json', 'w') as f:
        json.dump(data, f, indent = 4, sort_keys = True)


notes = ['ding', 'dong', 'deng', 'dung', 'dang']
w = web_input()
first = not w  # POST calls should have some input vars so must be GET
choice_made = bool(w.get('choice'))  # 'choice' will be missing if no radio button was pressed
wrong = choice_made and w['note'] != w['choice']  # test user selection against stored correct answer
sd = read_data() # returns data form json file
guest = bool('user' in w and w['user'] == '')
if 'user' in w and not guest:
    user = get_user(w['user'])
    u = user.keys()[0] # user name from json, first key
else:
    user = {}
    u = ''


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

if wrong:
    note = w['note']
else:
    temp_notes = list(notes)
    if not first:
        temp_notes.remove(w['note'])
    note = random.choice(temp_notes)

#  audio player
print """
<audio src="audio/{1}.mp3" {0} controls>
  <source src="audio/{1}.mp3" type="audio/mp3">
  <source src="audio/{1}.ogg" type="audio/ogg">
  <p>Your browser does not support the audio element.</p>
</audio>""".format("" if first else "autoplay", note)


#  form
print """<form action="" method="POST">"""

if first:
    print """
    <h4>Sign in or play as guest</h4>
    <label for="user">User</label>
    <input type="text" name="user" value="">
    <br><br>"""
else:
    print"""<input type="hidden" name="user" value="{0}">""".format(u)  
    print"""<h4>Select which note just played and click the submit button.</h4>"""

print"""<input type="hidden" name="note" value="{0}">""".format(note)

for n in notes:
    print """<label for="{0}">{1}</label>
    <input type="radio" name="choice" id="{0}" value="{0}"><br>""".format(n, n.capitalize())

print """<br><input type="submit" value='{}'>
</form>""".format("Sign In" if first else "Submit Answer")

print "</div>"

if first:
    pass
    
else:  # we only print a status on form submission
    if not choice_made:
        message = "Please select an answer"
    elif wrong:
        message = "Incorrect, try again"
        if not guest:
            user[u]['score'][1] += 1
    else:
        message = "Correct"
        if not guest:
            user[u]['score'][0] += 1

    print "<p><strong>{}</strong></p>".format(message)

    if 'user' in w:
        print '<p>Username is:', w['user'].capitalize() + "</p>"

    # print "<br>user: ", user
    # print "<br>user score: ", user[user.keys()[0]]['score']
    # print "<br>w: ", w
    # print "<br>is guest: ", guest
    # print "<br>correct: ", user[u]['score'][0]
    # print "<br>incorrect: ", user[u]['score'][1]
    if not guest:
        save_data(user)
        print "<p>Correct: {}".format(user[user.keys()[0]]['score'][0]) + " / " + "Incorrect: {}".format(user[user.keys()[0]]['score'][1]) + "</p>"


print """
    </body>
</html>
"""
