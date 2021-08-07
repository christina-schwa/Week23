#!/usr/bin/env python

from flask import Flask, render_template
from flask_pymongo import PyMongo

# Create instance of Flask app
app = Flask(__name__)

# Connect to mongodb on default port, which is 27017
# Connect to shows_db, then tv_shows
app.config['MONGO_URI']='mongodb://localhost:27017/shows_db'
mongo=PyMongo(app)
tv_shows=mongo.db.tv_shows

#CREATE
@app.route("/create")
def input_show():
    # Creating with input variables
    show_name = input('What is the title of the show? ')
    seasons = input('How many seasons are there? ')
    duration = input('How long is each episode? ')
    year = input('What year did the first season premiere? ')

    post_data = {'name':show_name,
                'seasons':seasons,
                'duration':duration,
                'year':year,
                }
    tv_shows.insert_one(post_data)
    return render_template("index.html",data=post_data)

#READ
@app.route("/")
def read():
    show_list = list(tv_shows.find())
    for show in show_list:
        print(show)
    
    return render_template("index.html",data=show_list)

#UPDATE
@app.route("/update")
def update():
    show_name = input('What is the title of the show? ')
    seasons = input('How many seasons are there? ')
    duration = input('How long is each episode? ')
    year = input('What year did the first season premiere? ')

    # Filter by title to select show
    update_show = { 'name':show_name}
    
    # Values that need to be updated:
    update_data = {'$set':{'name':show_name,
                'seasons':seasons,
                'duration':duration,
                'year':year,
                }}

    # Use update_one() method to make individual update. 
    tv_shows.update_one(update_show, update_data)
    return render_template("index.html",data=post_data)

#DELETE
@app.route("/delete")
def delete():
    show_name = input('What is the title of the show? ')
    
    #delete_data = {'name':show_name}
    #tv_shows.delete_one(delete_data)

    # Will this work in one line (instead of the two above)?
    tv_shows.delete_one({'name':show_name})
    return render_template("index.html",data=post_data)

'''When I try to run this I get an "address already in use" 
error message, and I'm not sure why...'''

if __name__ == "__main__":
    app.run(debug=True)