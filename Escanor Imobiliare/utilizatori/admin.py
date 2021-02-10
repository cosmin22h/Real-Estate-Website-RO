from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import *

### panoul adminului ###

#client
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'nume', 'prenume', 'email', 'tip_client',)
    list_display_links = ('id', 'user', 'nume', 'prenume',)
    list_filter = ('tip_client',)
    list_per_page = 25

#agentie imobiliara
class RealEstateAdmin(admin.ModelAdmin):
    list_display = ('user', 'nume', 'email', 'telefon1',)
    list_display_links = ('user', 'nume',)
    list_per_page = 25

#campurile vizibile fara a accesa user-ul
UserAdmin.list_display = ('username', 'email', 'is_staff', 'last_login', 'is_active')
#campul prin care se poate accesa user-ul
UserAdmin.list_display_links = ('username',)
UserAdmin.list_editable = ('is_active',)


#accesul la utilizatori in panoul de administratie
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(RealEstate, RealEstateAdmin)
