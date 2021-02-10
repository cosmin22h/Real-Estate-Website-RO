from django.shortcuts import render, get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib import messages

from .models import *
from utilizatori.models import Client 
from judete.models import District

from alte_date.cautare import TIP_PROPRIETATE
from alte_date.judete import JUDETE

### metode views ### 

#lista de cele mai recente anunturi
def anunturi(request):

    #se preaia din baza de date cele mai recente 3 anunturi din fiecare categorie, in functie 
    #de date de publicare si trebuie sa fie publice
    apartamente = Apartament.objects.order_by('-data_publicare').filter(publicat=True)[:3]
    case = House.objects.order_by('-data_publicare').filter(publicat=True)[:3]
    terenuri = Land.objects.order_by('-data_publicare').filter(publicat=True)[:3]

    #trimiterea datelor spre pagina html
    context = {
        'apartaments': apartamente,
        'houses': case,
        'lands': terenuri,
    }

    #randarea paginii html
    return render(request, 'anunturi/lista_anunturi.html', context)

#lista - apartamente
def lista_apartamente(request):

    #se preia din baza de date toate anunturile cu apartamentele publicate,
    #in functie de data de publicare
    apartamente = Apartament.objects.order_by('-data_publicare').filter(publicat=True)

    #paginare - 6 apartamente/pagina
    paginator_apartamente = Paginator(apartamente, 6) 
    page_apartamente = request.GET.get('page')
    paged_apartamente = paginator_apartamente.get_page(page_apartamente)

    #pregatirea datelor pentru pagina html
    context = {
        'apartaments': paged_apartamente,
    }

    #randarea paginii html
    return render(request, 'anunturi/lista_apartamente.html', context)

#lista - case
def lista_case(request):

    #se preia din baza de date toate anunturile cu casele publicate,
    #in functie de data de publicare
    case = House.objects.order_by('-data_publicare').filter(publicat=True)

    #paginare - 6 case/pagina
    paginator_case = Paginator(case, 6)
    page_case = request.GET.get('page')
    paged_case = paginator_case.get_page(page_case)

    #pregatirea datelor pentru pagina html
    context = {
        'houses': paged_case,
    }

    #randarea paginii html
    return render(request, 'anunturi/lista_case.html', context)

#lista - terenuri
def lista_terenuri(request):

    #se preia din baza de date toate anunturile cu terenurile publicate,
    #in functie de data de publicare
    terenuri = Land.objects.order_by('-data_publicare').filter(publicat=True)

    #paginare - 6 terenuri/pagina
    paginator_terenuri = Paginator(terenuri, 6)
    page_terenuri = request.GET.get('page')
    paged_terenuri = paginator_terenuri.get_page(page_terenuri)

    #pregatirea datelor pentru pagina html
    context = {
        'lands': paged_terenuri,
    }

    #randarea paginii html
    return render(request, 'anunturi/lista_terenuri.html', context)

#vizualizare apartament
def apartament(request, apartament_id):

    #preluare apartament din baza de date/eroare: pagina nu a fost gasita
    apartament = get_object_or_404(Apartament, pk=apartament_id) 

    #verificam daca un client este logat
    client = []
    if request.user.is_authenticated:
        try:
            client = Client.objects.get(user=request.user, tip_client='Client')
        except Exception:
            client = []

    #se doreste adagarea apartamentul la lista de favorite a clientului
    #metoda POST poate fi apelata doar de un client logat
    if request.method == 'POST':
        #clientul logat
        #anunturile favorite a clientulului
        anunturi_favorite = FavoriteListing.objects.get(client=client)

        #verificare - apartament deja adaugat in lista
        if apartament in anunturi_favorite.apartamente_favorite.all():
            #afisare mesaj informativ
            messages.info(request, 'Apartamentul se afla deja in lista de favorite')
        else:
            #adaugare apartament in lista de favorite
            anunturi_favorite.apartamente_favorite.add(apartament)
            anunturi_favorite.save()

    #pregatirea datelor pentru pagina html - apartament, client logat, judete
    context = {
        'apartament': apartament,
        'client': client,
        'districts': District.objects.all(),
    }

    #randarea paginii html
    return render(request, 'anunturi/apartament.html', context)

#vizualizare casa
def casa(request, casa_id):

    #preluare casa din baza de date/eroare: pagina nu a fost gasita
    casa = get_object_or_404(House, pk=casa_id)

    #verificam daca un client este logat
    client = []
    if request.user.is_authenticated:
        try:
            client = Client.objects.get(user=request.user, tip_client='Client')
        except Exception:
            client = []

    #se doreste adagarea casei la lista de favorite a clientului
    #metoda POST poate fi apelata doar de un client logat
    if request.method == 'POST':
        client = Client.objects.get(user=request.user)
        anunturi_favorite = FavoriteListing.objects.get(client=client)

        if casa in anunturi_favorite.case_favorite.all():
            #afisare mesaj informativ
            messages.info(request, 'Casa se afla deja in lista de favorite')
        else:
            #adaugare casa in lista de favorite
            anunturi_favorite.case_favorite.add(casa)
            anunturi_favorite.save()

    #pregatirea datelor pentru pagina html - casa, client logat, judete
    context = {
        'house': casa,
        'client': client,
        'districts': District.objects.all(),
    }

    #randarea paginii html
    return render(request, 'anunturi/casa.html', context)

#vizualizare teren
def teren(request, teren_id):

    #preluare teren din baza de date/eroare: pagina nu a fost gasita
    teren = get_object_or_404(Land, pk=teren_id)

    #verificam daca un client este logat
    client = []
    if request.user.is_authenticated:
        try:
            client = Client.objects.get(user=request.user, tip_client='Client')
        except Exception:
            client = []

    #se doreste adagarea terenului la lista de favorite a clientului
    #metoda POST poate fi apelata doar de un client logat
    if request.method == 'POST':
        client = Client.objects.get(user=request.user)
        anunturi_favorite = FavoriteListing.objects.get(client=client)

        if teren in anunturi_favorite.terenuri_favorite.all():
            #afisare mesaj informativ
            messages.info(request, 'Terenul se afla deja in lista de favorite')
        else:
            #adaugare casa in lista de favorite
            anunturi_favorite.terenuri_favorite.add(teren)
            anunturi_favorite.save()

    #pregatirea datelor pentru pagina html - teren, client logat, judete
    context = {
        'land': teren,
        'client': client,
        'districts': District.objects.all(),
    }

    #randarea paginii html
    return render(request, 'anunturi/teren.html', context)

#cautare anunt
def cautare(request):

    #tip anunt cautat
    tipAnunt = None
    #lista anunturi gasite
    anunt = None 
    
    #filtrare obligatorie - tip anunt
    tipCautat = request.GET['tip']
    #apartament
    if tipCautat in ['Garsoniera', 'Apartament']:
        #filtrare in functie de garsoniera si apartament
        anunt = Apartament.objects.order_by('-data_publicare').filter(tip__iexact=tipCautat)
        tipAnunt = 'apartament'
    #teren
    elif tipCautat in ['De constructii' , 'Agricol']:
        #filtrare in functie de tipul terenului - de constructie, agricol
        anunt = Land.objects.order_by('-data_publicare').filter(tip_teren__iexact=tipCautat)
        tipAnunt = 'land'
    #casa
    else:
        anunt = House.objects.order_by('-data_publicare')
        tipAnunt = 'house'

    #filtrare obligatorie - judet
    judetCautat = request.GET['judet']
    anunt = anunt.filter(judet__iexact=judetCautat)

    #filtrare optionala - oras/localitate
    if 'loc' in request.GET:
        locOrasCautat = request.GET['loc']
        if locOrasCautat:
            anunt = anunt.filter(oras_sau_localitate__iexact=locOrasCautat)

    #filtrare optionala - pret
    if 'pret' in request.GET:
        pretCautat = request.GET['pret']
        if pretCautat:
                anunt = anunt.filter(pret__lte=pretCautat)

    #pregatirea datelor pentru pagina html - judete, tipurile de proprietate,
    #anunturile filtrate, tipul de anunt, valorile de filtrare
    context = {
        'states': JUDETE,
        'type': TIP_PROPRIETATE,
        'listings': anunt,
        'listType': tipAnunt,
        'values': request.GET
    }

    #randarea paginii html
    return render(request, 'anunturi/cautare.html', context)
