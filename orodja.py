import csv
import json
import os
import requests
import sys
from models import Podjetje, Naslov

def pripravi_imenik(ime_datoteke):
    '''Če še ne obstaja, pripravi prazen imenik za dano datoteko.'''
    imenik = os.path.dirname(ime_datoteke)
    if imenik:
        os.makedirs(imenik, exist_ok=True)


def shrani_spletno_stran(url, ime_datoteke, vsili_prenos=False):
    '''Vsebino strani na danem naslovu shrani v datoteko z danim imenom.'''
    try:
        print('Shranjujem {} ...'.format(url), end='')
        sys.stdout.flush()
        if os.path.isfile(ime_datoteke) and not vsili_prenos:
            print('shranjeno že od prej!')
            return
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        print('stran ne obstaja!')
    else:
        pripravi_imenik(ime_datoteke)
        with open(ime_datoteke, 'w', encoding='utf-8') as datoteka:
            datoteka.write(r.text)
            print('shranjeno!')


def vsebina_datoteke(ime_datoteke):
    '''Vrne niz z vsebino datoteke z danim imenom.'''
    with open(ime_datoteke, encoding='utf-8') as datoteka:
        return datoteka.read()


def nalozi_json(ime_datoteke):
    with open(ime_datoteke,encoding="utf-8") as json_file:
        data = json.load(json_file)
    return data

def zapisi_csv(slovarji, imena_polj, ime_datoteke):
    '''Iz seznama slovarjev ustvari CSV datoteko z glavo.'''
    pripravi_imenik(ime_datoteke)
    with open(ime_datoteke, 'w', newline='', encoding='utf-8') as csv_datoteka:
        writer = csv.DictWriter(csv_datoteka, fieldnames=imena_polj)
        writer.writeheader()
        for slovar in slovarji:
            writer.writerow(slovar)

def nalozi_txt(vhodna,izhodna):
    podjetja = []
    objekti = []
    with open(vhodna, encoding="utf-8") as dat:
        for vrstica in dat.readlines():
            podjetja.append(vrstica.replace('\n','').split("/"))
    for podjetje in podjetja:
        naslov = Naslov(
            podjetje[1].split(',')[0].strip(),
            podjetje[1].split(',')[1].strip(),
            podjetje[2].strip(),
            podjetje[3].strip(),
            None
        )
        podjetje = Podjetje(
            podjetje[0].strip(),
            naslov,
            0,
        )
        print(podjetje.center)
        objekti.append(podjetje.json_oblika())
    slovar = {'zbiralisce':None,'podjetja':[podjetje for podjetje in objekti]}
    zapisi_json(slovar,izhodna)
    return objekti
    

def zapisi_json(objekt, ime_datoteke):
    '''Iz danega objekta ustvari JSON datoteko.'''
    pripravi_imenik(ime_datoteke)
    with open(ime_datoteke, 'w', encoding='utf-8') as json_datoteka:
        json.dump(objekt, json_datoteka, indent=4, ensure_ascii=False)
