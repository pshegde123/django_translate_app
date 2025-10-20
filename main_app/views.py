# main_app/views.py

from django.shortcuts import render

# Import HttpResponse to send text-based responses
from django.http import HttpResponse

# views.py

class Card:
    def __init__(self, title,inlang, textinput, outlang,result):
        self.title = title
        self.input_language = inlang
        self.textinput = textinput
        self.output_language = outlang
        self.result = result

cards = [
    Card('ENG->HND','English', 'hello', 'Hindi', 'XXXX1'),
    Card('ENG->HND','English', 'hello', 'Hindi', 'XXXX2'),
    Card('ENG->HND','English', 'hello', 'Hindi', 'XXXX3'),
    Card('ENG->HND','English', 'hello', 'Hindi', 'XXXX4'),
]


# Define the home view function
def home(request):
    # Send a simple HTML response
    return render(request, 'base.html')

def about(request):
    return render(request, 'about.html')

def cards_index(request):
    # Render the cats/index.html template with the cats data
    return render(request, 'cards/index.html', {'cards': cards})