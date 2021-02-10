from django.urls import path

from . import views

### url-uri ###

urlpatterns = [

    #contactare - anunt
    path('contactare', views.contact, name='contact'),
    
    #contactare - admin (suport)
    path('contact_escanor/', views.contact_escanor, name='contact_escanor'),
]