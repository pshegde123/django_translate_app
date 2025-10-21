from django import forms
from .models import Card, ResultCard
    
class CardForm(forms.ModelForm):
    class Meta:
        model = Card        
        fields = ['input_language','textinput','output_language']       

class ResultCardForm(forms.ModelForm):
    class Meta:
        model = ResultCard        
        fields = ['title','result','note']       
