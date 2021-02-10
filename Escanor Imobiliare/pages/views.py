from django.shortcuts import render

from anunturi.models import Apartament, House, Land
from alte_date.cautare import TIP_PROPRIETATE
from alte_date.judete import JUDETE

#home
def index(request):

    #cele mai recente anunturi postate
    ap = Apartament.objects.order_by('-data_publicare').filter(publicat=True)[:1]
    h = House.objects.order_by('-data_publicare').filter(publicat=True)[:1]
    l = Land.objects.order_by('-data_publicare').filter(publicat=True)[:1]

    #pregatirea datelor pentru pagina html - anunturile recente, judete, tipuri de proprietati
    context = {
        'apartaments': ap,
        'houses': h,
        'lands': l,
        'states': JUDETE,
        'type': TIP_PROPRIETATE,
    }

    #randarea paginii html 
    return render(request, 'pages/index.html', context)

#despre noi
def about(request):
    
    #randarea paginii html 
    return render(request, 'pages/about.html')
