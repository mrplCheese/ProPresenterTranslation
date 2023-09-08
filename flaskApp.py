# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 11:03:59 2023

@author: Bachs
"""
from flask import Flask, request, jsonify, render_template
import translationApp
import json
#import BibleAPIRequest #Eventually

allText = translationApp.getAllText()#optional param: host
languages = ['eng']
playlist_dict = {'eng':allText}
"""
Key-value pairs are like this: 
    'language_key_code'
"""

def create_app():
    app = Flask(__name__)
    
    @app.route('/', methods = ['GET'])
    def home():
        return(render_template('Dropdown.html'))
    
    @app.route('/secondOption', methods = ['GET'])
    def word():
        selected_value = request.args.get('data')
        print("selected value:", selected_value)
        return(render_template('secondOption.html')) 
    
    def check_lang(language = 'eng'):
        print("language:", language)
        if(language in languages):
            print("already in list")
        else:
            languages.append(language)
            value = translationApp.translate_list_of_list(text = allText, target_language_code = language)
            playlist_dict[language] = value
            print("Translated! Yay.")
    
    @app.route('/request', methods = ['POST'])
    def collect_selection():
        print("request called.")
        data = request.get_json()
        selected_value = data.get('selectedValue')
        print(selected_value)
        check_lang(language = selected_value)
        response_message = jsonify(playlist_dict[selected_value])
        return response_message
    
    return app

if(__name__ == '__main__'):
    print("huzzah!")
    app = create_app()
    app.run(debug = False, port = 5000)

#allText = translationApp.getAllText() #Every presentation in English. 
