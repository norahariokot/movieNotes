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
                               
                if (event.target.id == 'watched-stn-ctls') {
                    section_options_list = JSON.parse(document.getElementById('watched-options-list').innerHTML);
                
                }

                else if (event.target.id == "favourite-stn-ctls") {
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

                /*let watched_date = null;
                let date_div = document.createElement("div");
                let date_lbl = document.createElement("label");
                let date = document.createElement("input");
                date_lbl.innerHTML = "Include date";
                date.type = "date";
                date.id = "watched-date"
                date_div.appendChild(date_lbl);
                date_div.appendChild(date);
                date_div.style.display = "none"
                section_popup_menu.insertAdjacentElement('afterend', date_div);

                search_list_options.forEach(list_option => {
                    //console.log(list_option.firstChild.innerHTML)
                    if(list_option.firstChild.innerHTML == "Watched") {
                        console.log("Watched found")
                 
                        list_option.addEventListener('mouseover', function() {
                            date_div.style.display = "block";
                           
                        });

                        date_div.addEventListener('mouseover', function() {
                            date_div.style.display = "block";
                        });

                        date_div.addEventListener('mouseout', function() {
                            date_div.style.display = "none";
                        });

                   }
                })*/

                //Add event handlers to all links in the list items to send data to the server side
                for(let i = 0; i < section_list_options.length; i++) {
                    section_list_options[i].firstChild.addEventListener('click', function(event) {
                        event.preventDefault();
                        console.log(event.target);

                        let data = {
                            movie_title: event.target.parentNode.parentNode.parentNode.previousElementSibling.lastElementChild.firstElementChild.children[0].innerHTML,
                            movie_year: event.target.parentNode.parentNode.parentNode.previousElementSibling.lastElementChild.firstElementChild.children[1].innerHTML,
                            movie_stars: event.target.parentNode.parentNode.parentNode.previousElementSibling.lastElementChild.firstElementChild.children[2].innerHTML,
                            movie_poster: event.target.parentNode.parentNode.parentNode.previousElementSibling.children[2].firstElementChild.src,
                            movie_poster_sizes: event.target.parentNode.parentNode.parentNode.previousElementSibling.children[2].firstElementChild.sizes,
                            movie_poster_set: event.target.parentNode.parentNode.parentNode.previousElementSibling.children[2].firstElementChild.srcset
                                                           
                            };
                 

                        /*if (section_list_options[i].firstChild.innerHTML == "Watched") {
                            data.date = watched_date;
                        }*/

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
                
                /*function upDateWatchedDate() {
                        watched_date = date.value;
                }
                        
                date.addEventListener('change', function(event) {
                    console.log("date changing")
                    upDateWatchedDate();
                    console.log(watched_date);
                    console.log(event.target);

                    console.log("Watched fetch function after date change")
                    let data = {
                        movie_title: event.target.parentNode.parentNode.previousElementSibling.lastElementChild.firstElementChild.children[0].innerHTML,
                        movie_year: event.target.parentNode.parentNode.previousElementSibling.lastElementChild.firstElementChild.children[1].innerHTML,
                        movie_stars: event.target.parentNode.parentNode.previousElementSibling.lastElementChild.firstElementChild.children[2].innerHTML,
                        movie_poster: event.target.parentNode.parentNode.previousElementSibling.firstElementChild.firstChild.src,
                        movie_poster_sizes: event.target.parentNode.parentNode.previousElementSibling.firstElementChild.firstChild.sizes,
                        movie_poster_set: event.target.parentNode.parentNode.previousElementSibling.firstElementChild.firstElementChild.srcset,
                        date: watched_date                                   
                    }
                    
                    fetch("/watched", {
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
                watched_date = null;*/

        }

        
    }

});




