# Listnr

MCS 275 Project 4 by Hector Cedeno Indriago

## Assignment

Develop an application where 
users share the current or latest music pieces they listened to. 
The app consists of a home page displaying the latest posts, a ranking 
page where posts will be displayed according to their amount of votes, 
and an about page where information about the app can be found. 

Each post supports commenting and each post is clickable, meaning
each music piece will redirect to the page where it can be listened 
to if clicked on. Comments can be canceled. All posts and comments 
have timestamps and voting. Negative vote count is permitted to 
represent innappropriate posts or bad music pieces.

## How to test

*** The database can be resetted at any time using the app route
    /reset/ and the given port by Flask. E.g: http://127.0.0.1:5000/reset/
*** An existing .db file is not needed, the app will create a new one if
    necessary. 
*** The app can be tested intuitively too, for those who can't afford 
    reading for too long.

- Extract the static.zip file in the same directory as the .py file.
- Start the application using the Flask module for python/python3 
in Command Prompt/PowerShell. The module can be installed with pip.
- To test displaying the different pages, click on the buttons
at the top of the page, below the main header (Listnr). 
- To test voting, click the thumbs up/down icons. 
- To test posting, enter username, music, and URL in the indicated 
fields and click Share. The app should not accept an entry if any of
these fields is missing.
- To test the Timeline and Ranking functionalities, create two or three 
posts, with the older posts having the most votes. This way, the newest
post should be first in the Timeline, while the post with the most votes
should be first in the ranking.
- To test the commenting, click on "Add a comment..." next to the timestamp
of a post. Type in a username and a comment in the indicated fields, and click
the arrow button. If any of the two fields is missing, the app should ignore 
the request to.
- To test canceling a comment, click on "Add a comment..." and then click 
"Cancel" in the same place.
- To test the clickable post functionality, create a post with a valid URL
(YouTube), then click on the created post in the Timeline or Ranking.

## Personal contribution

Using Whinge.py as a starting point, I modified the entire style of the page
with CSS and icons, implemented a navigation bar, commenting, URL
referencing, added a Ranking and About page, wrote a JavaScript file from
scratch, and modified the database schema queries, along with variable naming
in all files.  

## Sources and credits

I ideated the app while working on Quiz 14 for this class.

The database initial main structure, voting and posting functionality, and the 
base HTML and CSS came from Whinge by David Dumas.

The icons for upvoting and downvoting came from a Google search on upvote icons.
The website is the following: https://dribbble.com/shots/6329261-User-Interface-2-2

I referenced w3schools while writing HTML and CSS, namely: HTML Input Types, HTML
DOM parentElement Property, HTML size Attribute, CSS Height and Width, HTML <input>
Tag, HTML <textarea> Tag, CSS Layout - Horizontal & Vertical Align, and HTML <button> Tag.

I referenced assignments of my own authoring for a different course, namely IT202,
when writing the JavaScript.

I referenced MDN Web Docs when writing the CSS and JavaScript for the app, namely
the documentation on the Node.removeChild() methor and on the cursor CSS property.

I referenced HTML.com when implementing the URL functionality using the HTML tag <a>
for it to open on a different browser tab. 

I referenced the following Stack Overflow question when implemented the JS for 
blocking form submission by pressing the "Enter" key: 
https://stackoverflow.com/questions/895171/prevent-users-from-submitting-a-form-by-hitting-enter

I referenced SQLite documentation on the SQLite Tutorial website when making modifications to
the data base.

