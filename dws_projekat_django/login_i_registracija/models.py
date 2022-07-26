from django.db import models

# Create your models here.
from django.db import models


class Korisnici(models.Model):
    ime = models.CharField(max_length=50)
    prezime = models.CharField(max_length=50)
    username = models.CharField(max_length=20)
    email = models.CharField(max_length=150)
    lozinka = models.CharField(max_length=20)
    slika = models.ImageField(null=True, blank=True, upload_to="images/")

class Agencije(models.Model):
    naziv = models.CharField(max_length=150)
    username = models.CharField(max_length=20)
    email = models.CharField(max_length=150)
    datum_osnivanja = models.DateField()
    lozinka = models.CharField(max_length=20)
    slika = models.ImageField(null=True, blank=True, upload_to="images/")

class Putovanja(models.Model):
    min_broj_putnika = models.IntegerField()
    max_broj_putnika = models.IntegerField()
    naziv_mjesta = models.CharField(max_length=150)
    latituda = models.FloatField()
    longituda = models.FloatField()
    datum = models.DateField()
    tip = models.CharField(max_length=100)
    vrsta_prevoza = models.CharField(max_length=100)
    opis_putovanja = models.CharField(max_length=1000)
    cijena = models.FloatField()
    slika = models.ImageField(null=True, blank=True, upload_to="images/")
    agencija_id = models.ForeignKey(Agencije, on_delete=models.CASCADE)

class Zahtjevi_Putovanja(models.Model):
    naziv_mjesta = models.CharField(max_length=150)
    datum = models.DateField()
    ponuda_cijena = models.FloatField()
    tip = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    vrsta_prevoza = models.CharField(max_length=100)
    latituda = models.FloatField(null = True)
    longituda = models.FloatField(null = True)
    korisnik_id = models.ForeignKey(Korisnici, on_delete=models.CASCADE)
    agencija_id = models.ForeignKey(Agencije, on_delete=models.CASCADE)

class Korisnik_Putovanja(models.Model):
    korisnik_id = models.ForeignKey(Korisnici, on_delete=models.CASCADE)
    putovanje_id = models.ForeignKey(Putovanja, on_delete=models.CASCADE)
