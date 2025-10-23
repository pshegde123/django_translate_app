from django.urls import path
from . import views # Import views to connect routes to view functions
from django.contrib.auth import logout

urlpatterns = [
    # Routes will be added here
    path('', views.Home.as_view(), name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('logout', views.logout, name='logout'),
    path('about/', views.about, name='about'),
    path('cards/', views.cards_index, name='cards'),
    path('cards/create/', views.add_new_card, name="card-create"),
    path('create-conversion/', views.create_conversion, name="create-conversion"),
    path('save-translation/', views.save_translation, name="save-translation") , 
    path('cards/<int:resultcard_id>/', views.card_detail, name='card-detail'),
    path('cards/<int:resultcard_id>/delete/', views.card_delete, name='card-delete'),
    path('cards/<int:resultcard_id>/update/', views.card_update, name='card-update'),
]