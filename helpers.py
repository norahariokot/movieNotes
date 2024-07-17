import json

from flask import redirect, session, request
from functools import wraps


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        #print(f"Accessing {request.path}: Session user_id: {session.get('user_id')}")
        if session.get("user_id") is None:
            print("User not authenticated, redirecting to login.")
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

movie_notes_sections = ["Watched", "Favourites", "Currently watching", "Watchlist", "Recommendations", "Movie Buddies"]

# sections to navigate the index page
section_links = {}
for section in movie_notes_sections:
    if " " in section:
        new_section = section.replace(" ", "_")
        section_link = "/" + new_section.lower() + "_section"
    else:
        section_link = "/" + section.lower() + "_section"
    section_links[section] = section_link    

# options for the pop up menu for search
search_options_list = [section for section in movie_notes_sections if section not in ["Recommendations","Movie Buddies"]]
search_options_list.append("Recommend")
#print(search_options_list)    
search_options = {}    
for option in search_options_list:
    if " " in option:
        new_search_option = option.replace(" ", "_")
        search_option = "/" + new_search_option.lower()
    else:
        search_option = "/" + option.lower()
    search_options[option] = search_option
#print(search_options)    

def extract_movie_info(movie_info):
    movie_title = movie_info["movie_title"]
    movie_year = movie_info["movie_year"]
    movie_stars = movie_info["movie_stars"]
    movie_poster = movie_info["movie_poster"]
    movie_poster_sizes = movie_info["movie_poster_sizes"]
    movie_poster_set = movie_info["movie_poster_set"]
    return movie_title, movie_year, movie_stars, movie_poster, movie_poster_sizes, movie_poster_set

#options for watched movie controls

# Convert search options dictionary to list of lists 
# To be used by buddy notes control options to create json data for controls
buddy_notes_options_list = []
for key, value in search_options.items():
    buddy_notes_option = []
    buddy_notes_option.append(key)
    buddy_notes_option.append(value)
    buddy_notes_options_list.append(buddy_notes_option)
#print(buddy_notes_options_list)
json_buddynotes_options = json.dumps(buddy_notes_options_list)
