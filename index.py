#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import random
import cgi
import cgitb
cgitb.enable()

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
notes = ['ding', 'dong', 'deng', 'dung', 'dang']

note = random.choice(notes)


print "<div id='container'>"

#  audio player
print """
<audio src="audio/{0}.mp3" controls autoplay loop>
  <source src="audio/{0}.mp3" type="audio/mp3">
  <source src="audio/{0}.ogg" type="audio/ogg">
<p>Your browser does not support the audio element </p>
</audio>""".format(note)

#  form
print"""
<h3>Select which note just played and click the submit button.</h3>

<form action="" method="POST">
  <input type="hidden" name="answer" value="{0}">
  """.format(note)

for n in notes:
  print '''<label for="{0}">{1}</label>
  <input type="radio" name="note" id="{0}" value="{0}"><br>'''.format(n, n.capitalize())

print """<input type="submit" value='Submit Answer'>
</form>""".format(note)

print "</div>"

def print_list_html(l):
  for s in l:
    print cgi.escape(s)
    print '<br>'

#print "Content Length:", os.getenv("CONTENT_LENGTH")
cl = os.getenv("CONTENT_LENGTH")
if cl:
  data = sys.stdin.read(int(cl))
  parts = data.split("&")

  t = []
  for bits in parts:
    kv = bits.split("=")
    t.append(kv[1])

  if t[0] == t[1]:
    print "Correct!"
  else:
    print "Wrong"

  print '<br><a href="/index.py">Try Again!</a>'

print """
    </body>
</html>
"""
