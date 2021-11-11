# MCS 275, Spring 2021, Project 4
# Hector Cedeno Indriago
# For sources and credits, refer to README.txt.
# I followed all the rules described on the 
# project description and course syllabus.

""" This program implements Listnr and its
    functionalities using Flask and SQLite. """
import sqlite3 as sql
from flask import Flask, url_for, request, redirect
import datetime
import time

app = Flask(__name__)

HEADER="""<!DOCTYPE html>
<html>
    <head>
        <title>Listnr</title>
        <link rel="stylesheet" href="/static/listnr.css">
    </head>

    <body>
        <h1>Listnr</h1>
        
        <div class="navigation">
            <span class="button"><a href="/home">Home</a></span>
            <span class="button"><a href="/ranking">Ranking</a></span>
            <span class="button"><a href="/about">About</a></span>
            <br>
        </div>
"""

FOOTER="""</div>
        <h3>Share music with everyone</h3>
        <div class="compose-form">
            <form action="/post" method="post">
                <div>
                    <label for="author">Username:</label>
                    <input type="text" placeholder="E.g: hceden, Hector, ..." id="author" name="author" size=30>
                </div>
                <div>
                    <label for="author">Music:</label>
                    <input type="text" placeholder="E.g: Queen - Bohemian Rhapsody" id="music" name="music" size="95">
                </div>
                <div>
                    <label for="author">URL:</label>
                    <input type="text" placeholder="E.g: https://www.youtube.com/watch?v=0OqZhwSRYwE" id="url" name="url" size="95"> 
                </div>
                <br>
                <input class="submit "type="submit" value="Share">
            </form>
            
        </div>
        <script src="/static/listnr.js"></script>
    </body>
</html>
"""

def get_db():
    """ Fetches the database """
    con = sql.connect("listnr.db")
    con.execute("""
CREATE TABLE IF NOT EXISTS posts (
    postid INTEGER PRIMARY KEY,
    author TEXT NOT NULL,
    content TEXT NOT NULL,
    url TEXT, 
    votes INTEGER DEFAULT 0,
    ts REAL NOT NULL,
    comment_id INTEGER DEFAULT 0
);
""")
    con.row_factory = sql.Row
    return con

def post_div(row):
    """ Create a post using data from db """
    timestr = datetime.datetime.fromtimestamp(row["ts"]).strftime("%Y-%m-%d %H:%M")

    DIV = """
<div id={7} class="post">
    <div class="post-main">
        <a class="post-agree" href="{5}"><img src="/static/upvote.png"></a>
        <span class="post-votes">{0}</span>
        <a class="post-disagree" href="{6}"><img src="/static/downvote.png"></a>
        <span class="post-content"><a href="{3}" target="_blank">{1}</a></span>
    </div>
    <div class="post-metadata">
        Posted by <span class="post-author">{2}</span> at <span class="post-timestamp">{4}</span>
        <span id="comment" class="comment" href="">Add a comment...</span>
    </div>
""".format(
        row["votes"],
        row["content"],
        row["author"],
        row["url"],
        timestr,
        url_for("agree", postid=row["postid"]),
        url_for("disagree", postid=row["postid"]),
        row["postid"]
    )

    return DIV

def post_comment(comment):
    """ Create a comment using data from db """
    timestr = datetime.datetime.fromtimestamp(comment["ts"]).strftime("%Y-%m-%d %H:%M")

    DIV = """
    <div class="post-comment">
        <span class="post-comment-content">{0}</span>
    </div>
    <div class="post-comment-metadata">
        <span class="post-author">{1}</span> commented on <span class="post-timestamp">{2}</span>
    </div>
""".format(
        comment["content"],
        comment["author"],
        timestr
    )

    return DIV

@app.route("/")
def root_redirect():
    """Root redirects to the home page"""
    return redirect(url_for("home"))

@app.route("/home/", methods=["GET", "POST"])
def home():
    """ Defines the Home page """
    con = get_db()
    document = HEADER
    document += """
        <h2>Timeline</h2>
"""
    if con:
        cur = con.execute("SELECT * FROM posts ORDER BY ts DESC LIMIT 10;")
        for row in cur.fetchall():
            if int(row["comment_id"]) != 0:
                continue
            else:
                document += post_div(row)
                postid = row["postid"]
                cur2 = con.execute("SELECT * FROM posts where comment_id=?", (postid,))
                for com in cur2.fetchall():
                    document += post_comment(com)
                document += """\n</div>"""
    con.close()
    document += FOOTER
    return document

@app.route("/ranking/", methods=["GET", "POST"])
def ranking():
    """ Defines the Ranking page """
    con = get_db()
    document = HEADER
    document += """
        <h2>Ranking</h2>
"""
    if con:
        cur = con.execute("SELECT * FROM posts ORDER BY votes DESC LIMIT 10;")
        for row in cur.fetchall():
            if int(row["comment_id"]) != 0:
                continue
            else:
                document += post_div(row)
                postid = row["postid"]
                cur2 = con.execute("SELECT * FROM posts where comment_id=?", (postid,))
                for com in cur2.fetchall():
                    document += post_comment(com)
                document += """\n</div>"""
    con.close()
    document += """
    </body>
</html>   
"""
    return document

@app.route("/about/",methods=["GET","POST"])
def about():
    """ Defines the about page. """
    document = HEADER
    document += """
        <h2>About this app</h2>
        <p class="about">
            This app was developed by Hector Cedeno Indriago for the MCS 275 course in <br>
            the University of Illinois-Chicago during the Spring 2021 semester. This app <br>
            serves as a platform where users can share any music they would like.<br><br>
            Each post needs a URL, for ease of access to your favorite music. This is so each 
            post can be clickable, and doing so redirects you to the page with <br> the music.<br><br>
            Please make sure to use appropiate usernames, post positive content, and use <br> 
            valid, safe URLs!<br><br>
            Hector Cedeno Indriago<br>
            E-mail: hcedenoindriago@gmail.com
        </p>
    </body>
</html>
"""
    return document

@app.route("/post",methods=["GET","POST"])
def create_post():
    """Receive form data and add a new post to the database"""

    # Check for and reject empty author, music, or URL
    if not request.values.get("author") or not request.values.get("music"):
        print("Ignoring request to with empty author or music")
    elif not request.values.get("url"):
        print("Ignoring request to with empty URL")
    else:
        con = get_db()
        con.execute("INSERT INTO posts (author,content,url,ts) VALUES (?,?,?,?);",
            (
                request.values.get("author"), 
                request.values.get("music"), 
                request.values.get("url"),
                time.time()
            )
        )
        con.commit()
        con.close()

    return redirect(url_for("home"))

@app.route("/comment", methods=["GET", "POST"])
def create_comment():
    """ Receive form data and add a new comment (post) to the database """
    if not request.values.get("author") or not request.values.get("comment"):
        print("Ignoring request to with empty author or music")
    else:
        postid = request.values.get("postid")
        con = get_db()
        con.execute("""INSERT INTO posts (author,content,ts,comment_id) VALUES (?,?,?,?);""", 
            (   
                request.values.get("author"),
                request.values.get("comment"),
                time.time(),
                postid
            )
        )
        con.commit()
        con.close()

    return redirect(url_for("home"))
    
@app.route("/agree")  
def agree():
    """Find a post by `postid` and increase its score by one."""

    postid = request.values.get("postid")
    con = get_db()
    con.execute("""
    UPDATE posts SET votes=votes+1 WHERE postid=?;
    """,
    (postid,))
    con.commit()
    con.close()
    return redirect(url_for("home"))

@app.route("/disagree")
def disagree():
    """Find a post by `postid` and decrease its votes by one."""
    postid = request.values.get("postid")
    con = get_db()
    con.execute("""
    UPDATE posts SET votes=votes-1 WHERE postid=?;
    """,
    (postid,))
    con.commit()
    con.close()
    return redirect(url_for("home"))

@app.route("/reset/")
def db_reset():
    """ Resets the database, Only doable from browser. """
    con = get_db()
    con.execute("""
    DROP TABLE IF EXISTS posts;
    """)    
    con.close()
    return redirect(url_for("home"))


if __name__=="__main__":
    app.run()

