# main_app/views.py
import asyncio
from django.shortcuts import render
from django.http import HttpResponse
from googletrans import Translator, LANGUAGES
from .models import Card, ResultCard
from .forms import CardForm

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
    #Access form
    cardform = CardForm()    

    #Test data  
    # short_lang = []
    # full_lang = []
    # for language in LANGUAGES:
    #     short_lang.append(language)
    #     full_lang.append(LANGUAGES[language].capitalize())        
    # zipped_data = zip(short_lang, full_lang)
    #return  render(request, 'cards/newcard.html',{'translated':translated, 'zipped_data':zipped_data})    
    return  render(request, 'cards/newcard.html',{'cardform':cardform})
    
async def create_conversion(request):
    if(request.method == "POST"):
        form = CardForm(request.POST)
        if form.is_valid():
            textinput = form.cleaned_data['textinput']
            input_language = form.cleaned_data['input_language']
            output_language = form.cleaned_data['output_language']                                                
            translator = Translator()
            translated = await translator.translate(text= textinput)   

    return render(request,'cards/newcard.html',{'cardform':form,'translated':translated})