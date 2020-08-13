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
file = "/Users/nedimdrekovic/Python/DB/simplemaps_worldcities/" + "worldcities.csv"
sqlFile = "/Users/nedimdrekovic/Python/DB/simplemaps_worldcities/" + "worlddb.sql"
backgroundFile = "/Users/nedimdrekovic/Python/DB/simplemaps_worldcities/Erde.jpg"
backgroundColor = "DeepSkyBlue3"

# eigentlich eher dumm geloest, aber es reicht fuers erste
imSelbenLand = False # um zu checken ob borrow doppelt vorhanden

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
    global imSelbenLand
    imSelbenLand = False

    cmd = zeiger.execute("Select latitude, longitude From cities Where name = '" + city.split(' (')[0] + "'")    # um die Stadt zu erkennen
    res = [(lat, long) for (lat, long) in zeiger.fetchall()]
    print("Len:", res)

    if len(res) > 1:    # d.h. wenn Stadt mehrmals vorhanden, zB in versch. Ländern
        print("Lat:",str(res[0][0]))
        print("Long:",str(res[0][1]))
        for i in range(len(res)):
            cmds = zeiger.execute("Select latitude, longitude from cities Where name = '" + city.split(' (')[0] + "' and country = '" + city.split(' (')[1][:-1] + "' and latitude = " + str(res[i][0]) + " and longitude = " + str(res[i][1]))
            c = cmds.fetchone()
            print("c:",c)
            if c != None:
                return c[0], c[1]
        return 0, 0
        """
        # damit kein falsches Land eingeben wird, also nur das, was zur Auswahl steht
        while True:
            res2 = res[1].split(", ")
            res2[-1] = res2[-1][:-1]  # um ")" zu entfernen
            # falls 2 Städte mit dem gleichen Namen sogar im gleichen Land sind
            if len(res2) > 1:
                imSelbenLand = True
                return df[(df["country"] == res2[0]) & (df["city"] == res[0]) & (df["admin_name"] == res2[1])].index[0]
            # falls die beiden Städte in versch. Länder sind.
            return df[(df["country"] == res2[0]) & (df["city"] == res[0])].index[0]
        """
    # falls es die Stadt nur einmal auf der Welt gibt

    #cmd = zeiger.execute("Select latitude, longitude From cities Where name = '" + city + "'")
    #res = zeiger.fetchone()
    return res[0][0], res[0][1]     # dummy


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

    l1_text = ("(" + df.loc[df.index[index1], "admin_name"] + ")" if imSelbenLand else "") + "(" + str(round(longitude1, digits_after_point)) + u'\N{DEGREE SIGN}/' + str(round(latitude1, digits_after_point)) + u'\N{DEGREE SIGN}' + ")"
    l2_text = ("(" + df.loc[df.index[index2], "admin_name"] + ")" if imSelbenLand else "") + "(" + str(round(longitude2, digits_after_point)) + u'\N{DEGREE SIGN}/' + str(round(latitude2, digits_after_point)) + u'\N{DEGREE SIGN}' + ")"

    tk.Label(tkFenster, text=l1_text, bg="red", fg="white").grid(row=2, column=3)
    tk.Label(tkFenster, text=l2_text, bg="blue", fg="orange").grid(row=3, column=3)
    tk.Label(tkFenster, text="(Längengrad/Breitengrad) von\n" + combo1.get() + " =", bg="red", fg="white").grid(row=2, column=2, pady=3)
    tk.Label(tkFenster, text="(Längengrad/Breitengrad) von\n" + combo2.get() + " =", bg="blue", fg="orange").grid(row=3, column=2, pady=3)
    tk.Label(tkFenster, text="Entfernung zwischen \"" + combo1.get() + "\"\nund \"" + combo2.get() + "\" = ", bg="yellow", fg="dark green").grid(row=4, column=2, padx=10, pady=10)

    resultText = str(round(distance, digits_after_point)).replace(".", ",") + " km\n(" + str(round(distance*1.60934, digits_after_point)) + " miles)"
    result = tk.Label(tkFenster, text=resultText, bg="yellow", fg="dark green").grid(row=4, column=3)

    print("Entfernung zwischen",city1,"und",city2,":",distance,"\n")

if __name__ == '__main__':
    df = pd.read_csv(file)

    connection = sqlite3.connect("/Users/nedimdrekovic/Python/DB/simplemaps_worldcities/worlddb.db", timeout=10)
    zeiger = connection.cursor()

    sql_file = open("/Users/nedimdrekovic/Python/DB/simplemaps_worldcities/Saving.sql", 'r')
    sql_as_string = str(sql_file.read())
    cmds = sql_as_string.split(';')
    #print(cmds)
    zeiger.execute("DROP TABLE IF EXISTS `cities`;")

    for index, line in enumerate(cmds):
        if index == 1e4:
            break
        try:
            zeiger.execute(line)
        except OperationalError:
            print("Fehler: " + line)

    cmd = zeiger.execute("Select name, country, region From cities;")
    cities = zeiger.fetchall()
    cities = sorted(cities)

    cities_array = []
    for index, city in enumerate(cities):
        if index == len(cities)-1:
            break
        if city[0] == ''.strip():   # city[0] ist hier immer der Name
            pass
            #cities_array.append(city[0].replace("{", "").replace("}", ""))
        elif (cities[index][0] == cities[index+1][0]) | (cities[index][0] == cities[index-1][0]): # bedeutet dass 2 Mal die selbe Stadt in der Liste ist und man nun das Land ueberprueft
            cities_array.append(cities[index][0] + " (" + cities[index][1] + ")")
        else:   # wenn Stadt nur einmal vorhanden
            cities_array.append(cities[index][0])

    #cities_array = [city[0].replace("{", "").replace("}", "") for city in cities if city[0] != '']
    for c in cities_array:
        print("C:",c)

    # Ein Fenster erstellen
    tkFenster = tk.Tk()
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
    combo1.current(1)
    combo2.current(1)

    label1 = tk.Label(tkFenster, text="1.Stadt", bg="red", fg="white").grid(row=0, column=0, padx=3)
    label2 = tk.Label(tkFenster, text="2.Stadt", bg="blue", fg="orange").grid(row=0, column=1, padx=3)
    berechne = ttk.Button(tkFenster, text="Berechne die Entfernung der beiden Städte", command=entfernung).grid(row=1, column=2)

    # In der Ereignisschleife auf Eingabe des Benutzers warten.
    tkFenster.mainloop()

    connection.commit()
    connection.close()
