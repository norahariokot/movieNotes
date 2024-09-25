let recommendie_ids = []; // This list is being defined here to store ids for recommendie buddies. It is in outer scope to retain state

// Function to create pop menu for section control buttons       
let isSectionPopupVisible = false;
let section_popup_menu;
let section_popup_menu_div;

document.addEventListener('click', function(event) {
    console.log(event.target);
    let element = event.target;
     
    // Target the control buttons in the search page and section pages
    if (event.target.matches('.section-controls')) {
        console.log("section options button clicked");
        if(isSectionPopupVisible && !section_popup_menu.contains(event.target)) {
            //remove popup menu
            section_popup_menu.remove();
            isSectionPopupVisible = false;
        } 
        else {
                section_popup_menu_div = document.createElement("div");
                if (event.target.id == 'recommendations-stn-ctls') {
                    section_popup_menu_div.className = "recommendations-popup-menu-wrapper";
                }

                else {
                    section_popup_menu_div.className = "section-popup-menu-wrapper";
                }                
                section_popup_menu = document.createElement("ul");
                if (event.target.id == 'recommendations-stn-ctls') {
                    section_popup_menu.className = "recommendations-popup-menu-list";
                }

                else {
                    section_popup_menu.className = "section-popup-menu-list";
                }  
                
                section_popup_menu
                let section_options_list;
                 
                // Add diffrent popup options to deferent links 
                if (event.target.id == 'watched-stn-ctls') {
                    console.log(event.target)
                    section_options_list = JSON.parse(document.getElementById('watched-options-list').innerText);                
                } 
                else if (event.target.id == "favourite-stn-ctls") {
                        console.log("Favourites sections options")
                        section_options_list = JSON.parse(document.getElementById('favourite-options-list').innerText);
                } 
                else if (event.target.id == "currentlywatching-stn-ctls") {
                    section_options_list = JSON.parse(document.getElementById('currentlywatching-options-list').innerText);
                } 
                else if (event.target.id == "watchlist-stn-ctls") {
                    section_options_list = JSON.parse(document.getElementById('watchlist-options-list').innerText);
                } 
                else if (event.target.id == "buddy-watched-stn-ctls") {
                    section_options_list = JSON.parse(document.getElementById('buddynotes-options-list').innerText);
                } 
                else if (event.target.id == "recommendations-stn-ctls") {
                    section_options_list = JSON.parse(document.getElementById('recommendations-sections-list').innerText);
                }               
                console.log(section_options_list)

                let section_options = {}
                section_options_list.forEach(list_item => {
                    section_options[list_item[0]] = list_item[1]
                });
              
                let section_list_options = [];
                for (let key in section_options) {
                    let section_popup_options = document.createElement("li");
                    section_popup_options.className = "popup-menu-li";
                    let section_link = document.createElement("a");
                    section_link.href = section_options[key];
                    section_link.innerText = key;
                    section_popup_options.appendChild(section_link);
                    section_popup_menu.appendChild(section_popup_options);
                    section_list_options.push(section_popup_options);
                }
          
                // Append pop-up menu to the DOM
                section_popup_menu_div.appendChild(section_popup_menu);
                if (event.target.id == "recommendations-stn-ctls") {
                    event.target.parentNode.parentNode.parentNode.parentNode.insertAdjacentElement('afterend', section_popup_menu_div);
                    console.log(event.target.parentNode.parentNode.parentNode)
                    isSectionPopupVisible = true;
                }
                else {
                    event.target.parentNode.parentNode.parentNode.insertAdjacentElement('afterend', section_popup_menu_div);
                    console.log(event.target.parentNode.parentNode.parentNode)
                    isSectionPopupVisible = true;
                }
              
                // Create elements to add watched date elements
                let section_watched_date = null;
                let section_date_div = document.createElement("div");
                section_date_div.className = "watched-date-div";
                let section_date_lbl = document.createElement("label");
                let section_date = document.createElement("input");
                section_date_lbl.innerText = "Include date";
                section_date.type = "date";
                section_date.id = "watched-date";
                section_date.className = "section-watched-date";
                section_date_div.appendChild(section_date_lbl);
                section_date_div.appendChild(section_date);
                section_date_div.style.display = "none"
                section_popup_menu.insertAdjacentElement('afterend', section_date_div);

                section_list_options.forEach(list_option => {
                    //console.log(list_option.firstChild.innerText)
                    if(list_option.firstChild.innerText == "Add to Watched") {
                        console.log("Completed watching or watched found")
                 
                        list_option.addEventListener('mouseover', function() {
                            section_date_div.style.display = "block"; 
                        });

                        section_date_div.addEventListener('mouseover', function() {
                            section_date_div.style.display = "block";
                        });

                        section_date_div.addEventListener('mouseout', function() {
                            section_date_div.style.display = "none";
                        });
                   }
                })

                // Create a pop up menu for recommending movie for movie buddies
                let buddy_recommendations_div = document.createElement('div');
                buddy_recommendations_div.className = 'buddy_recommendations_div';
                buddy_recommendations_div.id = 'recommendations_options';
                let recommend_btn = document.createElement('button');
                recommend_btn.innerHTML = 'Recommend';
                recommend_btn.id = 'recommend_btn';
                let close_recommend = document.createElement('button');
                let close_img = document.createElement('img');
                close_img.src = "../static/Images/Icons/close.png";
                close_img.id = "recommendations-close-btn";
                let recommendations = document.createElement('div');
                recommendations.className = 'recommendations-div';

                close_recommend.appendChild(close_img);
                buddy_recommendations_div.appendChild(close_recommend);
                buddy_recommendations_div.appendChild(recommendations);
                buddy_recommendations_div.appendChild(recommend_btn);
                buddy_recommendations_div.style.display = "none";
                section_popup_menu_div.insertAdjacentElement('afterend', buddy_recommendations_div)
              
                //Add event handlers to all links in the list items to send data to the server side
                for(let i = 0; i < section_list_options.length; i++) {
                    console.log(i);
                    section_list_options[i].firstChild.addEventListener('click', function(event) {
                        event.preventDefault();
                        console.log(event.target);
                        
                        if(section_list_options[i].firstChild.innerText == "Recommend to Buddy") {
                            fetch("/buddy_recommend_info")
                            .then(response => {
                               // Convert the response to JSON
                               console.log("buddy recommendation info returned")
                               return response.json();                                
                            })
                            .then(recommend_to => {
                                //Process the JSON data
                                console.log(recommend_to); 
                                let cleared_div = document.querySelectorAll(".recommendations-div");
                                console.log(cleared_div)
                                for (let i = 0; i < cleared_div.length; i++) {
                                    cleared_div[i].innerHTML = " ";
                                }
                                section_popup_menu_div.style.display = "none";
                                buddy_recommendations_div.style.display = "block";
                            
                                recommend_to.forEach(data_item => {
                                    console.log(data_item);
                                    let recommendie_wrapper = document.createElement('div');
                                    recommendie_wrapper.className = "recommendie_wrapper";

                                    let checkbox_div = document.createElement('div');
                                    checkbox_div.className = "checkbox-div";

                                    let checkbox = document.createElement('input');
                                    checkbox.className = 'checkbox';
                                    checkbox.type = 'checkbox';
                                    checkbox_div.appendChild(checkbox);
                                    // Add click event listner to the checkboxes
                                               
                                    checkbox.addEventListener('change', function(event) {
                                        let item = event.target;
                                        let data_item = item.parentNode.nextElementSibling.children[1].children[0].innerText;
                                        console.log(item);
                                        if(item.checked) {
                                            console.log("checkbox checked");
                                            console.log(data_item);
                                            recommendie_ids.push(data_item);
                                            console.log("click event added to checkbox")
                                        }
                                        else {
                                            console.log("checkbox unchecked");
                                            let index = recommendie_ids.indexOf(data_item);
                                            if(index !== -1) {
                                                recommendie_ids.splice(index, 1)
                                            }
                                        }
                                    });
                                    
                                    let recommendie_div = document.createElement('div');
                                    recommendie_div.className = 'recommendie_div';

                                    let recommendie_profile = document.createElement('div');
                                    recommendie_profile.className = 'recommendie_profile_div';

                                    let profile_pic = document.createElement('img');
                                    profile_pic.className = 'recommendie_profile_pic';
                                    profile_pic.src = data_item.profile_pic;
                                    recommendie_profile.appendChild(profile_pic);

                                    let recommendie_info = document.createElement('div');
                                    recommendie_info.className = 'recommendie_info';

                                    let recommendie_id = document.createElement('p');
                                    recommendie_id.className = "recommendie-id";
                                    recommendie_id.innerText = data_item.id;
                                    recommendie_id.style.display = 'none';

                                    let recommendie_name = document.createElement('p');
                                    recommendie_name.className = 'recommendie-name';
                                    recommendie_name.innerText = data_item.full_name;

                                    let recommendie_username = document.createElement('p');
                                    recommendie_username.className = 'recommendie_username';
                                    recommendie_username.innerText = data_item.user_name;

                                    // append elements to the recommendie_info div
                                    recommendie_info.appendChild(recommendie_id);
                                    recommendie_info.appendChild(recommendie_name);
                                    recommendie_info.appendChild(recommendie_username);

                                    // append recommendie_profile and recommendie_info to recommendie_div
                                    recommendie_div.appendChild(recommendie_profile);
                                    recommendie_div.appendChild(recommendie_info);

                                    //append recommendie_div and checkbox to recommendie_wrapper
                                    recommendie_wrapper.appendChild(checkbox_div);
                                    recommendie_wrapper.appendChild(recommendie_div);
                            
                                    // append recommendie_wrapper to recommendations
                                    recommendations.appendChild(recommendie_wrapper); 
                                }) 
                            })
                            .catch(error => {
                                // Handle any errors that occurred during the fetch
                                console.error('There was a problem with the fetch operation:', error);
                            });

                            close_img.addEventListener('click', function(event) {
                                buddy_recommendations_div.style.display = "none";
                                section_popup_menu_div.style.display = "flex";
                                let checkboxes = document.querySelectorAll('.checkbox');
                                console.log("Clear checkboxes");
                                console.log(checkboxes);
                                checkboxes.forEach(function(checkbox) {
                                    console.log("this checkbox is being cleared")
                                    checkbox.checked = false;
                                })
                            });
                        }

                        else if (element.id =="recommendations-stn-ctls") {
                           
                            let data  = {
                                movie_data_id: event.target.parentNode.parentNode.parentNode.previousElementSibling.firstElementChild.children[0].innerText,
                                movie_title: event.target.parentNode.parentNode.parentNode.previousElementSibling.firstElementChild.children[2].firstElementChild.children[0].children[1].innerText,
                                movie_year: event.target.parentNode.parentNode.parentNode.previousElementSibling.firstElementChild.children[2].firstElementChild.children[1].innerText,
                                movie_stars: event.target.parentNode.parentNode.parentNode.previousElementSibling.firstElementChild.children[2].firstElementChild.children[2].innerText,
                                movie_poster: event.target.parentNode.parentNode.parentNode.previousElementSibling.firstElementChild.children[1].firstElementChild.src,
                                movie_poster_sizes: event.target.parentNode.parentNode.parentNode.previousElementSibling.firstElementChild.children[1].firstElementChild.sizes,
                                movie_poster_set: event.target.parentNode.parentNode.parentNode.previousElementSibling.firstElementChild.children[1].firstElementChild.srcset
                            };
                            console.log(data);

                            let route = section_list_options[i].firstChild
                            console.log(route);

                            // Send data to server 
                            fetch(route, {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json'
                                },
                                body: JSON.stringify(data)
                            })
                            .then(response=> response.json())
                            .then(data => {
                                alert(data.message);
                            })
                            .catch((error) => console.error('Error:',error));                             
                        }
                        
                        else {
                            let data = {
                                movie_data_id: event.target.parentNode.parentNode.parentNode.previousElementSibling.firstElementChild.innerText,
                                movie_title: event.target.parentNode.parentNode.parentNode.previousElementSibling.lastElementChild.firstElementChild.firstElementChild.children[1].innerText,
                                movie_year: event.target.parentNode.parentNode.parentNode.previousElementSibling.lastElementChild.firstElementChild.children[1].innerText,
                                movie_stars: event.target.parentNode.parentNode.parentNode.previousElementSibling.lastElementChild.firstElementChild.children[2].innerText,
                                movie_poster: event.target.parentNode.parentNode.parentNode.previousElementSibling.children[1].firstElementChild.src,
                                movie_poster_sizes: event.target.parentNode.parentNode.parentNode.previousElementSibling.children[1].firstElementChild.sizes,
                                movie_poster_set: event.target.parentNode.parentNode.parentNode.previousElementSibling.children[1].firstElementChild.srcset
                                                               
                            };

                            console.log(data);

                            let element_to_delete1 = event.target.parentNode.parentNode.parentNode.previousElementSibling;
                            let element_to_delete2 = event.target.parentNode.parentNode.parentNode;
    

                            let link_element = section_list_options[i].firstChild;
                            console.log(link_element);
                            let route = link_element.getAttribute('href')
                            console.log(route)
                            

                            if (route == "/completed_watch") {
                                console.log("Completed watch route followed.");

                                let section_route_parent = event.target.parentNode.parentNode.parentNode.previousElementSibling.children[2]
                                console.log(section_route_parent);

                                let section_route = section_route_parent.querySelector('.section-route').innerText;

                                if (section_route) {
                                console.log("section route existing:",section_route)
                                data.date = section_watched_date;
                                data.data_route = section_route

                                fetch("/completed_watch", {
                                    method: 'POST',
                                    headers: {
                                        'Content-Type': 'application/json'
                                    },
                                    body: JSON.stringify(data)
                                })
                                    .then(response=> response.json())
                                    .then(data => {
                                        console.log(data)
                                        console.log(data.message)
                                        console.log(data.status)
                                        alert(data.message);
                                        if(data.status == "Remove") {
                                            element_to_delete2.remove();
                                            element_to_delete1.remove();
                                            console.log(data.section_count);
                                            if (data.route == "Currently Watching") {
                                                console.log("Update Currently Watching count")
                                                document.getElementById("currently-watching-count").innerText = data.section_count;
                                            }
                                            else if (data.route == "Watch List") {
                                                console.log("Update Watch List Count")
                                                document.getElementById("watchlist-count").innerText = data.section_count;
                                            }
                                        }
                                        
                                    })
                                    .catch((error) => console.error('Error:', error));
                                }
                            }    

                            else {
                                console.log("Not add to watch")
                                    fetch(route, {
                                        method: 'POST',
                                        headers: {
                                            'Content-Type': 'application/json'
                                        },
                                        body: JSON.stringify(data)
                                    })
                                    .then(response=> response.json())
                                    .then(data => {
                                        alert(data.message);
                                    })
                                    .catch((error) => console.error('Error:', error));
                            }
                                   
                                  
                                                    
                                            

                        }
                        

                        

                    });
                }  

                // Send data to the back end when section_date is updated               
                function upDateWatchedDate() {
                        section_watched_date = section_date.value;
                }
                        
                section_date.addEventListener('change', function(event) {
                    console.log("date changing")
                    upDateWatchedDate();
                    console.log(section_watched_date);
                    console.log(event.target);

                    console.log("Watched fetch function after date change")
                    let data = {
                        movie_data_id: event.target.parentNode.parentNode.previousElementSibling.firstElementChild.innerText,
                        movie_title: event.target.parentNode.parentNode.previousElementSibling.lastElementChild.firstElementChild.firstElementChild.children[1].innerText,
                        movie_year: event.target.parentNode.parentNode.previousElementSibling.lastElementChild.firstElementChild.children[1].innerText,
                        movie_stars: event.target.parentNode.parentNode.previousElementSibling.lastElementChild.firstElementChild.children[2].innerText,
                        movie_poster: event.target.parentNode.parentNode.previousElementSibling.children[1].firstElementChild.src,
                        movie_poster_sizes: event.target.parentNode.parentNode.previousElementSibling.children[1].firstElementChild.sizes,
                        movie_poster_set: event.target.parentNode.parentNode.previousElementSibling.children[1].firstElementChild.srcset,
                        date: section_watched_date                                              
                    }
                    let url;

                    console.log("section list item is :", section_list_options[0].firstChild.innerText)

                    let section_route_parent;   
                    let sibling_element = event.target.parentNode.parentNode  
                    console.log(sibling_element)   
                    if (section_list_options[0].firstChild.innerText == "Add to Watched") {
                        section_route_parent = event.target.parentNode.parentNode.previousElementSibling
                        console.log("add date to watched,", section_route_parent);

                        let section_route = section_route_parent.querySelector('.section-route').innerText;
                        console.log(section_route)

                        if (section_route) {
                            console.log("section route existing:",section_route)
                            data.data_route = section_route;
                            url = "/completed_watch";
                        }
                        else {
                            console.log("No section route")
                            data.date = section_watched_date;
                             url = "/watch"
                        }

                    } 
                   
                    console.log(data)

                    if (url == "/completed_watch") {

                        fetch("/completed_watch", {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify(data)
                        })
                            .then(response=> response.json())
                            .then(data => {
                                console.log(data)
                                console.log(data.message)
                                console.log(data.status)
                                alert(data.message);
                                if(data.status == "Remove") {
                                    section_route_parent.remove();
                                    sibling_element.remove();
                                    console.log(data.section_count);
                                    if (data.route == "Currently Watching") {
                                        console.log("Update Currently Watching count")
                                        document.getElementById("currently-watching-count").innerText = data.section_count;
                                    }
                                    else if (data.route == "Watch List") {
                                        console.log("Update Watch List Count")
                                        document.getElementById("watchlist-count").innerText = data.section_count;
                                    }
                                }
                                
                            })
                            .catch((error) => console.error('Error:', error));
                    }

                    else {
                        url = section_list_options[0].firstChild.getAttribute('href')
                        console.log("Undate url is",url)
                        fetch(url, {
                            method: 'POST',
                            headers: {
                                     'Content-Type': 'application/json'
                                    },
                            body: JSON.stringify(data)
                            })
                            .then(response=> response.json())
                            .then(data => {
                                    alert(data.message);
                                })
                            .catch((error) => console.error('Error:', error));
                    }

                    
                    
                    
                });
                watched_date = null;

            }

    }

});

// Function for search functions within watched, favourite, currenctly-watching, watchlist and movie-buddies sections
//Step 1: Select the search element using class name
document.addEventListener("DOMContentLoaded", function() {
    let section_search_input = document.getElementsByClassName('section-search');
    console.log(section_search_input);
    console.log(section_search_input.length);
    
    /* Step 2:add click event to selected search element so that when clicked the default view 
    dissapears and div to display search results appears */
    let search_close = document.getElementById('search-close')
    let section_display_tohide;
    let section_search_display;
    let fetch_url;
    
    for (let i = 0; i < section_search_input.length; i++) {
        section_search_input[i].addEventListener('click', function(event) {
        console.log(event.target);
        console.log("section_search input clicked")  

        search_close.style.display = "inline";
        
        // default div view is hidden 
        // conditionals are used to dyamically select the viewed and hidden displays for each section
        
        if (event.target.id == 'watched-movie-search') {
            section_display_tohide = document.getElementById('allwatched-movie-display');            
            console.log(section_display_tohide);
            section_display_tohide.style.display = "none";                       
        }       
        else if (event.target.id == 'favourite-movie-search') {
            section_display_tohide = document.getElementById('favourite-movie-display');            
            console.log(section_display_tohide);
            section_display_tohide.style.display = "none";
        } 
        else if (event.target.id == 'currentlyWatching-movie-search') {
            section_display_tohide = document.getElementById('currentlywatching-movie-display');            
            console.log(section_display_tohide);
            section_display_tohide.style.display = "none";
        }
        else if (event.target.id == 'watchlist-movie-search') {
            section_display_tohide = document.getElementById('watchlist-movie-display');            
            console.log(section_display_tohide);
            section_display_tohide.style.display = "none";
        }

        else if (event.target.id == 'movie-buddies-search') {
            section_display_tohide = document.getElementById('movie-buddies-display');            
            console.log(section_display_tohide);
            section_display_tohide.style.display = "none";
        }
        });
             
    // Step 3: input event is then added to the search input
    section_search_input[i].addEventListener('input', async function(event) {
        let search_close = document.getElementById('search-close')
        search_close.style.display = "inline";
         
        if (event.target.id == 'watched-movie-search') {
            section_display_tohide = document.getElementById('allwatched-movie-display'); 
            section_search_display = document.getElementById('search-watched-wrapper');        
            console.log(section_display_tohide);
            section_display_tohide.style.display = "none";
            section_search_display.style.display = "block";
            fetch_url = '/search_watched?q='           
        } 
        else if (event.target.id == 'favourite-movie-search') {
            section_display_tohide = document.getElementById('favourite-movie-display'); 
            section_search_display = document.getElementById('search-favourites-wrapper');        
            console.log(section_display_tohide);
            section_display_tohide.style.display = "none";
            section_search_display.style.display = "block";
            fetch_url = '/search_favourites?q='           
        } 
        else if (event.target.id == 'currentlyWatching-movie-search') {
            section_display_tohide = document.getElementById('currentlywatching-movie-display'); 
            section_search_display = document.getElementById('search-currentlyWatching-wrapper');        
            console.log(section_display_tohide);
            section_display_tohide.style.display = "none";
            section_search_display.style.display = "block";
            fetch_url = '/search_currentlyWatching?q='           
        } 
        else if (event.target.id == 'watchlist-movie-search') {
            section_display_tohide = document.getElementById('watchlist-movie-display'); 
            section_search_display = document.getElementById('search-watchlist-wrapper');        
            console.log(section_display_tohide);
            section_display_tohide.style.display = "none";
            section_search_display.style.display = "block";
            fetch_url = '/search_watchlist?q='           
        } 
        else if (event.target.id == 'movie-buddies-search') {
            section_display_tohide = document.getElementById('movie-buddies-display'); 
            section_search_display = document.getElementById('search-moviebuddies-wrapper');        
            console.log(section_display_tohide);
            section_display_tohide.style.display = "none";
            section_search_display.style.display = "block";
            fetch_url = '/search_moviebuddies?q='           
        }

        // Step 4: use fetch function to send the user query inputed in section search to the server
        let response = await fetch(fetch_url + event.target.value);
        let feedback = await response.json();
        console.log(feedback);
        section_search_display.innerText = '';
        if (event.target.id == 'movie-buddies-search') {
            for (let dict_item in feedback) {
                //let profile_pic = "../Images/Icons/user_profile.png";
                let id = feedback[dict_item].id;
                let name = feedback[dict_item].full_name;
                let user_name = feedback[dict_item].user_name;
                let status = feedback[dict_item].status;
                let moviebuddy_container = document.createElement("div");
                moviebuddy_container.className = "moviebuddy_container";

                let moviebuddy_profile = document.createElement("div");
                moviebuddy_profile.className = "moviebuddy_profile";
                let moviebuddy_profilepic = document.createElement("img")
                moviebuddy_profilepic.className = "moviebuddy_profilepic";
                moviebuddy_profilepic.src = "../static/Images/Icons/user_profile.png";
                moviebuddy_profile.appendChild(moviebuddy_profilepic);

                let movie_buddy_info = document.createElement("div");
                movie_buddy_info.className = "moviebuddy_info";
                let moviebuddy_id = document.createElement("p");
                moviebuddy_id.className = "movie-buddy-id";
                moviebuddy_id.innerText = id;
                moviebuddy_id.style.display = "none";
                let movie_buddyname = document.createElement("p");
                movie_buddyname.className = "movie-buddyname";
                movie_buddyname.innerText = name;
                let movie_buddyuser_name = document.createElement("p");
                movie_buddyuser_name.className = "movie_buddyuser_name";
                movie_buddyuser_name.innerText = user_name

                let movie_buddy_status;
                let buddy_cta;
                let movie_buddysearch_link;
                if (status == "Send Movie Buddy Request" || status == "Accept Movie Buddy Request") {
                    movie_buddy_status = document.createElement("button")
                    movie_buddy_status.textContent = status;
                    
                    if(status == "Send Movie Buddy Request") {
                        movie_buddy_status.id = "send_buddyrequest";
                    }
                    else if (status == "Accept Movie Buddy Request") {
                        movie_buddy_status.id = "accept_buddyrequest";
                    }
                } 
                else {
                    movie_buddy_status = document.createElement("span")
                    movie_buddy_status.textContent = "\u2022" + " "+ status;
                } 

                if (status == "Accept Movie Buddy Request" || status == "Buddy Request Declined") {
                    buddy_cta = document.createElement("button")
                    buddy_cta.className = "buddy_cta"

                    if (status == "Accept Movie Buddy Request") {
                        buddy_cta.innerText = "Decline Request"
                        buddy_cta.id = "cta_decline_request"
                    }

                    else if (status == "Buddy Request Declined") {
                        buddy_cta.innerText = "Resend Buddy Request"
                        buddy_cta.id = "cta_resend_request"
                    }
                }
                               
                movie_buddy_status.className = "movie-buddy-status"
                movie_buddyuser_name.appendChild(movie_buddy_status);
                if (buddy_cta) {
                    movie_buddyuser_name.appendChild(buddy_cta);
                }
                            
                movie_buddy_info.appendChild(moviebuddy_id);
                movie_buddy_info.appendChild(movie_buddyname);
                movie_buddy_info.appendChild(movie_buddyuser_name);
        
                moviebuddy_container.appendChild(moviebuddy_profile);
                moviebuddy_container.appendChild(movie_buddy_info);

                if (status == "Movie Buddy") {
                    movie_buddysearch_link = document.createElement("a");
                    
                    movie_buddysearch_link.href = "";
                    movie_buddysearch_link.appendChild(moviebuddy_container);
                    section_search_display.appendChild(movie_buddysearch_link);
                }
                else {
                    section_search_display.appendChild(moviebuddy_container);
                }               
         }

        }
        else {
            for (let dict_item in feedback) {
                let title = feedback[dict_item].movie_title.replace('<', '&lt;').replace('&', '&amp;');
                console.log(title)
               
                let year = feedback[dict_item].movie_year;
                let stars = feedback[dict_item].movie_stars;
                let poster = feedback[dict_item].movie_poster;
                let posterset = feedback[dict_item].movie_poster_set;
                let movie_container_div = document.createElement("div");
                movie_container_div.className = "movie-info-container";
                let movie_info_text = document.createElement("div");
                movie_info_text.className = "movie_info_text";
                let movie_info_div = document.createElement("div")
                movie_info_div.className = "movie-info"
                let movie_title = document.createElement("h3");
                movie_title.className = "search-movie-title";
                movie_title.innerText = title;
                let movie_year = document.createElement("p");
                movie_year.className = "movie-year";
                movie_year.innerText = year;
                let movie_stars = document.createElement("p");
                movie_stars.className = ("movie-stars");
                movie_stars.innerText = stars;
                let controls = document.createElement("img");
                controls.className = "section-controls";
                if (section_search_display.id == 'search-watched-wrapper') {
                    controls.id ='watched-stn-ctls'
                }                 
                else if (section_search_display.id == 'search-favourites-wrapper') {
                    controls.id ='favourite-stn-ctls'
                }     
                else if (section_search_display.id == 'search-currentlyWatching-wrapper') {
                    controls.id ='currentlywatching-stn-ctls'
                }
                
                else if (section_search_display.id == 'search-watchlist-wrapper') {
                    controls.id ='watchlist-stn-ctls'
                };
    
                controls.src = "../static/Images/Icons/9022327_dots_three_duotone_icon.png";
                let controls_btn = document.createElement("button");
                controls_btn.type = "button";
                controls_btn.className = "controls-btn";
                controls_btn.appendChild(controls);
                     
                let movie_poster_div = document.createElement("div");
                movie_poster_div.className= ("movie-poster-div")
                let movie_poster = document.createElement("img");
                movie_poster.src = poster;
                movie_poster.sizes = "50vw, (min-width: 480px) 34vw, (min-width: 600px) 26vw, (min-width: 1024px) 16vw, (min-width: 1280px) 16vw";
                movie_poster.srcset = posterset;                            
                movie_poster_div.appendChild(movie_poster);
    
                let movie_title_div = document.createElement("div");
                movie_title_div.className ="movie_info_title_wrapper";
                let empty_title = document.createElement("h3");
                empty_title.className = "empty_title";
                empty_title.innerText = "";
                movie_title_div.appendChild(empty_title);
                movie_title_div.appendChild(movie_title);
                movie_info_text.appendChild(movie_title_div);
                movie_info_text.appendChild(movie_year);
                movie_info_text.appendChild(movie_stars);
                movie_info_div.appendChild(movie_info_text);
                movie_info_div.appendChild(controls_btn);
    
                let movie_id = document.createElement("p");
                movie_id.innerText = feedback[dict_item].id;
                movie_id.style.display = "none";
                            
                movie_container_div.append(movie_id);
                movie_container_div.appendChild(movie_poster_div);
                movie_container_div.appendChild(movie_info_div);     
                               
                //document.getElementById("search-watched-wrapper").appendChild(movie_container_div);
                section_search_display.appendChild(movie_container_div);    
            }
        }
              
    });

    // Closing section search by clicking section close button 
    search_close.addEventListener('click', function(event) {
        console.log(event.target)
        console.log("search_close clicked")
        search_close.style.display = "none";
        section_display_tohide.style.display = "block";
        section_search_display.style.display = "none";
        event.target.parentNode.previousElementSibling.value = "";
        console.log(event.target.parentNode.previousElementSibling);
       
    });
}    
});

    /*1. Target search element in DOM
        2. When targeted display the search content window, initial display is hidden
        NB: Display the search results using format of the default views and also with , so use same class names and 
        3.Send request to server using fetch
        4. Close search*/
//};

// Function to send movie buddy request (activates "send movie buddy request button")
document.addEventListener("click", function(event) {

    // select element that triggers click event based on this condition
    if(event.target.id == 'send_buddyrequest' || event.target.id == "cta_resend_request") {
        //let send_moviebuddy_request = document.getElementById('send_buddyrequest');
        console.log(event.target);
      
        let request_recipient = event.target.parentNode.parentNode.firstElementChild.innerText;
        console.log(request_recipient)
        
        // Send data to server
        fetch("/send_moviebuddy_request", {
            method:'POST',
            headers: {
            'Content-Type': 'application/json'
            },
            body: JSON.stringify(request_recipient)
        })  
        .then(response=> response.json())
        .then(request_recipient => {
            alert(request_recipient.message)
        })
        .catch((error) => console.error('Error:', error));
        }
 
});


// Function to acctivate accept movie buddy request 
document.addEventListener("click", function(event) {

    // select element that triggers click event based on this condition
    if(event.target.id == "accept_buddyrequest" || event.target.id == "accept_buddyrequest_btn") {
        //let send_moviebuddy_request = document.getElementById('send_buddyrequest');
        console.log(event.target);
      
        let request_sender = event.target.parentNode.parentNode.firstElementChild.innerText;
        console.log(request_sender)
        
        // Send data to server
        fetch("/accept_moviebuddy_request", {
            method:'POST',
            headers: {
            'Content-Type': 'application/json'
            },
            body: JSON.stringify(request_sender)
        })  
        .then(response=> response.json())
        .then(request_recipient => {
            alert(request_recipient.message)
        })
        .catch((error) => console.error('Error:', error));
        }
 
});


// Function to acctivate decline movie buddy request 
document.addEventListener("click", function(event) {

    // select element that triggers click event based on this condition
    if(event.target.id == "cta_decline_request" || event.target.id == "decline_buddyrequest_btn") {
        //let send_moviebuddy_request = document.getElementById('send_buddyrequest');
        console.log(event.target);
      
        let request_sender = event.target.parentNode.parentNode.firstElementChild.innerText;
        console.log(request_sender)
        
        // Send data to server
        fetch("/decline_moviebuddy_request", {
            method:'POST',
            headers: {
            'Content-Type': 'application/json'
            },
            body: JSON.stringify(request_sender)
        })  
        .then(response=> response.json())
        .then(request_recipient => {
            alert(request_recipient.message)
        })
        .catch((error) => console.error('Error:', error));
        }
 
});


// Function to enable user view Movie Buddy notes ()
document.addEventListener("click", function(event) {
    console.log(event.target);

    const anchorElement = event.target.closest('a.view-buddy-notes');
    console.log(anchorElement);

    if (anchorElement) {
        event.preventDefault();

        // Use querySelector to find elements with specific ids within the anchorElement
        const idElement = anchorElement.querySelector('.movie-buddies-id');

        // Retrieve text content from the element
        let id = idElement ? idElement.innerText: '';
        console.log(id)

        let data = {
            id: id
        };

        fetch('/send_request_for_buddy_movienotes', {
            method:'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            console.log("View Movie Buddy Notes successfull", data)
            // Redirect to the view_buddy_movienotes section
            window.location.href = '/view_buddy_movienotes';
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }

});


// Function to enable user view buddy movie notes
document.addEventListener("click", function(event) {

    // Add condition to check for specific events so that not events trigger the 
    if(event.target.id == "buddy-notes-watched" || event.target.id == "buddy-notes-favourites" || event.target.id == "buddy-notes-currently-watching") {
        let movie_notes_id = event.target.id;
    console.log(movie_notes_id);
    let url_1; //stores the initial flask route to be fired, to store the user id of buddy being viewed on the server
    let url_2; //stores the flask route where user is redirected to view the notes of the buddy 
    let buddy_info = document.getElementById("buddy-notes-view-id").innerText;
    console.log(buddy_info)   

    // select element that triggers click event based on this condition
    if(movie_notes_id == "buddy-notes-watched") {
        console.log(movie_notes_id);
        url_1 = "/send_info_buddywatched";
        url_2 = "/view_buddy_watched"       
    } 
    else if (movie_notes_id == "buddy-notes-favourites") {
        console.log(movie_notes_id);
        url_1 = "/send_info_buddy_favourites";
        url_2 = "/view_buddy_favourites";
    } 
    else if (movie_notes_id == "buddy-notes-currently-watching") {
        console.log(movie_notes_id);
        url_1 = "/send_info_buddy_currentlywatching";
        url_2 = "/view_buddy_currentlywatching";
    }

    let buddy_data = {
        id:buddy_info
    }
    console.log(buddy_data);

    fetch(url_1, {
        method:'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(buddy_data)
    })
    .then(response => response.json())
    .then(data => {
        console.log("Successfull", data)
        // Redirect to the view_buddy_movienotes section
        window.location.href = url_2;
    })
    .catch((error) => {
        console.error('Error:', error);
    });
    }
});

document.addEventListener('click', function(event) {
    if(event.target.id == "recommend_btn" && recommendie_ids.length >= 1) {
        // data to be sent later to the server
        let data = {
            movie_title: event.target.parentNode.previousElementSibling.previousElementSibling.children[2].firstElementChild.firstElementChild.children[1].innerText,
            movie_year: event.target.parentNode.previousElementSibling.previousElementSibling.children[2].firstElementChild.children[1].innerText,
            movie_stars: event.target.parentNode.previousElementSibling.previousElementSibling.children[2].firstElementChild.children[2].innerText,
            movie_poster: event.target.parentNode.previousElementSibling.previousElementSibling.children[1].firstElementChild.src,
            movie_poster_sizes: event.target.parentNode.previousElementSibling.previousElementSibling.children[1].firstElementChild.sizes,
            movie_poster_set: event.target.parentNode.previousElementSibling.previousElementSibling.children[1].firstElementChild.srcset,
            recommendies: recommendie_ids
        }
        console.log(data);
        console.log(recommendie_ids);
        console.log('Recommend btn clicked & recommendie ids not empty')
        // Send data to 
        fetch("/recommend_movie", {
            method:'POST',
            headers: {
                'Content-Type':'application/json'
                },
                body: JSON.stringify(data)
            })
        .then(response => response.json())
        .then(data => {
                alert(data.message)
            })
        .catch((error) => console.log('Error:',error));
        console.log("recommend movie route has been fired");
        data = {};
        recommendie_ids = [];
    }

    else if (event.target.id == "recommend_btn" && recommendie_ids.length == 0) {
            console.log("only recommend_btn clicked");
            alert("No recommendies selected");
    }
    else {
        console.log("Not recommend btn clicked");
    }
    
   })

// Function to dynamically display and update data in the chat display area
function chatwith(event) {
    console.log("event.target:", event.target);
    console.log("event.currentTarget:", event.currentTarget);
    event.preventDefault();
    let chatwith_info = event.target.closest("#chatwith_buddy");

    console.log(chatwith_info);
    console.log("Movie Buddy to chat with clicked")

    let chat_area_header = document.getElementById('chat-area-header');
    chat_area_header.innerHTML = ''; // clear previously added clones from the header div
    console.log(chat_area_header)

    let originalElement = chatwith_info.firstElementChild;
    console.log(originalElement);
    let clone = originalElement.cloneNode(true);
    console.log(clone)

    chat_area_header.appendChild(clone);

    let visible_div = document.getElementById("newchatprofile-holder");
    visible_div.style.display = "none";

    let hidden_div = document.getElementById("defaultchat-profile");
    hidden_div.style.display = "block";
    
    let chathistory_id = {
        id:clone.children[1].firstElementChild.innerText
    }
    console.log(chathistory_id);

    fetch("/previous_chatmsgs", {
        method:'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(chathistory_id)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        let chats = data.chat_history;
        let user_id = data.user_id
        let grouped_msgs = chats.reduce((acc, chat) => {
            let date = chat.date;
            if(!acc[date]) {
                acc[date] = [];
            }
            acc[date].push(chat);
            return acc;
        }, {});
        console.log("Grouped_msgs:", grouped_msgs);
        let chat_display = document.getElementById('chat-display');
        chat_display.innerHTML = "";
        for(let date in grouped_msgs) {
            let today = new Date().toDateString();
            let db_date = new Date(date).toDateString()
            let display_date; // variable to store the date that will be displayed in chat display
            if (db_date == today) {
                display_date = "Today";
            }
            else if ((today - 1) == db_date) {
                display_date = "Yesterday";
            }
            else {
                display_date = date;
            }
            // Create variable to display date in chat display
            let text_date = document.createElement("div");
            text_date.innerText = display_date;
            text_date.className = "text-date-title"
            chat_display.appendChild(text_date);

            grouped_msgs[date].forEach(msg => {
                console.log(msg)
                // Create a div and paragraphs elements to display text and time    
                let text_div = document.createElement("div");   
                let msg_text = document.createElement("p");
                msg_text.textContent = msg.message;
                let msg_time = document.createElement("p");
                msg_time.textContent = msg.time;
                let msg_sender = document.createElement("span");
                msg_sender.textContent = msg.msg_sender;
                msg_text.appendChild(msg_sender);
                msg_sender.style.display = "None";
                // Append elements to DOM
                if (msg_sender.textContent == user_id) {
                        text_div.className = "sent-by-user"
                }
                else {
                text_div.className = "chat-msg"
                }
                text_div.appendChild(msg_text);
                text_div.appendChild(msg_time);
                chat_display.appendChild(text_div);
                
            })
        }

        console.log(chats);
        console.log(user_id)
        
    })
    .catch((error) => console.log('Error:', error)) 
    
} 

// Function for when new chat is clicked
document.addEventListener("click", function(event) {

    // Add condition to check for specific element to trigger the event
    if (event.target.id == "newchat-btn") {
        event.preventDefault();
        console.log("New Chat button clicked");

        //Clear previous fetch request display
        let new_chatholder = document.getElementById("newchatbuddies-profile-holder");
        console.log(new_chatholder);
        new_chatholder.innerHTML = " ";
      
        let visible_div = document.getElementById("newchatprofile-holder");
        visible_div.style.display = "block";

        let hidden_div = document.getElementById("defaultchat-profile");
        hidden_div.style.display = "none";

        let close_chat = document.getElementById("close-chat-btn");
        close_chat.addEventListener("click", function(event) {
            event.preventDefault();
            visible_div.style.display = "none";
            hidden_div.style.display = "block";
        })
             
        fetch("/chat_buddies_profile")
        .then(response => {
            console.log("chat buddy info returned")
            return response.json();
        })
        .then(chat_with => {
            // Process data recieved
            console.log(chat_with);

            chat_with.forEach(data_item => {
                console.log(data_item)

                let newchatbuddy_link = document.createElement('a')
                newchatbuddy_link.href = "/chat_with";
                newchatbuddy_link.className = "newchatbuddy-link";
                newchatbuddy_link.id = "chatwith_buddy";
                
                let newchatbuddy_div = document.createElement('div');
                newchatbuddy_div.className = 'newchatbuddy_div';
                newchatbuddy_div.id = "newchatbuddy-div"

                let newchatbuddy_profile = document.createElement('div');
                newchatbuddy_profile.className = 'newchatbuddy_profile_div';

                let newchat_profile_pic = document.createElement('img');
                newchat_profile_pic.className = 'newchatbuddy_profile_pic';
                newchat_profile_pic.src = data_item.profile_pic;
                newchatbuddy_profile.appendChild(newchat_profile_pic);

                let newchatbuddy_info = document.createElement('div');
                newchatbuddy_info.className = 'newchatbuddy_info';

                let newchatbuddy_id = document.createElement('p');
                newchatbuddy_id.className = "newchatbuddy-id";
                newchatbuddy_id.innerText = data_item.id;
                newchatbuddy_id.style.display = 'none';

                let newchatbuddy_name = document.createElement('p');
                newchatbuddy_name.className = 'newchatbuddy-name';
                newchatbuddy_name.innerText = data_item.full_name;

                let newchatbuddy_username = document.createElement('p');
                newchatbuddy_username.className = 'newchatbuddy_username';
                newchatbuddy_username.innerText = data_item.user_name;

                // append elements to the chat buddy info div
                newchatbuddy_info.appendChild(newchatbuddy_id);
                newchatbuddy_info.appendChild(newchatbuddy_name);
                newchatbuddy_info.appendChild(newchatbuddy_username);

                // append chatbuddy_profile and chatbuddy_info to chatbuddy div
                newchatbuddy_div.appendChild(newchatbuddy_profile);
                newchatbuddy_div.appendChild(newchatbuddy_info);

                //append chatbuddy div to chatbuddy link
                newchatbuddy_link.appendChild(newchatbuddy_div)

                //append chatbuddy div to the DOM (buddy-chat-profile)
                new_chatholder.appendChild(newchatbuddy_link);

                // Keep updating the text area with buddy info you are chatting with
                newchatbuddy_link.addEventListener('click', chatwith)
               
            })
            
        })

    }
})


// Function to send a message to a movie buddy
document.addEventListener('click', function(event) {

    // Add condition to check for click from particular element
    if (event.target.id == "send-msg-btn") {
        console.log("Send message to buddy clicked");

        let msgsent_date_time = new Date ();
        let time_zone = Intl.DateTimeFormat().resolvedOptions().timeZone;

        let text_holder = document.getElementById("type-msg-input");
        let text = text_holder.value;
        console.log(text);

        text_holder.value = " "; // clear the text holder after msg is sent

        let chat_msgdiv = document.createElement('div');
        chat_msgdiv.className = "sent-by-user";

        let chat_msg = document.createElement('p');
        chat_msg.innerText = text;

        let msg_time = document.createElement('p');
        let hours = msgsent_date_time.getHours();
        let minutes = msgsent_date_time.getMinutes()
        if (hours < 10) {
            hours = "0" + msgsent_date_time.getHours().toString();
        }
        else {
            hours = msgsent_date_time.getHours().toString()
        }
        if (minutes < 10) {
            minutes = "0" + msgsent_date_time.getMinutes().toString();          
        }
        else {
            minutes = msgsent_date_time.getMinutes().toString();
        }
        msg_time.innerText = hours + ":" + minutes;
        console.log(msg_time.innerText)       

        // send text to server side for recipeint to receive
        let chatmsg_display = document.getElementById('chat-display');
        console.log(chatmsg_display);

        //Append msg and time to chat_msg_div
        chat_msgdiv.appendChild(chat_msg)
        chat_msgdiv.appendChild(msg_time)

        //Append chat_msgdiv to the DOM (chat-display)
        chatmsg_display.appendChild(chat_msgdiv);

        let chat_data = {
            chat_msg: text,
            msg_recipient:chatmsg_display.previousElementSibling.firstElementChild.children[1].firstElementChild.innerText,
            date_time: msgsent_date_time,
            time_zone:time_zone
        }
        console.log(chat_data);

        fetch("/send_msg", {
            method:'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(chat_data)
        })
        .then(response => {
            return response.json();
        })
        .then(data => {
            alert(data.message)
        })
        .catch((error) => console.log('Error:', error))
             
    }   
})


document.addEventListener('click', function(event) {
    console.log(event.target)
    if (event.target.closest("#chatwith_buddy")) {
        console.log("Chat with Buddy clicked")
        chatwith(event)
    }
});

// Function to submit the form for clicked movie year when displaying movies by year
document.addEventListener('click', function(event) {
    console.log(event)

    if(event.target.matches('.watched-year-link')) {
        event.preventDefault();
        event.target.closest('.watched-year-form').submit();
    }
})

// Function to update profile picture in update user profile
document.addEventListener('click', function(event) {
    let element = event.target;
    console.log(element)

    if (element.id == 'update-profile-pic') {
        event.preventDefault();

        let visible_div = document.getElementById('update-profile-pic-div')
        console.log("Visible div: ", visible_div)
        visible_div.style.display = "block"

        profile_pic_controls = document.getElementsByClassName('profile-pic-ctls')
        console.log(profile_pic_controls)
        profile_pic_ctls_list = Array.from(profile_pic_controls)
        console.log(profile_pic_ctls_list)

        profile_pic_ctls_list.forEach(list_item => {
            console.log(list_item)
            list_item.addEventListener('click', function(event) {

                if (event.target.id == 'upload-profile-pic') {
                    event.preventDefault()

                    document.querySelector('input[name="profile_pic"]')
                    document.getElementById('update-profilepic-input').click();

                    document.getElementById("update-profilepic-input").addEventListener("change", function() {
                        document.getElementById('upload-profile-pic-form').submit();
                    });

                    visible_div.style.display = "none";
                  
                } 
                
                if (event.target.id == 'remove-profile-pic') {
                    event.preventDefault()

                    document.getElementById('remove-profile-pic-form').submit()
                }

                
            });
   
        })
     
    }

    else if (element.id == "close-update-profilepic" || element.id == "close-update-profile-ctls") {
        let hidden_div = document.getElementById('update-profile-pic-div')
        console.log("Div to hide: ", hidden_div)
        hidden_div.style.display = "none"
    }

})

// Function to display and hide password guidelines in the create account route
document.addEventListener('DOMContentLoaded', function() {
    if (window.location.pathname === '/create_account') {
        document.getElementById('password').addEventListener('focus', function() {
            document.getElementById('password-guidelines').style.display = 'block';
        });
    
        document.getElementById('password').addEventListener('blur', function() {
            document.getElementById('password-guidelines').style.display = 'none';
        });
    }
})

// Function to display and hide the password guidelines for the new password route
document.addEventListener('DOMContentLoaded', function() {
    if (window.location.pathname === "/reset_password") {
        document.getElementById('new-password').addEventListener('focus', function() {
            document.getElementById('new-password-guidelines').style.display = 'block';
        });
    
        document.getElementById('new-password').addEventListener('blur', function() {
            document.getElementById('new-password-guidelines').style.display = 'none';
        });
    }
})





                            


   





