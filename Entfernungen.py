import pandas as pd
import numpy as np
import math
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import sqlite3
from sqlite3 import OperationalError

#file = str(os.path.realpath(__file__))
csv_file = "/Users/nedimdrekovic/Python/DB/simplemaps_worldcities/" + "world_cities.csv"
sql_file = "/Users/nedimdrekovic/Python/DB/simplemaps_worldcities/" + "world_cities.sql"
db_file = "/Users/nedimdrekovic/Python/DB/simplemaps_worldcities/" + "world_cities.db"
backgroundImage_file = "/Users/nedimdrekovic/Python/DB/simplemaps_worldcities/Erde.jpg"
backgroundColor = "DeepSkyBlue3"

# eigentlich eher dumm geloest, aber es reicht fuers erste
imSelbenLand = False # um zu checken ob country doppelt vorhanden

n = 10000    # Anzal an zu suchende Städte
digits_after_point = 2

def rad(grad):
    return (math.pi * grad)/180

def isValid(i):
    while True:
        city = input(str(i) + ".Stadt: ")
        if city in df["city"].tolist():
            return city
        print("Diese Stadt exisiert nicht. Bitte existierende Stadt eingeben: ")

def getCity(city):
    stadt = city.split(' (')
    command_string = "Select latitude, longitude From cities Where name = '" + stadt[0] + "'"
    if len(stadt) >= 2: # falls es die Stadt also doppelt gibt
        if len(stadt[1].split(', ')) == 1:  # dann unterscheiden sich die Staedte im Land, weil es dann ein Komma gibt
            land = stadt[1][:-1]
            command_string += " and country = '" + land + "'"
        else:                               # im gleichen Land, also Region vorhanden
            land = stadt[1].split(',')[0]
            region = stadt[1].split(', ')[1][:-1]
            command_string += " and country = '" + land + "'" + " and region = '" + region + "'"
    zeiger.execute(command_string)
    latitude, longitude = zeiger.fetchone()
    return latitude, longitude

def entfernung():
    city1 = combo1.get()
    city2 = combo2.get()
    latitude1, longitude1 = getCity(city1)
    latitude2, longitude2 = getCity(city2)

#    print("\n(Längengrad/Breitengrad) von", city1 + ("(" + df.loc[df.index[index1], "admin_name"] + ")" if imSelbenLand else "") + ": (" + str(longitude1) + u'\N{DEGREE SIGN}/' + str(latitude1) + u'\N{DEGREE SIGN}' + ")")
#    print("(Längengrad/Breitengrad) von", city2 + ("(" + df.loc[df.index[index2], "admin_name"] + ")" if imSelbenLand else "") + ": (" + str(longitude2) + u'\N{DEGREE SIGN}/' + str(latitude2) + u'\N{DEGREE SIGN}' + ")")

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

    l1_text = "(" + str(round(longitude1, digits_after_point)) + u'\N{DEGREE SIGN}/' + str(round(latitude1, digits_after_point)) + u'\N{DEGREE SIGN}' + ")"
    l2_text = "(" + str(round(longitude2, digits_after_point)) + u'\N{DEGREE SIGN}/' + str(round(latitude2, digits_after_point)) + u'\N{DEGREE SIGN}' + ")"

    tk.Label(tkFenster, text=l1_text, bg="red", fg="white").grid(row=2, column=3)
    tk.Label(tkFenster, text=l2_text, bg="blue", fg="orange").grid(row=3, column=3)
    tk.Label(tkFenster, text="(Längengrad/Breitengrad) von\n" + combo1.get() + " =", bg="red", fg="white").grid(row=2, column=2, pady=3)
    tk.Label(tkFenster, text="(Längengrad/Breitengrad) von\n" + combo2.get() + " =", bg="blue", fg="orange").grid(row=3, column=2, pady=3)
    tk.Label(tkFenster, text="Entfernung zwischen \"" + combo1.get() + "\"\nund \"" + combo2.get() + "\" = ", bg="yellow", fg="dark green").grid(row=4, column=2, padx=10, pady=10)

    resultText = str(round(distance, digits_after_point)).replace(".", ",") + " km\n(" + str(round(distance/1.60934, digits_after_point)) + " miles)"
    result = tk.Label(tkFenster, text=resultText, bg="yellow", fg="dark green").grid(row=4, column=3)

    print("Entfernung zwischen",city1,"und",city2,":",str(round(distance, digits_after_point)),"km (= " + str(round(distance/1.60934, digits_after_point)) + " miles)")

if __name__ == '__main__':
    connection = sqlite3.connect(db_file, timeout=10)
    zeiger = connection.cursor()

    sql_as_string = open(sql_file, 'r').read()
    cmds = sql_as_string.split(';')[:n]     # suchen nur die ersten 1000 Werte
    zeiger.execute("DROP TABLE IF EXISTS `cities`;")

    for index in range(len(cmds)):
        try:
            zeiger.execute(cmds[index])
        except OperationalError:
            print("Fehler: " + cmds[index])

    zeiger.execute("Select name, country, region From cities Where name != '';")
    cities = sorted(zeiger.fetchall())[:n]

    cities_array = []
    staedte = [city[0] for city in cities]
    for index, city in enumerate(cities):
        if staedte.count(city[0]) >= 2: # bedeutet dass 2 Mal die selbe Stadt in der Liste ist und man nun das Land ueberprueft
            if ((cities[index][0] == cities[index+1][0]) & (cities[index][1] == cities[index+1][1])) | ((cities[index][0] == cities[index-1][0]) & (cities[index][1] == cities[index-1][1])): # Stadt und Land gleich
                cities_array.append(cities[index][0] + " (" + cities[index][1] + ", " + cities[index][2] + ")")
            else:   # Städte sind gleich, Länder aber nicht
                cities_array.append(cities[index][0] + " (" + cities[index][1] + ")")
        else:                   # wenn Stadt nur einmal vorhanden
            cities_array.append(cities[index][0])

    # Ein Fenster erstellen
    tkFenster = tk.Tk(className='AutocompleteCombobox')

    # Den Fenstertitle erstellen
    tkFenster.title("Entfernung zweier Städte (Luftlinie)")
    tkFenster.geometry("1000x225")
    tkFenster.configure(background=backgroundColor)

#    combo1_cities = df["city"].tolist()
#    combo1_cities = [city if city not in (combo1_cities[:index] + combo1_cities[index+1:]) else (city + " (" + str(df.loc[index, "country"]) + ", " + str(df.loc[index, "admin_name"]) + ")") if (len(df[(df["city"] == city) & (df["country"] == df.iloc[index]["country"])]) >= 2) else (city + " (" + str(df.loc[index, "country"]) + ")") for index, city in enumerate(combo1_cities)] # wenn bis auf city das gleiche element enthalten ist

    combo1 = ttk.Combobox(tkFenster, state="readonly", values=sorted(cities_array))
    combo2 = ttk.Combobox(tkFenster, state="readonly", values=sorted(cities_array))
    combo1.grid(column=0, row=1, padx=5)
    combo2.grid(column=1, row=1, padx=5)
    combo1.current(0)
    combo2.current(0)

    label1 = tk.Label(tkFenster, text="1.Stadt", bg="red", fg="white").grid(row=0, column=0, padx=3)
    label2 = tk.Label(tkFenster, text="2.Stadt", bg="blue", fg="orange").grid(row=0, column=1, padx=3)
    berechne = ttk.Button(tkFenster, text="Berechne die Entfernung", command=entfernung).grid(row=1, column=2, padx=3)
    quit = ttk.Button(tkFenster, text="Schließe die Anwendung", command=tkFenster.quit).grid(row=1, column=3, padx=3)


    # In der Ereignisschleife auf Eingabe des Benutzers warten.
    tkFenster.mainloop()

    connection.commit()
    connection.close()
