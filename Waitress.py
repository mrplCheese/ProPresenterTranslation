# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 11:48:39 2023

@author: Bachs
"""

from waitress import serve
from flaskapp import create_app

app = create_app()

if __name__ == '__main__':
    print("Will begin serving.")
    serve(app, host='192.168.1.123', port=8080) #10.0.0.122
    print("huzzah?")
