from django.contrib import admin

from .models import Apartament, House, Land, FavoriteListing

### panoul adminului ###

#list_display - campurile vizibile fara a accesa anuntul
#list_display_links - campurile prin care se poate accesa anuntul
#list_filter - campurile de filtrarea a anunturilor
#list_editable - campurile ce pot fi editate fara a accesa anuntul
#list_per_page - numarul de anunturi pe o pagina

#model apartament pentru admin
class ApartamentAdmin(admin.ModelAdmin):
    list_display = ('id', 'titlu', 'tip', 'judet', 'proprietar', 'agentie_responsabila',  'pret', 'posibilitate_inchiriere', 'publicat', 'data_publicare')
    list_display_links = ('id', 'titlu')
    list_filter = ('tip', 'publicat', 'posibilitate_inchiriere', 'agentie_responsabila', 'judet')
    list_editable = ('publicat', 'posibilitate_inchiriere',)
    list_per_page = 25

#model casa pentru admin
class HouseAdmin(admin.ModelAdmin):
    list_display = ('id', 'titlu', 'judet', 'proprietar', 'agentie_responsabila', 'pret', 'publicat', 'data_publicare')
    list_display_links = ('id', 'titlu')
    list_filter = ('publicat', 'posibilitate_inchiriere', 'agentie_responsabila', 'judet')
    list_editable = ('publicat',)
    list_per_page = 25

#model teren pentru admin
class LandAdmin(admin.ModelAdmin):
    list_display = ('id', 'titlu', 'tip_teren', 'judet', 'proprietar', 'agentie_responsabila', 'pret', 'publicat', 'data_publicare')
    list_display_links = ('id', 'titlu')
    list_filter = ('tip_teren', 'publicat', 'agentie_responsabila', 'judet')
    list_editable = ('publicat',)
    list_per_page = 25

#accesul la anunturi in panoul de administratie
admin.site.register(Apartament, ApartamentAdmin)
admin.site.register(House, HouseAdmin)
admin.site.register(Land, LandAdmin)
admin.site.register(FavoriteListing)

