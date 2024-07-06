from bs4 import BeautifulSoup
import requests

def user_query(query):
	
	url = "https://www.imdb.com/find/"

	querystring = {'q': query}

	headers = {
			"User-Agent": "Mozilla/5.0",
		}

	page = requests.get(url, headers=headers, params=querystring)

	print(page)

	#Parse the HTML content with BeautifulSoup
	soup=BeautifulSoup(page.text, 'html.parser')
	#print(soup.prettify())

	with open ('output.html', 'w') as f:
		f.write(soup.prettify())

	# Find all div elements with the specified class
	data_divs = soup.find_all('li', class_='ipc-metadata-list-summary-item ipc-metadata-list-summary-item--click find-result-item find-title-result')

	# Initialize an empty list to store the product information
	movies_list = []
	for movie in data_divs:
		print (movie)
		title = movie.find('div', class_="ipc-metadata-list-summary-item__tc").a.text
		year = movie.find('ul', class_="ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--no-wrap ipc-inline-list--inline ipc-metadata-list-summary-item__tl base").li.span.text
		stars_listitem = movie.find('ul', class_="ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--no-wrap ipc-inline-list--inline ipc-metadata-list-summary-item__stl base").li.span.text
		print(stars_listitem)
		if stars_listitem:
			print("Stars List item found")
			stars = stars_listitem
		else:
			stars = ""		
		img_div = movie.find('div', class_="ipc-media ipc-media--poster-27x40 ipc-image-media-ratio--poster-27x40 ipc-media--base ipc-media--custom ipc-media__img")
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

	return(movies_list)

	



