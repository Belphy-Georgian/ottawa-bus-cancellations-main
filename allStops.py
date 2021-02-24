import folium
import json
import csv
import os

filename = 'data/route_stops.csv'

filename1 = 'stops.csv'

filename2 = 'cancelFeb.csv'

filename3 = 'xFeb.csv'
r3 = []
c3 = []
r2 = []
c2 = []
r1 = []
c1 = []
r =[]
c = []

with open(filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    c=next(csvreader)

    for i in  csvreader:
            r.append(i)

with open(filename1, 'r') as csvfile:
    csvreader1 = csv.reader(csvfile)
    c1=next(csvreader1)

    for j in  csvreader1:
            r1.append(j)
