#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import random
from random import randrange
import cgitb
cgitb.enable()

def rand(array):
    a = array[:]
    for i in xrange(len(a) - 1):
        j = random.randint(i + 1, len(a) - 1)
        a[i], a[j] = a[j], a[i]
    return a


def web_input():
    c = os.getenv("CONTENT_LENGTH")
    if c:
        data = sys.stdin.read(int(c))
        d = {}

        for kv in data.split('&'):
            k, v = kv.split('=')
            d[k] = v

        return d
    else:
        return {}

notes = ['ding', 'dong', 'deng', 'dung', 'dang']
d = web_input()
first = not any(d)  # POST calls should have some input vars so must be GET
choice_made = d.get('choice')  # 'note' will be missing if no radio button pressed
wrong = choice_made and d['note'] != d['choice']  # test user selection against stored correct answer

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
    note = d['note']
else:
    temp_notes = list(notes)
    if not first:
        temp_notes.remove(d['note'])
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
  <input type="hidden" name="org" value="gsj">
  <input type="hidden" name="user" value="andrej">
  <input type="hidden" name="note" value="{0}">
  """.format(note)

# notes = rand(notes) # maybe later, changes the order of inputs so you don't get used to an answer pattern
for n in notes:
    print """<label for="{0}">{1}</label>
    <input type="radio" name="choice" id="{0}" value="{0}"><br>""".format(n, n.capitalize())

print """<input type="submit" value='Submit Answer'>
</form>""".format(note)

print "</div>"


if not first: # we only print a status on form submission
    if not choice_made:
        message = "Please select an answer"
    elif wrong:
        message = "Incorrect, try again"
    else:
        message = "Correct"

    print "<p><strong>{}</strong></p>".format(message)

    if 'org' in d:
        print '<p>Organization name is:', d.get('org','').upper() + "</p>"

    if 'user' in d:
        print '<p>User name is:', d.get('user','').capitalize() + "</p>"
  
print """
    </body>
</html>
"""
