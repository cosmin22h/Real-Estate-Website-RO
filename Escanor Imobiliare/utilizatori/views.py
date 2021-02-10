from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail

from datetime import datetime, date
from .models import *
from anunturi.models import *
from contacte.models import *
from judete.models import District
from alte_date.imobile import *
from alte_date.conturi import TIP_CLIENT, SPECIAL_CHARACTERS
from alte_date.judete import JUDETE
from alte_date.terenuri import TEREN_T


#validatori - creare cont nou
class InputValidators:
    #validator parola
    def validatorParola(self, request, parola, confirma_parola, date_cont):
        #parolele se potrivesc
        if parola != confirma_parola:
            messages.error(request, 'Parolele nu se potrivesc')
            return False
        #parola nu contine date ale contului
        for info in date_cont:
            if info in parola:
                messages.error(request, 'Parola nu poate fi similară cu alte date ale contului')
                return False
        #parola are lungimea potrivita
        if len(parola) < 8:
            messages.error(request, 'Parola trebuie sa contina minim 8 carcactere pentru a fi valida')
            return False
        #parola nu este comuna
        if 'password' in parola or 'parola' in parola:
            messages.error(request, 'Parola e prea comună')
            return False
        #parola nu contine doar caractere numerice
        if parola.isdigit():
            messages.error(request, 'Parola nu poate să conțină exclusiv caractere numerice')
            return False
        
        return True

    #validator pentru data nasterii
    def validatorDataDeNastere(self, request, ziDeNastere_str):
        #ziua prezenta
        dataPrez = date.today()
        try:
            #converitirea datei de nastere din str in date
            ziDeNastere = datetime.strptime(ziDeNastere_str, '%Y-%m-%d').date()
        except ValueError:
            #an invalid
            messages.error(request, 'An nu este valid')
            return False
        #calcularea varstei
        ani = dataPrez.year - ziDeNastere.year - ((dataPrez.month, dataPrez.day) < (ziDeNastere.month, ziDeNastere.day)) 
        #verificarea varstei minime
        if ani < 18:
            messages.error(request, 'Varsta minima trebuie sa fie de 18 ani')
            return False

        return True

#inregitrare
def inregistrare(request):
    #randarea paginii html
    return render(request, 'utilizatori/tip_cont.html')

#inregitrare client
def inregistrare_client_nou(request):

    #confirmare creare cont
    if request.method == 'POST':
        #preuare valori
        username = request.POST['username']
        tip_client = request.POST['tip_client']
        nume = request.POST['nume']
        prenume = request.POST['prenume']
        telefon = request.POST['telefon']
        email = request.POST['email']
        data_nasterii = request.POST['data_nasterii']
        password = request.POST['password']
        confirm_password = request.POST['password2']

        #validator
        validator = InputValidators()

        #verificare parola
        if validator.validatorParola(request, password, confirm_password, [username, tip_client, nume, prenume, telefon, email, data_nasterii]) == False:
            return redirect('register_client')

        #verificare username - nu exista deja, nu contine doar cifre, nu contine caractere speciale
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Acest username exista deja')
            return redirect('register_client')
        if username.isdigit():
            messages.error(request, 'Username-ul nu poate contine doar caractere numerice')
            return redirect('register_client')
        for caracter in SPECIAL_CHARACTERS:
            if caracter in username:
                messages.error(request, 'Nu se pot folosi caractere speciale in username')
                return redirect('register_client')

        #verificare email
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Acest email exista deja')
            return redirect('register_client')

        #verificare data nasterii
        if validator.validatorDataDeNastere(request, data_nasterii) == False:
            return redirect('register_client')

        #inregistrare user
        if tip_client == 'Client':
            user = User.objects.create_user(username=username, password=password, email=email, first_name=prenume)
        else:
            user = User.objects.create_user(username=username, password=password, email=email, first_name=prenume)
        user.save()
        #inregistrare client
        if tip_client == 'Client':
            client = Client(user= user,tip_client=TIP_CLIENT[0][0], nume=nume, prenume=prenume,  telefon=telefon, email=email, data_nasterii=data_nasterii)
            client.save()
            #creare lista favorite
            anunturi_client = FavoriteListing(client=client)
            anunturi_client.save()
        else:
            #inregistrare proprietar
            proprietar = Client(user=user, tip_client=TIP_CLIENT[1][0], nume=nume, prenume=prenume, telefon=telefon, email=email, data_nasterii=data_nasterii)
            proprietar.save()

        #mesaj succes
        messages.success(request, '\n contul a fost creat')

        #redirectionare catre pagina de login
        return redirect('login')  
    else:
        #randarea paginii html 
        return render(request, 'utilizatori/cont_nou_client.html')

#inregitrare agentie imobiliara
def inregistrare_agentie_imobiliara(request):

    #confirmare creare cont
    if request.method == 'POST' and 'imagine_logo' in request.FILES:

        #preluare valori
        CIF = request.POST['username']
        nume = request.POST['nume']
        logo = request.FILES['imagine_logo']
        email = request.POST['email']
        telefon1 = request.POST['telefon']
        adresa_sediu = request.POST['adresa_sediu']
        an_infiintare = request.POST['an_infiintare']
        password = request.POST['password']
        confirm_password = request.POST['password2']

        #validator
        validator = InputValidators()

        #verificare parola
        if validator.validatorParola(request, password, confirm_password, [CIF, nume, email, telefon1, adresa_sediu, an_infiintare]) == False:
            return redirect('register_real_estate')

        #verificare username - nu exista, nu contine caractere exclusiv caractere numerice
        if User.objects.filter(username=CIF).exists():
            messages.error(request, 'Acesta agentie este inregistrata')
            return redirect('register_real_estate')
        if CIF.isdigit() == False:
            messages.error(request, 'CIF-ul trebuie sa contine doar caractere numerice')
            return redirect('register_real_estate')

        #verificare email
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Acest email exista deja')
            return redirect('register_real_estate')

        #verificare an infiintare
        anPrez = date.today().year
        if int(an_infiintare) > anPrez:
            messages.error(request, 'An de infiintare necorespunzator')
            return redirect('register_real_estate')

        #inregistrare user
        user = User.objects.create_user(username=CIF, password=password, email=email, first_name=nume)
        #cont inactiv - adminul trebuie sa il activeze
        user.is_active = False
        #inregistrare agentie imobiliara
        realEstate = RealEstate(user=user, nume=nume, logo=logo, email=email, telefon1=telefon1, adresa_sediu=adresa_sediu, an_infiintare=an_infiintare)
        user.save()
        realEstate.save()

        #mesaj succes
        messages.success(request, 'cererea a fost trimisa')

        #redirectionare catre pagina de login
        return redirect('login')  
    else:
        #randarea paginii html
        return render(request, 'utilizatori/cont_nou_agentie.html')

#login
def login(request):

    #confirmare login
    if request.method == 'POST':
        #preluare username si parola
        username = request.POST['username']
        password = request.POST['password']

        #verificare username
        if User.objects.filter(username=username).exists():
            user = auth.authenticate(username=username, password=password)
            #parola nu e corecta sau contul este inactiv
            if user is None:
                messages.error(request, 'Parola este incorecta sau contul este inactiv')
                return redirect(request.path_info)

            #user-ul e admin
            if user.is_superuser:
                auth.login(request, user)
                return redirect('index')

            #autentificare si mesaj succes    
            auth.login(request, user)

            #redirectionare cont agentie imobiliara
            if user.username.isdigit():
                return redirect('real_estate_account')
            #redirectionare cont client/proprietar
            else:
                return redirect('client_account')

        #utilizatorul nu exista
        else:
            messages.error(request, 'Utilizator nu este inregistrat')
            #redirectionare pagina login
            return redirect(request.path_info)
    else:
        #randare pagina html
        return render(request, "utilizatori/login.html")

#logout
def logout(request):

    #confirmare logout
    if request.method == 'POST':
        auth.logout(request)
        return redirect('index')

#pagina cont client
def cont_client(request):

    #client autentificat
    client = Client.objects.get(user=request.user)

    #client propriu-zis
    if client.tip_client == 'Client':

        #preluarea celor mai recente 5 contacte  trimise de client
        contacte = Contact.objects.order_by('-data_contactare').filter(ID_client=client.id)[:5]
        
        #randare pagina html si trimitere date - client si contacte
        return render(request, "utilizatori/cont_client.html", {
            'client': client,
            'contacts': contacte,
        })

    #proprietar
    else:
        #preluarea celor mai recente 5 mesaje (contacte) trimise de clienti
        contacte = Contact.objects.order_by('-data_contactare').filter(username_proprietar=client.user.username, proprietar_contactat=True, vazut=False)[:5]
        
        #randare pagina html si trimitere date - client (proprietar) si contacte
        return render(request, "utilizatori/cont_proprietar.html", {
            'client': client,
            'contacts': contacte,
        })

#lista contacte - client
def contacte_client(request):

    #clientul inregistrat
    client = Client.objects.get(user=request.user)

    #lista cu toate contactele trimise
    contacte = Contact.objects.order_by('-data_contactare').filter(ID_client=client.id)

    #randare pagina html si trimitere date - client si contacte
    return render(request, "utilizatori/lista_contacte_clienti.html", {
            'client': client,
            'contacts': contacte,
        })

#lista mesaje (contacte) - proprietar
def mesaje(request):

    #propritar autentificat
    propritar = Client.objects.get(user=request.user)

    #toate mesajele (contactele) proprietarului
    contacte = Contact.objects.all().filter(username_proprietar=request.user.username, proprietar_contactat=True)
   
    # pregatire date pentru html - proprietar si contacte
    context = {
        'owner': propritar,
        'contacts': contacte,
    }

    #randare pagina html
    return render(request, "utilizatori/mesaje.html", context)

#vizualizare mesaj - proprietar
def mesaj(request, msg_id):

    #proprietar autentificat
    owner = Client.objects.get(user=request.user)
    #mesajul (contactul) 
    contact = Contact.objects.get(id=msg_id)
    #agenitia responsabila ce a trimis contactul de la client catre proprietar
    realEstate = RealEstate.objects.get(id=contact.ID_agentie)

    #modificare camp mesajul (contactul) vazut
    contact.vazut = True
    contact.save()

    #pregatire date pentru html - proprietar, contact, agentie responsabila
    context = {
        'owner': owner,
        'contact': contact,
        'realEstate': realEstate,
    }

    #randare pagina html
    return render(request, "utilizatori/mesaj.html", context)

#editare cont client
def editare_cont_client(request):

    #clientul autentificat
    client = Client.objects.get(user=request.user)

    #confirmare - salvare
    if request.method == 'POST':
        #preluare date modificate

        #nume si prenume
        client.nume = request.POST['nume']
        client.prenume = request.POST['prenume']

        #email
        if request.POST['email']:
            #verificarea email - sa nu existe deja
            if User.objects.filter(email=request.POST['email']).exists():
                messages.error(request, 'Acest email exista deja')
            else:    
                client.email = request.POST['email']
                request.user.email = client.email
                request.user.save()

        #numar telefon
        if request.POST['telefon']:
            client.telefon = request.POST['telefon']

        #data nasterii
        if request.POST['data_nasterii']:
            validator = InputValidators()
            #validare data de nastere
            if validator.validatorDataDeNastere(request, request.POST['data_nasterii']) == True:
                client.data_nasterii = request.POST['data_nasterii']

        client.save()

        return redirect(request.path_info)

    #pregatire date pentru html - client
    context = {
        'client': client,
    }

    #randare pagina html
    return render(request, "utilizatori/editare_cont_client.html", context)

#pagina cont agentie
def cont_agentie(request):

    #agentie imobiliara autentificata
    agentie = RealEstate.objects.get(user=request.user)

    #cele mai recente 5 contacte primite de la clienti
    contacte = Contact.objects.order_by('-data_contactare').filter(ID_agentie=agentie.id)[:5]

    #pregatire date catre html - agentie imobiliara, contactare
    context = {
        'realEstate': agentie,
        'contacts': contacte,
    }

    #randare pagina html
    return render(request, "utilizatori/cont_agentie.html", context)

#contacte - agentie
def contacte_agentie(request):

    #agentie autentificata
    agentie = RealEstate.objects.get(user=request.user)

    #toate contactele agentiei
    contacte = Contact.objects.order_by('-data_contactare').filter(ID_agentie=agentie.id)

    #randare pagina html si trimitere date - agentie si toate contactele ei
    return render(request, "utilizatori/lista_contacte_agentie.html", {
            'realEstate': agentie,
            'contacts': contacte,
        })

#contact - agentie
def contact_agentie(request, contact_id):

    #agentie autentificata
    agentie = RealEstate.objects.get(user=request.user)

    #contact
    contact = Contact.objects.get(id=contact_id)

    #contactare proprietar anunt
    if request.method == 'POST':
        #proprietar deja contactat
        if contact.proprietar_contactat == True:
            messages.error(request, 'Ai contactat proprietarul deja')
        #contactare proprietar
        else:
            #preluare mesaj
            contact.mesaj = request.POST['mesaj']
            #modificare camp 'proprietar_contactat' pentru ca proprietarul
            #sa vada contactul
            contact.proprietar_contactat = True
            contact.save()

            #notificare propritar prin emial 
            proprietar = User.objects.get(username=contact.username_proprietar)

            try:
                send_mail(
                    'Potențial cumpărător',
                    'Aveți un nou contact la anunțul: ' + contact.titlu_anunt + ' ',
                    'escanor.imobiliare@gmail.com',
                    [proprietar.email,  ], 
                    fail_silently=False
                )
            except TimeoutError:
                messages.info(request, 'E-mailul nu a putut fi trimis\nVă rugăm să ne contactați.')

            #mesaj succes
            messages.success(request, 'Proprietar contactat')

    #pregatire date pentru html - agentie, contact
    context = {
        'realEstate': agentie,
        'contact': contact,
    }

    #randare pagina html
    return render(request, 'utilizatori/contact_agentie.html', context)

#editare cont agentie
def editare_cont_agentie(request):

    #agentie autentificata
    agentie = RealEstate.objects.get(user=request.user)

    #confirmare salvare
    if request.method == 'POST':
        #preluare date modificate si salvarea lor

        #nume
        agentie.nume = request.POST['nume']

        #logo
        if 'imagine_logo' in request.FILES:
            agentie.logo = request.FILES['imagine_logo']

        #descriere
        agentie.descriere = request.POST['descriere']

        #adresa website
        if request.POST['website']:
            agentie.website = request.POST['website']

        #email - se verifica daca nu exista deja
        if User.objects.filter(email=request.POST['email']).exists():
            messages.error(request, 'Acest email exista deja')
        else:
            if request.POST['email']:
                agentie.email = request.POST['email']
                request.user.email = agentie.email
                request.user.save()

        #numar telefon
        agentie.telefon1 = request.POST['telefon1']
        
        #numar telefon 2
        if request.POST['telefon2']:
            agentie.telefon2 = request.POST['telefon2']
        agentie.adresa_sediu = request.POST['adresa_sediu']

        #an infiintare - se verifica daca e valid
        if int(request.POST['an_infiintare']) > date.today().year:
            messages.error(request, 'An necorspunzator')
        else:
            agentie.an_infiintare = request.POST['an_infiintare']
        agentie.save()

        return redirect(request.path_info)

    #pregatire date catre html - agentie
    context = {
        'realEstate': agentie,
    }

    #randarea paginii html
    return render(request, "utilizatori/editare_cont_agentie.html", context)

#profil agentie
def profil_agentie(request, real_estate_id):

    #agentie autentificata
    agentie = RealEstate.objects.get(id=real_estate_id)

    #pregatire date catre html - agentie
    context = {
        'realEstate': agentie,
    }

    #randare pagina html
    return render(request, "utilizatori/profil_agentie.html", context)

#lista agentii
def lista_agentii(request):

    #clientul (proprietarul) autentificat
    client = Client.objects.get(user=request.user)

    #toate agentiile imobiliare din baza de date
    agentii = RealEstate.objects.all()

    #pregatire date pentru html - date proprietar si agentii
    context = {
        'client': client,
        'realEstates': agentii,
    }

    #randare pagina html
    return render(request, "utilizatori/lista_agentii.html", context)

#adaugare apartament de proprietar
def adaugare_apartament(request):

    #confirmare - trimirere cerere de postare a apartamentului
    if request.method == 'POST':

        #campurile preluate din html
        tip_proprietate = request.POST['tip_proprietate']
        titlu = request.POST['titlu']
        judet = request.POST['judet']
        oras_sau_localitate = request.POST['oras_sau_localitate']
        adresa = request.POST['adresa']
        descriere = request.POST['descriere']
        suprafata_construita = request.POST['suprafata_construita']
        suprafata_utila = request.POST['suprafata_utila']
        numar_camere = request.POST['numar_camere']
        numar_bai = request.POST['numar_bai']
        numar_bucatarii = request.POST['numar_bucatarii']
        etaj = request.POST['etaj']
        numar_balcoane = request.POST['numar_balcoane']
        nivel_confort = request.POST['nivel_confort']
        compartimentare = request.POST['compartimentare']
        expunere = request.POST['expunere']
        regim_inaltime = request.POST['regim_inaltime']
        an_constructie = request.POST['an_constructie']
        utilitati_generale = request.POST['utilitati_generale']
        finisaje = request.POST['finisaje']
        pret = request.POST['pret']
        fotografie1 = request.FILES['fotografie1']

        #creare apartament
        apartament = Apartament(tip=tip_proprietate, titlu=titlu, judet=judet, oras_sau_localitate=oras_sau_localitate, adresa=adresa, 
        descriere=descriere, suprafata_construita=suprafata_construita, suprafata_utila=suprafata_utila, numar_camere=numar_camere,
        numar_bai=numar_bai, numar_bucatarii=numar_bucatarii, etaj=etaj, numar_balcoane=numar_balcoane, nivel_confort=nivel_confort,
        compartimentare=compartimentare, expunere=expunere, regim_inaltime=regim_inaltime, an_constructie=an_constructie,
        utilitati_generale=utilitati_generale, finisaje=finisaje, pret=pret, fotografie1=fotografie1)

        #verificare campurile de tip Boolean
        #loc de parcare
        if request.POST['loc_de_parcare'] == "Da":
            apartament.loc_de_parcare = True
        else:
            apartament.loc_de_parcare = False
        #posibilitate inchiriere
        if request.POST['posibilitate_inchiriere'] == "Da":
            apartament.posibilitate_inchiriere = True
        else:
            apartament.posibilitate_inchiriere = False

        #adugare datalii suplimentare - daca este completat
        if 'alte_detalii' in request.POST:
            apartament.alte_detalii = request.POST['alte_detalii']

        #adugare poze - daca sunt adaugate
        if 'fotografie2' in request.FILES:
            apartament.fotografie2 = request.FILES['fotografie2']
        if 'fotografie3' in request.FILES:
            apartament.fotografie3 = request.FILES['fotografie3']
        if 'fotografie4' in request.FILES:
            apartament.fotografie4 = request.FILES['fotografie4']
        if 'fotografie5' in request.FILES:
            apartament.fotografie5 = request.FILES['fotografie5']
        if 'fotografie6' in request.FILES:
            apartament.fotografie6 = request.FILES['fotografie6']

        #salvare proprietar
        apartament.proprietar = request.user

        #agentie responsabila
        apartament.agentie_responsabila = RealEstate.objects.get(nume=request.POST['agentie'])

        apartament.save()

        #trimitere email de notificare catre agentie - cerere de postare
        try:
            send_mail(
                'Anuț nou pe Escanor Imobiliare',
                'Utilizatorul ' + request.user.username + ' dorește să posteze un nou anunț pe Escanor Imobiliare. Conectează-te pentru mai multe detalii.',
                'escanor.imobiliare@gmail.com',
                [apartament.agentie_responsabila.email, ], 
                fail_silently=False
            )
        except TimeoutError:
            messages.info(request, 'E-mailul nu a putut fi trimis\nVă rugăm să ne contactați.')

        #mesaj succes
        messages.success(request, 'Cerere de postare a apartamentul a fost trimisa')

        #proprietarul autentificat
        client = Client.objects.get(user=request.user)

        #pregatire date proprietar catre html
        context = {
            'client': client,
        }

        #randare pagina html
        return render(request, "utilizatori/cont_proprietar.html", context)

    #agentiile imobiliare din baza de date
    agentii = RealEstate.objects.all()

    #formarea unei lista cu numele agentiilor 
    numeAgentii = []
    for i in range(len(agentii)):
        numeAgentii.insert(i, agentii[i].nume)

    #pregatirea datelor pentru html - nume agentii imobiliare, tip apartament,
    #judetem, nivel confort, compartimentare, expunere
    context = {
        'namesRealEstates': numeAgentii,
        'tip': APARTAMENT_T,
        'judete': JUDETE,
        'confort': NIVEL_CONFORT_T,
        'compartimente': COMPARTIMENTE_T,
        'expunere': EXPUNERE_T,
    }

    #randare pagina html
    return render(request, "anunturi/adaugare_apartament.html", context)

#adaugare casa de proprietar
def adaugare_casa(request):

    #confirmare - trimirere cerere de postare a casei
    if request.method == 'POST':
        
        #campuri preluate din html
        titlu = request.POST['titlu']
        judet = request.POST['judet']
        oras_sau_localitate = request.POST['oras_sau_localitate']
        adresa = request.POST['adresa']
        descriere = request.POST['descriere']
        suprafata_construita = request.POST['suprafata_construita']
        suprafata_utila = request.POST['suprafata_utila']
        numar_dormitoare = request.POST['numar_dormitoare']
        numar_livinguri = request.POST['numar_livinguri']
        numar_bai = request.POST['numar_bai']
        numar_bucatarii = request.POST['numar_bucatarii']
        numar_balcoane = request.POST['numar_balcoane']
        numar_terase = request.POST['numar_terase']
        numar_garaje = request.POST['numar_garaje']
        suprafata_teren = request.POST['suprafata_teren']
        structura_rezistenta = request.POST['structura_rezistenta']
        tip_acoperis = request.POST['tip_acoperis']
        regim_inaltime = request.POST['regim_inaltime']
        an_constructie = request.POST['an_constructie']
        utilitati_generale = request.POST['utilitati_generale']
        finisaje = request.POST['finisaje']
        pret = request.POST['pret']
        fotografie1 = request.FILES['fotografie1']

        #creare casa
        casa = House(titlu=titlu, judet=judet, oras_sau_localitate=oras_sau_localitate, adresa=adresa, descriere=descriere, suprafata_construita=suprafata_construita,
        suprafata_utila=suprafata_utila, numar_dormitoare=numar_dormitoare, numar_livinguri=numar_livinguri, numar_bai=numar_bai, numar_bucatarii=numar_bucatarii,
        numar_balcoane=numar_balcoane, numar_terase=numar_terase, numar_garaje=numar_garaje, suprafata_teren=suprafata_teren, structura_rezistenta=structura_rezistenta,
        tip_acoperis=tip_acoperis, regim_inaltime=regim_inaltime, an_constructie=an_constructie, utilitati_generale=utilitati_generale, 
        finisaje=finisaje, pret=pret, fotografie1=fotografie1)

        #verificare camp de tip Boolean
        #posibilitate inchiriere
        if request.POST['posibilitate_inchiriere'] == "Da":
            casa.posibilitate_inchiriere = True
        else:
            casa.posibilitate_inchiriere = False

        #alte detalii - dace e completat
        if 'alte_detalii' in request.POST:
            casa.alte_detalii = request.POST['alte_detalii']

        #poze - daca sunt adaugate
        if 'fotografie2' in request.FILES:
            casa.fotografie2 = request.FILES['fotografie2']
        if 'fotografie3' in request.FILES:
            casa.fotografie3 = request.FILES['fotografie3']
        if 'fotografie4' in request.FILES:
            casa.fotografie4 = request.FILES['fotografie4']
        if 'fotografie5' in request.FILES:
            casa.fotografie5 = request.FILES['fotografie5']
        if 'fotografie6' in request.FILES:
            casa.fotografie6 = request.FILES['fotografie6']

        #salvare proprietar
        casa.proprietar = request.user

        #agentie responsabila
        casa.agentie_responsabila = RealEstate.objects.get(nume=request.POST['agentie'])

        casa.save()

        #trimitere email catre agentie - cerere nou
        try:
            send_mail(
                'Anuț nou pe Escanor Imobiliare',
                'Utilizatorul ' + request.user.username + ' dorește să posteze un nou anunț pe Escanor Imobiliare. Conectează-te pentru mai multe detalii.',
                'escanor.imobiliare@gmail.com',
                [casa.agentie_responsabila.email, ], 
                fail_silently=False
            )
        except TimeoutError:
            messages.info(request, 'E-mailul nu a putut fi trimis\nVă rugăm să ne contactați.')

        #mesaj succes
        messages.success(request, 'Cerere de postare a casei a fost trimisa')

        #proprietar autentificat
        client = Client.objects.get(user=request.user)

        #pregatire date proprietar pentru html
        context = {
            'client': client,
        }

        #randare pagina html
        return render(request, "utilizatori/cont_proprietar.html", context)

    #agentiile imobiliare din baza de date
    agentii = RealEstate.objects.all()

    #formarea unei lista cu numele agentiilor 
    numeAgentii = []
    for i in range(len(agentii)):
        numeAgentii.insert(i, agentii[i].nume)

    #pregatirea datelor pentru html - nume agentii, judete
    context = {
        'namesRealEstates': numeAgentii,
        'judete': JUDETE,
    }

    #randare pagina html
    return render(request, "anunturi/adaugare_casa.html", context)

#adaugare teren de proprietar
def adagare_teren(request):

    #confirmare - trimirere cerere de postare a terenului
    if request.method == 'POST':

        #campuri preluate din html
        tip_teren = request.POST['tip_teren']
        titlu = request.POST['titlu']
        judet = request.POST['judet']
        oras_sau_localitate = request.POST['oras_sau_localitate']
        adresa = request.POST['adresa']
        descriere = request.POST['descriere']
        suprafata_teren = request.POST['suprafata_teren']
        facilitati = request.POST['facilitati']
        pret = request.POST['pret']
        fotografie1 = request.FILES['fotografie1']

        teren = Land(tip_teren=tip_teren, titlu=titlu, judet=judet, oras_sau_localitate=oras_sau_localitate, adresa=adresa, descriere=descriere, 
        suprafata_teren=suprafata_teren, facilitati=facilitati, pret=pret, fotografie1=fotografie1)

        if 'alte_detalii' in request.POST:
            teren.alte_detalii = request.POST['alte_detalii']
        if 'fotografie2' in request.FILES:
            teren.fotografie2 = request.FILES['fotografie2']
        if 'fotografie3' in request.FILES:
            teren.fotografie3 = request.FILES['fotografie3']
        if 'fotografie4' in request.FILES:
            teren.fotografie4 = request.FILES['fotografie4']
        if 'fotografie5' in request.FILES:
            teren.fotografie5 = request.FILES['fotografie5']
        if 'fotografie6' in request.FILES:
            teren.fotografie6 = request.FILES['fotografie6']

        teren.proprietar = request.user

        teren.agentie_responsabila = RealEstate.objects.get(nume=request.POST['agentie'])

        teren.save()

        try:
            send_mail(
                'Anuț nou pe Escanor Imobiliare',
                'Utilizatorul ' + request.user.username + ' dorește să posteze un nou anunț pe Escanor Imobiliare. Conectează-te pentru mai multe detalii.',
                'escanor.imobiliare@gmail.com',
                [teren.agentie_responsabila.email, ], 
                fail_silently=False
            )
        except TimeoutError:
            messages.info(request, 'E-mailul nu a putut fi trimis\nVă rugăm să ne contactați.')

        messages.success(request, 'Cerere de postare a terenului a fost trimisa')

        client = Client.objects.get(user=request.user)

        context = {
            'client': client,
        }

        return render(request, "utilizatori/cont_proprietar.html", context)

    agentii = RealEstate.objects.all()
    numeAgentii = []
    for i in range(len(agentii)):
        numeAgentii.insert(i, agentii[i].nume)
    context = {
        'namesRealEstates': numeAgentii,
        'judete': JUDETE,
        'tip_teren': TEREN_T,
    }
    return render(request, "anunturi/adaugare_teren.html", context)

#lista anunturi proprietar
def anunturi_proprietar(request):

    #proprietar autentificat
    client = Client.objects.get(user=request.user)
    
    #anunturile proprietarului
    apartamente = Apartament.objects.filter(proprietar=request.user)
    case = House.objects.filter(proprietar=request.user) 
    terenuri = Land.objects.filter(proprietar=request.user)  

    #pregatire date pentru html - proprietar, anunturi
    context = {
        'client': client,
        'apartaments': apartamente,
        'houses': case,
        'lands': terenuri,
    }

    #randare pagina html
    return render(request, "utilizatori/lista_anunturi_proprietar.html", context)

#stergere apartament
def stergere_apartament(request, apartament_id):

    #apartamentul ce va fi sters
    apartament = Apartament.objects.get(id=apartament_id)
    apartament_titlu = apartament.titlu
    apartament.delete()
    #contacele apartamentului - trebuie sterse si ele
    contacte = Contact.objects.all().filter(tip_anunt='Apartament', ID_anunt=apartament_id)
    contacte.delete()

    #notificare propiretar - s-a sters apartamentul
    try:
        send_mail(
            'Anunț șters de pe Escanor Imobiliare',
            'Anunțul postat de dumneavoastră cu titlul: ' + apartament_titlu + ' a fost respins/șters de pe Escanor Imobiliare.',
            'escanor.imobiliare@gmail.com',
            [apartament.proprietar.email,  ], 
            fail_silently=False
        )
    except TimeoutError:
        messages.info(request, 'E-mailul nu a putut fi trimis\nVă rugăm să ne contactați.')

    #mesaj succes
    messages.success(request, 'Anunț șters')

    #stergere de catre client
    try:
        userClient = request.user.client
        #redirectionare catre pagina de anunturi ale proprietarului
        return redirect('owner_listings')
     #stergere de catre agentie
    except Exception:
         #redirectionare catre pagina de cereri
        return redirect('listing_request')

#stergere casa
def stergere_casa(request, casa_id):

    casa = House.objects.get(id=casa_id)
    casa_titlu = casa.titlu
    casa.delete()

    contacte = Contact.objects.all().filter(tip_anunt='Casa', ID_anunt=casa_id)
    contacte.delete()

    try:
        send_mail(
            'Anunț șters de pe Escanor Imobiliare',
            'Anunțul postat de dumneavoastră cu titlul: ' + casa_titlu + ' a fost respins/șters de pe Escanor Imobiliare.',
            'escanor.imobiliare@gmail.com',
            [casa.proprietar.email,  ], 
            fail_silently=False
        )
    except TimeoutError:
        messages.info(request, 'E-mailul nu a putut fi trimis\nVă rugăm să ne contactați.')

    messages.success(request, 'Anunț șters')

    try:
        userClient = request.user.client
        return redirect('owner_listings')
    except Exception:
        return redirect('listing_request')        
    
#stergere teren
def stergere_teren(request, teren_id):

    teren = Land.objects.get(id=teren_id)
    teren_titlu = teren.titlu
    teren.delete()

    contacts = Contact.objects.all().filter(tip_anunt='Teren', ID_anunt=teren_id)
    contacts.delete()

    try:
        send_mail(
            'Anunț șters de pe Escanor Imobiliare',
            'Anunțul postat de dumneavoastră cu titlul: ' + teren_titlu + ' a fost respins/șters de pe Escanor Imobiliare.',
            'escanor.imobiliare@gmail.com',
            [teren.proprietar.email,  ], 
            fail_silently=False
        )
    except TimeoutError:
        messages.info(request, 'E-mailul nu a putut fi trimis\nVă rugăm să ne contactați.')

    messages.success(request, 'Anunț șters')

    try:
        userClient = request.user.client
        return redirect('owner_listings')
    except Exception:
        return redirect('listing_request')

#cereri anunturi - agentie
def cereri_anunturi(request):

    #agentia autentificata
    agentie = RealEstate.objects.get(user=request.user)

    #anunturile agentiei nepublicate
    apartamente = Apartament.objects.filter(agentie_responsabila=agentie, publicat=False)
    case = House.objects.filter(agentie_responsabila=agentie, publicat=False)
    terenuri = Land.objects.filter(agentie_responsabila=agentie, publicat=False)

    #pregatire date catre html - agentie, anunturi
    context = {
        'realEstate': agentie,
        'apartaments': apartamente,
        'houses': case,
        'lands': terenuri,
    }

    #randare pagina html
    return render(request, "utilizatori/cereri.html", context)

#detalii proprietar - pentru agentie
def owner_contacts(request, username):

    #agentia autentificata
    realEstate = RealEstate.objects.get(user=request.user)

    #proprietarul
    owner = Client.objects.get(user=User.objects.get(username=username))

    #pregatire date pentru html
    context = {
        'realEstate': realEstate,
        'owner': owner,
    }

    #randare pagina html
    return render(request, "utilizatori/detalii_proprietar.html", context)

#posteaza apartament - pentru agentie
def posteaza_apartament(request, apartament_id):

    #apartament
    apartament = Apartament.objects.get(id=apartament_id)
    #publicare apartament
    apartament.publicat = True
    apartament.save()

    #notificare proprietar
    try:
        send_mail(
            'Anunț postat de pe Escanor Imobiliare',
            'Anunțul dumneavoastră: ' + apartament.titlu + ' a fost postat pe Escanor Imobiliare.\nAgenție responsabilă: ' + apartament.agentie_responsabila.nume + ".",
            'escanor.imobiliare@gmail.com',
            [apartament.proprietar.email,  ], 
            fail_silently=False
        )
    except TimeoutError:
        messages.info(request, 'E-mailul nu a putut fi trimis\nVă rugăm să ne contactați.')
    
    #mesaj succes
    messages.success(request, 'Anunț postat')

    #redirectionare lista cereri
    return redirect('listing_request')

#posteaza casa - pentru agentie
def posteaza_casa(request, casa_id):

    casa = House.objects.get(id=casa_id)
    casa.publicat = True
    casa.save()

    try:
        send_mail(
            'Anunț postat de pe Escanor Imobiliare',
            'Anunțul dumneavoastră: ' + casa.titlu + ' a fost postat pe Escanor Imobiliare.\nAgenție responsabilă: ' + casa.agentie_responsabila.nume + ".",
            'escanor.imobiliare@gmail.com',
            [casa.proprietar.email,  ], 
            fail_silently=False
        )
    except TimeoutError:
        messages.info(request, 'E-mailul nu a putut fi trimis\nVă rugăm să ne contactați.')

    messages.success(request, 'Anunț postat')

    return redirect('listing_request')

#posteaza teren - pentru agentie
def posteaza_teren(request, teren_id):

    teren = Land.objects.get(id=teren_id)
    teren.publicat = True
    teren.save()

    try:
        send_mail(
            'Anunț postat de pe Escanor Imobiliare',
            'Anunțul dumneavoastră: ' + teren.titlu + ' a fost postat pe Escanor Imobiliare.\nAgenție responsabilă: ' + teren.agentie_responsabila.nume + ".",
            'escanor.imobiliare@gmail.com',
            [teren.proprietar.email,  ], 
            fail_silently=False
        )
    except TimeoutError:
        messages.info(request, 'E-mailul nu a putut fi trimis\nVă rugăm să ne contactați.')

    messages.success(request, 'Anunț postat')

    return redirect('listing_request')

#anunturi postate - pentru agentie
def anunturi_agentie(request):

    #agentie autentificata
    agentie = RealEstate.objects.get(user=request.user)

    #anunturi publice
    apartamente = Apartament.objects.filter(agentie_responsabila=agentie, publicat=True)
    case = House.objects.filter(agentie_responsabila=agentie, publicat=True)
    terenuri = Land.objects.filter(agentie_responsabila=agentie, publicat=True)

    #pregatire date pentru html
    context = {
        'realEstate': agentie,
        'apartaments': apartamente,
        'houses': case,
        'lands': terenuri,
    }

    #randare pagina html
    return render(request, "utilizatori/lista_anunturi_agentie.html", context)

#editare apartament - pentru agentie
def edit_apartament(request, apartament_id):

    #apartament
    apartament = Apartament.objects.get(id=apartament_id)

    #salvare
    if request.method == 'POST':

        #preluare campuri ce pot fi schimbate
        apartament.titlu = request.POST['titlu']
        apartament.descriere = request.POST['descriere']
        apartament.utilitati_generale = request.POST['utilitati_generale']
        apartament.finisaje = request.POST['finisaje']

        if request.POST['posibilitate_inchiriere'] == 'Da':
            apartament.posibilitate_inchiriere = True
        else:
            apartament.posibilitate_inchiriere = False

        apartament.pret = request.POST['pret']

        if 'alte_detalii' in request.POST:
            apartament.alte_detalii = request.POST['alte_detalii']

        if 'fotografie1' in request.FILES:
            apartament.fotografie1 = request.FILES['fotografie1']
        if 'fotografie2' in request.FILES:
            apartament.fotografie2 = request.FILES['fotografie2']
        if 'fotografie3' in request.FILES:
            apartament.fotografie3 = request.FILES['fotografie3']
        if 'fotografie4' in request.FILES:
            apartament.fotografie4 = request.FILES['fotografie4']
        if 'fotografie5' in request.FILES:
            apartament.fotografie5 = request.FILES['fotografie5']
        if 'fotografie6' in request.FILES:
            apartament.fotografie6 = request.FILES['fotografie6']

        # anuntul nu va mai fi publicat
        if request.POST['publicat'] == 'Da':
            apartament.publicat = False
        else:
            apartament.publicat = True

        apartament.save()
      
        #mesaj succes
        messages.success(request, 'Anunț editat')

        return redirect('listings_real_estate')

    #pregatire date pentru html
    context = {
        'apartament': apartament,
        'realEstate': apartament.agentie_responsabila,
    }

    #randare pagina html
    return render(request, "anunturi/editare_anunt.html", context)

#editare casa - pentru agentie
def edit_casa(request, casa_id):

    casa = House.objects.get(id=casa_id)

    if request.method == 'POST':
        casa.titlu = request.POST['titlu']
        casa.descriere = request.POST['descriere']
        casa.utilitati_generale = request.POST['utilitati_generale']
        casa.finisaje = request.POST['finisaje']

        if request.POST['posibilitate_inchiriere'] == 'Da':
            casa.posibilitate_inchiriere = True
        else:
            casa.posibilitate_inchiriere = False

        casa.pret = request.POST['pret']

        if 'alte_detalii' in request.POST:
            casa.alte_detalii = request.POST['alte_detalii']

        if 'fotografie1' in request.FILES:
            casa.fotografie1 = request.FILES['fotografie1']
        if 'fotografie2' in request.FILES:
            casa.fotografie2 = request.FILES['fotografie2']
        if 'fotografie3' in request.FILES:
            casa.fotografie3 = request.FILES['fotografie3']
        if 'fotografie4' in request.FILES:
            casa.fotografie4 = request.FILES['fotografie4']
        if 'fotografie5' in request.FILES:
            casa.fotografie5 = request.FILES['fotografie5']
        if 'fotografie6' in request.FILES:
            casa.fotografie6 = request.FILES['fotografie6']

        # anuntul nu va mai fi publicat
        if request.POST['publicat'] == 'Da':
            casa.publicat = False
        else:
            casa.publicat = True

        casa.save()
      
        messages.success(request, 'Anunț editat')

        return redirect('listings_real_estate')

    context = {
        'house': casa,
        'realEstate': casa.agentie_responsabila,
    }

    return render(request, "anunturi/editare_anunt.html", context)

#editare teren - pentru agentie
def edit_teren(request, teren_id):

    teren = Land.objects.get(id=teren_id)

    if request.method == 'POST':
        teren.titlu = request.POST['titlu']
        teren.descriere = request.POST['descriere']
        teren.facilitati = request.POST['facilitati']

        teren.pret = request.POST['pret']

        if 'alte_detalii' in request.POST:
            teren.alte_detalii = request.POST['alte_detalii']

        if 'fotografie1' in request.FILES:
            teren.fotografie1 = request.FILES['fotografie1']
        if 'fotografie2' in request.FILES:
            teren.fotografie2 = request.FILES['fotografie2'] 
        if 'fotografie3' in request.FILES:
            teren.fotografie3 = request.FILES['fotografie3']
        if 'fotografie4' in request.FILES:
            teren.fotografie4 = request.FILES['fotografie4']
        if 'fotografie5' in request.FILES:
            teren.fotografie5 = request.FILES['fotografie5']
        if 'fotografie6' in request.FILES:
            teren.fotografie6 = request.FILES['fotografie6']

        # anuntul nu va mai fi publicat
        if request.POST['publicat'] == 'Da':
            teren.publicat = False
        else:
            teren.publicat = True

        teren.save()
      
        messages.success(request, 'Anunț editat')

        return redirect('listings_real_estate')

    context = {
        'land': teren,
        'realEstate': teren.agentie_responsabila,
    }

    return render(request, "anunturi/editare_anunt.html", context)

#raport - pentru agentie
def vizualizeaza_raport(request):

    #raportul vizibil
    raport = Raport.objects.get(raport_vizibil=True)

    #randare pagina html si trimitere date catre aceasta
    return render(request, "utilizatori/raport.html", {
        'realEstate': RealEstate.objects.get(user=request.user),
        'raport': raport,
    })

#schimare parola
def schimbare_parola(request):

    #confirmare shimbare parola
    if request.method == 'POST':

        #form-ul predefinit pentru schimbarea parolei
        form = PasswordChangeForm(request.user, request.POST)
        #verificam form-ul
        #parola veche a fost introdusa corect
        #parola noua este valida
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) 
            messages.success(request, 'Parola a fost schimbată!')
            return redirect('change_password')
        else:
            #mesaj de eroare
            messages.error(request, 'Verifică dacă ai introdus parola corectă și dacă ai respectat cele 4 reguli')
    else:
        #form predefinit
        form = PasswordChangeForm(request.user)

    #randare pagina html si trmiterea form-ului
    return render(request, 'parola/change_password.html', {
        'form': form
    })

#lista favorite - pentru client
def favorite(request):

    #clientul autentificat
    client = Client.objects.get(user=request.user)
    
    #anunturile favorite
    anunturi_favorite = FavoriteListing.objects.get(client=client)
    apartamente_favorite = anunturi_favorite.apartamente_favorite.all()
    case_favorite = anunturi_favorite.case_favorite.all()
    terenuri_favorite = anunturi_favorite.terenuri_favorite.all()

    #pregatire date pentru html
    context = { 
        'client': client, 
        'apartamente_favorite': apartamente_favorite,
        'case_favorite': case_favorite,
        'terenuri_favorite': terenuri_favorite,
        }

    #randare pagina html
    return render(request, "utilizatori/anunturi_favorite.html", context)

#stergere apartament din lista de favorite
def stergere_apartament_favorit(request, apartament_id):

    #lista anunturi favorite pentru clientul autentificat
    anunturi_favorite = FavoriteListing.objects.get(client=Client.objects.get(user=request.user))
    #stergere apartament
    anunturi_favorite.apartamente_favorite.remove(Apartament.objects.get(id=apartament_id))

    #redirectionare la lista de favorite
    return redirect('favorites')

#stergere casa din lista de favorite
def stergere_casa_favorita(request, casa_id):

    anunturi_favorite = FavoriteListing.objects.get(client=Client.objects.get(user=request.user))
    anunturi_favorite.case_favorite.remove(House.objects.get(id=casa_id))

    return redirect('favorites')

#stergere teren din lista de favorite
def stergere_teren_favorit(request, teren_id):

    anunturi_favorite = FavoriteListing.objects.get(client=Client.objects.get(user=request.user))
    anunturi_favorite.terenuri_favorite.remove(Land.objects.get(id=teren_id))
    
    return redirect('favorites')