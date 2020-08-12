import pandas as pd
import numpy as np
import math
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

#file = str(os.path.realpath(__file__))
file = "/Users/nedimdrekovic/Python/DB/simplemaps_worldcities/" + "worldcities.csv"
backgroundFile = "/Users/nedimdrekovic/Python/DB/simplemaps_worldcities/Erde.jpg"
backgroundColor = "DeepSkyBlue3"

# eigentlich eher dumm geloest, aber es reicht fuers erste
doppeltesBorrow = False # um zu checken ob borrow doppelt vorhanden
#spezifischesBorrow = "" # um Namen des Borrows zu speichern statt ganz zum Schluss eintragen

digits_after_point = 4

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

    res = city.split(" (")

    if len(res) > 1:    # d.h. wenn Stadt mehrmals vorhanden, zB in versch. Ländern
        countrys = df[df["city"] == res[0]]["country"]
        # damit kein falsches Land eingeben wird, also nur das, was zur Auswahl steht
        while True:
            res2 = res[1].split(", ")
            res2[-1] = res2[-1][:-1]  # um ")" zu entfernen
            # falls 2 Städte mit dem gleichen Namen sogar im gleichen Land sind
            if len(res2) > 1:
                doppeltesBorrow = True
                return df[(df["country"] == res2[0]) & (df["city"] == res[0]) & (df["admin_name"] == res2[1])].index[0]
            # falls die beiden Städte in versch. Länder sind.
            return df[(df["country"] == res2[0]) & (df["city"] == res[0])].index[0]
    # falls es die Stadt nur einmal auf der Welt gibt
    return df[df["city"] == res[0]].index[0]


def entfernung():
    city1 = combo1.get()
    city2 = combo2.get()

    index1 = getCity(city1)
    latitude1 = df.loc[index1, "lat"]
    longitude1 = df.loc[index1, "lng"]
    index2 = getCity(city2)
    latitude2 = df.loc[index2, "lat"]
    longitude2 = df.loc[index2, "lng"]

#    print("\n(Längengrad/Breitengrad) von", city1 + ("(" + df.loc[df.index[index1], "admin_name"] + ")" if doppeltesBorrow else "") + ": (" + str(longitude1) + u'\N{DEGREE SIGN}/' + str(latitude1) + u'\N{DEGREE SIGN}' + ")")
#    print("(Längengrad/Breitengrad) von", city2 + ("(" + df.loc[df.index[index2], "admin_name"] + ")" if doppeltesBorrow else "") + ": (" + str(longitude2) + u'\N{DEGREE SIGN}/' + str(latitude2) + u'\N{DEGREE SIGN}' + ")")
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

    l1_text = ("(" + df.loc[df.index[index1], "admin_name"] + ")" if doppeltesBorrow else "") + "(" + str(round(longitude1, digits_after_point)) + u'\N{DEGREE SIGN}/' + str(round(latitude1, digits_after_point)) + u'\N{DEGREE SIGN}' + ")"
    l2_text = ("(" + df.loc[df.index[index2], "admin_name"] + ")" if doppeltesBorrow else "") + "(" + str(round(longitude2, digits_after_point)) + u'\N{DEGREE SIGN}/' + str(round(latitude2, digits_after_point)) + u'\N{DEGREE SIGN}' + ")"

    l1 = tk.Label(tkFenster, text=l1_text).grid(row=2, column=3)
    l2 = tk.Label(tkFenster, text=l2_text).grid(row=3, column=3)

    lb1 = tk.Label(tkFenster, text="(Längengrad/Breitengrad) von " + combo1.get() + " =", bg="blue", fg="orange").grid(row=2, column=2, pady=3)
    lb2 = tk.Label(tkFenster, text="(Längengrad/Breitengrad) von " + combo2.get() + " =", bg="blue", fg="orange").grid(row=3, column=2, pady=3)
    entf = tk.Label(tkFenster, text="Entfernung zwischen \"" + combo1.get() + "\" und \"" + combo1.get() + "\" = ", bg="yellow", fg="dark green").grid(row=4, column=2, padx=10, pady=10)

    resultText = str(round(distance, digits_after_point)).replace(".", ",") + " km"
    result = tk.Label(tkFenster, text=resultText, bg="red", fg="white").grid(row=4, column=3)

    print("Entfernung zwischen",city1,"und",city2,":",distance,"\n")

if __name__ == '__main__':
    df = pd.read_csv(file)

    # Ein Fenster erstellen
    tkFenster = tk.Tk()
    # Den Fenstertitle erstellen
    tkFenster.title("Entfernung zweier Städte (Luftlinie)")
    tkFenster.geometry("900x200")
    tkFenster.configure(background=backgroundColor)

#    single_cities = [city for city in df["city"] if df["city"].tolist().count(city) == 1]
#    double_cities = sorted(list(set(df["city"].tolist()) - set(single_cities)))
    # und dann zusammenfügen zum Schluss

    combo1_cities = df["city"].tolist()
    combo1_cities = [city if city not in (combo1_cities[:index] + combo1_cities[index+1:]) else (city + " (" + str(df.loc[index, "country"]) + ", " + str(df.loc[index, "admin_name"]) + ")") if (len(df[(df["city"] == city) & (df["country"] == df.iloc[index]["country"])]) >= 2) else (city + " (" + str(df.loc[index, "country"]) + ")") for index, city in enumerate(combo1_cities)] # wenn bis auf city das gleiche element enthalten ist

#    combo1_cities = [city for city in df["city"]]
#    combo1_cities = [city if city in (combo1_cities[:index] + combo1_cities[index+1:]) else city for index, city in enumerate(combo1_cities)] # wenn bis auf city das gleiche element enthalten ist
#    +" ("+df.iloc[index]["country"]+")"
#    combo1_cities = [(city + " (" + str(df.loc[index, "admin_name"]) + ")") if len(df[df["city"] == city]) > 1 else city for index, city in enumerate(combo1_cities)]

    combo1 = ttk.Combobox(tkFenster, state="readonly", values=combo1_cities)
    combo2 = ttk.Combobox(tkFenster, state="readonly", values=combo1_cities)
    combo1.grid(column=0, row=1, padx=5)
    combo2.grid(column=1, row=1, padx=5)
    combo1.current(1)
    combo2.current(1)

    label1 = tk.Label(tkFenster, text="1.Stadt", bg="red", fg="white").grid(row=0, column=0, padx=3)
    label2 = tk.Label(tkFenster, text="2.Stadt", bg="green", fg="black").grid(row=0, column=1, padx=3)
#    label1.config(width=20)
#    label2.config(width=20)

    berechne = ttk.Button(tkFenster, text="Berechne die Entfernung der beiden Städte", command=entfernung).grid(row=1, column=2)

    # In der Ereignisschleife auf Eingabe des Benutzers warten.
    tkFenster.mainloop()
#
""" for index, city in enumerate(double_cities):
        if combo1_cities.count(city) == 1:  # Stadt existiert nur einmal
            res.append(city)
        else:
            if city in df[(df["city"] == city) & (df["country"] == df.iloc[index]["country"])]:
                res.append(city + " (" + str(df.loc[index, "country"]) + ")")
            else:
                res.append(city + " (" + str(df.loc[index, "country"]) + ", " + str(df.loc[index, "admin_name"]) + ")")
"""
