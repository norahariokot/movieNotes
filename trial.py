info = [{'id': 1, 'first_name': 'Faith', 'last_name': 'Frances', 'user_name': 'Faith Frances', 'profile_pic': None, 'movie_title': 'Sherlock Holmes', 'movie_year': '2009', 'movie_stars': 'Robert Downey Jr., Jude Law'},{'id': 2, 'first_name': 'Kellos', 'last_name': 'Unicorn', 'user_name': 'Unicorn_Kellos', 'profile_pic': None, 'movie_title': 'Sherlock Holmes', 'movie_year': '2009', 'movie_stars': 'Robert Downey Jr., Jude Law'}]

recommendations = []
for dict_item in info:
    found = False
    user_name = []
    user_name_dict = {}
    if dict_item["profile_pic"] == None:
        dict_item["profile_pic"] = "../static/Images/Icons/user_profile.png"
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