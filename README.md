# Nacrt pobiranja pnevmatik

Naloga je nastala kot pomoč študentu Managementa na koprski fakulteti pri izdelavi diplomske naloge. Tematika diplomske naloge se loteva pojma povratne logistike na področju odpadnih pnevmatik ter možnosti zaslužka, kjer bi za dosega tega bilo potrebno vzpostaviti nov inovativen načrt pobiranja rabljenih pnevmatik na območju Slovenije.

Naloge sem se lotil s pomočjo predanih podatkov oziroma seznamom kontaktnih podatkov vseh pravnih oseb, ki se ukvarjajo s zamenjavo pnevmatik - vulkanizerji/avtomobilski servisi, ki ga je študent dobil iz portala Ajpes ter dodatno še podatke o zbirnih centrih podjetja Slopak, d.o.o., kjer se tudi nahajajo odpadne pnevmatike.

Dobljeni podatki so vsebovali imena, naslove, poštne številke ter delno regije

Podatke sem prejel v txt obliki, vendar ker so bili pomankljivi sem jih moral dopolniti. Na primer vsak vulkanizer je imel podatek o regiji medtem ko zbirni centri tega podatka niso imeli, zato sem analiziral povezave med poštnimi številkami in regijami ter za vsak zbirni center na podlagi številke določil pripadajočo regijo. 

Nato sem določil tudi lokacijo velikega zbirnega centra 

### Zajeti podatki:

* ime podjetja
* ulica
* mesto
* pošta
* regija
* dolžina poti do zbirnega centra
* trajanje poti do zbirnega centra
* pot po odsekih
* za vsak odsek:
  - Ime ceste
  - Dolžina odseka
  
 ### Delovne hipoteze:
 
  * Izračunati želimo stroške prevoza v obdobju enega leta,
      - Če imamo podano letno količino rabljenih pnevmatik na območju slovenije jih lahko razdelimo med posamezne vulkanizerje in zbirne        centre ter izračunamo strošek poti do vsakega.
 
 * Primerjati stroške prevoza v odvisnosti od radija pobiranja,
 
 * Izračunati stroške obdelave pnevmatik v odvisnosti od radija pobiranja,
 
 * Končen izračun prihodka takšnega načrta
 
 * Preveriti, če drži, da je glede na obliko Slovenije boljše imeti dve večji oz več zbirališč namesto ene.
 
## Zbiranje podatkov:

S pomočjo knjižnice selenium, geckodriver-a in firefox-a sem na spletni strani [najdi.si zemljevid](https://zemljevid.najdi.si/najdi/?kaj=&kje=) zajel še lokacijo posameznega podjetja oz. zbirnega centra, dolžino poti do glavnega centra, trajanje ter cestne odseke.

Skripta za zajem podatkov se nahaja v datoteki pgs.py.
Za poskus delovanja je potrebo naloziti selenium ter firefox,pognati sktipto. V mapi Poskusni_podatki se nahajajo json datoteke pripravljene na obdelavo. Za najhitrejšo preverjanje skripte priporočam uporabo 10_podjetij.json datoteke. V python terminalu pokličite funkcijo main in ji kot argument podajte pot do želene poskusne datoteke npr:

main('Poskusne_datoteke/10_podjetij.json')


## Analiza:

Analiza se nahaja v jupyterjevem notebooku nacrt_pobiranja_pnevmatik.ipynb.


