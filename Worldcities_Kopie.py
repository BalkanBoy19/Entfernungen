import pandas as pd
import numpy as np
import math

file = "/Users/nedimdrekovic/Python/DB/simplemaps_worldcities/worldcities.csv"

def rad(grad):
    return (math.pi * grad)/180

def index(city):
    if len(df[df["city"] == city]) > 1:    # d.h. wenn Stadt mehrmals vorhanden, zB in versch. Ländern
        countrys = df[df["city"] == city]["country"]
        res = "/".join(countrys)
        # damit kein falsches Land eingeben wird, also nur das, was zur Auswahl steht
        while True:
            country = input("Die Stadt " + city + " gibt es mehrmals auf der Welt. Wähle eines der folgendne Länder aus (" + res + "): ")
            # falls 2 Städte mit dem gleichen Namen sogar im gleichen Land sind
            if len(df[(df["country"] == country) & (df["city"] == city)]) > 1:
                borrows = df[(df["country"] == country) & (df["city"] == city)]["admin_name"]
                res = "/".join(borrows)
                while True:
                    borrow = input("Die Stadt " + city + " gibt es mehrmals in " + country + ". Wähle den Bezirk aus (" + res + "): ")
                    if borrow in res.split('/'):
                        return df[(df["country"] == country) & (df["city"] == city) & (df["admin_name"] == borrow)].index[0]
            # damit auch wirklich eines der Länder ausgewaehlt wird
            if country in res.split('/'):
                return df[(df["country"] == country) & (df["city"] == city)].index[0]
    # falls es city nur einmal gibt
    return df[df["city"] == city].index[0]


def entfernung(city1, city2):
    index1 = index(city1)
    latitude1 = df.loc[index1, "lat"]
    longitude1 = df.loc[index1, "lng"]
    print("(Längengrad/Breitengrad) von", city1, ": (" + str(longitude1) + u'\N{DEGREE SIGN}/' + str(latitude1) + u'\N{DEGREE SIGN}' + ")")

    index2 = index(city2)
    latitude2 = df.loc[index2, "lat"]
    longitude2 = df.loc[index2, "lng"]
    print("(Längengrad/Breitengrad) von", city2, ": (" + str(longitude2) + u'\N{DEGREE SIGN}/' + str(latitude2) + u'\N{DEGREE SIGN}' + ")")

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

    print("Entfernung zwischen",city1,"und",city2,":",distance)

def existing(i):
    while True:
        city = input(str(i) + ".Stadt: ")
        if city in df["city"].tolist():
            return city
        print("Diese Stadt exisiert nicht. Bitte existierende Stadt eingeben: ")

if __name__ == '__main__':
    df = pd.read_csv(file)
    city1 = existing(1)
    city2 = existing(2)
    entfernung(city1, city2)


#
