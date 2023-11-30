import requests
import time
import os
import json


def get_urls() -> list:
	res = requests.get('https://www.globalfirepower.com/countries-listing.asp')
	soup = BeautifulSoup(res.text, 'html.parser')
	
	a_tags = soup.find_all("a")
	urls = [a['href'] for a in a_tags]
	urls = [url for url in urls if url.startswith('/country-military-strength-detail')]
	urls = list(set(urls))
	urls = ["https://www.globalfirepower.com" + url for url in urls]

	return urls


def get_pages(urls):
	for url in urls:
		country_id = url.split("country_id=")[1]
		time.sleep(0.4)
		res = requests.get(url)
		text = res.text
		
		# dump in text file in /pages
		with open(f'pages/{country_id}.txt', 'w') as f:
			f.write(text)


if __name__ == "__main__":
	print("Getting urls...")
	urls = get_urls()
	print("Getting pages...")
	get_pages(urls)
	print("Done...")