#!/usr/bin/env python2.7
"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver

To run locally:

    python server.py

Go to http://localhost:8111 in your browser.

A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, send_from_directory

tmpl_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@w4111a.eastus.cloudapp.azure.com/proj1part2
#
# For example, if you had username gravano and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://gravano:foobar@w4111a.eastus.cloudapp.azure.com/proj1part2"
#
DATABASEURI = "postgresql://<userID>:<userPassword>vm.eastus.cloudapp.azure.com/w4111"

#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#
##### THIS IS THE SAMPLE
#####
#engine.execute("""CREATE TABLE IF NOT EXISTS test (
#  id serial,
#  name text
#);""")
#engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")


@app.before_request
def before_request():
    """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
    try:
        g.conn = engine.connect()
    except:
        print "uh oh, problem connecting to database"
        import traceback
        traceback.print_exc()
        g.conn = None


@app.teardown_request
def teardown_request(exception):
    """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
    try:
        g.conn.close()
    except Exception as e:
        pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/redditors')
def index():
    cursor = g.conn.execute("select R.author,count(C.id),url from mhv2109.redditor R left join mhv2109.comment C on R.id=C.author_id group by R.id order by R.author asc")
    names = []
    for result in cursor:
        names.append(result[0])  # can also be accessed using result[0]
        names.append(result[1])
        names.append(result[2])
    cursor.close()

    context = dict(data=names)
    return render_template("redditor.html", **context)


@app.route('/threads')
def threads():
    connect = g.conn.execute('select subreddit,author,title,url from mhv2109.thread')
    data1 = []
    for result in connect:
        data1.append(result[0])
        data1.append(result[1])
        data1.append(result[2])
	data1.append(result[3])
    connect.close()
    output = dict(data=data1)
    return render_template("thread.html", **output)


@app.route('/subreddits')
def subreddit():
    connect = g.conn.execute('select count(S.id),S.name,S.url from mhv2109.subreddit S left join mhv2109.thread T on S.id=T.subreddit_id group by s.name,S.url')
    data1 = []
    for result in connect:
        data1.append(result[0])
        data1.append(result[1])
        data1.append(result[2])
    connect.close()
    output = dict(data=data1)
    return render_template("subreddit.html", **output)

@app.route('/comments')
def comment():
    connect = g.conn.execute('select C.author,C.body,subreddit from mhv2109.comment C join mhv2109.thread T on C.thread_id=T.id ')
    data1 = []
    for result in connect:
        data1.append(result[0])
        data1.append(result[1])
        data1.append(result[2])
    connect.close()
    output = dict(data=data1)
    return render_template("comment.html", **output)

@app.route('/media')
def media():
    connect = g.conn.execute('select description,author_name,thumbnail_url from mhv2109.media')
    data1 = []
    for result in connect:
        data1.append(result[0])
        data1.append(result[1])
        data1.append(result[2])
    connect.close()
    output = dict(data=data1)
    return render_template("media.html", **output)

@app.route('/error')
def throwError():
    return render_template("error.html")

@app.route('/search/', methods=['GET'])
def search():
    if 'id' in request.args:
      if len(request.args['id']) < 1:
            return redirect("/error")
      else:
	if 't' in request.args and 's' in request.args and request.args['s'] == 't' and request.args['t'] == 'thread':
	  try:
            connect = g.conn.execute('select T.author,T.title,T.url from mhv2109.thread T join mhv2109.subreddit S on T.subreddit_id=S.id where S.name=\'' + request.args['id'] + '\'')
          except:
                return redirect("/error")
        elif 't' in request.args and 's' in request.args and request.args['s'] == 'f' and request.args['t'] == 'thread':
          try:
	    query = request.args['id'].replace (" ", "%%")
	    query = query.replace("\'", "")
            connect = g.conn.execute('select T.author,T.title,T.url from mhv2109.thread T join mhv2109.subreddit S on T.subreddit_id=S.id where T.title ilike \'%%' + query + '%%\'')
          except:
                return redirect("/error")
	elif 't' in request.args and request.args['s'] == 't' and request.args['t'] == 'comment':
	  try:
	    connect = g.conn.execute('select C.author,C.body,T.url from mhv2109.comment C join mhv2109.thread T on C.thread_id=T.id left join mhv2109.subreddit S on T.subreddit_id=S.id where S.name=\'' + request.args['id'] + '\'')
	  except:
		return redirect('/error')
	elif 't' in request.args and request.args['s'] == 'f' and request.args['t'] == 'comment':
          try:
            query = request.args['id'].replace (" ", "%%")
            query = query.replace("\'", "")
            connect = g.conn.execute('select C.author,C.body,T.url from mhv2109.comment C join mhv2109.thread T on C.thread_id=T.id left join mhv2109.subreddit S on T.subreddit_id=S.id where C.body ilike \'%%' + query + '%%\'')
          except:
                return redirect('/error')
        else: 
	  try:
            if 'q' in request.args and request.args['q'] == 'like':
                connect = g.conn.execute(
                    'select C.author,C.body,T.permalink from mhv2109.comment C join mhv2109.thread T on C.thread_id=T.id where C.author like \'%%'
                    + request.args['id'] + '%%\'')
            else:
                connect = g.conn.execute(
                    'select C.author,C.body,T.permalink from mhv2109.comment C join mhv2109.thread T on C.thread_id=T.id where C.author=\''
                    + request.args['id'] + '\'')
	  except:
		return redirect("/error")
        data1 = []
        for result in connect:
            data1.append(result[0])
	    data1.append(result[1])
            data1.append(result[2])
        connect.close()
        output = dict(data=data1)
        return render_template("search.html", **output)
    else:
        return render_template("newsearch.html")


@app.route('/medias')
def media_rw():
    return redirect('/media')


@app.route('/stats')
def stats_rw():
    return redirect('/')

@app.route('/')
def stats():
    connect = g.conn.execute(
        'SELECT \'redditor\' AS table_name, COUNT(*) FROM mhv2109.redditor UNION SELECT \'thread\' as table_name, COUNT(*) from mhv2109.thread UNION SELECT \'subreddit\' as table_name, COUNT(*) from mhv2109.subreddit UNION SELECT \'comment\' as table_name, COUNT(*) from mhv2109.comment UNION SELECT \'media\' as table_name, COUNT(*) from mhv2109.media ORDER BY table_name asc')
    data1 = []
    for result in connect:
        data1.append(result[0])
        data1.append(result[1])
    connect.close()
    output = dict(data=data1)
    return render_template("stats.html", **output)


@app.route('/another')
def another():
    return render_template("another.html")


@app.route('/about')
def about():
    return render_template("about.html")

#
# Create the application and bind for web access
#

if __name__ == "__main__":
    import click

    @click.command()
    @click.option('--debug', is_flag=True)
    @click.option('--threaded', is_flag=True)
    @click.argument('HOST', default='0.0.0.0')
    @click.argument('PORT', default=8111, type=int)
    def run(debug, threaded, host, port):
        """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

        HOST, PORT = host, port
        print "running on %s:%d" % (HOST, PORT)
        app.run(host=HOST, port=PORT, debug=debug, threaded=True)

    run()
