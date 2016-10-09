#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os.path
from flask import Flask
from flask.ext.autoindex import AutoIndex

app = Flask(__name__)
AutoIndex(app, browse_root='/data/pub')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5001)

