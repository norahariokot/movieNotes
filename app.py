import datetime
import os


from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from dotenv import load_dotenv
from werkzeug.security import check_password_hash, generate_password_hash
from scrapper import user_query

#from helpers import apology, login_required, lookup, usd, owned

# Configure application
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("app_secret_key")


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///movies.db")

@app.route("/")
def index():
    return render_template("index.html", current_route="/")

@app.route("/login")
def login():
     return render_template("index.html", current_route="/")


@app.route("/create_account")
def create_account():
    return render_template("create_account.html", current_route="/")


@app.route("/signedin")
def signedin():
    return render_template("signedin.html")    


@app.route("/search_page")
def search_page():
    search_page = True
    print("search page")
    return render_template("signedin.html", search_page=search_page)

@app.route("/search")
def search():
    q = request.args.get("q")
    if q:
        movies = user_query(q)
        #print(movies)
        print("movies receieved by flask function")
        for movie in movies:
            print(movie['title'])
    
    else:  
        movies = []
    return jsonify(movies)  


@app.route("/watch", methods=["POST"])
def watch():
    title = request.get_json()
    print(title)
    
    return jsonify(title)      



