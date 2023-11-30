from bs4 import BeautifulSoup
import os
import json

HEADINGS = [
	'FINANCIALS',
	'GEOGRAPHY',
	'MANPOWER',
	'AIRPOWER',
	'LAND FORCES',
	'NAVAL FORCES',
	'NATURAL RESOURCES'
	'LOGISTICS'
]


def parse_countries():
	data_dict = dict()
	
	# read file titles in /pages
	for file in os.listdir('pages'):
		with open(f'pages/{file}', 'r') as f:
			text = f.read()
			soup = BeautifulSoup(text, 'html.parser')
			country_id = file.split(".")[0]
			parse_country(soup, country_id, data_dict)


def parse_country(soup, country_id, data_dict) -> dict:
	this_country_dict = dict()
	
	a = soup.find_all("button", class_="collapsible")
	intro_paragraph = soup.find("span", class_="textLarge textDkGray")
	index = intro_paragraph.find("a", {"href": "/countries-listing.php"}).next_sibling.next_sibling.text

	this_country_dict['pwrIndex'] = index

	for item in a:
		divs = item.next_sibling.next_sibling.find_all("div", class_="specsGenContainers")
		for div in divs:
			title = div.find("span", {"class": "textLarge textYellow textBold textShadow"})
			if not title:
				title = div.find("span", {"class": "textLarge textWhite textBold textShadow"})
			title = title.text if title else None
			
			info = div.find("span", class_="textWhite textShadow")
			if not info:
				info = div.find("span", class_="textLarge textWhite textShadow")
			
			info = info.text if info else None

			if "Stock: " in info:
				split = info.split("\n")
				stock = split[0]
				readiness = ''
				for s in split:
					if "Readiness: " in s:
						readiness = s
						break
				
				if stock:
					stock_splitted = stock.split(" ")
					for s in stock_splitted:
						# if it has a digit in it and does not have ( in it
						if any(char.isdigit() for char in s) and "(" not in s:
							stock = s
							break
					stock = stock.replace(" ", "")
					stock = stock.replace("\t", "")

				if readiness:
					readiness = readiness.split(" ")[1].replace("*", "")
					readiness = readiness.replace(" ", "")
					readiness = readiness.replace("\t", "")

				info = stock, readiness

			this_country_dict[title] = info


	data_dict[country_id] = this_country_dict
	# dump in json file
	with open('gfpdata.json', 'w') as outfile:
		json.dump(data_dict, outfile, indent=2)


if __name__ == "__main__":
	print("Parsing countries and dumping into gfpdata.json...")
	parse_countries()
	print("Done...")