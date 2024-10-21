<img src="/static/Images/Movie Notes-logo/Movie Notes (4).png" alt="Movie Notes Logo, an illustration of a notebook" width="90" height="90">

# Movie Notes
**Movie Notes** is a web application that enables users to track their movie-watching experiences. With Movie Notes, users can easily maintain an organized record of movies they have watched, are currently watching, have favourited, and plan to watch all in one place.

The app also includes social features that allow users to connect with one another, chat, and share movie recommendations and experiences. This fosters a sense of community and helps users discover new movies through personalized recommendations.

Whether you are a casual viewer or a dedicated movie enthusiast, Movie Notes is a must-try!

## :bulb: Motivation for building Movie Notes
As a movie enthusiast, I often struggled to keep track of all the movies I had watched, my favourites, and those I planned to see in the future. I wanted a single place where I could organize my movie experiences—what I've watched, what I love, what I'm currently watching, and what I plan to watch next. Additionally, I wanted a way to easily store and access recommendations from friends and family so that I wouldn't forget them. Most importantly, I hoped to connect with fellow movie lovers and share our experiences. Movie Notes was built to bring all these elements together into one platform, making it easier to explore, organize, and enjoy movies while fostering a sense of community among movie enthusiasts.


## :rocket: Quick Start
To start using Movie Notes, click this link :link: https://movie-notes.onrender.com


## :open_book: Features of the application
**1. User Account Management:**
Movie Notes offers secure user authentication using `Flask-WTForms`. Users can create password-protected accounts with validation checks for secure login and logout, ensuring secure access to their personal data and movie experiences.

**2. Effortless and seamless Movie Discovery:**
Movie Notes streamlines movie discovery and tracking by allowing users to enter a movie title into a search bar, which triggers an HTTP request to IMDb.com using the `requests` library. The response is then processed with **Beautiful Soup** to extract key details like the title, release date, poster, and cast. This information is immediately displayed, enabling users to effortlessly add movies to their personalized sections: Watched, Currently Watching, Favourites, or Watchlist.

By utilizing HTTP requests and web scraping, Movie Notes ensures a smooth and intuitive movie-tracking experience for users.

**3. Dynamic Movie Categorization:**
Movie Notes lets you easily organize your movie experiences into Watched, Favourites, Watchlist, Currently Watching, and Recommendations sections. To add a movie to any of the sections, a user selects the section from a pop-up menu. The selected option triggers a `fetch` request, sending the movie data and chosen section to the server, where `Flask` processes the request and stores the information in a `SQLite` database, ensuring all sections are updated in real time.

**4. Organized Watched History**
Movie Notes allows users to organize movies in the Watched section by the date they were viewed. When selecting a movie to add, a date input menu appears, enabling users to specify when they watched it. This information is stored alongside the movie details in the `SQLite` database. Later, users can easily view their watched movies categorized by year and month, providing insights into their viewing history. 

**Note:** This feature is available only for movies that have a watched date recorded.

**5. Social Connectivity:**
Movie Notes also has social features that foster interaction among users and community. These social features include:
- **Friending Feature**  
  Users can connect with fellow movie enthusiasts by sending friend requests, once accepted, they become "Movie Buddies" and can view each other's movie notes. The status of these friendships is stored in the `SQLite` database.

- **In-App Chat**  
  The app features a chat feature that allows users can chat with their "Movie Buddies" directly within the app, fostering social interaction around shared movie experiences. 

- **Viewing Friends' Movie Notes**  
  Users can explore the movie notes of their "Movie Buddies", gaining insights into their preferences and recommendations. The app retrieves relevant data based on the user's friend sections stored in the database.

- **Making and Receiving Recommendations**  
  Users can recommend movies to Movie Buddies and view suggestions made to them, encouraging the sharing and the discovery of new movies. This feature tracks recommendations in the database, allowing users to access suggestions based on their connections.

## :handshake: Contributing to Movie Notes
If you would like to contribute to the Movie Notes App, please follow the steps below:
### 1. Fork the Repository:
Visit this URL on GitHub [Movie Notes Remote Repository on GitHub](https://github.com/norahariokot/movieNotes). Click on the "Fork" button in the upper right corner. This creates a copy of the repository under your GitHub account.

### 2. Set Up the Project Locally
Here's how to set up the project locally:

- #### Create a parent directory for your projects (if you don't already have one):
```
mkdir your-directory-name
```
> [!NOTE]
> Remember to replace your-directory-name with your desired name for the parent directory.

- #### Navigate to the newly created directory:
```
cd your-directory-name
```

- #### Clone the repository into that directory:
```
git clone https://github.com/your-username/repository-name.git
```
> [!NOTE]
> Remember to replace `repository-name` with the name of the repository being cloned.

- #### Then navigate to the cloned folder 
```
cd repository-name
```

- #### Configure Remotes:
Add the original repository as a remote to keep your fork up-to-date
```
git remote add upstream https://github.com/original-user/original-repo.git
```

- #### Create a Virtual Environment
  - On MacOS/Linux:
  ```
   python3 -m venv venv
  ```
  - On Windows:
  ```
   python -m venv venv
  ```
- #### Activate the Virtual Environment
  - On MacOS/Linux:
  ```
   source venv/bin/activate
  ```
  - On Windows:
  ```
   venv/bin/activate
  ```  

- #### Install the required dependencies:
```
pip install -r requirements.txt
```

- #### Set up Environment Variables:
Inside the project directory, there is a `.env`file to manage sensitive variables like secret keys. Assign a value to the `app_secret_key` variable. 
**Note**: Keep the value assigned to this variable confidential and do not share your `.env` file publicly.


- #### Create a branch
Before making changes, create a new branch to keep your work organised.
```
git checkout -b my-feature-branch
```

### 3. Upload Changes and Make a Pull Request:
- #### Commit Your Changes:
```
git add .
git commit -m "Brief description of the changes"
```

- #### Push Changes to Your Forked Repository:
```
git push origin my-feature-branch
```

- ### Create a Pull Request:
1. Navigate to the original repository on GitHub.
2. Click on the "Pull Requests" tab and then on "New Pull Request."
3. Select the branch from your forked repository and submit your pull request.





