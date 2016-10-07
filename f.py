#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import movman
import pandas as pd
from flask import Flask
app = Flask(__name__)

@app.route("/")
def show_tables():
    data = pd.read_excel('mm2.xlsx','doing')
    #data.set_index(['Name'], inplace=True)
    #data.index.name=None
    #females = data.loc[data.Gender=='f']
    #males = data.loc[data.Gender=='m']
    return data.to_html()

if __name__ == "__main__":
    app.run(debug=True)
