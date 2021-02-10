from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

### url-uri ###

urlpatterns = [
    #inregistrare cont nou
    path('cont_nou/', views.inregistrare, name='register'),
    path('cont_nou/client_nou', views.inregistrare_client_nou, name='register_client'),
    path('cont_nou/agentie_noua', views.inregistrare_agentie_imobiliara, name='register_real_estate'),

    #logare, delogare, resetare parola
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name = "parola/reset_password.html"), name ='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name = "parola/password_reset_sent.html"), name ='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name = "parola/password_reset_form.html"), name ='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = "parola/password_reset_done.html"), name ='password_reset_complete'),
    
    #schimare parola
    path('change_password/', views.schimbare_parola, name='change_password'),
    
    #cont client
    path('', views.cont_client, name='client_account'),
    path('editare_cont', views.editare_cont_client, name='edit_client_account'),
    path('client/contactele_mele', views.contacte_client, name='client_contacts'), 

    #cont agentie
    path('agentie', views.cont_agentie, name='real_estate_account'),
    path('agentie/contactele_mele', views.contacte_agentie, name='real_estate_contacts'),
    path('agentie/contactele_mele/<int:contact_id>', views.contact_agentie, name='real_estate_contact'),   
    path('editare_cont_agenite', views.editare_cont_agentie, name='edit_real_estate_account'),
    
    #profil agentii
    path('agentii_imobiliare', views.lista_agentii, name='list_real_estate'),
    path('agentii_imobiliare/profil_agentie/<int:real_estate_id>', views.profil_agentie, name='profil_real_estate'),

    #adaugare anunturi - exclusiv proprietar
    path('adaugare_apartament', views.adaugare_apartament, name='add_apartament'),
    path('adaugare_casa', views.adaugare_casa, name='add_house'),
    path('adaugare_teren', views.adagare_teren, name='add_land'),

    #anunturile proprietarului
    path('anunturile_mele', views.anunturi_proprietar, name='owner_listings'),
    path('anunturile_mele/stergere_apartament/<int:apartament_id>', views.stergere_apartament, name='delete_apartament'),
    path('anunturile_mele/stergere_casa/<int:casa_id>', views.stergere_casa, name='delete_house'),
    path('anunturile_mele/stergere_teren/<int:teren_id>', views.stergere_teren, name='delete_land'),

    #cereri pentru agentii
    path('cereri', views.cereri_anunturi, name='listing_request'),
    path('date_contact_proprietar/<str:username>', views.owner_contacts, name='owner_contacts'),
    path('cereri/posteaza_apartament/<int:apartament_id>', views.posteaza_apartament, name='posts_apartament'),  
    path('cereri/posteaza_casa/<int:casa_id>', views.posteaza_casa, name='posts_house'),
    path('cereri/posteaza_teren/<int:teren_id>', views.posteaza_teren, name='posts_land'),
        
    #anunturi postate - exclusiv agentie
    path('anunturi_postate', views.anunturi_agentie, name='listings_real_estate'),
    path('anunturi_postate/editare_apartament/<int:apartament_id>', views.edit_apartament, name='edit_apartament'),  
    path('anunturi_postate/editare_casa/<int:casa_id>', views.edit_casa, name='edit_house'),
    path('anunturi_postate/editare_teren/<int:teren_id>', views.edit_teren, name='edit_land'), 

    #mesaj - client
    path('mesaje', views.mesaje, name='msgs'),
    path('mesaje/mesaj/<int:msg_id>', views.mesaj, name='msg'),

    #raport - agentie
    path('raport', views.vizualizeaza_raport, name='view_raport'),

    #anunturi favorite - exclusiv client
    path('anunturi_favorite', views.favorite, name='favorites'),
    path('sterge_din_favorite_apartament/<int:apartament_id>', views.stergere_apartament_favorit, name='delete_favorites_apartament'),
    path('sterge_din_favorite_casa/<int:casa_id>', views.stergere_casa_favorita, name='delete_favorites_house'),
    path('sterge_din_favorite_teren/<int:teren_id>', views.stergere_teren_favorit, name='delete_favorites_land'),
]