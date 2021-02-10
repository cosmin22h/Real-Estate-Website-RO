from django.db import models

from datetime import datetime

### modele contacte ###

#modelul contact
class Contact(models.Model):
    #tipul de anunt
    ANUNTURI = [
        ('Apartament', 'Apartament'),
        ('Casa', 'Casa'),
        ('Teren', 'Teren'),
    ] 
    #campuri ce fac legatura cu anuntul si agentia responsabila
    tip_anunt = models.CharField(max_length=50, choices=ANUNTURI, null=True)
    ID_anunt = models.PositiveIntegerField(null=True)
    titlu_anunt = models.CharField(max_length=200, null=True)
    ID_agentie = models.PositiveIntegerField(null=True)
    username_proprietar = models.CharField(max_length=200, null=True)
    
    #campurile clientului ce a trimis contactul
    ID_client = models.PositiveIntegerField(null=True)
    nume = models.CharField(max_length=200, null=True)
    prenume = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True)
    telefon = models.CharField(max_length=10, null=True)
    #campuri ale contactului
    mesaj = models.TextField(blank=True)
    data_contactare = models.DateTimeField(default=datetime.now, blank=True)
    proprietar_contactat = models.BooleanField(default=False)
    vazut = models.BooleanField(default=False)

    #metoda de identificare a contactului
    def __str__(self):
        return self.nume

#modelul raport
class Raport(models.Model):
    
    #campurile raportului
    luna_raport = models.PositiveIntegerField(null=True)
    an_raport = models.PositiveIntegerField(null=True)
    contacte_apartamente = models.PositiveIntegerField(null=True)
    contacte_case = models.PositiveIntegerField(null=True)
    contacte_terenuri = models.PositiveIntegerField(null=True)
    raport_vizibil = models.BooleanField(default=False)
    
    #metoda de identificare a raportului
    def __str__(self):
        return str(self.luna_raport) + '/' + str(self.an_raport)
    