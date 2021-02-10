from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist

from .models import Contact, Raport
from anunturi.models import *
import datetime

### metode views ###

#contact anunt
def contact(request):

    #trimitere contact si actualizare raport
    if request.method == 'POST':

        ### CREARE CONTACT ###

        #preluare date din html
        tip_anunt = request.POST['tip_anunt']
        id_anunt = request.POST['id_anunt']
        titlu_anunt = request.POST['titlu_anunt']
        id_agentie = request.POST['id_agentie']
        id_proprietar = request.POST['id_proprietar']

        id_client = request.POST['id_client']
        nume = request.POST['nume']
        prenume = request.POST['prenume']
        email = request.POST['email']
        telefon = request.POST['telefon']
    
        #verifcare - contactare spam
        if Contact.objects.all().filter(tip_anunt=tip_anunt, ID_anunt=id_anunt, ID_client=id_client):
            messages.error(request, 'Deja ai contactat agenția în legătură cu acest anunț')
            return redirect('listings')

        #creare contact
        contact = Contact(tip_anunt=tip_anunt, ID_anunt=id_anunt, titlu_anunt=titlu_anunt, ID_agentie=id_agentie, username_proprietar=id_proprietar, ID_client=id_client, nume=nume, prenume=prenume, email=email, telefon=telefon)

        #atasare mesaj - daca exista
        if 'mesaj' in request.POST:
            contact.mesaj = request.POST['mesaj']

        contact.save()

        ### ACTUALIZARE RAPORT ###

        #luna si anul cand s-a creat contactul
        lunaPrez = int(datetime.date.today().month)
        anPrez = int(datetime.date.today().year)

        #creare raport
        try:
            #raportul deja exista 
            raport = Raport.objects.get(luna_raport=lunaPrez, an_raport=anPrez)
        except ObjectDoesNotExist:
            #raportul nu exista => raport nou
            raport = Raport(luna_raport=lunaPrez, an_raport=anPrez, contacte_apartamente=0, contacte_case=0, contacte_terenuri=0)        

        #actualizare raport
        if tip_anunt == 'Apartament':
            raport.contacte_apartamente += 1
        else:
            if tip_anunt == 'Casa':
                raport.contacte_case += 1
            else:
                 raport.contacte_terenuri += 1

        raport.save()

        ### TRIMITERE EMAIL ###

        #mesaj pentru agentie - aparatia unui nou contact
        msg = nume + ' ' + prenume + ' vă conteactează în legătură cu anunțul: '
        if tip_anunt in ['Garsoniera', 'Apartament']:
            anunt = Apartament.objects.get(id=id_anunt)
            msg += anunt.titlu + " (" + anunt.tip + ", " + str(anunt.id)
        else:
            if tip_anunt == 'Casa':
                anunt = House.objects.get(id=id_anunt)
                msg += anunt.titlu + " (Casă, " + str(anunt.id)
            else:
                anunt = Land.objects.get(id=id_anunt)
                msg += anunt.titlu + " (Teren - " + anunt.tip_teren + ", " + str(anunt.id)

        msg += ') de pe Escanor Imobiliare.'

        #trimitere email - subiect, mesaj, expeditor, destinatari
        try:
            send_mail(
                'Contact nou pe Escanor Imobiliare',
                msg,
                'escanor.imobiliare@gmail.com',
                [anunt.agentie_responsabila.email,  ], 
                fail_silently=False
            )
        except TimeoutError:
            messages.info(request, 'E-mailul nu a putut fi trimis\nVă rugăm să ne contactați.')
        
        #mesaj pentru client - agentia a fost contactata
        messages.success(request, 'Mesaj trimis. Vei fi contactat de agenție în cel mai scurt timp posibil.')

        #redirectinare la pagina cu anunturile recente
        return redirect('listings')

#contact admin - suport
def contact_escanor(request):

    #se trimite mesajul adminului
    if request.method == 'POST':
        #preluarea datelor de contact + mesaj
        nume = request.POST['nume']
        prenume = request.POST['prenume']
        email = request.POST['email']
        telefon = request.POST['telefon']
        subiect = request.POST['subiect']
        mesaj = request.POST['mesaj']

        #compunere mesaj
        contact = '\n\nDate de contact\nNume: ' + nume + '\nPrenume: ' + prenume + '\nEmail: ' + email + '\nTelefon: ' + telefon
        msg = mesaj + contact
        #trimitere email catre escanor.imobiliare@gmail.com
        try:
            send_mail(
                'Suport clienți Escanor Imobiliare: ' + subiect,
                msg,
                'escanor.imobiliare@gmail.com',
                ['escanor.imobiliare@gmail.com',  ], 
                fail_silently=False
            )
        except TimeoutError:
            messages.info(request, 'E-mailul nu a putut fi trimis\nVă rugăm să ne contactați.')

        #mesaj de succes - contact trimis
        messages.success(request, 'Mesaj trimis. Veți fi contact în cel mai scurt timp posbil')

        #redirectionare catre pagina principala (home)
        return redirect('index')

    #randarea paginii html
    return render(request, "utilizatori/contact_escanor.html")