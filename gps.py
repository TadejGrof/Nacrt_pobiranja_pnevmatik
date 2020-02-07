from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import orodja
import time
import re
import json
from models import Podjetje, Naslov, Pot

# stran na kateri bomo zbirali podatke
zemljevid_stran = "https://zemljevid.najdi.si/najdi/?kaj=&kje="

vzorec = (
    r'\n.*?<h3.*?>(?P<firma>.+?)</h3>'
    r'\n.*?<address .*?>(?P<naslov>.+?)</address>'
    r'\n.*?'
    r'\n.*?'
    r'\n.*?'
    r'\n.*?'
    r'\n.*?'
    r'\n.*?'
    r'\n.*?'
    r'\n.*?'
    r'\n.*?'
    r'\n.*?'
    r'\n.*?'
    r'<a.*?id="(?P<gumb_id>.+?)"'
    r'.*?data-lat="(?P<dolzina>.+?)" data-lon="(?P<sirina>.+?)".*?</a>'
)

vzorec_podatkov_poti = (
    r'<div class="direction">'
    r'.*?'
    r'<p>(?P<dolzina>.+?)</p>'
    r'.*?'
    r'<p>(?P<trajanje>.+?)</p>'
)

vzorec_poti = (
    r'<div class="direction__steps">'
    r'(?P<vmesne_poti>.+?)'
    r'</div></div></div></div>'
)

vzorec_delne_poti = (
    r'<div class="direction__step">'
    r'.*?'
    r'<h5>(?P<cesta>.*?)</h5>'
    r'.*?'
    r'<span class="direction__step__distance__from">(?P<dolzina>.*?)</span>'
)

# nekateri id-ji in class-i gumbov katere je potrebno med nabiranjem podatkov prtisniti
iskanje_input_id = "cphBody_ctlSearchInline_inWhat"
iskanje_gumb_id = "cphBody_ctlSearchInline_btnSearch"

class_gumba_za_izbris_točke = "point__remove"
class_gumba_za_izracun_poti = "route__compute"

# podatki vnaprej določenega zbirališča
naslov_zbiralisca = Naslov("Tržaška cesta 511","Ljubljana","1000 Ljubljana","OSREDNJESLOVENSKA",None)
zbiralisce = Podjetje('zbiralisce',naslov_zbiralisca,None,None)

zbiralisca = {0:zbiralisce}


def shrani_stran(driver):
    '''funkcija, ki mi je shranila html stran, na kateri sem iskal podatke gumbov ter razne vzorce'''
    with open('stran.html',"w",encoding="utf-8") as dat:
        dat.write(driver.page_source)

def isci(driver,iskanje):
    print("iscem " + iskanje)
    index = zemljevid_stran.find('&')
    stran = zemljevid_stran[:index] + iskanje + zemljevid_stran[index:]
    driver.get(stran)


def objekti(driver):
    '''vrne vse zadetke, najdene na prvi strani iskanja'''
    vsebina = driver.page_source
    podjetja = []
    
    for zadetek in re.finditer(vzorec,vsebina):
        podjetja.append(zadetek.groupdict())
    return podjetja


def preveri_objekt(objekt,naslov):
    '''preveri če je naslov zadetka ujema z podanim naslovom iskanja'''
    naslov_objekta = objekt['naslov'].split(',')[0].strip()
    if naslov_objekta == naslov:
        return True
    return False


def najdi_in_dodaj(driver,podjetje):
    '''za podano podjetje na strani poišče naslov podjetja ter, če najde ujemanje naslova
    podjetju doda lokacijo ter ga na strani doda v iskanje poti...'''
    isci_prek_strani(driver, podjetje.naslov.ulica)
    for objekt in objekti(driver):
        if preveri_objekt(objekt, podjetje.naslov.ulica):
            if podjetje.naslov.koordinate == None:
                podjetje.naslov.koordinate = (float(objekt['dolzina']),float(objekt['sirina']))
            dodaj_tocko(driver,objekt)
            return True
    isci_prek_strani(driver,podjetje.naslov.ulica + " " + podjetje.naslov.posta)
    for objekt in objekti(driver):
        if preveri_objekt(objekt, podjetje.naslov.ulica):
            if podjetje.naslov.koordinate == None:
                podjetje.naslov.koordinate = (float(objekt['dolzina']),float(objekt['sirina']))
            dodaj_tocko(driver,objekt)
            return True
    print(podjetje.naslov.ulica)
    return False


def dodaj_tocko(driver,objekt):
    '''klikne gumb zadetka, kateri ga vrze v postopek racunanja poti na strani'''
    gumb_id = objekt['gumb_id']
    driver.find_element_by_id(gumb_id).click()


def izbriši_točko(driver,točka=1):
    '''določeno točko izbriše iz postopka racunanja poti na strani'''
    klik_gumba_class(driver,class_gumba_za_izbris_točke, točka)


def isci_prek_strani(driver,iskanje):
    '''da ohrani prvo tocko v postopku iskanja poti je treba naslednje podjetje iskati preko strani ne preko url-ja.'''
    iskanje_input = driver.find_element_by_id(iskanje_input_id)
    driver.execute_script("arguments[0].value = '" + iskanje + "';", iskanje_input) 
    driver.find_element_by_id(iskanje_gumb_id).click()


def izračun_poti(driver):
    '''klikne gumb za izračun poti'''
    klik_gumba_class(driver,class_gumba_za_izracun_poti)


def vrni_pot(driver):
    ''' na podlagi vzorcev poti poišče ter vrne izračunano pot'''
    i = 0
    while i < 10:
        try:
            vsebina = driver.page_source
            for zadetek in re.finditer(vzorec_podatkov_poti,vsebina):
                podatki_poti = zadetek.groupdict()
            vsebina_poti = re.findall(vzorec_poti,vsebina)[0]
            pot = []
            for zadetek in re.finditer(vzorec_delne_poti,vsebina_poti):
                del_poti = zadetek.groupdict()
                pot.append((del_poti['cesta'],del_poti['dolzina']))
            podatki_poti.update({'pot':pot})
            return podatki_poti
        except:
            time.sleep(1)
            i += 1
    

def klik_gumba_class(driver,class_name,index=0):
    ''' funkcija ki klikne gumb z podanim indexom v seznamo gumbov na strani z podanim classom'''
    try: 
        gumb = driver.find_elements_by_class_name(class_name)[index]
        gumb.click()
    except:
        print('ni gumba' + class_name)
        print("ni gumbov")


def doloci_poti(driver, podjetja):
    '''za vsako podjetje v podanih podjetjih določi pot do centra.'''
    zbiralisce = None
    for podjetje in podjetja:
        if podjetje.center != zbiralisce:
            if zbiralisce != None:
                izbriši_točko(driver,0) 
            zbiralisce = podjetje.center
            najdi_in_dodaj(driver,zbiralisca[zbiralisce])
        if podjetje.pot == None:
            if najdi_in_dodaj(driver, podjetje):
                izračun_poti(driver)
                pot = vrni_pot(driver)
                podjetje.dodaj_pot(pot)
                izbriši_točko(driver)
    return podjetja


def nalozi_podjetja(podjetja_list):
    '''iz seznama slovarjev podjetij vrne seznam podjetjih class Podjetje iz knjiznice models'''
    podjetja = []
    for podjetje in podjetja_list:
        naslov = Naslov(
            ulica = podjetje['ulica'],
            mesto = podjetje['mesto'],
            posta = podjetje['posta'],
            regija = podjetje['regija'],
            koordinate = podjetje['koordinate']
        )
        podjetja.append(
            Podjetje(
                podjetje['ime'],
                naslov,
                podjetje['center'],
                podjetje['pot']
            )
        )
    return podjetja

def main(datoteka):
    ''' glavna funkcija, kateri podamo json datoteko s seznamom slovarjev podjetij
    za vsako podjetje poišče pot ter lokacijo, podatke doda in jih zapiše nazaj
    v isto datoteko.  '''
    # odpre brskalnik firefox 
    driver = webdriver.Firefox()
    # nalozi stran na kateri zbiramo podatke    
    driver.get(zemljevid_stran)
    podjetja = nalozi_podjetja(orodja.nalozi_json(datoteka))
    try:
        podjetja = doloci_poti(driver, podjetja)
    except:
        pass
    podjetja = [podjetje.json_oblika() for podjetje in podjetja]
    orodja.zapisi_json(podjetja, datoteka)
    # zapre brskalnik
    driver.close()


def ustvari_csv(vhodna, izhodna):
    '''iz json dodateke s seznamom slovarjev podjetij pretvori v csv datoteko'''
    podjetja = nalozi_podjetja(orodja.nalozi_json(vhodna))
    podjetja = [podjetje.csv_oblika() for podjetje in podjetja ]
    imena_polj = ['ime','ulica','mesto','posta','regija','koordinate','center','dolzina','trajanje','pot']
    orodja.zapisi_csv(podjetja,imena_polj, izhodna)
    
