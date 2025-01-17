from bs4 import BeautifulSoup

import requests
import re

def get_movie_details(query):
	# Define URL and query
	url = "https://www.imdb.com/find/?s=tt"
	querystring = {'q': query}
	headers = {
			"User-Agent": "Mozilla/5.0",
		}

	# Fetch page with dynamic query
	page = requests.get(url, headers=headers, params=querystring)

	#Parse the HTML content with BeautifulSoup
	soup=BeautifulSoup(page.text, 'html.parser')
	#print(soup.prettify())

	# Extract relevant data
	movie_item = soup.find_all("a", string=re.compile(r"\b"+ re.escape(query) + r"\b", re.IGNORECASE))

	# Initialize an empty list to store the product information
	movies_list = []

	if movie_item:
		for movie in movie_item:
			#print(f"Movie element{movie}")

			# Extract movie title
			movie_title = movie.text
			print(f"New extract of movie titles is {movie_title}")

			# Extract parent element to get other detials
			parent_movieinfo_element = movie.find_parent("li")
			#print(f"Parent element{parent_movieinfo_element}")

			if parent_movieinfo_element:
				# Extract movie poster
				try:
					movie_img= parent_movieinfo_element.find("img").get("src")
					movie_posterset = parent_movieinfo_element.find("img").get("srcset")
				except AttributeError:
					movie_img= "../static/Images/Icons/movie_icon.png"
					movie_posterset = ""
				#else:
					#print(f"New extract of movie img src is {movie_img} and imgset is {movie_posterset}")

				# Extract movie year information
				try:
					movie_year_element = movie.find_next_sibling("ul")
					if movie_year_element:
						movie_year = movie_year_element.find("span").text
					print(movie_year)
				except AttributeError:
					movie_year = ""	

				# Extract stars information
				try:
					movie_stars= movie_year_element.find_next_sibling("ul").find("span").text
					print(movie_stars)
				except AttributeError:
					movie_stars = ""
					print(movie_stars)

				# Add movie information to a dict
				movie_dict = {"title": movie_title, "year": movie_year, "stars":movie_stars, "poster": movie_img, "posterset": movie_posterset}
				print(movie_dict)

				movies_list.append(movie_dict)

					
						
		return(movies_list)		
			
	else:
		print(f"New extract not found")
		return(None)
		


	"""
	# Find all div elements with the specified class
	data_divs = soup.find_all('li', class_='ipc-metadata-list-summary-item ipc-metadata-list-summary-item--click find-result-item find-title-result')

	# Initialize an empty list to store the product information
	movies_list = []
	for movie in data_divs:
		print (movie)
		title = movie.find('div', class_="ipc-metadata-list-summary-item__tc").a.text
		year = movie.find('ul', class_="ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--no-wrap ipc-inline-list--inline ipc-metadata-list-summary-item__tl base").li.span.text
		stars_ul = movie.find('ul', class_="ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--no-wrap ipc-inline-list--inline ipc-metadata-list-summary-item__stl base").li.span.text
												  #ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--no-wrap ipc-inline-list--inline ipc-metadata-list-summary-item__stl base" role="presentation"><li role="presentation" class="ipc-inline-list__item"><span class="ipc-metadata-list-summary-item__li" aria-disabled="false">Jeff Goldblum, Geena Davis</span></li></ul>
		stars_listitem = movie.find('ul', class_="ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--no-wrap ipc-inline-list--inline ipc-metadata-list-summary-item__stl base").li.span.text
		
		if stars_ul:
			print("Stars ul found")
			stars_span = stars_ul.find('li').find('span')
			if stars_span:
				st
		if stars_listitem:
			print("Stars List item found")
			stars = stars_listitem
		else:
			stars = ""	
				
			
		img_div = movie.find('div', class_="ipc-media ipc-media--poster-27x40 ipc-image-media-ratio--poster-27x40 ipc-media--base ipc-media--custom ipc-media__img")
										   #"ipc-media ipc-media--poster-27x40 ipc-image-media-ratio--poster-27x40 ipc-media--media-radius ipc-media--base ipc-media--custom ipc-media__img" style="width:50px"><img alt="Scarlett Johansson and Channing Tatum in Fly Me to the Moon (2024)" class="ipc-image" loading="lazy" src="https://m.media-amazon.com/images/M/MV5BYTExMDhkYTQtZTc3Ni00ZmI0LThiY2ItYTk0YzIyZDNkYjEzXkEyXkFqcGc@._V1_QL75_UX50_CR0,0,50,74_.jpg" srcset="https://m.media-amazon.com/images/M/MV5BYTExMDhkYTQtZTc3Ni00ZmI0LThiY2ItYTk0YzIyZDNkYjEzXkEyXkFqcGc@._V1_QL75_UX50_CR0,0,50,74_.jpg 50w, https://m.media-amazon.com/images/M/MV5BYTExMDhkYTQtZTc3Ni00ZmI0LThiY2ItYTk0YzIyZDNkYjEzXkEyXkFqcGc@._V1_QL75_UX75_CR0,0,75,111_.jpg 75w, https://m.media-amazon.com/images/M/MV5BYTExMDhkYTQtZTc3Ni00ZmI0LThiY2ItYTk0YzIyZDNkYjEzXkEyXkFqcGc@._V1_QL75_UX100_CR0,0,100,148_.jpg 100w" sizes="50vw, (min-width: 480px) 34vw, (min-width: 600px) 26vw, (min-width: 1024px) 16vw, (min-width: 1280px) 16vw" width="50"></div>
		poster = None
		posterset = None
		if img_div:
			poster = img_div.img.get('src')
			posterset= img_div.img.get('srcset')
		img_div2 = 	movie.find('div', class_="ipc-media ipc-media--poster-27x40 ipc-image-media-ratio--poster-27x40 ipc-media--rounded ipc-media--base ipc-media--custom ipc-media__img") 
		if img_div2:
			poster = img_div2.img.get('src') 
			posterset= img_div2.img.get('srcset')

		#posterset = movie.find('div', class_="ipc-media ipc-media--poster-27x40 ipc-image-media-ratio--poster-27x40 ipc-media--base ipc-media--custom ipc-media__img").img.get('srcset')
		print(title)
		movie_dict = {"title": title, "year": year, "stars":stars, "poster": poster, "posterset": posterset}
		movies_list.append(movie_dict)
		#print(movie_dict)
		"""



	

	



