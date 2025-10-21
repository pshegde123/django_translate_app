# main_app/views.py
import asyncio
from django.shortcuts import render
from django.http import HttpResponse
from googletrans import Translator, LANGUAGES
from .models import Card

def home(request):
    # Send a simple HTML response
    return render(request, 'base.html')

def about(request):
    return render(request, 'about.html')

def cards_index(request):
    # Render the cats/index.html template with the cats data
    cardz = Card.objects.all()
    print(cardz)
    cards=[]
    return render(request, 'cards/index.html', {'cards': cardz})

def show_languages():
    for language in LANGUAGES:
        print(language," " * (8 - len(language)),LANGUAGES[language])

async def add_new_card(request):
    translator = Translator()
    translated = await translator.translate(text= "Buen día")   
    short_lang = []
    full_lang = []
    for language in LANGUAGES:
        short_lang.append(language)
        full_lang.append(LANGUAGES[language].capitalize())        
    zipped_data = zip(short_lang, full_lang)

    return  render(request, 'cards/newcard.html',{'translated':translated, 'zipped_data':zipped_data})