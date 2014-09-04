#!/usr/bin/env python

import random

print "Content-Type: text/html"
print
print """
<!DOCTYPE html>
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
        <!--<link rel="stylesheet" href="css/main.css">-->

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

<form action="answer.py" method="POST">
	<input type="hidden" name="answer" value="{0}">
	<label for="ding">Ding</label>
  	<input type="radio" name="note" id="ding" value="ding"><br>
	<label for="dong">Dong</label>
  	<input type="radio" name="note" id="dong" value="dong"><br>
	<label for="deng">Deng</label>
  	<input type="radio" name="note" id="deng" value="deng"><br>
	<label for="dung">Dung</label>
  	<input type="radio" name="note" id="dung" value="dung"><br>
	<label for="dang">Dang</label>
  	<input type="radio" name="note" id="dang" value="dang"><br>
  	<input type="submit" value='Submit Answer'>
</form>""".format(note)

print "</div>"


print """
    </body>
</html>
"""