import os
import requests
from bs4 import BeautifulSoup


from sheet import Sheet


sanborn_root = r'http://www.loc.gov/rr/geogmap/sanborn/'
vt_page = sanborn_root + r'/states.php?stateID=52'
img_root = r'http://tile.loc.gov/image-services/iiif/service:gmd:gmd375m:g3754m:{full_id}:{part1}_{year}-{sheet}/full/pct:25/0/default.jpg'


def build_sheet_list():

	city_dict = build_city_dict(vt_page)

	city_dict = add_sheet_lists(city_dict)

	sheet_list = download_data(city_dict)

	return sheet_list


def build_city_dict(vt_page):
	r = requests.get(vt_page)
	soup = BeautifulSoup(r.content, "lxml")

	final_dict = {}
	rows = soup.find_all("tr", { "class" : "alternatetr" })

	for row in rows:
	    cols = row.find_all('td')

	    for cell in cols:
	    	if '*' in cell.text.strip():
	    		city_name = cell.text.replace('*','').strip()
	    		city_link = cell.find('a').get('href')
	    		final_dict[city_name] = {'base_url': city_link, 'data': []}

	# print 'filtering by lyndonville remove this'
	# skip_list = ['Bennington', 'Springfield', 'Bethel', 'Burlington', 'South Royalton', 'Barre', 'Waterbury', 'Brattleboro', "Saxton's River", 'Essex Junction', 'Fair Haven', 'Middlebury', 'Hyde_Park', 'Stowe', 'Poultney', 'Lyndonville', 'Brandon', 'Richmond', 'Barton Landing', 'Lyndon']
	# final_dict = {x:y for (x,y) in final_dict.iteritems() if x not in skip_list}

	return final_dict

def add_sheet_lists(final_dict):

	for city, city_dict in final_dict.iteritems():

		city_url = sanborn_root + r'/' + city_dict['base_url']

		r = requests.get(city_url)
		soup = BeautifulSoup(r.content, "lxml")

		table_list = soup.find_all('table')
		for table in table_list:
			if table.get('cellspacing') == '3':
				t = table
				break

		for row in t.find_all('tr'):
			cols = row.find_all('td')

			if cols:
				date = cols[0].text
				sheet_num = cols[1].text
				date_url = cols[4].text

				city_dict['data'].append({'date': date, 'url': date_url, 'sheets': int(sheet_num)})

	return final_dict

def download_data(final_dict):
	sheet_list = []

	old_lookup_dict = {'Middlebury': 1905, 'Lyndonville': 1900,
					   'Lyndon': 1900, 'Manchester': 1904,
					   'Montpelier': 1905}

	for city, city_dict in final_dict.iteritems():

		valid_rows = [x for x in city_dict['data'] if 'http' in x['url']]

		for row in valid_rows:
			year = row['date'].split()[1]

			try:
				year_limit = old_lookup_dict[city]

				if int(year) >= year_limit:
					sheet_list += build_old_url(city, row, year)

				else:
					sheet_list += build_new_url(city, row, year)

			except KeyError:
				sheet_list += build_new_url(city, row, year)

	return sheet_list

def build_new_url(city, row, year):

	sheet_list = []

	sanborn_id = os.path.split(row['url'])[1].replace('.', ':')
	id_part1 = sanborn_id.replace(year, '').split(':')[1][1:]

	for sheet_num in range(1, row['sheets'] + 1):
		sheet_id = str(sheet_num).zfill(4)

		sheet_url = img_root.format(full_id=sanborn_id, part1=id_part1, year=year, sheet=sheet_id)
		sheet = Sheet(city, year, sheet_num, sheet_url)
		sheet_list.append(sheet)

		print sheet_url

		sheet.download()

	return sheet_list

def build_old_url(city, row, year):

	sheet_list = []

	base_url = 'http://memory.loc.gov/'

	r = requests.get(row['url'])
	soup = BeautifulSoup(r.content, "lxml")

	final_dict = {}
	links = [x.get('href') for x in soup.find_all("a") if 'Image' in x.text]

	for l in links:
		single_page = base_url + l

		r = requests.get(single_page)
		soup = BeautifulSoup(r.content, "lxml")

		download_link = base_url + [x.get('href') for x in soup.find_all('a') if 'Download JPEG2000' in x.text][0]
		loc_image_name = os.path.splitext(os.path.basename(download_link))[0]

		sheet_num = str(int(loc_image_name[3:]) / 10)

		sheet = Sheet(city, year, sheet_num, download_link)
		sheet_list.append(sheet)

		sheet.download()

		sheet.convert()

	return sheet_list


