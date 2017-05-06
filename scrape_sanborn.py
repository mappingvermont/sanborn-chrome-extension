import os
import requests
from bs4 import BeautifulSoup


sanborn_root = r'http://www.loc.gov/rr/geogmap/sanborn/'
vt_page = sanborn_root + r'/states.php?stateID=52'
img_root = r'http://tile.loc.gov/image-services/iiif/service:gmd:gmd375m:g3754m:{full_id}:{part1}_{year}-{sheet}/full/pct:25/0/default.jpg'

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


	break

for city, city_dict in final_dict.iteritems():

	valid_rows = [x for x in city_dict['data'] if 'http' in x['url']]

	for row in valid_rows:
		#print row

		sanborn_id = os.path.split(row['url'])[1].replace('.', ':')
		year = row['date'].split()[1]

		id_part1 = sanborn_id.replace(year, '').split(':')[1][1:]

		for sheet_num in range(1, row['sheets'] + 1):
			sheet_id = str(sheet_num).zfill(4)

			sheet_url = img_root.format(full_id=sanborn_id, part1=id_part1, year=year, sheet=sheet_id)
			print sheet_url