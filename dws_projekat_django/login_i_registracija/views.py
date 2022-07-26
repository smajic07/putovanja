from django.core import serializers
from django.core.mail import send_mail
from django.shortcuts import redirect
from password_generator import PasswordGenerator
from datetime import datetime, date

# Create your views here.
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view

from operator import itemgetter
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter


from dws_projekat_django import settings
from login_i_registracija.models import Korisnici, Agencije, Zahtjevi_Putovanja, Putovanja, Korisnik_Putovanja


@api_view(['POST'])
def login(request):
    print("EVO ME U LOGINU")
    username = request.data.get('username')
    lozinka = request.data.get('lozinka')
    ima_korisnika = False
    ima_agencije = False

    if "@" in username:
        try:
            korisnik = Korisnici.objects.get(email=username)
            if(korisnik):
                ima_korisnika = True
                if(lozinka == korisnik.lozinka):
                    return JsonResponse({'tip': 'Korisnik', 'id': korisnik.id, 'slika': str(korisnik.slika)})
        except:
            print("Nema takvog korisnika")
        try:
            agencija = Agencije.objects.get(email=username)
            if(agencija):
                ima_agencije = True
                if(lozinka == agencija.lozinka):
                    return JsonResponse({'tip': 'Agencija', 'id': agencija.id, 'slika': str(agencija.slika)})
        except:
            print("Nema takve agencije")

        if (ima_korisnika or ima_agencije):
            return HttpResponse("Pogresna lozinka")

        return HttpResponse('Ne postoji takav email')
    else:
        try:
            korisnik = Korisnici.objects.get(username=username)
            if(korisnik):
                ima_korisnika = True
                if(lozinka == korisnik.lozinka):
                    return JsonResponse({'tip': 'Korisnik', 'id': korisnik.id, 'slika': str(korisnik.slika)})
        except:
            print("Nema takvog korisnika")
        try:
            agencija = Agencije.objects.get(username=username)
            if(agencija):
                ima_agencije = True
                if(lozinka == agencija.lozinka):
                    return JsonResponse({'tip': 'Agencija', 'id': agencija.id, 'slika': str(agencija.slika)})
        except:
            print("Nema takve agencije")

        if (ima_korisnika or ima_agencije):
            return HttpResponse("Pogresna lozinka")

        return HttpResponse("Ne postoji takav username")

@api_view(['POST'])
def resetuj_lozinku(request):
    print("EVO ME U RESETOVANJU LOZINKE")
    username = request.data.get('username')

    pwo = PasswordGenerator()
    pwo.minlen = 12

    try:
        korisnik = Korisnici.objects.get(username=username)
        if(korisnik):
            nova_lozinka = pwo.generate()
            send_mail('RESETOVANJE LOZINKE', 'Vaša nova lozinka je: ' + nova_lozinka, 'putovanja.smajic.edin.7@hotmail.com', [korisnik.email], fail_silently=False)
            korisnik.lozinka = nova_lozinka
            korisnik.save()
            return HttpResponse("Resetovana lozinka uspjesno")
    except:
        print("Nema takvog korisnika")
    try:
        agencija = Agencije.objects.get(username=username)
        if(agencija):
            nova_lozinka = pwo.generate()
            send_mail('RESETOVANJE LOZINKE', 'Vaša nova lozinka je: ' + nova_lozinka, 'putovanja.smajic.edin.7@hotmail.com', [agencija.email], fail_silently=False)
            agencija.lozinka = nova_lozinka
            agencija.save()
            return HttpResponse("Resetovana lozinka uspjesno")
    except:
        print("Nema takve agencije")

    return HttpResponse("Ne postoji takav username")

@api_view(['POST'])
def registracija_korisnik(request):
    print("EVO ME U REGISTRACIJI KORISNIKA")
    ime = request.data.get('ime')
    prezime = request.data.get('prezime')
    username = request.data.get('username')
    email = request.data.get('email')
    lozinka = request.data.get('lozinka')

    try:
        korisnik = Korisnici.objects.get(username=username)
        return HttpResponse("Postoji")
    except:
        print("Nema takvog korisnika")
    try:
        agencija = Agencije.objects.get(username=username)
        return HttpResponse("Postoji")
    except:
        print("Nema takve agencije")

    k = Korisnici(ime=ime, prezime=prezime, username=username, email=email, lozinka=lozinka)
    k.save()

    return HttpResponse("Dodat")

@api_view(['POST'])
def registracija_agencija(request):
    print("EVO ME U REGISTRACIJI AGENCIJE")
    naziv = request.data.get('naziv')
    username = request.data.get('id')
    email = request.data.get('email')
    datum_osnivanja = request.data.get('datum_osnivanja')
    lozinka = request.data.get('lozinka')

    try:
        korisnik = Korisnici.objects.get(username=username)
        return HttpResponse("Postoji")
    except:
        print("Nema takvog korisnika")
    try:
        agencija = Agencije.objects.get(username=username)
        return HttpResponse("Postoji")
    except:
        print("Nema takve agencije")

    a = Agencije(naziv=naziv, username=username, email=email, datum_osnivanja=datum_osnivanja, lozinka=lozinka)
    a.save()

    return HttpResponse("Dodat")


@api_view(['POST'])
def povuci_agencije(request):
    print("EVO ME U POVLAČENJU AGENCIJA")
    agencije = Agencije.objects.all()
    obj = serializers.serialize('json', agencije)
    return HttpResponse(obj)

@api_view(['POST'])
def podnesi_zahtjev_za_putovanje(request):
    print("EVO ME U PODNEŠENJU ZAHTJEVA ZA PUTOVANJE")
    naziv_mjesta = request.data.get('naziv_mjesta')
    datum = request.data.get('datum')
    ponuda_cijena = request.data.get('ponuda_cijena')
    korisnik_id = int(request.data.get('korisnik_id'))
    agencija_id = int(request.data.get('agencija_id'))
    vrsta_prevoza = request.data.get('vrsta_prevoza')

    Zahtjevi_Putovanja.objects.create(naziv_mjesta=naziv_mjesta, datum=datum, ponuda_cijena=ponuda_cijena, tip='Pojedinacno putovanje',
                            vrsta_prevoza=vrsta_prevoza, korisnik_id_id=korisnik_id, agencija_id_id=agencija_id, status='Cekanje')

    return HttpResponse("Dodat")

@api_view(['POST'])
def dodaj_putovanje(request):
    print("EVO ME U DODAVANJU PUTOVANJA")
    latituda = request.data.get('latituda')
    longituda = request.data.get('longituda')
    min_broj_putnika = request.data.get('min_broj_putnika')
    max_broj_putnika = request.data.get('max_broj_putnika')
    naziv_mjesta = request.data.get('naziv_mjesta')
    datum = request.data.get('datum')
    cijena = request.data.get('cijena')
    tip = request.data.get('tip')
    vrsta_prevoza = request.data.get('vrsta_prevoza')
    agencija_id = request.data.get('agencija_id')
    opis_putovanja = request.data.get('opis_putovanja')
    slika = request.FILES['slika']

    Putovanja.objects.create(latituda=latituda, longituda=longituda, min_broj_putnika=min_broj_putnika,
                             max_broj_putnika=max_broj_putnika,naziv_mjesta=naziv_mjesta, datum=datum, cijena=cijena,
                             tip=tip, vrsta_prevoza=vrsta_prevoza,agencija_id_id=agencija_id,
                             opis_putovanja=opis_putovanja, slika=slika)

    return redirect('http://localhost:3000/agencija/dodaj_putovanje')


@api_view(['POST'])
def daj_sva_putovanja(request):
    print("EVO ME U DOBIJANJU SVIH PUTOVANJA")
    putovanja = Putovanja.objects.all()
    niz_putovanja = []
    for p in putovanja:
        if days_between(date.today(), p.datum) > 0:
            niz_putovanja.append(p)
    obj = serializers.serialize('json', niz_putovanja)
    return HttpResponse(obj)

def days_between(d1, d2):
    d1 = d1.strftime("%Y-%m-%d")
    d2 = d2.strftime("%Y-%m-%d")
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return (d2 - d1).days

@api_view(['POST'])
def daj_sva_putovanja_za_korisnika_iz_proslosti(request):
    print("EVO ME U DOBIJANJU SVIH PUTOVANJA IZ PROŠLOSTI ZA SPECIFIČNOG KORISNIKA")
    id_korisnika = request.data.get('korisnik_id')
    putovanja = Korisnik_Putovanja.objects.filter(korisnik_id_id=id_korisnika)
    niz_putovanja = []
    for p in putovanja:
        if days_between(date.today(), p.putovanje_id.datum) <= 0:
            putovanje = {"agencija_id": p.putovanje_id.agencija_id_id, "cijena": p.putovanje_id.cijena, "datum": p.putovanje_id.datum,
                 "min_broj_putnika": p.putovanje_id.min_broj_putnika, "max_broj_putnika": p.putovanje_id.max_broj_putnika,
                 "naziv_mjesta": p.putovanje_id.naziv_mjesta, "opis_putovanja": p.putovanje_id.opis_putovanja,
                 "longituda": p.putovanje_id.longituda, "latituda": p.putovanje_id.latituda, "tip": p.putovanje_id.tip,
                  "id": p.putovanje_id.id, "vrsta_prevoza": p.putovanje_id.vrsta_prevoza, "slika": p.putovanje_id.slika.url}
            niz_putovanja.append(putovanje)

    niz_putovanja2 = sorted(niz_putovanja, key=itemgetter('datum'), reverse=True)

    return JsonResponse(niz_putovanja2, safe=False)

@api_view(['POST'])
def daj_sva_putovanja_za_korisnika_u_buducnosti(request):
    print("EVO ME U DOBIJANJU SVIH PUTOVANJA U BUDUĆNOSTI ZA SPECIFIČNOG KORISNIKA")
    id_korisnika = request.data.get('korisnik_id')
    putovanja = Korisnik_Putovanja.objects.filter(korisnik_id_id=id_korisnika)
    niz_putovanja = []
    for p in putovanja:
        if days_between(date.today(), p.putovanje_id.datum) > 0:
            putovanje = {"agencija_id": p.putovanje_id.agencija_id_id, "cijena": p.putovanje_id.cijena, "datum": p.putovanje_id.datum,
                 "min_broj_putnika": p.putovanje_id.min_broj_putnika, "max_broj_putnika": p.putovanje_id.max_broj_putnika,
                 "naziv_mjesta": p.putovanje_id.naziv_mjesta, "opis_putovanja": p.putovanje_id.opis_putovanja,
                 "longituda": p.putovanje_id.longituda, "latituda": p.putovanje_id.latituda, "tip": p.putovanje_id.tip,
                  "id": p.putovanje_id.id, "vrsta_prevoza": p.putovanje_id.vrsta_prevoza, "slika": p.putovanje_id.slika.url}
            niz_putovanja.append(putovanje)

    niz_putovanja2 = sorted(niz_putovanja, key=itemgetter('datum'), reverse=True)

    return JsonResponse(niz_putovanja2, safe=False)

@api_view(['POST'])
def daj_sve_zahtjeve_za_putovanja_korisnika(request):
    print("EVO ME U DOBIJANJU SVIH ZAHTJEVA ZA PUTOVANJA ZA SPECIFIČNOG KORISNIKA")
    id_korisnika = request.data.get('korisnik_id')
    putovanja = Zahtjevi_Putovanja.objects.filter(korisnik_id_id=id_korisnika)
    niz_putovanja = []
    for p in putovanja:
        putovanje = {"agencija_id": p.agencija_id_id, "naziv_agencije": p.agencija_id.naziv, "cijena": p.ponuda_cijena, "datum": p.datum,
             "naziv_mjesta": p.naziv_mjesta, "tip": p.tip, "id": p.id, "vrsta_prevoza": p.vrsta_prevoza, "status": p.status}
        niz_putovanja.append(putovanje)

    niz_putovanja2 = sorted(niz_putovanja, key=itemgetter('datum'), reverse=True)

    return JsonResponse(niz_putovanja2, safe=False)

@api_view(['POST'])
def daj_putovanje(request):
    print("EVO ME U DOBIJANJU SPECIFIČNOG PUTOVANJA")
    id_putovanja = request.data.get('id_putovanja')
    id_korisnika = request.data.get('korisnik_id')
    putovanje = Putovanja.objects.get(id=id_putovanja)
    agencija = Agencije.objects.get(id=putovanje.agencija_id_id)
    niz_putovanja = []
    niz_putovanja.append(putovanje)
    niz_putovanja.append(agencija)
    try:
        putovanja_ovog_korisnika = Korisnik_Putovanja.objects.filter(korisnik_id_id=id_korisnika)
        for p in putovanja_ovog_korisnika:
            if int(p.putovanje_id_id) == int(id_putovanja):
                niz_putovanja.append(p)
                break
    except:
        print("EXCEPTION")
        obj = serializers.serialize('json', niz_putovanja)
        return HttpResponse(obj)
    obj = serializers.serialize('json', niz_putovanja)
    return HttpResponse(obj)

@api_view(['POST'])
def dodaj_putovanje_za_korisnika(request):
    print("EVO ME U KUPOVANJU KARTE KORISNIKA ZA PUTOVANJE")
    korisnik_id = request.data.get('korisnik_id')
    putovanje_id = request.data.get('putovanje_id')

    Korisnik_Putovanja.objects.create(korisnik_id_id=korisnik_id, putovanje_id_id=putovanje_id)

    return HttpResponse("Dodat")

@api_view(['POST'])
def ponisti_putovanje_za_korisnika(request):
    print("EVO ME U PONIŠTAVANJU KARTE KORISNIKA ZA PUTOVANJE")
    korisnik_id = request.data.get('korisnik_id')
    putovanje_id = request.data.get('putovanje_id')

    Korisnik_Putovanja.objects.filter(korisnik_id_id=korisnik_id).filter(putovanje_id_id=putovanje_id).delete()

    return HttpResponse("Ponisteno")

@api_view(['POST'])
def daj_sva_putovanja_za_agenciju_iz_proslosti(request):
    print("EVO ME U DOBIJANJU SVIH PUTOVANJA IZ PROŠLOSTI ZA SPECIFIČNU AGENCIJU")
    id_agencije = request.data.get('agencija_id')
    print(id_agencije)
    putovanja = Putovanja.objects.filter(agencija_id_id=id_agencije)
    niz_putovanja = []
    for p in putovanja:
        if days_between(date.today(), p.datum) <= 0:
            putovanje = {"agencija_id": p.agencija_id_id, "cijena": p.cijena, "datum": p.datum,
                 "min_broj_putnika": p.min_broj_putnika, "max_broj_putnika": p.max_broj_putnika,
                 "naziv_mjesta": p.naziv_mjesta, "opis_putovanja": p.opis_putovanja,
                 "longituda": p.longituda, "latituda": p.latituda, "tip": p.tip,
                  "id": p.id, "vrsta_prevoza": p.vrsta_prevoza, "slika": p.slika.url}
            niz_putovanja.append(putovanje)
    niz_putovanja2 = sorted(niz_putovanja, key=itemgetter('datum'), reverse=True)

    return JsonResponse(niz_putovanja2, safe=False)

@api_view(['POST'])
def daj_sva_putovanja_za_agenciju_u_buducnosti(request):
    print("EVO ME U DOBIJANJU SVIH PUTOVANJA U BUDUĆNOSTI ZA SPECIFIČNOG KORISNIKA")
    id_agencije = request.data.get('agencija_id')
    print(id_agencije)
    putovanja = Putovanja.objects.filter(agencija_id_id=id_agencije)
    niz_putovanja = []
    for p in putovanja:
        if days_between(date.today(), p.datum) > 0:
            putovanje = {"agencija_id": p.agencija_id_id, "cijena": p.cijena, "datum": p.datum,
                 "min_broj_putnika": p.min_broj_putnika, "max_broj_putnika": p.max_broj_putnika,
                 "naziv_mjesta": p.naziv_mjesta, "opis_putovanja": p.opis_putovanja,
                 "longituda": p.longituda, "latituda": p.latituda, "tip": p.tip,
                  "id": p.id, "vrsta_prevoza": p.vrsta_prevoza, "slika": p.slika.url}
            niz_putovanja.append(putovanje)
    niz_putovanja2 = sorted(niz_putovanja, key=itemgetter('datum'), reverse=True)

    return JsonResponse(niz_putovanja2, safe=False)

@api_view(['POST'])
def daj_putovanje_agenciji(request):
    print("EVO ME U DOBIJANJU SPECIFIČNOG PUTOVANJA AGENCIJI")
    id_putovanja = request.data.get('id_putovanja')
    id_agencije = request.data.get('agencija_id')
    putovanje = Putovanja.objects.get(id=id_putovanja)
    agencija = Agencije.objects.get(id=putovanje.agencija_id_id)
    niz_putovanja = []
    niz_putovanja.append(putovanje)
    niz_putovanja.append(agencija)

    obj = serializers.serialize('json', niz_putovanja)
    return HttpResponse(obj)

@api_view(['POST'])
def daj_sve_zahtjeve_za_putovanja_agencije(request):
    print("EVO ME U DOBIJANJU SVIH ZAHTJEVA ZA PUTOVANJA ZA SPECIFIČNU AGENCIJU")
    id_agencije = request.data.get('agencija_id')
    putovanja = Zahtjevi_Putovanja.objects.filter(agencija_id_id=id_agencije)
    niz_putovanja = []
    for p in putovanja:
        putovanje = {"agencija_id": p.agencija_id_id, "naziv_agencije": p.agencija_id.naziv, "cijena": p.ponuda_cijena, "datum": p.datum,
             "naziv_mjesta": p.naziv_mjesta, "tip": p.tip, "id": p.id, "vrsta_prevoza": p.vrsta_prevoza, "status": p.status,
             "korisnik_username": p.korisnik_id.username}
        niz_putovanja.append(putovanje)

    niz_putovanja2 = sorted(niz_putovanja, key=itemgetter('datum'), reverse=True)

    return JsonResponse(niz_putovanja2, safe=False)

@api_view(['POST'])
def promijeni_status_putovanju(request):
    print("EVO ME U PROMIJENI STATUSA PUTOVANJA")
    id_putovanja = request.data.get('id_putovanja')
    status = request.data.get('status')

    zahtjev_za_putovanje = Zahtjevi_Putovanja.objects.get(id=id_putovanja)
    if (zahtjev_za_putovanje):
        zahtjev_za_putovanje.status = status
        zahtjev_za_putovanje.save()

    return HttpResponse("Promijenjeno")

@api_view(['POST'])
def ukloni_putovanje(request):
    print("EVO ME U UKLANJANJU PUTOVANJA")
    id_putovanja = request.data.get('id_putovanja')

    putovanje = Putovanja.objects.get(id=id_putovanja)
    if (putovanje):
        putovanje.delete()
        return HttpResponse("Uklonjeno")

    return HttpResponse("Belaj")

@api_view(['POST'])
def daj_info_za_korisnika(request):
    print("EVO ME U DOHVATANJU INFA ZA KORISNIKA")
    id_korisnika = request.data.get('id_korisnika')

    niz_korisnika = []
    korisnici = Korisnici.objects.filter(id=id_korisnika)
    for k in korisnici:
        niz_korisnika.append(k)

    obj = serializers.serialize('json', niz_korisnika)
    return HttpResponse(obj)

@api_view(['POST'])
def daj_info_za_agenciju(request):
    print("EVO ME U DOHVATANJU INFA ZA AGENCIJU")
    id_agencije = request.data.get('id_agencije')

    niz_agencija = []
    agencije = Agencije.objects.filter(id=id_agencije)
    for a in agencije:
        niz_agencija.append(a)

    obj = serializers.serialize('json', niz_agencija)
    return HttpResponse(obj)

@api_view(['POST'])
def izmjeni_info_profila_korisnika(request):
    print("EVO ME U IZMJENI PROFILA KORISNIKA")
    id_korisnika = request.data.get('id_korisnika')
    ime = request.data.get('ime')
    prezime = request.data.get('prezime')
    lozinka = request.data.get('lozinka')
    slika = request.FILES['slika']

    korisnik = Korisnici.objects.get(id=id_korisnika)
    if (korisnik):
        korisnik.ime = ime
        korisnik.prezime = prezime
        korisnik.lozinka = lozinka
        korisnik.slika = slika
        korisnik.save()

    return redirect('http://localhost:3000/korisnik/postavke')

@api_view(['POST'])
def izmjeni_info_profila_agencije(request):
    print("EVO ME U IZMJENI PROFILA AGENCIJE")
    id_agencije = request.data.get('id_agencije')
    naziv = request.data.get('naziv')
    lozinka = request.data.get('lozinka')
    slika = request.FILES['slika']

    agencija = Agencije.objects.get(id=id_agencije)
    if (agencija):
        agencija.naziv = naziv
        agencija.lozinka = lozinka
        agencija.slika = slika
        agencija.save()

    return redirect('http://localhost:3000/agencija/postavke')

@api_view(['POST'])
def generisi_pdf_za_putovanje(request):
    id_putovanja = request.data.get('id_putovanja')
    putovanje = Putovanja.objects.get(id=id_putovanja)
    buf = io.BytesIO()

    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)

    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)

    lines = [
        "INFORMACIJE O PUTOVANJU",
        "",
        "Naziv posjecenog mjesta: " + putovanje.naziv_mjesta,
        "Datum odrzavanja: " + str(putovanje.datum),
        "Tip: " + putovanje.tip,
        "Vrsta prevoza: " + putovanje.vrsta_prevoza,
        "Cijena: " + str(putovanje.cijena) + " KM",
        "Opis: " + putovanje.opis_putovanja,
    ]

    for line in lines:
        textob.textLine(line)

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename="putovanje.pdf")


@api_view(['POST'])
def daj_putovanja_u_posljednjih_mjesec_dana_za_korisnika(request):
    print("EVO ME U DOBIJANJU SVIH PUTOVANJA U ZADNJIH MJESEC DANA ZA SPECIFIČNOG KORISNIKA")
    id_korisnika = request.data.get('korisnik_id')
    putovanja = Korisnik_Putovanja.objects.filter(korisnik_id_id=id_korisnika)
    niz_putovanja = []
    for p in putovanja:
        if days_between(date.today(), p.putovanje_id.datum) <= 0 and days_between(date.today(), p.putovanje_id.datum) >= -30:
            putovanje = {"agencija_id": p.putovanje_id.agencija_id_id, "cijena": p.putovanje_id.cijena, "datum": p.putovanje_id.datum,
                 "min_broj_putnika": p.putovanje_id.min_broj_putnika, "max_broj_putnika": p.putovanje_id.max_broj_putnika,
                 "naziv_mjesta": p.putovanje_id.naziv_mjesta, "opis_putovanja": p.putovanje_id.opis_putovanja,
                 "longituda": p.putovanje_id.longituda, "latituda": p.putovanje_id.latituda, "tip": p.putovanje_id.tip,
                  "id": p.putovanje_id.id, "vrsta_prevoza": p.putovanje_id.vrsta_prevoza, "slika": p.putovanje_id.slika.url}
            niz_putovanja.append(putovanje)

    niz_putovanja2 = sorted(niz_putovanja, key=itemgetter('datum'), reverse=True)

    return JsonResponse(niz_putovanja2, safe=False)


@api_view(['POST'])
def daj_putovanja_u_posljednjih_mjesec_dana_za_agenciju(request):
    print("EVO ME U DOBIJANJU SVIH PUTOVANJA U ZADNJIH MJESEC DANA ZA SPECIFIČNOG AGENCIJU")
    id_agencije = request.data.get('agencija_id')
    putovanja = Putovanja.objects.filter(agencija_id_id=id_agencije)
    niz_putovanja = []
    for p in putovanja:
        if days_between(date.today(), p.datum) <= 0 and days_between(date.today(), p.datum) >= -30:
            putovanje = {"agencija_id": p.agencija_id_id, "cijena": p.cijena, "datum": p.datum,
                 "min_broj_putnika": p.min_broj_putnika, "max_broj_putnika": p.max_broj_putnika,
                 "naziv_mjesta": p.naziv_mjesta, "opis_putovanja": p.opis_putovanja,
                 "longituda": p.longituda, "latituda": p.latituda, "tip": p.tip,
                  "id": p.id, "vrsta_prevoza": p.vrsta_prevoza, "slika": p.slika.url}
            niz_putovanja.append(putovanje)
    niz_putovanja2 = sorted(niz_putovanja, key=itemgetter('datum'), reverse=True)

    return JsonResponse(niz_putovanja2, safe=False)

@api_view(['POST'])
def podnesi_zahtjev_za_putovanje_sa_mape(request):
    print("EVO ME U PODNEŠENJU ZAHTJEVA ZA PUTOVANJE")
    latituda = request.data.get('latituda')
    longituda = request.data.get('longituda')
    naziv_mjesta = request.data.get('naziv_mjesta')
    datum = request.data.get('datum')
    ponuda_cijena = request.data.get('ponuda_cijena')
    korisnik_id = int(request.data.get('korisnik_id'))
    agencija_id = int(request.data.get('agencija_id'))
    vrsta_prevoza = request.data.get('vrsta_prevoza')

    Zahtjevi_Putovanja.objects.create(latituda=latituda, longituda=longituda, naziv_mjesta=naziv_mjesta, datum=datum, ponuda_cijena=ponuda_cijena, tip='Pojedinacno putovanje',
                            vrsta_prevoza=vrsta_prevoza, korisnik_id_id=korisnik_id, agencija_id_id=agencija_id, status='Cekanje')

    return HttpResponse("Dodat")

@api_view(['POST'])
def dodaj_putovanje_sa_mape(request):
    print("EVO ME U DODAVANJU PUTOVANJA SA MAPE")
    latituda = request.data.get('latituda')
    longituda = request.data.get('longituda')
    min_broj_putnika = request.data.get('min_broj_putnika')
    max_broj_putnika = request.data.get('max_broj_putnika')
    naziv_mjesta = request.data.get('naziv_mjesta')
    datum = request.data.get('datum')
    cijena = request.data.get('cijena')
    tip = request.data.get('tip')
    vrsta_prevoza = request.data.get('vrsta_prevoza')
    agencija_id = request.data.get('agencija_id')
    opis_putovanja = request.data.get('opis_putovanja')
    slika = request.FILES['slika']

    Putovanja.objects.create(latituda=latituda, longituda=longituda, min_broj_putnika=min_broj_putnika, max_broj_putnika=max_broj_putnika, naziv_mjesta=naziv_mjesta,
                             datum=datum, cijena=cijena, tip=tip, vrsta_prevoza=vrsta_prevoza,
                             agencija_id_id=agencija_id, opis_putovanja=opis_putovanja, slika=slika)

    return redirect('http://localhost:3000/agencija/planirana_putovanja')
