import os
import requests
import errno
import shutil
import subprocess
from retrying import retry


class Sheet(object):

	def __init__(self, city, year, sheet_num, loc_url, gallery_url):

		print 'Creating sheet for {} in {}, sheet num {}'.format(city, year, sheet_num)
		self.city = city.lower()
		self.year = year
		self.sheet_num = str(sheet_num)
		self.loc_url = loc_url
		self.gallery_url = gallery_url

		self.s3_url = None
		self.local_path = None

	@retry(wait_exponential_multiplier=1000, wait_exponential_max=10000)
	def download(self):
		city_text = self.city.replace(' ', '_')

		ext = os.path.splitext(self.loc_url)[1]

		cwd = os.path.dirname(os.path.realpath(__file__))
		self.local_path = os.path.join(cwd, 'images', city_text, self.year, self.sheet_num + ext)

		s3_base_url = r'http://vermont-sanborn-maps.s3.amazonaws.com/from-loc/{}/{}/{}.jpg'
		self.s3_url = s3_base_url.format(city_text, self.year, self.sheet_num)

		mkdir_p(os.path.dirname(self.local_path))

		r = requests.get(self.loc_url, stream=True)
		if r.status_code == 200:
		    with open(self.local_path, 'wb') as f:
		        r.raw.decode_content = True
		        shutil.copyfileobj(r.raw, f)  
		else:
			print self.city, self.year, self.sheet_num
			print self.loc_url
			raise ValueError('status code {} returned'.format(r.status_code))

	def convert(self):

		jp2_output = self.local_path.replace('jp2', 'jpg')
		cmd = ['convert',  self.local_path, '-resize', '15%', jp2_output]

		print 'converting year {}, sheet {} from jp2 to jpg'.format(self.year, self.sheet_num)
		subprocess.check_call(cmd)

	def dump_vars(self):
		skip_list = ['local_path', 'loc_url']

		return {x:y for x, y in self.__dict__.iteritems() if x not in skip_list}


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


