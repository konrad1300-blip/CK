# -*- coding: utf-8 -*-
"""
Flask web app do szacowania czasu kroju na podstawie plików DXF.
Uruchomienie: python app.py
"""

import os
import tempfile
import dxfgrabber
from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = 'twoj_tajny_klucz_zmien_w_produkcji'  # Wymagane do flash

# Mnożniki (stałe)
MCKZ = 0.08307067       # Zund – czysty krój
MCKL = 0.090474006      # Lectra – czysty krój
MCKJ = 0.101171631      # Jigwei – czysty krój
MR = 1.08748            # Mnożnik ramki

def oblicz_dlugosc_sciezki(plik_dxf):
    """Oblicza całkowitą długość ścieżki z pliku DXF."""
    dxf = dxfgrabber.readfile(plik_dxf)
    dlugosc = 0.0
    poprzedni_punkt = None

    for entity in dxf.entities:
        if entity.dxftype == 'LINE':
            start = (entity.start.x, entity.start.y)
            end = (entity.end.x, entity.end.y)
            dlugosc += ((end[0] - start[0])**2 + (end[1] - start[1])**2)**0.5
        elif entity.dxftype in ('LWPOLYLINE', 'POLYLINE'):
            for point in entity.points:
                aktualny = (point[0], point[1])
                if poprzedni_punkt:
                    dlugosc += ((aktualny[0] - poprzedni_punkt[0])**2 + (aktualny[1] - poprzedni_punkt[1])**2)**0.5
                poprzedni_punkt = aktualny
            poprzedni_punkt = None
    return dlugosc

def oblicz_czasy(dlugosc, sztuk):
    """Zwraca słownik z obliczonymi czasami."""
    cz = round((((dlugosc * MCKZ) * MR) / 60) / sztuk, 2)
    cl = round((((dlugosc * MCKL) * MR) / 60) / sztuk, 2)
    cw = round((((dlugosc * MCKJ) * MR) / 60) / sztuk, 2)
    ckz = round(((dlugosc * MCKZ) * MR) / 60, 2)
    ckl = round(((dlugosc * MCKL) * MR) / 60, 2)
    ckw = round(((dlugosc * MCKJ) * MR) / 60, 2)
    return {
        'dlugosc': round(dlugosc, 1),
        'cz': cz, 'cl': cl, 'cw': cw,
        'ckz': ckz, 'ckl': ckl, 'ckw': ckw
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    results = None
    filename = None

    if request.method == 'POST':
        # Sprawdzenie pliku
        if 'file' not in request.files:
            flash('Nie wybrano pliku.', 'error')
            return redirect(url_for('index'))
        file = request.files['file']
        if file.filename == '':
            flash('Nie wybrano pliku.', 'error')
            return redirect(url_for('index'))

        # Pobranie liczby sztuk
        try:
            sztuk = int(request.form.get('sztuk', 1))
            if sztuk < 1:
                raise ValueError
        except ValueError:
            flash('Liczba sztuk musi być liczbą całkowitą większą od 0.', 'error')
            return redirect(url_for('index'))

        # Zapis tymczasowego pliku
        with tempfile.NamedTemporaryFile(delete=False, suffix='.dxf') as tmp:
            file.save(tmp.name)
            tmp_path = tmp.name

        try:
            dlugosc = oblicz_dlugosc_sciezki(tmp_path)
            results = oblicz_czasy(dlugosc, sztuk)
            filename = os.path.basename(file.filename)
        except Exception as e:
            flash(f'Błąd przetwarzania pliku: {str(e)}', 'error')
        finally:
            os.unlink(tmp_path)

    return render_template('index.html', results=results, filename=filename)

if __name__ == '__main__':
    app.run(debug=True)