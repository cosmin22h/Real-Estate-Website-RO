from django.db import models
from django.contrib.auth.models import User

from utilizatori.models import RealEstate, Client
from datetime import datetime
from alte_date import judete, imobile, terenuri

### modele anunturi ###

### modelul apartament
class Apartament(models.Model):
    #campuri ce leaga apartamentul de o agentie si un propiretar
    proprietar = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    agentie_responsabila = models.ForeignKey(RealEstate, on_delete=models.CASCADE, null=True)
    #campuri ce definesc un apartament
    tip = models.CharField(max_length=10, choices=imobile.APARTAMENT_T, null=True)
    titlu = models.CharField(max_length=300, null=True)
    judet = models.CharField(max_length=50, choices=judete.JUDETE, null=True)
    oras_sau_localitate = models.CharField(max_length=100, null=True)
    adresa = models.CharField(max_length=200, null=True)
    descriere = models.TextField(null=True)
    suprafata_construita = models.FloatField(null=True)
    suprafata_utila = models.FloatField(null=True)
    numar_camere = models.PositiveIntegerField(null=True)
    numar_bai = models.PositiveIntegerField(null=True)
    numar_bucatarii = models.PositiveIntegerField(null=True)
    etaj = models.PositiveIntegerField(null=True)
    numar_balcoane = models.PositiveIntegerField(null=True)
    nivel_confort = models.CharField(max_length=1, choices=imobile.NIVEL_CONFORT_T, null=True)
    compartimentare = models.CharField(max_length=20, choices=imobile.COMPARTIMENTE_T ,null=True)
    expunere = models.CharField(max_length=10, choices=imobile.EXPUNERE_T, null=True)
    loc_de_parcare = models.BooleanField(default=False)
    regim_inaltime = models.CharField(max_length=50, null=True)
    an_constructie = models.PositiveIntegerField(null=True)
    utilitati_generale = models.TextField(null=True)
    finisaje = models.TextField(null=True)
    posibilitate_inchiriere = models.BooleanField(default=False)
    pret = models.PositiveIntegerField(null=True)
    alte_detalii = models.TextField(blank=True, null=True)
    fotografie1 = models.ImageField(upload_to='photos/%Y/%M/%D/', null=True)
    fotografie2 = models.ImageField(upload_to='photos/%Y/%M/%D/', blank=True, null=True)
    fotografie3 = models.ImageField(upload_to='photos/%Y/%M/%D/', blank=True, null=True)
    fotografie4 = models.ImageField(upload_to='photos/%Y/%M/%D/', blank=True, null=True)
    fotografie5 = models.ImageField(upload_to='photos/%Y/%M/%D/', blank=True, null=True)
    fotografie6 = models.ImageField(upload_to='photos/%Y/%M/%D/', blank=True, null=True)
    publicat = models.BooleanField(default=False)
    data_publicare = models.DateField(default = datetime.now, blank=True, null=True)

    #metoda de identificare a apartamentului
    def __str__(self):
        return self.titlu

#modelul casa
class House(models.Model):
    #campuri ce leaga casa de o agentie si un propiretar
    proprietar = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    agentie_responsabila = models.ForeignKey(RealEstate, on_delete=models.CASCADE, null=True)
    #campuri ce definesc o casa
    titlu = models.CharField(max_length=300, null=True)
    tip = models.CharField(max_length=10, editable=False, default='casa', null=True)
    judet = models.CharField(max_length=50, choices=judete.JUDETE, null=True)
    oras_sau_localitate = models.CharField(max_length=100, null=True)
    adresa = models.CharField(max_length=200, null=True)
    descriere = models.TextField(null=True)
    suprafata_construita = models.FloatField(null=True)
    suprafata_utila = models.FloatField(null=True)
    numar_dormitoare = models.PositiveIntegerField(null=True)
    numar_livinguri = models.PositiveIntegerField(null=True)
    numar_bai = models.PositiveIntegerField(null=True)
    numar_bucatarii = models.PositiveIntegerField(null=True)
    numar_balcoane = models.PositiveIntegerField(null=True)
    numar_terase = models.PositiveIntegerField(null=True)
    numar_garaje = models.PositiveIntegerField(null=True)
    suprafata_teren = models.FloatField(null=True)
    structura_rezistenta = models.CharField(max_length=100, null=True)
    tip_acoperis = models.CharField(max_length=100, null=True)
    regim_inaltime = models.CharField(max_length=50, null=True)
    an_constructie = models.PositiveIntegerField(null=True)
    utilitati_generale = models.TextField(null=True)
    finisaje = models.TextField(null=True)
    posibilitate_inchiriere = models.BooleanField(default=False)
    pret = models.PositiveIntegerField(null=True)
    alte_detalii = models.TextField(blank=True, null=True)
    fotografie1 = models.ImageField(upload_to = 'photos/%Y/%M/%D/', null=True)
    fotografie2 = models.ImageField(upload_to = 'photos/%Y/%M/%D/', blank = True, null=True)
    fotografie3 = models.ImageField(upload_to = 'photos/%Y/%M/%D/', blank = True, null=True)
    fotografie4 = models.ImageField(upload_to = 'photos/%Y/%M/%D/', blank = True, null=True)
    fotografie5 = models.ImageField(upload_to = 'photos/%Y/%M/%D/', blank = True, null=True)
    fotografie6 = models.ImageField(upload_to = 'photos/%Y/%M/%D/', blank = True, null=True)
    publicat = models.BooleanField(default=False)
    data_publicare = models.DateField(default = datetime.now, blank = True)

    #metoda de identificare a casei
    def __str__(self):
        return self.titlu

#modelul teren
class Land(models.Model):
    #campuri ce leaga ternul de o agentie si un propiretar
    proprietar = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    agentie_responsabila = models.ForeignKey(RealEstate, on_delete=models.CASCADE, null=True)
    #campuri ce definesc un teren
    tip_teren = models.CharField(max_length=40, choices=terenuri.TEREN_T, null=True)
    titlu = models.CharField(max_length=300, null=True)
    judet = models.CharField(max_length=50, choices=judete.JUDETE, null=True)
    oras_sau_localitate = models.CharField(max_length=100, null=True)
    adresa = models.CharField(max_length=200, null=True)
    descriere = models.TextField(null=True)
    suprafata_teren = models.FloatField(null=True)
    facilitati = models.TextField(null=True)
    pret = models.PositiveIntegerField(null=True)
    alte_detalii = models.TextField(blank=True, null=True)
    fotografie1 = models.ImageField(upload_to = 'photos/%Y/%M/%D/', null=True)
    fotografie2 = models.ImageField(upload_to = 'photos/%Y/%M/%D/', blank = True, null=True)
    fotografie3 = models.ImageField(upload_to = 'photos/%Y/%M/%D/', blank = True, null=True)
    fotografie4 = models.ImageField(upload_to = 'photos/%Y/%M/%D/', blank = True, null=True)
    fotografie5 = models.ImageField(upload_to = 'photos/%Y/%M/%D/', blank = True, null=True)
    fotografie6 = models.ImageField(upload_to = 'photos/%Y/%M/%D/', blank = True, null=True)
    publicat = models.BooleanField(default=False)
    data_publicare = models.DateField(default = datetime.now, blank = True, null=True)

    #metoda de identificare a terenului
    def __str__(self):
        return self.titlu

#modelul de anunturi favorite
class FavoriteListing(models.Model):
    #clientul
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    #anunturile favorite
    apartamente_favorite = models.ManyToManyField(Apartament, blank=True)
    case_favorite = models.ManyToManyField(House, blank=True)
    terenuri_favorite = models.ManyToManyField(Land,  blank=True)

    #metoda de identificare - prin numele si prenumele clientului
    def __str__(self):
        return self.client.nume + ' ' + self.client.prenume