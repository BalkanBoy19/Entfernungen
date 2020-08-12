import pandas as pd
import numpy as np
import math
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

file = str(os.path.realpath(__file__))
file = "/Users/nedimdrekovic/Python/DB/simplemaps_worldcities/Entfernungen.py"
backgroundFile = "/Users/nedimdrekovic/Python/DB/simplemaps_worldcities/Erde.jpg"

# eigentlich eher dumm geloest, aber es reicht fuers erste
doppeltesBorrow = False # um zu checken ob borrow doppelt vorhanden
#spezifischesBorrow = "" # um Namen des Borrows zu speichern statt ganz zum Schluss eintragen

def rad(grad):
    return (math.pi * grad)/180

def isValid(i):
    while True:
        city = input(str(i) + ".Stadt: ")
        if city in df["city"].tolist():
            return city
        print("Diese Stadt exisiert nicht. Bitte existierende Stadt eingeben: ")

def getCity(city):
    global doppeltesBorrow
    doppeltesBorrow = False

    if len(df[df["city"] == city]) > 1:    # d.h. wenn Stadt mehrmals vorhanden, zB in versch. Ländern
        countrys = df[df["city"] == city]["country"]
        res = "/".join(countrys)
        # damit kein falsches Land eingeben wird, also nur das, was zur Auswahl steht
        while True:
            country = input("Die Stadt " + city + " gibt es mehrmals auf der Welt. Wähle eines der folgendne Länder aus (" + res + "): ")
            # falls 2 Städte mit dem gleichen Namen sogar im gleichen Land sind
            if len(df[(df["country"] == country) & (df["city"] == city)]) > 1:
                doppeltesBorrow = True
                borrows = df[(df["country"] == country) & (df["city"] == city)]["admin_name"]
                res = "/".join(borrows)
                while True:
                    borrow = input("Die Stadt " + city + " gibt es mehrmals in " + country + ". Wähle den Bezirk aus (" + res + "): ")
                    if borrow in res.split('/'):
                        return df[(df["country"] == country) & (df["city"] == city) & (df["admin_name"] == borrow)].index[0]
            # damit auch wirklich eines der Länder ausgewaehlt wird
            if country in res.split('/'):
                return df[(df["country"] == country) & (df["city"] == city)].index[0]
    # falls es die Stadt nur einmal auf der Welt gibt
    return df[df["city"] == city].index[0]


def entfernung():
    city1 = combo1.get().split('(')[0].strip()
    city2 = combo2.get().split('(')[0].strip()

    index1 = getCity(city1)
    latitude1 = df.loc[index1, "lat"]
    longitude1 = df.loc[index1, "lng"]

    index2 = getCity(city2)
    latitude2 = df.loc[index2, "lat"]
    longitude2 = df.loc[index2, "lng"]

    # evtl. noch Borrow in Klammern hinter Stadt einfuegen
    print("\n(Längengrad/Breitengrad) von", city1 + ("(" + df.loc[df.index[index1], "admin_name"] + ")" if doppeltesBorrow else "") + ": (" + str(longitude1) + u'\N{DEGREE SIGN}/' + str(latitude1) + u'\N{DEGREE SIGN}' + ")")
    print("(Längengrad/Breitengrad) von", city2 + ("(" + df.loc[df.index[index2], "admin_name"] + ")" if doppeltesBorrow else "") + ": (" + str(longitude2) + u'\N{DEGREE SIGN}/' + str(latitude2) + u'\N{DEGREE SIGN}' + ")")
    durchmesser = 12756.27
    radius = durchmesser / 2

    lat1 = rad(latitude1)
    lon1 = rad(longitude1)
    lat2 = rad(latitude2)
    lon2 = rad(longitude2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * math.atan2(np.sqrt(a), np.sqrt(1 - a))
    distance = radius * c

    l1_text = "(Längengrad/Breitengrad) von " + city1 + ("(" + df.loc[df.index[index1], "admin_name"] + ")" if doppeltesBorrow else "") + ": (" + str(longitude1) + u'\N{DEGREE SIGN}/' + str(latitude1) + u'\N{DEGREE SIGN}' + ")"
    l2_text = "(Längengrad/Breitengrad) von " + city2 + ("(" + df.loc[df.index[index2], "admin_name"] + ")" if doppeltesBorrow else "") + ": (" + str(longitude2) + u'\N{DEGREE SIGN}/' + str(latitude2) + u'\N{DEGREE SIGN}' + ")"


    l1 = tk.Label(tkFenster, text=l1_text).grid(row=2, column=0)
    l2 = tk.Label(tkFenster, text=l2_text).grid(row=2, column=1)

    resulttext = "Entfernung zwischen " + city1 + " und " + city2 + ": " + str(distance) + " km"
    result = tk.Label(tkFenster, text=resulttext).grid(row=2, column=2, padx=10, pady=10)

    print("Entfernung zwischen",city1,"und",city2,":",distance)
#    result.depositLabel['text'] = "Entfernung zwischen " + city1 + " und " + city2 + ": " + str(distance)

if __name__ == '__main__':
    df = pd.read_csv(file)
    #city1 = isValid(1)
    #city2 = isValid(2)
    #entfernung(city1, city2)

    # Ein Fenster erstellen
    tkFenster = tk.Tk()
    # Den Fenstertitle erstellen
    tkFenster.title("Entfernung zweier Städte (Luftlinie)")
    tkFenster.geometry("1000x300")
    tkFenster.configure(background='turquoise')

    label1 = tk.Label(tkFenster, text="1.Stadt", bg="red", fg="white").grid(row=0, column=0, padx=10, pady=10)
    label2 = tk.Label(tkFenster, text="2.Stadt", bg="green", fg="black").grid(row=0, column=1, padx=10, pady=10)

    combo1_cities = [city for city in df["city"]]
    combo1_cities = [city if city not in (combo1_cities[:index] + combo1_cities[index+1:]) else (city + " (" + str(df.loc[index, "country"]) + ", " + str(df.loc[index, "admin_name"]) + ")") if (len(df[(df["city"] == city) & (df["country"] == df.iloc[index]["country"])]) >= 2) else (city + " (" + str(df.loc[index, "country"]) + ")") for index, city in enumerate(combo1_cities)] # wenn bis auf city das gleiche element enthalten ist


    combo1 = ttk.Combobox(tkFenster, state="readonly", values=combo1_cities)
    combo2 = ttk.Combobox(tkFenster, state="readonly", values=df["city"].tolist())
    combo1.grid(column=0, row=1)
    combo2.grid(column=1, row=1)
    combo1.current(1)
    combo2.current(1)

    x = df["city"].tolist()
    print(x)

    berechne = ttk.Button(tkFenster, text="Berechne die Entfernung der beiden Städte", command=entfernung)
    berechne.grid(row=1, column=2)

    """ combo1_cities = [city for city in df["city"]]
        combo1_cities = [city if city in (combo1_cities[:index] + combo1_cities[index+1:]) else city for index, city in enumerate(combo1_cities)] # wenn bis auf city das gleiche element enthalten ist
        # +" ("+df.iloc[index]["country"]+")"
        combo1_cities = [(city + " (" + str(df.loc[index, "admin_name"]) + ")") if len(df[df["city"] == city]) > 1 else city for index, city in enumerate(combo1_cities)]

    """

    # In der Ereignisschleife auf Eingabe des Benutzers warten.
    tkFenster.mainloop()
#
