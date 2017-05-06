import os
import requests
import errno
import shutil


class Sheet(object):

	def __init__(self, city, year, sheet_num, loc_url):

		print 'Creating sheet for {} in {}, sheet num {}'.format(city, year, sheet_num)
		self.city = city.lower()
		self.year = year
		self.sheet_num = str(sheet_num)
		self.loc_url = loc_url

		self.s3_url = None


	def download(self):
		city_text = self.city.replace(' ', '_')

		cwd = os.path.dirname(os.path.realpath(__file__))
		local_path = os.path.join(cwd, 'images', city_text, self.year, self.sheet_num + '.jpg')

		s3_base_url = r'http://vermont-sanborn-maps.s3.amazonaws.com/from-loc/{}/{}/{}.jpg'
		self.s3_url = s3_base_url.format(city_text, self.year, self.sheet_num)

		mkdir_p(os.path.dirname(local_path))

		#r = requests.get(self.loc_url, stream=True)
		#if r.status_code == 200:
		#    with open(self.local_path, 'wb') as f:
		#        r.raw.decode_content = True
		#        shutil.copyfileobj(r.raw, f)  




def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


