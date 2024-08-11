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
from helpers import login_required, section_links, search_options, extract_movie_info, json_buddynotes_options


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
    return render_template("index.html", sections=sections, user_profile=session.get("user_profile"))


@app.route("/login", methods=["GET", "POST"])
def login():
    print("Login route")
   
    login_form = LoginForm()
    #print(login_form)

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

            
            user_profile = {}
            user_profile["full_name"] = user_info[0]['first_name'] +" " + user_info[0]['last_name']
            user_profile["user_name"] = user_info[0]['user_name']
            user_profile["profile_pic"] = user_info[0]['profile_pic']
            if user_profile["profile_pic"] == None:
                user_profile["profile_pic"] = "../static/Images/Icons/user_profile.png"

            session["user_profile"] = user_profile
            print(session["user_profile"])  
            print(session)  

            user_profile = session.get("user_profile")
            print(user_profile)
            
        


        # Redirect user to the home page
        return redirect("/")

    return render_template("login.html", login_form=login_form, current_route="/login")


@app.route("/logout")
def logout():
    """ Log user out """

    # forget user if of loggined user
    session.clear()

    # redirect user to login page
    return redirect("/login")




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
        profile_pic = "../static/Images/Icons/user_profile.png"

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
    print("search page")
    search_page = True
    
    return render_template("index.html", search_page=search_page, sections=sections, user_profile=session.get("user_profile"), json_buddynotes_options=json_buddynotes_options)

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
    movie_info_id = int(movie_info["movie_data_id"])
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
    watched_options = [["Favourites", "/favourites"], ["Recommend", "/buddy_recommend_info"], ["Delete", "/delete_watched"]]
    json_watched_options = json.dumps(watched_options)
    #print(watched_options)
    #print(movie)
    
    return render_template("index.html", watched_section=watched_section, sections=sections, movie=movie, json_watched_options=json_watched_options, user_profile=session.get("user_profile"))   


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
    movie_info_id = int(movie_info["movie_data_id"])
    print(movie_info_id)

    # Delete move from favourite table in database
    db.execute("DELETE FROM favourites WHERE id = ?", movie_info_id)
    return jsonify({"message": "Movie successfully deleted from your Favourites List"})


@app.route("/favourites_section", methods=["GET"])
def favourites_section():
    print("Favourites sections")
    favourite_section = True
    favourite_movies = db.execute("SELECT * FROM favourites WHERE user_id = ?", session["user_id"])
    favourite_ctl_options = [["Recommend", "/buddy_recommend_info"], ["Delete", "/delete_favourite"]]
    json_favourite_options = json.dumps(favourite_ctl_options)
    return render_template("index.html", favourite_section=favourite_section, sections=sections, favourite_movies=favourite_movies, json_favourite_options=json_favourite_options, user_profile=session.get("user_profile"))


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
    movie_info_id = int(movie_info["movie_data_id"])
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
    currently_watching_options = [["Completed Watching", "/completed_watch"], ["Recommend", "/buddy_recommend_info"], ["Delete", "/delete_currentlywatching"]] 
    json_currently_watching_options = json.dumps(currently_watching_options)    
    return render_template("index.html", sections=sections, currently_watching=currently_watching, currently_watching_movies=currently_watching_movies, json_currently_watching_options=json_currently_watching_options, user_profile=session.get("user_profile")) 


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
    movie_info_id = int(movie_info["movie_data_id"])
    print(movie_info_id)

    # Delete movie from watchlist table in database
    db.execute("DELETE FROM watchlist WHERE id = ?", movie_info_id)
    return jsonify({"message": "Movie successfully deleted from your Watch List"})





@app.route("/watchlist_section", methods=["GET"])
def watchlist_section():
    watchlist = True
    movies_in_watchlist = db.execute("SELECT * FROM watchlist WHERE user_id = ?", session["user_id"])
    watchlist_options = [["Completed Watching", "/completed_watch"], ["Delete", "/delete_watchlist"]] 
    json_watchlist_options = json.dumps(watchlist_options)
    return render_template("index.html", sections=sections, watchlist=watchlist, movies_in_watchlist=movies_in_watchlist, json_watchlist_options=json_watchlist_options, user_profile=session.get("user_profile"))


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

@app.route("/recommendations_section")
def recommendations_section():
    recommendations_section = True
    recommendations_info = db.execute("SELECT users.id AS user_id, first_name, last_name, user_name, profile_pic, recommendations.id AS recommendation_id, movie_title, movie_year, movie_stars, movie_poster, movie_poster_sizes, movie_poster_set FROM users JOIN recommendations ON users.id = recommender WHERE recommendie = ?", session["user_id"])
    print(len(recommendations_info))
    print(recommendations_info)

    recommendations = []
    for dict_item in recommendations_info:
        found = False
        user_name = []
        user_name_dict = {}
        if dict_item["profile_pic"] == None:
            dict_item["profile_pic"] = "../static/Images/Icons/user_profile.png"
        user_name_dict["user_id"]   = dict_item["user_id"]
        user_name_dict['first_name'] = dict_item['first_name']
        user_name_dict['last_name'] = dict_item['last_name']
        user_name_dict['user_name'] = dict_item['user_name']
        user_name_dict['profile_pic'] = dict_item['profile_pic']
        user_name.append(user_name_dict)
        dict_item['user_name'] = user_name
        dict_item.pop('first_name')
        dict_item.pop('last_name')
        dict_item.pop('profile_pic')
        for dict in recommendations:
            if dict_item["movie_title"] in dict["movie_title"]:
                print("Found")
                found = True 
                dict['user_name'].append(dict_item['user_name'][0])
        if found is False:
            recommendations.append(dict_item)
   
    print(recommendations)               
    
    recommendations_options = [["Watchlist", "/watchlist"], ["Delete", "/delete_recommendation"]]
    json_recommendations_options =json.dumps(recommendations_options)

    return render_template("index.html", recommendations_section=recommendations_section, sections=sections, recommendations=recommendations, json_recommendations_options=json_recommendations_options, user_profile=session.get("user_profile"))


@app.route("/delete_recommendation", methods=["POST"])  
def delete_recommendation():  
    print("Delete recommendation route fired")
    # Receive data from frontend / client via a fetch function
    recommendation_info = request.get_json()
    print(recommendation_info)

    # Retrieve id of movie in database
    recommended_movie_id = int(recommendation_info["movie_data_id"])
    print(recommended_movie_id)
    print(type(recommended_movie_id))

    # Delete movie from recommendations table in database
    db.execute("DELETE FROM recommendations WHERE id = ?", recommended_movie_id)
    
    return jsonify({"message": "Movie successfully deleted from your Recommendations"})

@app.route("/buddy_recommend_info")
def buddy_recommend_info():
    print("Buddy Recommend Info route followed")
    buddy_info = db.execute("SELECT users.id, first_name, last_name, user_name, profile_pic FROM users JOIN movie_buddies ON users.id = movie_buddies.buddy_request_sender WHERE (buddy_request_sender = ? OR buddy_request_recipient = ?) AND buddy_status = 'Movie Buddies' AND users.id!= ? UNION SELECT users.id, first_name, last_name, user_name, profile_pic FROM users JOIN movie_buddies ON users.id = movie_buddies.buddy_request_recipient WHERE (buddy_request_sender = ? OR buddy_request_recipient = ?) AND buddy_status = 'Movie Buddies' AND users.id!= ?", session["user_id"], session["user_id"], session["user_id"], session["user_id"], session["user_id"], session["user_id"])
    print(buddy_info)

    for dict_item in buddy_info:
        dict_item['full_name'] = dict_item['first_name'] + " " + dict_item['last_name']
        dict_item.pop('first_name')
        dict_item.pop('last_name')
        if dict_item['profile_pic'] == None:
            dict_item['profile_pic'] = "../static/Images/Icons/user_profile.png"
    
    return jsonify(buddy_info)  


@app.route("/recommend_movie", methods=["POST"])
def recommend_movie():
    print("Recommend movie route")
    recommend_info = request.get_json()
    print(recommend_info)

    # Convert the values of recommendies in recomend_info to integars because they were sent as a string from the fetch function
    recommend_to = []
    for item in recommend_info['recommendies']:
        id = int(item)
        recommend_to.append(id)
    print(recommend_to) 

    # Update the value of recommendies in recommend_info with the intergars
    recommend_info['recommendies'] = recommend_to
    #print(recommend_info)

    # Extract the data in recommend_info
    movie_title, movie_year, movie_stars, movie_poster, movie_poster_sizes, movie_poster_set = extract_movie_info(recommend_info)

    # Ensure not duplicates in the recommendations table
    # This will be done by running loop to check for existing data based on the recommendie and recommender for the same movie in table
    # a new list is created to store values of recommendies, if a record is found as duplicated its id will be removed from the new list which will store the updated values for recommendies in recommend_info
    new_recommend_to = recommend_to.copy()
    print(f"ids before checking for duplicates {new_recommend_to}")
    for id in recommend_to:
        already_recommended = db.execute("SELECT * FROM recommendations WHERE recommender = ? AND recommendie = ? AND movie_title = ? AND movie_year= ? AND movie_stars = ?", session["user_id"], id, movie_title, movie_year, movie_stars)
        #print(already_recommended)
        if already_recommended:
            print("Recommendaton found")
            new_recommend_to.remove(id)
    print(new_recommend_to)   

    # update recommendies in recommend_info with the values of ids which dont contain duplicates for a specific movie
    recommend_info['recommendies'] = new_recommend_to
    #print(recommend_info)

    for id in new_recommend_to:
        db.execute("INSERT INTO recommendations(movie_title, movie_year, movie_stars, movie_poster, movie_poster_sizes, movie_poster_set, recommender, recommendie) VALUES (?,?,?,?,?,?,?,?)", movie_title, movie_year, movie_stars, movie_poster, movie_poster_sizes, movie_poster_set, session["user_id"], id)  

    return jsonify({"message": "Movie successfully recommended"})





@app.route("/movie_buddies_section", methods=["GET"])
def moviebuddies_section():
    print("Movie Buddies section")
    movie_buddies_section = True

    #Retrieve movie buddies from database
    # Step 1: Retrieve the user ids of users who are movie buddies with current users from from movie_buddies table
    status = "Movie Buddies"
    movie_buddies = db.execute("SELECT * FROM movie_buddies WHERE (buddy_request_sender = ? OR buddy_request_recipient = ?) AND buddy_status = ?", session["user_id"], session["user_id"], status)
    print(movie_buddies)

    # Step 2: Retrieved values to be stored in a list
    movie_buddyid_list = []
    for dict_item in movie_buddies:
        if dict_item["buddy_request_sender"] == session["user_id"]:
            movie_buddyid_list.append(dict_item["buddy_request_recipient"])
        elif dict_item["buddy_request_recipient"] == session["user_id"]:
            movie_buddyid_list.append(dict_item["buddy_request_sender"])  
    print(movie_buddyid_list)   

    # Step 3 : Retrieve information about those users from users table
    movie_buddies_list = []
    for id in movie_buddyid_list:
        buddy_info = db.execute("SELECT id, first_name, last_name, user_name, profile_pic FROM users WHERE id = ?", id)
        print(buddy_info)
        
        id = buddy_info[0]["id"]
        name = buddy_info[0]["first_name"] + " " + buddy_info[0]["last_name"]
        user_name = buddy_info[0]["user_name"]
        profile_pic = buddy_info[0]["profile_pic"]
        print(profile_pic)
        if profile_pic == None:
            print("profile pic empty")
            profile_pic = "../static/Images/Icons/user_profile.png"

        buddy_dict = {}
        buddy_dict["id"] = id
        buddy_dict["name"] = name
        buddy_dict["user_name"] = user_name
        buddy_dict["profile_pic"] = profile_pic
        status = db.execute("SELECT buddy_status from movie_buddies WHERE (buddy_request_sender = ? OR buddy_request_recipient = ?) AND (buddy_request_sender = ? OR buddy_request_recipient = ?)", session["user_id"], session["user_id"], id, id)
        print(status)
        buddy_dict["buddy_status"] = status[0]["buddy_status"]
        movie_buddies_list.append(buddy_dict)
    print(movie_buddies_list)    

    return render_template("index.html", movie_buddies_section=movie_buddies_section, sections=sections, movie_buddies_list=movie_buddies_list, user_profile=session.get("user_profile"))


@app.route("/search_moviebuddies", methods=["GET"])    
def search_moviebuddies():
    print("Search Movie buddies fired")
    q = request.args.get("q")
    if q:
        movie_buddies_response = db.execute("SELECT id, first_name, last_name, user_name FROM users WHERE user_name LIKE ? AND NOT id = ?", "%" + q + "%", session["user_id"])
    else:
        movie_buddies_response = []
    print(movie_buddies_response) 

    # Look for Movie_buddy status for each user returned in the above search
    for dict_item in movie_buddies_response:
        print(f"Dict item is {dict_item}")
        movie_buddy_status = db.execute("SELECT * FROM movie_buddies WHERE (buddy_request_sender = ? OR buddy_request_recipient = ?) AND (buddy_request_sender = ? OR buddy_request_recipient = ?)", session["user_id"], session["user_id"], dict_item["id"], dict_item["id"])
        print(movie_buddy_status)
        
        if movie_buddy_status:
            for item in movie_buddy_status:
                print(f"Item is {item}")
                if item["buddy_status"] == "Movie Buddies":
                    dict_item["status"] = "Movie Buddy"
                elif item["buddy_status"] == "Request Sent":
                    if session["user_id"] == item["buddy_request_sender"] and dict_item["id"] ==  item["buddy_request_recipient"]:
                        dict_item["status"] = "Movie Buddy Request Sent"
                    elif session["user_id"] == item["buddy_request_recipient"] and dict_item["id"] ==  item["buddy_request_sender"]:
                        dict_item["status"] = "Accept Movie Buddy Request"
                elif item["buddy_status"] == "Request Declined":
                    if session["user_id"] == item["buddy_request_sender"] and dict_item["id"] ==  item["buddy_request_recipient"]:
                        dict_item["status"] = "Buddy Request Declined"
                    elif session["user_id"]  == item["buddy_request_recipient"] and dict_item["id"] == item["buddy_request_sender"]:
                        dict_item["status"] = "Send Movie Buddy Request"

        else:
            print("No status")
            dict_item["status"] = "Send Movie Buddy Request"       
        user_fullname = dict_item["first_name"] + " " + dict_item["last_name"]
        dict_item.pop('first_name', None)
        dict_item.pop('last_name', None)
        dict_item["full_name"] = user_fullname
    print(movie_buddies_response)   
    return jsonify(movie_buddies_response)


@app.route("/send_moviebuddy_request", methods=["POST"])
def send_moviebuddy_request():
    print("Send Movie Request route fired")

    request_recipient = request.get_json()
    print(request_recipient)

    # Check is uer is resending request
    resending_request = db.execute("SELECT * FROM movie_buddies WHERE buddy_request_sender = ? AND buddy_request_recipient = ? AND buddy_status = ?", session["user_id"], request_recipient, "Request Declined")
    print(resending_request)

    declined_now_sending_request = db.execute("SELECT * FROM movie_buddies WHERE buddy_request_sender = ? AND buddy_request_recipient = ? AND buddy_status = ?", request_recipient, session["user_id"],"Request Declined")
    print(declined_now_sending_request)

    status = "Request Sent"
    if resending_request:
        db.execute("UPDATE movie_buddies SET buddy_status = ? WHERE id = ?", status, resending_request[0]["id"])
        
    elif declined_now_sending_request:
        db.execute("UPDATE movie_buddies SET buddy_request_sender = ?, buddy_request_recipient = ?, buddy_status = ? WHERE id = ?", session["user_id"], request_recipient, status, declined_now_sending_request[0]["id"])    
    else:
        db.execute("INSERT INTO movie_buddies (buddy_request_sender, buddy_request_recipient, buddy_status) VALUES (?,?,?)", session["user_id"], request_recipient, status)

    return jsonify({"message": "Movie Buddy Request sent!"})


@app.route("/accept_moviebuddy_request", methods=["POST"])
def accept_moviebuddy_request():
    print("Accept Movie Request route fired")

    request_sender = request.get_json()
    print(request_sender)
    status = "Movie Buddies"
            
    db.execute("UPDATE movie_buddies SET buddy_status = ? WHERE buddy_request_sender = ? AND buddy_request_recipient = ?", status, request_sender, session["user_id"])

    return jsonify({"message": "Movie Buddies"})


@app.route("/decline_moviebuddy_request", methods=["POST"])
def decline_moviebuddy_request():
    print("Decline Movie Request route fired")

    request_sender = request.get_json()
    print(request_sender)
    status = "Request Declined"
            
    db.execute("UPDATE movie_buddies SET buddy_status = ? WHERE buddy_request_sender = ? AND buddy_request_recipient = ?", status, request_sender, session["user_id"])

    return jsonify({"message": "Movie Buddy Request Declined"})


@app.route("/view_movie_buddyrequests")    
def view_movie_buddyrequests():
    view_movie_buddyrequests = True
    print("View Movie Buddy requests")

    status = "Request Sent"
    movie_buddy_requests = db.execute("SELECT * FROM movie_buddies WHERE buddy_request_recipient = ? AND buddy_status = ?", session["user_id"], status)
    print(movie_buddy_requests)

    request_ids = []
    for dict_item in movie_buddy_requests:
        id = dict_item["buddy_request_sender"]
        request_ids.append(id)

    movie_buddy_requests_list = []
    for id in request_ids:
        buddy_request_info = db.execute("SELECT id, first_name, last_name, user_name FROM users WHERE id = ?", id)

        #Details of buddy request sender
        buddy_requestdict = {}
        buddy_requestdict["id"] = buddy_request_info[0]["id"]
        buddy_requestdict["name"] = buddy_request_info[0]["first_name"] + " " + buddy_request_info[0]["last_name"]
        buddy_requestdict["user_name"] = buddy_request_info[0]["user_name"]

        movie_buddy_requests_list.append(buddy_requestdict)
    
    print (movie_buddy_requests_list)   
    return render_template("index.html", sections=sections, movie_buddy_requests_list=movie_buddy_requests_list, view_movie_buddyrequests=view_movie_buddyrequests, user_profile=session.get("user_profile"))


@app.route("/send_request_for_buddy_movienotes", methods=["POST"])
def send_request_for_buddy_movienotes():
    print("Send request for buddy movie notes route")
    data = request.json

    #store the data in the session
    session["buddy_data"] = data
    print(session)
    return jsonify({"message": "View buddy movie notes granted"}), 200


@app.route("/view_buddy_movienotes")   
def view_buddy_movienotes():
    print("View buddy movie notes routes fired")
    buddy_data = session.get('buddy_data', None)
    print(buddy_data)
    buddy_id = buddy_data["id"]
    print(buddy_id)

    buddy_info_list = []
    if buddy_data:
        view_buddy_movienotes = True
        session["view_buddynotes"] = view_buddy_movienotes
        buddy_info = db.execute("SELECT id, first_name, last_name, user_name, profile_pic FROM users WHERE id = ?", buddy_id)
        print(buddy_info)

        buddy_info_dict = {}
        buddy_info_dict["id"] = buddy_info[0]["id"]
        buddy_info_dict["name"] = buddy_info[0]["first_name"] + " " + buddy_info[0]["last_name"]
        buddy_info_dict["username"] = buddy_info[0]["user_name"]
        buddy_info_dict["profile_pic"] = buddy_info[0]["profile_pic"]
        if buddy_info_dict["profile_pic"] == None:
            buddy_info_dict["profile_pic"] = "../static/Images/Icons/user_profile.png"
        session["buddy_notes_info"] = buddy_info_dict
        print(session["buddy_notes_info"])
        print(session)
        buddy_watched_notes = db.execute("SELECT * FROM watched WHERE user_id = ?", buddy_id)
        print(buddy_watched_notes)

    return render_template("index.html", sections=sections, view_buddynotes=session["view_buddynotes"], buddy_notes_info=session["buddy_notes_info"], buddy_watched_notes=buddy_watched_notes,json_buddynotes_options=json_buddynotes_options, user_profile=session.get("user_profile"))   


@app.route("/send_info_buddywatched", methods=["POST"])  
def send_info_buddywatched():
    print("Get buddy watched info")
    buddy_info = request.json
    print(buddy_info)  

    #store the data in the session
    session["buddy_watched_info"] = buddy_info
    print(session["buddy_watched_info"])
    return jsonify({"message": "View buddy watched notes info saved"})


@app.route("/view_buddy_watched")  
def view_buddy_watched():
    view_buddy_watched = True
    print("View buddy info watched")
    watched_info = session.get('buddy_watched_info', None)
    print(watched_info)
    watched_info_id = watched_info["id"]
    print(watched_info_id)

    buddy_watched_notes = db.execute("SELECT * FROM watched WHERE user_id = ?", watched_info_id)
    print(buddy_watched_notes)

    return render_template("index.html", sections=sections,view_buddy_watched=view_buddy_watched, buddy_watched_notes=buddy_watched_notes, view_buddynotes=session["view_buddynotes"], buddy_notes_info=session["buddy_notes_info"], json_buddynotes_options=json_buddynotes_options, user_profile=session.get("user_profile"))


@app.route("/send_info_buddy_favourites", methods=["POST"])
def send_info_buddy_favourites():
    print("Get buddy favourites info")
    buddy_info = request.json
    print(buddy_info)

    #store the data in the session
    session["buddy_favourites_info"] = buddy_info
    print(session["buddy_favourites_info"])
    return jsonify({"message": "View buddy favourites info saved"})


@app.route("/view_buddy_favourites")
def view_buddy_favourites():
    view_buddy_favourites = True
    print("View buddy favourites notes")
    favourites_info = session.get("buddy_favourites_info", None)
    print(favourites_info)
    favourites_info_id = favourites_info["id"]
    print(favourites_info_id)


    # Retrieve favourite movies of the user whose id is stored in favourites_info_id
    buddy_favourites_notes = db.execute("SELECT * FROM favourites WHERE user_id = ?", favourites_info_id)

    return render_template("index.html", sections=sections, view_buddy_favourites=view_buddy_favourites, buddy_favourites_notes=buddy_favourites_notes,view_buddynotes=session["view_buddynotes"], buddy_notes_info=session["buddy_notes_info"], json_buddynotes_options=json_buddynotes_options, user_profile=session.get("user_profile"))


@app.route("/send_info_buddy_currentlywatching", methods=["POST"])
def send_info_buddy_currentlywatching():
    print("Get buddy Currently watching info")
    buddy_info = request.json
    print(buddy_info)

    #store the data in the session
    session["buddy_currently_watching_info"] = buddy_info
    print(session["buddy_currently_watching_info"])
    return jsonify({"message": "View buddy currently watching info saved"})


@app.route("/view_buddy_currentlywatching")
def view_buddy_currentlywatching():
    view_buddy_currentlywatching = True
    print("View buddy Currently watching notes")
    currentlywatching_info = session.get("buddy_currently_watching_info", None)
    print(currentlywatching_info)
    currentlywatching_info_id = currentlywatching_info["id"]
    print(currentlywatching_info_id)


    # Retrieve favourite movies of the user whose id is stored in favourites_info_id
    buddy_currentlywatching_notes = db.execute("SELECT * FROM currently_watching WHERE user_id = ?", currentlywatching_info_id)


    return render_template("index.html", sections=sections, view_buddy_currentlywatching=view_buddy_currentlywatching, buddy_currentlywatching_notes=buddy_currentlywatching_notes,view_buddynotes=session["view_buddynotes"], buddy_notes_info=session["buddy_notes_info"], json_buddynotes_options=json_buddynotes_options, user_profile=session.get("user_profile"))


# View Function to display buddy chats
@app.route("/buddy_chats")  
def buddy_chats():
    buddy_chats = True 
    print("View Buddy Chats")

    return render_template("index.html", sections=sections, buddy_chats=buddy_chats, user_profile=session.get("user_profile"))

# View function to retrieve buddy info for buddy chats
@app.route("/chat_buddies_profile")   
def buddy_chat_profile():
    print("Buddy Chat Profile route fired")

    buddychat_profiles = db.execute("SELECT users.id, first_name, last_name, user_name, profile_pic FROM users JOIN movie_buddies ON users.id = movie_buddies.buddy_request_sender WHERE (buddy_request_sender = ? OR buddy_request_recipient = ?) AND buddy_status = 'Movie Buddies' AND users.id!= ? UNION SELECT users.id, first_name, last_name, user_name, profile_pic FROM users JOIN movie_buddies ON users.id = movie_buddies.buddy_request_recipient WHERE (buddy_request_sender = ? OR buddy_request_recipient = ?) AND buddy_status = 'Movie Buddies' AND users.id!= ?", session["user_id"], session["user_id"], session["user_id"], session["user_id"], session["user_id"], session["user_id"])
    print(buddychat_profiles)

    for dict_item in buddychat_profiles:
        dict_item['full_name'] = dict_item['first_name'] + " " + dict_item['last_name']
        dict_item.pop('first_name')
        dict_item.pop('last_name')
        if dict_item['profile_pic'] == None:
            dict_item['profile_pic'] = "../static/Images/Icons/user_profile.png"

    return jsonify(buddychat_profiles)        
        





















