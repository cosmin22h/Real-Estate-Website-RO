from django.urls import path

from . import views

### url-uri ###

urlpatterns = [
    #pagina home
    path('', views.index, name='index'),
    #pagina cu informatii - despre noi
    path('about', views.about, name='about'),
]