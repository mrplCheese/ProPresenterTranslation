# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 12:54:30 2023

@author: Bachs
"""
import os
import google.cloud.translate
import requests

presentation = "place_holder"
language_list = ["rw", "es", "fr"]
translated_dict = {}
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '' #Credential file location here. 

def translate_text(text="Hello world!", project_id="my-project-1-275421", target_language_code="rw"):
    print("target_language_code in translate_text: ", target_language_code)
    client = google.cloud.translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": "en-US",
            "target_language_code": target_language_code,
        }
    )
    for translation in response.translations:
        guy = "{}".format(translation.translated_text)
    return guy
    
def translate_list(text=["Hello all!","Hello world!"], project_id="my-project-1-275421", target_language_code = "rw"):
    translated_presentation = []
    print("translate list recieved target language: ", target_language_code)
    for i in text:
        if (len(i)>2):
            #print("i: ", i)
            translated_presentation.append(translate_text(text = i,project_id = project_id, target_language_code = target_language_code))
        else:
            translated_presentation.append(i)
    #print("translated presentation: ", translated_presentation)
    return translated_presentation

def translate_list_of_list(text = [["hello all!"],["hello world!"]], project_id="my-project-1-275421", target_language_code = "rw"):
    #print("recieved target language: ",target_language_code)
    translated_playlist = []
    for i in text:
        translated_playlist.append(translate_list(text = i, target_language_code=target_language_code))
        #print("translated one list!")
    return translated_playlist

def translate_languages(original_text, languages, project_id="my-project-1-275421"):
    global translated_dict
    for language in languages:
        text = translate_list(original_text, project_id, language)
        translated_dict.update({language : text})
#Translate_languages is probably no longer necessary, choosing to have language management in the flaskapp itself. 

def get_presentation_text(request):
    response = request.get("groups")
    original_slides = []
    for x in response:
        woah = x.get("slides")
        for i in woah:
            original_slides.append(i.get("text"))
    return original_slides

def check_for_anoms(host, uuid):
    #print("checking", uuid, "for anomoly")
    try:
        bob = requests.get("http://"+ host +"/v1/presentation/" + uuid + "?chunked =false").json().get('presentation')
        return [True, bob]
    except:
        return [False, "Null"]
    
    

def getAllText(host = 'localhost:50001'):
    #print("http://" + host + "/v1/playlist/active?chunked=false")
    response = requests.get("http://"+ host + "/v1/playlist/active?chunked=false").json()
    #print("first request: success")
    #retrieve UUID for the second piece.
    print(response)
    uuid = response.get('presentation').get('playlist').get('uuid')
    new_url = "http://"+ host +"/v1/playlist/" + uuid + "?chunked=false"
    next_response = requests.get(new_url).json()
    pres_list = next_response.get('items')
    uuid_list = []
    for item in pres_list:
        #print(item.get('id').get('uuid'))
        uuid_list.append(item.get('id').get('uuid'))

    pres_list = []
    for item in uuid_list:
        checker = check_for_anoms(host, item)
        if (checker[0]):
            pres_list.append(checker[1])

    slides_list = []
    for item in pres_list:
        slides_list.append(get_presentation_text(item))
    return (slides_list)
