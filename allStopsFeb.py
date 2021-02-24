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

with open(filename2, 'r') as csvfile:
    csvreader2 = csv.reader(csvfile)
    c2=next(csvreader2)

    for m in  csvreader2:
            r2.append(m)

with open(filename3, 'r') as csvfile:
    csvreader3 = csv.reader(csvfile)
    c3=next(csvreader3)

    for n in  csvreader3:
            r3.append(n)

print(r2)
print(c2)
print("==========")
print(r3)
print(c3)


m = folium.Map(location=[45.4215, -75.6972], zoom_start=13)
for k in r1:
#    if (k[1] == "11"):
#        #print("Here")
#        for l in r1:
#            if(k[3] == l[0]):
                folium.Marker(location=[k[4], k[5]], tooltip=[k[2], k[1]],
                              icon=folium.Icon(color='blue', icon='bus', prefix='fa')).add_to(m)

for a in r2:
#    if(a[2] == "11"):
        for b in r3:
            if(a[0] == b[0]):
                if(b[1] < "2"):
                    print("Hello")
                    folium.Marker(location=[a[3], a[4]], tooltip=[a[1], 'Cancellation:', b[1]],
                                  icon=folium.Icon(color='purple', icon='bus', prefix='fa')).add_to(m)
                elif(b[1] >= "2" and b[1] < "4"):
                    print("Hello 1")
                    folium.Marker(location=[a[3], a[4]], tooltip=[a[1],b[1], 'Cancellations'],
                                  icon=folium.Icon(color='orange', icon='bus', prefix='fa')).add_to(m)
                elif(b[1] >= "4"):
                    print("Hello 2")
                    folium.Marker(location=[a[3], a[4]], tooltip=[a[1], b[1]],
                                  icon=folium.Icon(color='red', icon='bus', prefix='fa')).add_to(m)

m.save('allStopsMapFeb.html')