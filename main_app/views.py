# main_app/views.py
import asyncio
from django.shortcuts import render, redirect
from django.http import HttpResponse
from googletrans import Translator, LANGUAGES
from .models import Card, ResultCard
from .forms import CardForm, ResultCardForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.contrib.auth import login
from asgiref.sync import sync_to_async

def logout(request):
    if request.method=="POST":
        auth.logout(request)
        return redirect('about')

def signup(request):
    error_message = ''
    if request.method == 'POST':      
        form = UserCreationForm(request.POST)
        if form.is_valid():           
            user = form.save()            
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid sign up - try again'
   
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)

class Home(LoginView):
    template_name = 'home.html'

def home(request):
    # Send a simple HTML response
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def cards_index(request):
    # Render the cats/index.html template with the cats data
    cardz = ResultCard.objects.filter(user=request.user)
    #print(cardz)    
    return render(request, 'cards/index.html', {'resultcards': cardz})

def show_languages():
    for language in LANGUAGES:
        print(language," " * (8 - len(language)),LANGUAGES[language])

@login_required
def add_new_card(request):
    #Access form
    cardform = CardForm()    
    result_form = ResultCardForm()   
    return  render(request, 'cards/newcard.html',{'cardform':cardform, 'resultform':result_form})

def get_translation(request):
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
                    translated =  translator.translate(text= textinput)                       
                else:
                    translated =  translator.translate(text= textinput, dest=output_language)   
            else:
                translated =  translator.translate(text= textinput,src=input_language,dest=output_language)   
            
            try:
                translate_result = asyncio.run(translated)
                translated_text = translate_result.text         
            except Exception as e:
                print(f"Error = {e}")
                return { "form_valid":False}

            return {                
                    'result':translated_text,
                    'title':input_language+" -> "+output_language,
                    'form_valid': True               
            }
        return {"form_valid":False}

@login_required    
async def create_conversion(request):
    data = await sync_to_async(get_translation,thread_sensitive=True)(request)
    
    def check_auth_status(user):
        return user.is_authenticated
    
    is_user_authenticated = await sync_to_async(check_auth_status)(request.user)
   
    context = {}
    if data and data["form_valid"]:
        translated_text = data["result"]
        print("translated_text = {translated_text}")
        title = data["title"]
        result_form = ResultCardForm(
            initial = {
                'result':translated_text,
                'title':title
            }
        )        
        form = CardForm(request.POST)
        context = {
            'cardform':form,
            'resultform':result_form,
            'user_is_authenticated':is_user_authenticated
        }    
    else:
        form = CardForm(request.POST or None)
        result_form = ResultCardForm()
        context = {
            'cardform':form,
            'resultform':result_form,
            'user_is_authenticated':is_user_authenticated            
        }
    context['user_is_authenticated'] = is_user_authenticated
    #print(context)
    return render(request,'cards/newcard.html',context)

@login_required
def save_translation(request):    
    if(request.method == "POST"):
        result_form = ResultCardForm(request.POST)            
        if result_form.is_valid():    
            title =  result_form.cleaned_data['title'] 
            result = result_form.cleaned_data['result']
            note = result_form.cleaned_data['note']    
            result_form.instance.user = request.user        
            result_form.save()   
    cardz = ResultCard.objects.filter(user=request.user)                    
    return render(request, 'cards/index.html', {'resultcards': cardz})

@login_required
def saveupdate(request,resultcard_id):        
    if(request.method == "POST"):
        result_form = ResultCardForm(request.POST)            
        if result_form.is_valid():    
            title =  result_form.cleaned_data['title'] 
            result = result_form.cleaned_data['result']
            updated_note = result_form.cleaned_data['note']                     
            obj_to_update = ResultCard.objects.get(id=resultcard_id)
            obj_to_update.note = updated_note
            obj_to_update.save()
    cardz = ResultCard.objects.filter(user=request.user)                  
    return render(request, 'cards/index.html', {'resultcards': cardz})       

@login_required
def card_detail(request, resultcard_id):
    card = ResultCard.objects.get(id=resultcard_id)            
    return render(request, 'cards/details.html', {'card':card})

@login_required
def card_delete(request, resultcard_id):
    obj_to_delete = ResultCard.objects.get(id=resultcard_id)
    obj_to_delete.delete()
    cardz = ResultCard.objects.filter(user=request.user)    
    return render(request, 'cards/index.html', {'resultcards': cardz})
    
@login_required
def card_update(request, resultcard_id):            
    card = ResultCard.objects.get(id=resultcard_id)    
    #print(f"card data = {card.note}")
    form_to_update = ResultCardForm(
         initial = {
                'title':card.title,
                'result':card.result,                
                'note':card.note
            }
    )              
    return render(request, 'cards/newnote.html',{'resultform':form_to_update, 'card':card ,'resultcard_id':resultcard_id})
