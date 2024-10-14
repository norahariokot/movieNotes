<img src="/static/Images/Movie Notes-logo/Movie Notes (4).png" alt="Movie Notes Logo, an illustration of a notebook" width="90" height="90">

# Movie Notes
**Movie Notes** is a web application that enables users to track their movie-watching experiences. With Movie Notes, users can easily maintain an organized record of movies they have watched, are currently watching, have favorited, and plan to watch all in one place.

The app also includes social features that allow users to connect with one another, chat, and share movie recommendations and experiences. This fosters a sense of community and helps users discover new movies through personalized recommendations.

Whether you are a casual viewer or a dedicated movie enthusiast, Movie Notes is a must-try!

## :bulb: Motivation for building Movie Notes
As a movie enthusiast, I often struggled to keep track of all the movies I had watched, my favorites, and those I planned to see in the future. I wanted a single place where I could organize my movie experiences—what I've watched, what I love, what I'm currently watching, and what I plan to watch next. Additionally, I wanted a way to easily store and access recommendations from friends and family so that I wouldn't forget them. Most importantly, I hoped to connect with fellow movie lovers and share our experiences. Movie Notes was built to bring all these elements together into one platform, making it easier to explore, organize, and enjoy movies while fostering a sense of community among movie enthusiasts.


## :rocket: Quick Start
To start using Movie Notes, click this link :link: https://movie-notes.onrender.com


## :open_book: Usage - Features of the application
**User Account Management:**
Movie Notes offers secure user authentication using Flask-WTForms. Users can create password-protected accounts with validation checks for secure login and logout, ensuring secure access to thier personal data and movie experiences.

**Effortless and seamless Movie Discovery:**
Movie Notes streamlines the process of tracking your movie experiences. Simply enter a movie title into the search bar, and this query prompts an HTTP request to be sent to IMDb.com. The returned web page is then scraped using Beautiful Soup to extract essential details such as the movie title, release date, poster image, and cast.This automated process ensures you can effortlessly discover and add movies to the respective sections saving you time. 


## :handshake: Contributing
