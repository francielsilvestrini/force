#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import json

csvfile = open('MUNICIPIOS.CSV', 'r')

hearders = ('name', 'code', 'state')
reader = csv.DictReader(csvfile, hearders)
current_state = ''
jsonfile = None
for row in reader:
	if current_state != row['state']:
		if jsonfile is not None:
			jsonfile.close()
		current_state = row['state']
		jsonfile = open('data/%s.json' % current_state, 'w')
	row['name'] = row['name'].title()
	json.dump(row, jsonfile)
	jsonfile.write('\n')
csvfile.close()
if jsonfile is not None:
	jsonfile.close()

