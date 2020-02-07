class Podjetje:
    def __init__(self, ime, naslov, center, pot=None):
        self.ime = ime
        self.naslov = naslov
        self.center = center
        if pot == None:
            self.pot = None
        else:
            self.pot = Pot(pot)

    def __str__(self):
        return self.ime

    def dodaj_pot(self,pot):
        self.pot = Pot(pot)

    def json_oblika(self):
        slovar = {
            'ime': self.ime,
            'ulica': self.naslov.ulica,
            'mesto': self.naslov.mesto,
            'posta': self.naslov.posta,
            'regija': self.naslov.regija,
            'koordinate': self.naslov.koordinate,
            'pot': self.pot.json_oblika() if self.pot != None else None,
            'center': self.center
        }
        return slovar

    def csv_oblika(self):
        slovar = {
            'ime': self.ime,
            'ulica': self.naslov.ulica,
            'mesto': self.naslov.mesto,
            'posta': self.naslov.posta,
            'regija': self.naslov.regija,
            'koordinate': self.naslov.string_koordinat(),
            'center': self.center,
            'dolzina': self.pot.dolzina if self.pot != None else None,
            'trajanje': self.pot.trajanje if self.pot != None else None,
            'pot': self.pot.string_poti() if self.pot != None else None
        }
        return slovar

class Naslov:
    def __init__(self, ulica, mesto, posta, regija, koordinate):
        self.ulica = ulica
        self.mesto = mesto
        self.posta = posta
        self.regija = regija
        self.koordinate = koordinate

    def string_koordinat(self):
        return str(self.koordinate[0]) + ';' + str(self.koordinate[1])

class Pot:
    def __init__(self,pot):
        dolzina = pot['dolzina']
        if isinstance(dolzina,str):
            dolzina = float(dolzina.replace('km','').replace(',','.').strip())
        self.dolzina = dolzina
        trajanje = pot['trajanje']
        if isinstance(trajanje,str):
            if 'ur' in trajanje:
                slovar = trajanje.split('ur')
                ure = int(slovar[0]) if slovar[0] != "" else 0
                minute = slovar[1].replace('min','').strip()
                minute = int(minute) if minute != "" else 0
                trajanje = ure * 60 + minute
            else:
                minute = trajanje.replace('min','').strip()
                minute = int(minute) if minute != "" else 0
                trajanje = minute
        self.trajanje = trajanje
        pot = pot['pot']
        for n in range(len(pot)):
            razdalja = pot[n][1]
            cesta = pot[n][0]
            if isinstance(razdalja,str):
                pot[n] = (cesta,float(razdalja.replace('km','').replace(',','.').strip()))
        self.pot = pot

    def json_oblika(self):
        slovar = {
            'dolzina':self.dolzina,
            'trajanje':self.trajanje,
            'pot':self.pot
        }
        return slovar   

    def string_poti(self):
        string = ""
        for pot in self.pot:
            string += str(pot[0]) + ';' + str(pot[1]) + "--"
        if len(string) > 0:
            string = string[:-2]
        return string

