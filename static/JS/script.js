// Function to create pop menu for section control buttons
         
let isSectionPopupVisible = false;
let section_popup_menu;
let section_popup_menu_div;

document.addEventListener('click', function(event) {
    console.log(event.target);
        
    if (event.target.matches('.section-controls')) {
        console.log("section options button clicked");
        if(isSectionPopupVisible && !section_popup_menu.contains(event.target)) {
            //remove popup menu
            section_popup_menu.remove();
            isSectionPopupVisible = false;
        }

        else {
                section_popup_menu_div = document.createElement("div");
                section_popup_menu_div.className = "popup-menu-wrapper";
                section_popup_menu = document.createElement("ul");
                section_popup_menu.className = "section_popup_menu-list";
                section_popup_menu
                let section_options_list;
                 
                // Add diffrent popup options to deferent links 
                if (event.target.id == 'watched-stn-ctls') {
                    console.log(event.target)
                    section_options_list = JSON.parse(document.getElementById('watched-options-list').innerHTML);
                
                }

                else if (event.target.id == "favourite-stn-ctls") {
                        console.log("Favourites sections options")
                        section_options_list = JSON.parse(document.getElementById('favourite-options-list').innerHTML);
                }

                else if (event.target.id == "currentlywatching-stn-ctls") {
                    section_options_list = JSON.parse(document.getElementById('currentlywatching-options-list').innerHTML);
                }

                else if (event.target.id == "watchlist-stn-ctls") {
                    section_options_list = JSON.parse(document.getElementById('watchlist-options-list').innerHTML);
                }

                console.log(typeof(section_options_list))
                console.log(section_options_list)

                let section_options = {}
                section_options_list.forEach(list_item => {
                    section_options[list_item[0]] = list_item[1]
                });
                console.log(section_options)

                let section_list_options = [];
                for (let key in section_options) {
                    let section_popup_options = document.createElement("li");
                    section_popup_options.className = "popup-menu-li";
                    let section_link = document.createElement("a");
                    section_link.href = section_options[key];
                    section_link.innerHTML = key;
                    section_popup_options.appendChild(section_link);
                    section_popup_menu.appendChild(section_popup_options);
                    section_list_options.push(section_popup_options);
                }

                section_popup_menu_div.appendChild(section_popup_menu);
                event.target.parentNode.parentNode.parentNode.insertAdjacentElement('afterend', section_popup_menu_div);
                isSectionPopupVisible = true;

                let section_watched_date = null;
                let section_date_div = document.createElement("div");
                let section_date_lbl = document.createElement("label");
                let section_date = document.createElement("input");
                section_date_lbl.innerHTML = "Include date";
                section_date.type = "date";
                section_date.id = "watched-date"
                section_date_div.appendChild(section_date_lbl);
                section_date_div.appendChild(section_date);
                section_date_div.style.display = "none"
                section_popup_menu.insertAdjacentElement('afterend', section_date_div);

                section_list_options.forEach(list_option => {
                    //console.log(list_option.firstChild.innerHTML)
                    if(list_option.firstChild.innerHTML == "Completed Watching") {
                        console.log("Completed watching found")
                 
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

                //Add event handlers to all links in the list items to send data to the server side
                for(let i = 0; i < section_list_options.length; i++) {
                    section_list_options[i].firstChild.addEventListener('click', function(event) {
                        event.preventDefault();
                        console.log(event.target);

                        let data = {
                            movie_data_id: event.target.parentNode.parentNode.parentNode.previousElementSibling.firstElementChild.innerHTML,
                            movie_title: event.target.parentNode.parentNode.parentNode.previousElementSibling.lastElementChild.firstElementChild.firstElementChild.children[1].innerHTML,
                            movie_year: event.target.parentNode.parentNode.parentNode.previousElementSibling.lastElementChild.firstElementChild.children[1].innerHTML,
                            movie_stars: event.target.parentNode.parentNode.parentNode.previousElementSibling.lastElementChild.firstElementChild.children[2].innerHTML,
                            movie_poster: event.target.parentNode.parentNode.parentNode.previousElementSibling.children[1].firstElementChild.src,
                            movie_poster_sizes: event.target.parentNode.parentNode.parentNode.previousElementSibling.children[1].firstElementChild.sizes,
                            movie_poster_set: event.target.parentNode.parentNode.parentNode.previousElementSibling.children[1].firstElementChild.srcset
                                                           
                            };
                 

                        if (section_list_options[i].firstChild.innerHTML == "Completed Watching") {
                            data.date = section_watched_date;
                            data.data_route = document.getElementsByClassName('route')[0].innerHTML;
                        }

                        console.log(data);
                        let route = section_list_options[i].firstChild
                        console.log(route)
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
                        movie_data_id: event.target.parentNode.parentNode.previousElementSibling.firstElementChild.innerHTML,
                        movie_title: event.target.parentNode.parentNode.previousElementSibling.lastElementChild.firstElementChild.firstElementChild.children[1].innerHTML,
                        movie_year: event.target.parentNode.parentNode.previousElementSibling.lastElementChild.firstElementChild.children[1].innerHTML,
                        movie_stars: event.target.parentNode.parentNode.previousElementSibling.lastElementChild.firstElementChild.children[2].innerHTML,
                        movie_poster: event.target.parentNode.parentNode.previousElementSibling.children[1].firstElementChild.src,
                        movie_poster_sizes: event.target.parentNode.parentNode.previousElementSibling.children[1].firstElementChild.sizes,
                        movie_poster_set: event.target.parentNode.parentNode.previousElementSibling.children[1].firstElementChild.srcset,
                        date: section_watched_date,   
                        data_route: document.getElementsByClassName('route')[0].innerHTML                          
                    }
                    console.log(data)

                    fetch("/completed_watch", {
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
                });
                watched_date = null;

        }

        
    }

});




