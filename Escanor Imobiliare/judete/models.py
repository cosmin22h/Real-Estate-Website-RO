from django.db import models

from alte_date.judete import JUDETE

#judet
class District(models.Model):
    #camp judet
    judet = models.CharField(max_length=20, choices=JUDETE, null=True)
    #camp harta
    harta = models.CharField(max_length=800, null=True)

    #identificare
    def __str__(self):
        return self.judet