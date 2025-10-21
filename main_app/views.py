# main_app/views.py
import asyncio
from django.shortcuts import render
from django.http import HttpResponse
from googletrans import Translator, LANGUAGES
from .models import Card, ResultCard
from .forms import CardForm, ResultCardForm

def home(request):
    # Send a simple HTML response
    return render(request, 'base.html')

def about(request):
    return render(request, 'about.html')

def cards_index(request):
    # Render the cats/index.html template with the cats data
    cardz = Card.objects.all()
    #print(cardz)    
    return render(request, 'cards/index.html', {'cards': cardz})

def show_languages():
    for language in LANGUAGES:
        print(language," " * (8 - len(language)),LANGUAGES[language])

async def add_new_card(request):
    #Access form
    cardform = CardForm()    
    result_form = ResultCardForm()
    #Test data  
    # short_lang = []
    # full_lang = []
    # for language in LANGUAGES:
    #     short_lang.append(language)
    #     full_lang.append(LANGUAGES[language].capitalize())        
    # zipped_data = zip(short_lang, full_lang)
    #return  render(request, 'cards/newcard.html',{'translated':translated, 'zipped_data':zipped_data})    
    return  render(request, 'cards/newcard.html',{'cardform':cardform, 'resultform':result_form})
    
async def create_conversion(request):
    if(request.method == "POST"):
        form = CardForm(request.POST)       
        result_form = ResultCardForm(request.POST)          
        if form.is_valid():
            textinput = form.cleaned_data['textinput']
            input_language = form.cleaned_data['input_language']
            output_language = form.cleaned_data['output_language']                                                
            translator = Translator()
            if(input_language == 'auto'):
                if(output_language == 'en'):
                    translated = await translator.translate(text= textinput)                       
                else:
                    translated = await translator.translate(text= textinput, dest=output_language)   
            else:
                translated = await translator.translate(text= textinput,src=input_language,dest=output_language)   
            translated_text = translated.text                
            result_form = ResultCardForm(
                initial={
                    'result':translated_text,
                    'title':input_language+" -> "+output_language
                }
            )
            
    return render(request,'cards/newcard.html',{'cardform':form,'resultform':result_form})

def save_translation(request):    
    if(request.method == "POST"):
        result_form = ResultCardForm(request.POST)            
        if result_form.is_valid():      
            result = result_form.cleaned_data['result']
            note = result_form.cleaned_data['note']            
            print(title,result,note)
                   
    return render(request, 'about.html')