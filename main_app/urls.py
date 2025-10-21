from django.urls import path
from . import views # Import views to connect routes to view functions

urlpatterns = [
    # Routes will be added here
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('cards/', views.cards_index, name='cards'),
    path('cards/create/', views.add_new_card, name="card-create"),
    path('create-conversion/', views.create_conversion, name="create-conversion")  
]