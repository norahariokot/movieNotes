import datetime
import os
import json

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, g, session, jsonify
from flask_session import Session
from dotenv import load_dotenv
from werkzeug.security import check_password_hash, generate_password_hash
from scrapper import user_query
from forms import CreateUserForm, LoginForm
from helpers import login_required, section_links, search_options, extract_movie_info


# Configure application
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("app_secret_key")


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///movie_notes.db")

# Global variables
sections= section_links

@app.before_request
def before_request():
    g.db = db


@app.route("/")
@login_required
def index():
   
    #print(sections)
    return render_template("index.html", sections=sections)


@app.route("/login", methods=["GET", "POST"])
def login():
    print("Login route")
   
    login_form = LoginForm()
    print(login_form)

    #Ensure login info is validated and login form is submitted via POST request method
    if login_form.validate_on_submit():
        print("Login form validated")
        user = login_form.user_name.data
        
        # Query database for user info
        user_info =db.execute("SELECT * FROM users WHERE user_name = ?", user)
        
        # Remember which user has logged in
        if user_info:
            session.clear()
            session["user_id"] = user_info[0]['id']

        # Redirect user to the home page
        return redirect("/")

    return render_template("login.html", login_form=login_form, current_route="/login")




@app.route("/create_account", methods=["GET","POST"])
def create_account():
    #print("Reg form submitted")
    reg_form = CreateUserForm()
   
    # Ensure all user account registration is validated and account reg form is submitted via POST request method
    if reg_form.validate_on_submit():
        firstname = reg_form.first_name.data
        lastname = reg_form.last_name.data
        username = reg_form.user_name.data
        password = reg_form.password.data

        # Generate hash for password
        hash = generate_password_hash(password)

        # user registration data stored in users table in movie_notes db
        db.execute("INSERT INTO users (first_name, last_name, user_name, hash) VALUES (?,?,?,?)", firstname, lastname, username, hash)

        # user is then redirected to the login page
        return redirect('/')
    return render_template("create_account.html", reg_form=reg_form, current_route="/create_account")


@app.route("/signedin")
def signedin():
    return render_template("signedin.html")    


@app.route("/search_page")
def search_page():
    search_page = True
    search_page_options = search_options
    search_options_list= list(search_page_options.items())
    print(search_page_options)
    print(search_options_list)
    print("search page")
    return render_template("index.html", search_page=search_page, sections=sections, search_options_list=search_options_list)

@app.route("/search")
def search():
    q = request.args.get("q")
    if q:
        movies = user_query(q)
        #print(movies)
        #print("movies receieved by flask function")
        #for movie in movies:
            #print(movie['title'])
    
    else:  
        movies = []
    return jsonify(movies)  


@app.route("/watched", methods=["POST"])
def watched():
    print("Watched route followed")
    movie_info = request.get_json()
    print(movie_info)
    movie_title, movie_year, movie_stars, movie_poster, movie_poster_sizes, movie_poster_set = extract_movie_info(movie_info)
    watched_date = movie_info["date"]
    
    # retrieve data from database to check of data submitted already exists to avoid duplication
    movies_watched = db.execute ("SELECT movie_title, movie_year, movie_stars FROM watched where user_id = ?", session["user_id"])
    print(movies_watched)

    movies_watched_found = False
    for dict_item in movies_watched:
        if movie_title == dict_item["movie_title"] and movie_year == dict_item["movie_year"] and movie_stars == dict_item["movie_stars"]:
            movies_watched_found = True
            print("Movie already exits in this list")
            return jsonify({"message": "Movie already exists in the list"})
            break
    if not movies_watched_found:
        print("Not found") 
        db.execute("INSERT INTO watched (movie_title, movie_year, movie_stars, movie_poster, movie_poster_sizes, movie_poster_set, movie_watched_date, user_id) VALUES (?,?,?,?,?,?,?,?)", movie_title, movie_year, movie_stars, movie_poster, movie_poster_sizes, movie_poster_set, watched_date,  session["user_id"])
        
    return jsonify({"message": "Movie added successfully"})   


# Route to handle completed watching
@app.route("/completed_watch", methods=["POST"])
def completed_watch():
    print("Completed watching route")
    movie_info = request.get_json()
    print(movie_info)
    movie_title, movie_year, movie_stars, movie_poster, movie_poster_sizes, movie_poster_set = extract_movie_info(movie_info)
    watched_date = movie_info["date"]
    watched_route = movie_info["data_route"]
    data_id = int(movie_info["movie_data_id"])
    print(type(data_id))

    # Add movie to watched table in database
    # Ensure movie doesnt exist in watched before adding it to the database
    movies_watched = db.execute ("SELECT movie_title, movie_year, movie_stars FROM watched where user_id = ?", session["user_id"])
    #print(movies_watched)

    movies_watched_found = False
    for dict_item in movies_watched:
        if movie_title == dict_item["movie_title"] and movie_year == dict_item["movie_year"] and movie_stars == dict_item["movie_stars"]:
            movies_watched_found = True
            print("Movie already exits in this list")
            return jsonify({"message": "Movie already exists in your watched list"})
            break
    if not movies_watched_found:
        print("Not found") 
        # Insert movie into watched table
        db.execute("INSERT INTO watched (movie_title, movie_year, movie_stars, movie_poster, movie_poster_sizes, movie_poster_set, movie_watched_date, user_id) VALUES (?,?,?,?,?,?,?,?)", movie_title, movie_year, movie_stars, movie_poster, movie_poster_sizes, movie_poster_set, watched_date,  session["user_id"])
        
        # Delete movie after completing watching
        if watched_route == "Currently Watching":
            print(watched_route)
            db.execute("DELETE FROM currently_watching WHERE id = ?", data_id)

        elif watched_route == "Watch List":
            print(watched_route)
            db.execute("DELETE FROM watchlist WHERE id = ?", data_id)    
        return jsonify({"message":f"Movie added successfully added to your Watched List and removed from your {watched_route}"})  

    
@app.route("/delete_watched", methods=["POST"])
def delete_watched():
    print("Delete watched movie route")
    # Receive data from frontend via fetch function:
    movie_info = request.get_json()
    print(movie_info)

    # Retrieve id for data to delete
    movie_info_id = movie_info["movie_data_id"]
    print(movie_info_id)

    # Delete movie from watched table in data base
    db.execute("DELETE FROM watched WHERE id = ?", movie_info_id)
    return jsonify({"message": "Movie successfully removed from your Watched List"})

@app.route("/search_watched")   
def search_watched ():
    print("Search watched fired")
    q = request.args.get("q")
    if q:
        watched_search_response = db.execute("SELECT * FROM watched WHERE movie_title LIKE ? AND user_id = ?", "%" + q + "%", session["user_id"])
    else:
        watched_search_response = []
    #print(search_response) 
    for dict_item in watched_search_response:
        print(dict_item["movie_title"])   
    return jsonify(watched_search_response)
        

@app.route("/watched_section", methods=["GET"]) 
def watched_section():
    watched_section = True
    movie = db.execute ("SELECT *, strftime('%Y', movie_watched_date) AS WatchedYear, strftime('%m', movie_watched_date) AS WatchedMonth FROM watched WHERE user_id = ?", session["user_id"])
    watched_options = [["Favourites", "/favourites"], ["Recommend", "/recommend"], ["Delete", "/delete_watched"]]
    json_watched_options = json.dumps(watched_options)
    #print(watched_options)
    #print(movie)
    
    return render_template("index.html", watched_section=watched_section, sections=sections, movie=movie, json_watched_options=json_watched_options)   


@app.route("/favourites", methods=["POST"])
def favourites():
    print("Favourites route followed")
    movie_info= request.get_json()
    print(movie_info)
    movie_title, movie_year, movie_stars, movie_poster, movie_poster_sizes, movie_poster_set = extract_movie_info(movie_info)
    
    #Ensure that the movie doesnt already exit in user list before adding it to the db
    favourite_movies = db.execute("SELECT * FROM favourites WHERE user_id = ?", session["user_id"]) 
    print(favourite_movies)

    favourite_movie_exists = False
    for dict_item in favourite_movies:
        if movie_title == dict_item["movie_title"] and movie_year == dict_item["movie_year"] and movie_stars == dict_item["movie_stars"]:
            print("Favourite movie found")
            favourite_movie_exists = True
            return jsonify({"message": "Movie already exists in your Favourites list"})
            break
    if not favourite_movie_exists:
        print("Favourite movie not found")
        db.execute("INSERT INTO favourites(movie_title, movie_year, movie_stars, movie_poster, movie_poster_sizes, movie_poster_set, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)", movie_title, movie_year, movie_stars, movie_poster, movie_poster_sizes, movie_poster_set, session["user_id"])    

    return jsonify({"message": "Movie successfully added to your Favourites list"})  


@app.route("/delete_favourite", methods=["POST"])
def delete_favourite():
    print("Delete Favourite movie route")
    # Receive data from frontend via fetch function:
    movie_info = request.get_json()
    print(movie_info)

    # Retrieve id for data to delete
    movie_info_id = movie_info["movie_data_id"]
    print(movie_info_id)

    # Delete move from favourite table in database
    db.execute("DELETE FROM favourites WHERE id = ?", movie_info_id)
    return jsonify({"message": "Movie successfully deleted from your Favourites List"})


@app.route("/favourites_section", methods=["GET"])
def favourites_section():
    print("Favourites sections")
    favourite_section = True
    favourite_movies = db.execute("SELECT * FROM favourites WHERE user_id = ?", session["user_id"])
    favourite_ctl_options = [["Recommend", "/recommend"], ["Delete", "/delete_favourite"]]
    json_favourite_options = json.dumps(favourite_ctl_options)
    return render_template("index.html", favourite_section=favourite_section, sections=sections, favourite_movies=favourite_movies, json_favourite_options=json_favourite_options)


@app.route("/search_favourites")   
def search_favourites ():
    print("Search favourites fired")
    q = request.args.get("q")
    if q:
        favourites_search_response = db.execute("SELECT * FROM favourites WHERE movie_title LIKE ? AND user_id = ?", "%" + q + "%", session["user_id"])
    else:
        favourites_search_response = []
    #print(search_response) 
    for dict_item in favourites_search_response:
        print(dict_item["movie_title"])   
    return jsonify(favourites_search_response)
        


@app.route("/currently_watching", methods=["POST"])
def currently_watching():
    print("Currently_watching route followed")
    movie_info= request.get_json()
    print(movie_info)
    movie_title, movie_year, movie_stars, movie_poster, movie_poster_sizes, movie_poster_set = extract_movie_info(movie_info)
    
    # Ensure movie doesnt already exist in currently watching before adding it to database
    currently_watching_movies = db.execute("SELECT * FROM currently_watching WHERE user_id = ?", session["user_id"])

    currently_watching_exists = False
    for dict_item in currently_watching_movies:
        if movie_title == dict_item["movie_title"] and movie_year == dict_item["movie_year"] and movie_stars == dict_item["movie_stars"]:
            print("Currenlty watched movie found")
            currently_watching_exists = True
            return jsonify({"message": "Movie already exists in your Currently Watching list"})
            break
    if not currently_watching_exists:
        print("Currently watched movie not found")
        db.execute("INSERT INTO currently_watching(movie_title, movie_year, movie_stars, movie_poster, movie_poster_sizes, movie_poster_set, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)", movie_title, movie_year, movie_stars, movie_poster, movie_poster_sizes, movie_poster_set, session["user_id"])    

    return jsonify({"message": "Movie successfully added to Currently Watching List"}) 


@app.route("/delete_currentlywatching", methods=["POST"])
def delete_currentlywatching():
    print("Delete Currently watching route")
    # Receive data from frontend via fetch function:
    movie_info = request.get_json()
    print(movie_info)

    # Retrieve id for data to delete
    movie_info_id = movie_info["movie_data_id"]
    print(movie_info_id)

    # Delete move from currently_watching table in database
    db.execute("DELETE FROM currently_watching WHERE id = ?", movie_info_id)
    return jsonify({"message": "Movie successfully deleted from your Currently Watching List"})


@app.route("/currently_watching_section")
def currently_watching_section():
    print("Currently watching section")
    currently_watching = True
    currently_watching_movies = db.execute("SELECT *  FROM currently_watching WHERE user_id = ?", session["user_id"])    
    print(currently_watching_movies)
    currently_watching_options = [["Completed Watching", "/completed_watch"], ["Recommend", "/recommend"], ["Delete", "/delete_currentlywatching"]] 
    json_currently_watching_options = json.dumps(currently_watching_options)    
    return render_template("index.html", sections=sections, currently_watching=currently_watching, currently_watching_movies=currently_watching_movies, json_currently_watching_options=json_currently_watching_options) 


@app.route("/search_currentlyWatching")   
def search_currentlyWatching ():
    print("Search Currently watching fired")
    q = request.args.get("q")
    if q:
        currentlyWatching_search_response = db.execute("SELECT * FROM currently_watching WHERE movie_title LIKE ? AND user_id = ?", "%" + q + "%", session["user_id"])
    else:
         currentlyWatching_search_response = []
    #print(search_response) 
    for dict_item in currentlyWatching_search_response:
        print(dict_item["movie_title"])   
    return jsonify(currentlyWatching_search_response)



@app.route("/watchlist", methods=["POST"])
def watchlist():
    print("Watchlist route followed")
    movie_info= request.get_json()
    print(movie_info)
    movie_title, movie_year, movie_stars, movie_poster, movie_poster_sizes, movie_poster_set = extract_movie_info(movie_info)
    
    #Ensure movie doesnt already exist in watch list before adding it to the database
    watchlist_movies = db.execute("SELECT * FROM watchlist WHERE user_id=?", session["user_id"])

    watchlist_movie_exists = False
    for dict_item in watchlist_movies:
        if movie_title == dict_item["movie_title"] and movie_year == dict_item["movie_year"] and movie_stars == dict_item["movie_stars"]:
            print("Movie already in watchlist")
            watchlist_movie_exists = True
            return jsonify({"message": "Movie already exists in your Watch list"})
            break
    if not watchlist_movie_exists:
        print("Movie not in your  watch list")
        db.execute("INSERT INTO watchlist(movie_title, movie_year, movie_stars, movie_poster, movie_poster_sizes, movie_poster_set, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)", movie_title, movie_year, movie_stars, movie_poster, movie_poster_sizes, movie_poster_set, session["user_id"])    

    return jsonify({"message": "Movie successfully added to your Watch List"}) 


@app.route("/delete_watchlist", methods=["POST"])
def delete_watchlist():
    print("Delete Favourite movie route")
    # Receive data from frontend via fetch function:
    movie_info = request.get_json()
    print(movie_info)

    # Retrieve id for data to delete
    movie_info_id = movie_info["movie_data_id"]
    print(movie_info_id)

    # Delete move from watchlist table in database
    db.execute("DELETE FROM watchlist WHERE id = ?", movie_info_id)
    return jsonify({"message": "Movie successfully deleted from your Watch List"})





@app.route("/watchlist_section", methods=["GET"])
def watchlist_section():
    watchlist = True
    movies_in_watchlist = db.execute("SELECT * FROM watchlist WHERE user_id = ?", session["user_id"])
    watchlist_options = [["Completed Watching", "/completed_watch"], ["Delete", "/delete_watchlist"]] 
    json_watchlist_options = json.dumps(watchlist_options)
    return render_template("index.html", sections=sections, watchlist=watchlist, movies_in_watchlist=movies_in_watchlist, json_watchlist_options=json_watchlist_options)


@app.route("/search_watchlist")   
def search_watchlist ():
    print("Search Watchlist fired")
    q = request.args.get("q")
    if q:
        watchlist_search_response = db.execute("SELECT * FROM watchlist WHERE movie_title LIKE ? AND user_id = ?", "%" + q + "%", session["user_id"])
    else:
         watchlist_search_response = []
    #print(search_response) 
    for dict_item in watchlist_search_response:
        print(dict_item["movie_title"])   
    return jsonify(watchlist_search_response)




@app.route("/recommend", methods=["POST"])
def recommend():
    print("Recommend route followed")
    movie_info= request.get_json()
    print(movie_info)
    movie_title, movie_year, movie_stars, movie_poster, movie_poster_sizes, movie_poster_set = extract_movie_info(movie_info)
    
    print(movie_title)
    print(movie_year)
    print(movie_stars)
    print(movie_poster)
    print(movie_poster_sizes)
    print(movie_poster_set)

    return jsonify(movie_info)    


@app.route("/movie_buddies_section", methods=["GET"])
def moviebuddies_section():
    movie_buddies_section = True
    return render_template("index.html", movie_buddies_section=movie_buddies_section, sections=sections)



