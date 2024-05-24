from abc import ABC, abstractmethod
from datetime import datetime, timedelta
import random

class Szoba(ABC):
    def __init__(self, ar, szobaszam):
        self.ar = ar
        self.szobaszam = szobaszam

    @abstractmethod
    def __str__(self):
        pass

class EgyagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(ar=5000, szobaszam=szobaszam)

    def __str__(self):
        return f"Egyágyas szoba, Szám: {self.szobaszam}, Ár: {self.ar} Ft/éj"

class KetagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(ar=8000, szobaszam=szobaszam)

    def __str__(self):
        return f"Kétágyas szoba, Szám: {self.szobaszam}, Ár: {self.ar} Ft/éj"

class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []
        self.foglalasok = []

    def add_szoba(self, szoba):
        self.szobak.append(szoba)

    def add_foglalas(self, foglalas):
        self.foglalasok.append(foglalas)

class Foglalas:
    def __init__(self, szoba, datum):
        self.szoba = szoba
        self.datum = datum

    def __str__(self):
        return f"Foglalás - Szoba: {self.szoba.szobaszam}, Dátum: {self.datum}"

class FoglalasKezelo:
    @staticmethod
    def foglalas(szalloda, szobaszam, datum):
        for szoba in szalloda.szobak:
            if szoba.szobaszam == szobaszam:
                for foglalas in szalloda.foglalasok:
                    if foglalas.szoba.szobaszam == szobaszam and foglalas.datum == datum:
                        return "Ez a szoba már foglalt ezen a dátumon."
                uj_foglalas = Foglalas(szoba, datum)
                szalloda.add_foglalas(uj_foglalas)
                return f"Foglalás sikeres! Ár: {szoba.ar} Ft"

        return "Nincs ilyen szobaszám a szállodában."

    @staticmethod
    def lemondas(szalloda, szobaszam, datum):
        for foglalas in szalloda.foglalasok:
            if foglalas.szoba.szobaszam == szobaszam and foglalas.datum == datum:
                szalloda.foglalasok.remove(foglalas)
                return "Foglalás lemondva."

        return "Nincs ilyen foglalás."

    @staticmethod
    def listaz_foglalasok(szalloda):
        if not szalloda.foglalasok:
            return "Nincs foglalás ebben a szállodában."
        return "\n".join(str(foglalas) for foglalas in szalloda.foglalasok)

def szalloda_kivalasztas(szallodak):
    while True:
        print("\nVálassza ki a szállodát:")
        for i, szalloda in enumerate(szallodak):
            print(f"{i + 1}. {szalloda.nev}")
        print(f"{len(szallodak) + 1}. Kilépés")
        valasztas = int(input("Szálloda sorszáma: ")) - 1
        if valasztas == len(szallodak):
            return None
        elif 0 <= valasztas < len(szallodak):
            return szallodak[valasztas]
        else:
            print("Érvénytelen választás, próbálja újra.")

def szalloda_menu(szalloda):
    while True:
        print(f"\n{szalloda.nev} menüje:")
        print("1. Szoba foglalása")
        print("2. Foglalás lemondása")
        print("3. Foglalások listázása")
        print("4. Vissza a szálloda választáshoz")
        valasztas = input("Válasszon egy műveletet: ")

        if valasztas == "1":
            szobaszam = int(input("Adja meg a szobaszámot: "))
            datum = input("Adja meg a dátumot (YYYY-MM-DD): ")
            try:
                foglalas_datum = datetime.strptime(datum, "%Y-%m-%d")
                if foglalas_datum <= datetime.now():
                    print("A dátumnak jövőbelinek kell lennie.")
                    continue
                eredmeny = FoglalasKezelo.foglalas(szalloda, szobaszam, datum)
                print(eredmeny)
            except ValueError:
                print("Érvénytelen dátum formátum.")
        elif valasztas == "2":
            szobaszam = int(input("Adja meg a szobaszámot: "))
            datum = input("Adja meg a dátumot (YYYY-MM-DD): ")
            eredmeny = FoglalasKezelo.lemondas(szalloda, szobaszam, datum)
            print(eredmeny)
        elif valasztas == "3":
            print("Összes foglalás:")
            print(FoglalasKezelo.listaz_foglalasok(szalloda))
        elif valasztas == "4":
            break
        else:
            print("Érvénytelen választás, próbálja újra.")

def random_datum():
    today = datetime.now()
    random_number_of_days = random.randint(1, 365)
    random_date = today + timedelta(days=random_number_of_days)
    return random_date.strftime("%Y-%m-%d")

def random_foglalasok(szalloda, szobak_szama=100, foglalasok_szama=5):
    for _ in range(foglalasok_szama):
        szobaszam = random.randint(1, szobak_szama)
        datum = random_datum()
        szoba = next((sz for sz in szalloda.szobak if sz.szobaszam == szobaszam), None)
        if szoba:
            szalloda.add_foglalas(Foglalas(szoba, datum))

def felhasznaloi_interfesz():
    szalloda1 = Szalloda("Four Seasons")
    szalloda2 = Szalloda("A Gottwalld")
    szallodak = [szalloda1, szalloda2]

    # Szobák hozzáadása: páratlan egyágyas, páros kétágyas mindkét szállodában
    for szalloda in szallodak:
        for i in range(1, 101):
            if i % 2 == 1:
                szalloda.add_szoba(EgyagyasSzoba(i))
            else:
                szalloda.add_szoba(KetagyasSzoba(i))

    # Véletlenszerű foglalások hozzáadása mindkét szállodához
    random_foglalasok(szalloda1)
    random_foglalasok(szalloda2)

    while True:
        szalloda = szalloda_kivalasztas(szallodak)
        if szalloda is None:
            print("Kilépés...")
            break
        else:
            szalloda_menu(szalloda)

if __name__ == "__main__":
    felhasznaloi_interfesz()
