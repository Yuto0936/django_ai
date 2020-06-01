from django.urls import path
from . import views


app_name = 'animal_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('predict/', views.predict, name='predict')
]
