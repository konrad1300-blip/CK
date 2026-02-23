# -*- coding: utf-8 -*-
"""
Created on Wed May 15 12:03:02 2024

@author: k.piaskowski
"""
import dxfgrabber
import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Kalkulator czasu kroju v 0.15")

        # Tworzenie etykiety do wyświetlania przeciągniętego pliku
        self.label = tk.Label(root, text="Przeciągnij i upuść plik tutaj", width=40, height=10, bg="lightgray", font=('Arial', 12))
        self.label.pack(padx=10, pady=10)

        # Dodanie obsługi przeciągania i upuszczania plików
        self.label.drop_target_register(DND_FILES)
        self.label.dnd_bind('<<Drop>>', self.on_drop)

        # Zmienna do przechowywania ścieżki do pliku
        self.file_path = None

    def on_drop(self, event):
        # Aktualizacja zmiennej przechowującej ścieżkę do pliku
        self.file_path = event.data.strip('{}')
        # Wyświetlenie ścieżki do pliku w etykiecie
        self.label.config(text=f"Ścieżka do pliku: {self.file_path}")

        # Wywołanie funkcji Licz z plikiem jako argumentem
        self.Licz(self.file_path)

        # Wydrukowanie ścieżki do pliku w konsoli
        print(f"Plik został przeciągnięty: {self.file_path}")

    def Licz(self, plik):
        print(f"Nazwa pliku: {plik}")
        nazwa = plik       # pobieranie nazwy (str) z pola wprowadzania w oknie
        dlugosc = oblicz_dlugosc_sciezki(nazwa)
        sztuk = int(dzielnik.get())
        cz = round((((dlugosc * mckz) * mr) / 60 )/ sztuk, 2)    # Obliczenia czasu kroju
        cl = round((((dlugosc * mckl) * mr) / 60 )/ sztuk, 2)
        cw = round((((dlugosc * mckj) * mr) / 60 )/ sztuk, 2)
        ckz = round(((dlugosc * mckz) * mr) / 60, 2)    # Obliczenia czasu kroju (czysty krój)
        ckl = round(((dlugosc * mckl) * mr) / 60, 2)
        ckw = round(((dlugosc * mckj) * mr) / 60, 2)

        # Prezentacja wyników w obiekcie Label
        
        # ustawienie nowej zmiennej dla tekstu
        
        ttz =('ZUND czas kroju na 1 sztukę : ' + str(cz) + ' minut')
        ttl =('LEKTRA czas kroju na 1 sztukę : ' + str(cl) + ' minut')
        ttj =('JIGWEI czas kroju na 1 sztukę : ' + str(cw) + ' minut')
        tts =  ('Długość ścieżki       : ' + str(round((dlugosc),1))+' mm')
        ttzck =('ZUND czas kroju      : ' + str(ckz) + ' minut')
        ttlck =('LECTRA czas kroju    : ' + str(ckl) + ' minut')
        ttjck =('JIGWEI czas kroju  : ' + str(ckw) + ' minut') 

        #zmiana tekstu metodą config

        sciezka.config(text=tts)
        podzie_zund.config(text=ttz)
        podzie_lect.config(text=ttl)
        podzie_jing.config(text=ttj)
        zundck.config(text=ttzck)
        lectrack.config(text=ttlck)
        jigweick.config(text=ttjck)

       
        return(nazwa)
    
global mz, ml, mj, mckz, mckl, mckj, mr # Zmienne globalne z mnożnikiem dla poszczególnych maszyn
mz = 0.142839397        # Mnożnik średni
ml = 0.138815305
mj = 0.20800791
mckz = 0.08307067       # Mnożnik czysty krój
mckl = 0.090474006
mckj = 0.101171631
mr = 1.08748        # Mnożnik ramki

def oblicz_dlugosc_sciezki(plik_dxf):
    dxf = dxfgrabber.readfile(plik_dxf)
    
    dlugosc = 0.0
    poprzedni_punkt = None

    for entity in dxf.entities:
        # print(' ')
        if entity.dxftype == 'LINE':
            start_point = (entity.start.x, entity.start.y)
            end_point = (entity.end.x, entity.end.y)

            dlugosc += ((end_point[0] - start_point[0])**2 + (end_point[1] - start_point[1])**2)**0.5
        elif entity.dxftype == 'LWPOLYLINE' or entity.dxftype == 'POLYLINE':
            for point in entity.points:
                aktualny_punkt = (point[0], point[1])
                if poprzedni_punkt:
                    dlugosc += ((aktualny_punkt[0] - poprzedni_punkt[0])**2 + (aktualny_punkt[1] - poprzedni_punkt[1])**2)**0.5
                poprzedni_punkt = aktualny_punkt
            poprzedni_punkt = None
    return (dlugosc)



def pokaz():

    sztuk = int(dzielnik.get())
    
    nazwa = file_path       # pobieranie nazwy (str) z pola wprowadzania w oknie
    dlugosc = oblicz_dlugosc_sciezki(nazwa)
    cz = round((((dlugosc * mckz) * mr) / 60)/ sztuk, 2)    # Obliczenia czasu kroju
    cl = round((((dlugosc * mckl) * mr) / 60)/ sztuk, 2)
    cw = round((((dlugosc * mckj) * mr) / 60)/ sztuk, 2)
    ckz = round(((dlugosc * mckz) * mr) / 60, 2)            # Obliczenia czasu kroju (czysty krój)
    ckl = round(((dlugosc * mckl) * mr) / 60, 2)
    ckw = round(((dlugosc * mckj) * mr) / 60, 2)

    # Prezentacja wyników w obiekcie Label
    
    # ustawienie nowej zmiennej dla tekstu
    
    ttz =('ZUND średnia : ' + str(cz) + ' minut')
    ttl =('LEKTRA średnia : ' + str(cl) + ' minut')
    ttj =('JIGWEI średnia : ' + str(cw) + ' minut')
    tts =  ('Długość ścieżki       : ' + str(round((dlugosc),1))+' mm')
    ttzck =('ZUND czas kroju      : ' + str(ckz) + ' minut')
    ttlck =('LECTRA czas kroju    : ' + str(ckl) + ' minut')
    ttjck =('JIGWEI czas kroju  : ' + str(ckw) + ' minut') 

    #zmiana tekstu metodą config

    sciezka.config(text=tts)
    podzie_zund.config(text=ttz)
    podzie_lect.config(text=ttl)
    podzie_jing.config(text=ttj)
    zundck.config(text=ttzck)
    lectrack.config(text=ttlck)
    jigweick.config(text=ttjck)

   
    return(nazwa)

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    root.geometry('480x490+460+200')
    root. title('Szacowanie czasu kroju')
    root.config(bg='#223441')
    root.resizable=False
    
    app = App(root)
    
  
    
    ramka_wynikow = tk.Frame(root)
    ramka_wynikow.pack(pady=10)
    
    sciezka = tk.Label(ramka_wynikow,text=('Witaj w szacowaniu czasu kroju'), bg='#270606', font=('times', 14), foreground='#ffffff', width=45)
    sciezka.pack(pady=1, padx=1)
    jigweick = tk.Label(ramka_wynikow, text=('-------------------------------'), bg='#223441', font=('times', 14), foreground='#ffffff', width=45)
    jigweick.pack(pady=1, padx=1)
    zundck = tk.Label(ramka_wynikow, text=('Średnia oznacza realny czas na wykrój'), bg='#223441', font=('times', 14),justify='left', foreground='#ffffff', width=45)
    zundck.pack(pady=1, padx=1)
    lectrack = tk.Label(ramka_wynikow, text=('Czysty krój oznacza wyłącznie czas kroju'), bg='#223441', font=('times', 14), foreground='#ffffff', width=45)
    lectrack.pack(pady=1, padx=1)

    ramka = tk.Frame(root, bg='#223441')
    ramka.pack(pady=3)

    dzielnik = tk.Entry(ramka, font=('Arial', 14), width=5, justify='center')
    dzielnik.insert(0,'1')
    dzielnik.pack(pady=3)

    ram_wyn_2 = tk.Frame(root)
    ram_wyn_2.pack(pady=10)

    podzie_jing = tk.Label(ram_wyn_2, text=('-------------------------------'), bg='#223441', font=('times', 14), foreground='#ffffff', width=45)
    podzie_jing.pack(pady=1, padx=1)
    podzie_zund = tk.Label(ram_wyn_2, text=('-------------------------------'), bg='#223441', font=('times', 14), foreground='#ffffff', width=45)
    podzie_zund.pack(pady=1, padx=1)
    podzie_lect = tk.Label(ram_wyn_2, text=('-------------------------------'), bg='#223441', font=('times', 14), foreground='#ffffff', width=45)
    podzie_lect.pack(pady=1, padx=1)



 
    
    root.mainloop()
