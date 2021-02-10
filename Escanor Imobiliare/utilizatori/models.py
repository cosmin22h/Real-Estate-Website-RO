from django.db import models
from django.contrib.auth.models import User

from alte_date.conturi import TIP_CLIENT

### modele utilizatori ###

#client
class Client(models.Model):
    #legatura cu utilizatorul
    user = models.OneToOneField(User, null = True, on_delete = models.CASCADE)
    #tipul de client
    tip_client = models.CharField(max_length=50, choices=TIP_CLIENT, null=True)
    #campuri pentru client
    nume = models.CharField(max_length=200, null=True)
    prenume = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True)
    telefon = models.CharField(max_length=10, null=True)
    data_nasterii = models.DateField(null=True)

    #identificator
    def __str__(self):
        return str(self.nume + " " + self.prenume)

#agentia imobiliara
class RealEstate(models.Model):
    #legatura cu utilizatorul
    user = models.OneToOneField(User, null = True, on_delete = models.CASCADE)
    #campuri pentru agentia imobiliara
    nume = models.CharField(max_length=200, null=True)
    logo = models.ImageField(upload_to='logo/', null=True) 
    descriere = models.TextField(null=True, blank=True)
    website = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(null=True)
    telefon1 = models.CharField(max_length=10, null=True)
    telefon2 = models.CharField(max_length=10, blank=True, null=True)
    adresa_sediu = models.CharField(max_length=400, null=True)
    an_infiintare = models.PositiveIntegerField(null=True)

    #identificator
    def __str__(self):
        return str(self.nume)


        