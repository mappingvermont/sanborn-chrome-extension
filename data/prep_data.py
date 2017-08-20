import os
import json
import subprocess

import scrape_loc


def main():

	sheet_list = scrape_loc.build_sheet_list()

	push_to_s3()

	dump_to_json(sheet_list)


def push_to_s3():

	cwd = os.path.dirname(os.path.realpath(__file__))
	images_dir = os.path.join(cwd, 'images')

	s3_basedir = r's3://vermont-sanborn-maps/from-loc/'
	cmd = ['aws', 's3', 'cp', '.', s3_basedir, '--recursive']
	cmd += ['--exclude', '*', '--include', '*.jpg']
	cmd += ['--profile', 'mappingvt']

	subprocess.check_call(cmd, cwd=images_dir)

def dump_to_json(sheet_list):

	root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
	output_json = os.path.join(root_dir, 'sheets.json')

	sheet_prop_list = [s.dump_vars() for s in sheet_list]

	# add the var so we can just include this in the header
	# and not worry about loading it asynchronously
	as_js = 'var sheets = ' + json.dumps(sheet_prop_list)

	with open(output_json, 'wb') as thefile:
		thefile.write(as_js)


if __name__ == '__main__':

	main()
