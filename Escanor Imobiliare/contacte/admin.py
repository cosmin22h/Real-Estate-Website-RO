from django.contrib import admin

from .models import Contact, Raport

### panoul adminului ###

#contact
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'titlu_anunt', 'tip_anunt', 'ID_anunt', 'ID_client', 'data_contactare')
    list_display_links = ('id', 'titlu_anunt')
    list_filter = ('tip_anunt'),
    list_per_page = 25

#raport
class RaportAdmin(admin.ModelAdmin):
    list_display = ('luna_raport', 'an_raport', 'contacte_apartamente', 'contacte_case', 'contacte_terenuri', 'raport_vizibil')
    list_display_links = ('luna_raport', 'an_raport')
    list_filter = ('an_raport'),
    list_editable = ('raport_vizibil',)
    list_per_page = 25

#accesul la contacte si la raporturi in panoul de administratie
admin.site.register(Contact, ContactAdmin)
admin.site.register(Raport, RaportAdmin)