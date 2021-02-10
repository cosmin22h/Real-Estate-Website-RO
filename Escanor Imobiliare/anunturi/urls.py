from django.urls import path

from . import views

### url-uri ###

#path(cale_acces, metoda_din_views, nume_pentru_identificare_din_html)
urlpatterns = [
    #liste anunturi
    path('', views.anunturi, name='listings'),
    path('apartamente', views.lista_apartamente, name='apartaments'),
    path('case', views.lista_case, name='houses'),
    path('terenuri', views.lista_terenuri, name='lands'),

    #anunt
    path('apartamente/apartament/<int:apartament_id>', views.apartament, name='apartament'),
    path('case/casa/<int:casa_id>', views.casa, name='house'),
    path('terenuri/teren/<int:teren_id>', views.teren, name='land'),

    #cautare anunt
    path('cautare', views.cautare, name='search'),

]