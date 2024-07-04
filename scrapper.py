from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def user_query(query):
	url = f"https://www.imdb.com/find/?q={query}"
	print(url)

	# Set up headless Chrome
	chrome_options = Options()
	chrome_options.add_argument("--headless")
	chrome_options.add_argument("--no-sandbox")
	chrome_options.add_argument("--disable-dev-shm-usage")
	chrome_options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"')
	
	# Update with the path to your chromedriver
	chromediver_path =r"/mnt/c/WebDriver/chromedriver.exe"
	print(chromediver_path)
	service = Service(chromediver_path)

	driver = webdriver.Chrome(service=service, options=chrome_options) 
	
	driver.get(url)
    
    # Allow time for the page to load
	driver.implicitly_wait(10)  # Adjust as needed
    
    # Get page source and parse with BeautifulSoup
	page_source = driver.page_source 
	driver.quit()
    	
	soup=BeautifulSoup(page_source, 'html.parser')
	#print(soup.prettify())

	with open ('output.html', 'w') as f:
		f.write(soup.prettify())

	# Find all div elements with the specified class
	data_divs = soup.find_all('li', class_='ipc-metadata-list-summary-item ipc-metadata-list-summary-item--click find-result-item find-title-result')

	# Initialize an empty list to store the product information
	movies_list = []
	for movie in data_divs:
		title = movie.find('div', class_="ipc-metadata-list-summary-item__tc").a.text
		year = movie.find('ul', class_="ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--no-wrap ipc-inline-list--inline ipc-metadata-list-summary-item__tl base").li.span.text
		stars = movie.find('ul', class_="ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--no-wrap ipc-inline-list--inline ipc-metadata-list-summary-item__stl base").li.span.text
		poster = movie.find('div', class_="ipc-media ipc-media--poster-27x40 ipc-image-media-ratio--poster-27x40 ipc-media--base ipc-media--custom ipc-media__img").img.get('src')
		posterset = movie.find('div', class_="ipc-media ipc-media--poster-27x40 ipc-image-media-ratio--poster-27x40 ipc-media--base ipc-media--custom ipc-media__img").img.get('srcset')
		print(title)
		movie_dict = {"title": title, "year": year, "stars":stars, "poster": poster, "posterset": posterset}
		movies_list.append(movie_dict)
		#print(movie_dict)

	return(movies_list)


#user_query("Inception")

	



