#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import movman
import os
import pandas as pd
from flask import Flask
from flask import render_template
from multiprocessing import Process
app = Flask(__name__)

@app.route("/")
def show_tables():

	if os.path.isfile('db.xlsx'):
		data = pd.read_excel('db.xlsx','doing')
	elif os.path.isfile('/Volumes/data/pt/db.xlsx'):
		data = pd.read_excel('/Volumes/data/pt/db.xlsx','doing')
	else:
		print("error")
		pass


	
	hcol=['db_images','db_title','db_rating','mi_duration','db_countries','db_genres', 'db_subtype','db_year',  'db_summary',]
#        o[o.status != 'done'][col].sort_values(['db_rating'],ascending=0).to_excel(writer, sheet_name='doing')
#        o[o.status == 'done'][col].sort_values(['db_rating'],ascending=0).to_excel(writer, sheet_name='done')

    #data.set_index(['Name'], inplace=True)
    #data.index.name=None
    #females = data.loc[data.Gender=='f']
    #males = data.loc[data.Gender=='m']


	#print(data[hcol].to_json('db.json'))


	pd.set_option('display.max_colwidth', -1)

	return render_template('movman.html', table=data[hcol].to_html(escape=False))

if __name__ == "__main__":
	p = Process(target=movman.run)
	
	p.start()
	
	app.run(debug=True,host='0.0.0.0')
