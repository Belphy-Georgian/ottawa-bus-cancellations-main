import folium

import json
import csv
import os

filename = 'data/route_stops.csv'

filename1 = 'stops.csv'

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

'''print(r)
print(c)
print(r1)
print(c1)'''

m = folium.Map(location=[45.4215, -75.6972], zoom_start=13)
for k in r:
    if (k[1] == "5" and k[2] == "0"):
        #print("HEre")
        for l in r1:
            if(k[3] == l[0]):
                folium.Marker(location=[l[4], l[5]], tooltip=[l[2], l[1]],
                              icon=folium.Icon(color='red', icon='bus', prefix='fa')).add_to(m)

m.save('templates//map.html')
