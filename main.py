
# BUS SCHEDULE

import pymongo
from pymongo import MongoClient
from pymongo.errors import CollectionInvalid
import folium
import json
import csv
import os
import routes
import database
import gpsapi
from flask import json
import pandas as pd
from folium.plugins import MarkerCluster # for clustering the markers
import datetime
import main_scrape
import time
import threading


#MongoDB

client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.jv3iz.mongodb.net/CitizenInformation?retryWrites=true&w=majority")
db=client['CitizenInformation']


filename = 'data//route_stops.csv'
filename1 = 'data//stops.csv'
filename2 = 'data//cancel.csv'
filename3 = 'data//x.csv'
filename4 = 'data//cancelFeb.csv'
filename5 = 'data//xFeb.csv'
filename6 = 'data//shapes.csv'
filename7 = 'data//trips.csv'
filename8 = 'data//routes.csv'
filename9 = 'csv//cancellations_raw.csv'
filename10 = 'csv//cancellations_stop_list.csv'

r8 = []
c8 = []
r7 = []
c7 = []
r6 = []
c6 = []
r5 = []
c5 = []
r4 = []
c4 = []
r3 = []
c3 = []
r2 = []
c2 = []
r1 = []
c1 = []
r =[]
c = []



rt_stop123 = db["Route_Stops"]
x = rt_stop123.find_one()
print("Data of Route_stop table :" + str(x))


stop123 = db["Stops"]
y = stop123.find_one()
print("Data of Stop table :" + str(y))

#list of all the data
# for x in col.find():
#     r1.append(x)


# BUS CANCELLATION

cancel123 = db["Cancel"]
x = cancel123.find_one()
print("Data of Cancel table :" + str(x))

x123 = db["X"]
y = x123.find_one()
print("Data of X table :" + str(y))



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

with open(filename6, 'r') as csvfile:
    csvreader4 = csv.reader(csvfile)
    c4=next(csvreader4)

    for n in  csvreader4:
            r4.append(n)

with open(filename7, 'r') as csvfile:
    csvreader5 = csv.reader(csvfile)
    c5=next(csvreader5)

    for n in  csvreader5:
            r5.append(n)

with open(filename8, 'r') as csvfile:
    csvreader6 = csv.reader(csvfile)
    c6=next(csvreader6)

    for n in  csvreader6:
            r6.append(n)

with open(filename9, 'r') as csvfile:
    csvreader7 = csv.reader(csvfile)
    c7=next(csvfile)
    df = pd.read_csv(filename9, header = 0)
    df = df.head(20)
    for n in csvreader7:
            r7.append(n)

with open(filename10, 'r') as csvfile:
    csvreader8 = csv.reader(csvfile)
    c8=next(csvreader8)

    for n in csvreader8:
            r8.append(n)


#January Bus Cancels

#with open(route_stops_fname, 'r') as csvfile:
#    print(f'alita with open route_stops_fname')
#    csvreader = csv.reader(csvfile)
#    c=next(csvreader)

#    for i in  csvreader:
#           r.append(i)

#with open(stops_fname, 'r') as csvfile:
#    print(f'alita with open stops_fname')
#    csvreader1 = csv.reader(csvfile)
#    c1=next(csvreader1)

#    for j in  csvreader1:
#            r1.append(j)

#with open(cancelFeb_fname, 'r') as csvfile:
#    print(f'alita with open cancelFeb')
#    csvreader2 = csv.reader(csvfile)
#    c2=next(csvreader2)

#    for m in  csvreader2:
#            r2.append(m)

#with open(xFeb_fname, 'r') as csvfile:
#    print(f'alita with open xFeb')
#    csvreader3 = csv.reader(csvfile)
#    c3=next(csvreader3)

#    for n in  csvreader3:
#            r3.append(n)




#MAIN

database.onStart()

from flask import Flask, request, g, redirect, url_for, abort, render_template
app = Flask(__name__)

# Global Vars
# I'll do the work here and we can later move it out to its on .py

class STATUSLEVELS():
    DANGER = 2,
    WARNING = 1,
    OK = 0

class transitElement():    
    def __init__(self, imp_id, status, canCount, warnCount):
        self.eId = imp_id
        self.eStatus = status
        self.eCanCount = canCount
        self.eWarnCount = warnCount

class fakeRouteElement(transitElement):    
    def __init__(self, imp_id, status, canCount, warnCount):
        self.eId = imp_id
        self.eStatus = status
        self.eCanCount = canCount
        self.eWarnCount = warnCount


class fakeStopElement():
    def __init__(self, imp_id, status, canCount, warnCount):
        self.eId = imp_id
        self.eStatus = status
        self.eCanCount = canCount
        self.eWarnCount = warnCount


def populateRoutesForStopDatabase(stopID, date):
    #database call
    database.findRoutesForStop(stopID, "17:00:00")
    
    fakeRouteList=[
        fakeRouteElement(95,1,0,0),
        fakeRouteElement(75,1,0,0),
        fakeRouteElement(85,1,0,0),
        fakeRouteElement(88,1,0,0),
        fakeRouteElement(4,1,1,2)
    ]

    return fakeRouteList


fakeRouteList=[
    fakeRouteElement(95,1,0,0),
    fakeRouteElement(75,1,0,0),
    fakeRouteElement(85,1,0,0),
    fakeRouteElement(88,1,0,0),
    fakeRouteElement(4,1,1,2)
]

fakeRouteList2=[
    { "eId": 5, "eStatus": 1,"eCanCount": 1, "eWarnCount": 2}
]

def webScrapping():
    print('Retrieving cancellation tweets from OCTranspo')
    main_scrape.download_tweets()
    main_scrape.export_csv()

def get_data():
    webScrapping()
    while True:
        time.sleep(900)
        get_data()
# Routes
@app.route('/<routeID>/<stopID>')
def routesAndStops(routeID, stopID):

    #Route and stop valid parsing needs to be done here
    #add "isValid" to the first if

    if routeID is not None or stopID is not None: 
        if routeID.lower() == "all":

            #Here we will need to do a quick call to get the cached health of all the routes
            #Filter out the routes we don't need and update a list of
            # RouteID's, statusLevel, HasCancellations, HasWarnings
            # WE can update the JS on the page to hardcode the images used for "bus route types"
            # So we don't need to pass extra data per cycle

            #API check also needed here as well as cancellation check

            #Switch over to class return type

            return render_template("stops.html",
            title="Occasional Transport: Ottawa Bus Edition", 
            mastHead="Stops Page",
            selectedRouteID="all",
            selectedstopID=stopID,
            statusLevel=STATUSLEVELS.OK, 
            locationText="Located between at the intersection of Two and Fern",
            locationDescrip="Lovely Stop. Great Atmosphere",
            mastDescrip="Display all Stops For " + stopID + " stop ID",
            fakeRouteListSend=fakeRouteList)
        else:
            return render_template("stops.html",
            title="Occasional Transport: Ottawa Bus Edition", 
            mastHead="Stops Page",
            selectedRouteID=routeID,
            selectedstopID=stopID,
            statusLevel=STATUSLEVELS.OK,
            locationText="Located between at the intersection of Two and Fern",
            locationDescrip="Lovely Stop. Great Atmosphere",
            mastDescrip="Display "+ routeID +" route information for " + stopID + " stop ID",
            fakeRouteListSend=fakeRouteList)
    else:
        index()

@app.route('/<routeID>/<stopID>/json')
def routesAndStopsJson(routeID, stopID):

    def make_summary():
        return fakeRouteList2

    if routeID is not None or stopID is not None: 
        if routeID.lower() == "all":
            if routeID is not None:
                data = make_summary()
                response = app.response_class(
                    response=json.dumps(data),
                    status=200,
                    mimetype='application/json'
                )
                return response

        else:
            if routeID is not None:
                data = make_summary()
                response = app.response_class(
                    response=json.dumps(data),
                    status=200,
                    mimetype='application/json'
                )
                return response

    else:
        index()


@app.route('/<routeID>')
def busRoutes(routeID):

    #Route valid parsing needs to be done here
    #add "isValid" to the first if

    if routeID is not None:
        return render_template("routes.html",
        title="Occasional Transport: Ottawa Bus Edition", 
        mastHead="Routes Page",
        selectedRouteID=routeID,
        statusLevel=STATUSLEVELS.OK, 
        mastDescrip="Display "+ routeID +" route information ")
    else:
        index()

@app.route('/<routeID>/json')
def busRoutesJson(routeID):

    #Route valid parsing needs to be done here
    #add "isValid" to the first if

    def make_summary():
        return fakeRouteList2

    if routeID is not None:
        data = make_summary()
        response = app.response_class(
            response=json.dumps(data),
            status=200,
            mimetype='application/json'
        )
        return response

    else:
        index()


@app.route('/', methods=['GET', 'POST'])

def usuarios():
    print(df)
    # resultado de SELECT id, nombre FROM usuarios ORDER BY nombre
    res = [{'id': 1, 'nombre': '1'}, {'id': 2, 'nombre': '2'}, {'id': 3, 'nombre': '5'}, {'id': 4, 'nombre': '6'}, {'id': 5, 'nombre': '7'}, {'id': 6, 'nombre': '9'}, {'id': 7, 'nombre': '10'}, {'id': 8, 'nombre': '11'}, {'id': 9, 'nombre': '12'}, {'id': 10, 'nombre': '14'}, {'id': 11, 'nombre': '15'}, {'id': 12, 'nombre': '16'}, {'id': 13, 'nombre': '17'}, {'id': 14, 'nombre': '18'}, {'id': 15, 'nombre': '19'}, {'id': 16, 'nombre': '20'}, {'id': 17, 'nombre': '21'}, {'id': 18, 'nombre': '23'}, {'id': 19, 'nombre': '24'}, {'id': 20, 'nombre': '25'}, {'id': 21, 'nombre': '26'}, {'id': 22, 'nombre': '27'}, {'id': 23, 'nombre': '28'}, {'id': 24, 'nombre': '30'}, {'id': 25, 'nombre': '31'}, {'id': 26, 'nombre': '32'}, {'id': 27, 'nombre': '33'}, {'id': 28, 'nombre': '34'}, {'id': 29, 'nombre': '35'}, {'id': 30, 'nombre': '37'}, {'id': 31, 'nombre': '38'}, {'id': 32, 'nombre': '39'}, {'id': 33, 'nombre': '40'}, {'id': 34, 'nombre': '42'}, {'id': 35, 'nombre': '44'}, {'id': 36, 'nombre': '45'}, {'id': 37, 'nombre': '46'}, {'id': 38, 'nombre': '47'}, {'id': 39, 'nombre': '48'}, {'id': 40, 'nombre': '49'}, {'id': 41, 'nombre': '50'}, {'id': 42, 'nombre': '51'}, {'id': 43, 'nombre': '53'}, {'id': 44, 'nombre': '54'}, {'id': 45, 'nombre': '55'}, {'id': 46, 'nombre': '56'}, {'id': 47, 'nombre': '57'}, {'id': 48, 'nombre': '58'}, {'id': 49, 'nombre': '61'}, {'id': 50, 'nombre': '62'}, {'id': 51, 'nombre': '63'}, {'id': 52, 'nombre': '64'}, {'id': 53, 'nombre': '66'}, {'id': 54, 'nombre': '73'}, {'id': 55, 'nombre': '74'}, {'id': 56, 'nombre': '75'}, {'id': 57, 'nombre': '80'}, {'id': 58, 'nombre': '81'}, {'id': 59, 'nombre': '82'}, {'id': 60, 'nombre': '83'}, {'id': 61, 'nombre': '84'}, {'id': 62, 'nombre': '85'}, {'id': 63, 'nombre': '86'}, {'id': 64, 'nombre': '87'}, {'id': 65, 'nombre': '88'}, {'id': 66, 'nombre': '89'}, {'id': 67, 'nombre': '90'}, {'id': 68, 'nombre': '92'}, {'id': 69, 'nombre': '93'}, {'id': 70, 'nombre': '96'}, {'id': 71, 'nombre': '97'}, {'id': 72, 'nombre': '98'}, {'id': 73, 'nombre': '99'}, {'id': 74, 'nombre': '111'}, {'id': 75, 'nombre': '114'}, {'id': 76, 'nombre': '131'}, {'id': 77, 'nombre': '138'}, {'id': 78, 'nombre': '140'}, {'id': 79, 'nombre': '141'}, {'id': 80, 'nombre': '153'}, {'id': 81, 'nombre': '154'}, {'id': 82, 'nombre': '155'}, {'id': 83, 'nombre': '158'}, {'id': 84, 'nombre': '161'}, {'id': 85, 'nombre': '162'}, {'id': 86, 'nombre': '164'}, {'id': 87, 'nombre': '165'}, {'id': 88, 'nombre': '166'}, {'id': 89, 'nombre': '167'}, {'id': 90, 'nombre': '168'}, {'id': 91, 'nombre': '170'}, {'id': 92, 'nombre': '171'}, {'id': 93, 'nombre': '173'}, {'id': 94, 'nombre': '175'}, {'id': 95, 'nombre': '176'}, {'id': 96, 'nombre': '179'}, {'id': 97, 'nombre': '186'}, {'id': 98, 'nombre': '187'}, {'id': 99, 'nombre': '190'}, {'id': 100, 'nombre': '197'}, {'id': 101, 'nombre': '198'}, {'id': 102, 'nombre': '199'}, {'id': 103, 'nombre': '221'}, {'id': 104, 'nombre': '222'}, {'id': 105, 'nombre': '224'}, {'id': 106, 'nombre': '225'}, {'id': 107, 'nombre': '228'}, {'id': 108, 'nombre': '231'}, {'id': 109, 'nombre': '232'}, {'id': 110, 'nombre': '233'}, {'id': 111, 'nombre': '234'}, {'id': 112, 'nombre': '235'}, {'id': 113, 'nombre': '236'}, {'id': 114, 'nombre': '237'}, {'id': 115, 'nombre': '251'}, {'id': 116, 'nombre': '252'}, {'id': 117, 'nombre': '256'}, {'id': 118, 'nombre': '257'}, {'id': 119, 'nombre': '258'}, {'id': 120, 'nombre': '261'}, {'id': 121, 'nombre': '262'}, {'id': 122, 'nombre': '263'}, {'id': 123, 'nombre': '264'}, {'id': 124, 'nombre': '265'}, {'id': 125, 'nombre': '266'}, {'id': 126, 'nombre': '267'}, {'id': 127, 'nombre': '268'}, {'id': 128, 'nombre': '270'}, {'id': 129, 'nombre': '271'}, {'id': 130, 'nombre': '272'}, {'id': 131, 'nombre': '273'}, {'id': 132, 'nombre': '275'}, {'id': 133, 'nombre': '277'}, {'id': 134, 'nombre': '278'}, {'id': 135, 'nombre': '282'}, {'id': 136, 'nombre': '283'}, {'id': 137, 'nombre': '284'}, {'id': 138, 'nombre': '290'}, {'id': 139, 'nombre': '291'}, {'id': 140, 'nombre': '294'}, {'id': 141, 'nombre': '299'}, {'id': 142, 'nombre': '301'}, {'id': 143, 'nombre': '302'}, {'id': 144, 'nombre': '303'}, {'id': 145, 'nombre': '304'}, {'id': 146, 'nombre': '305'}, {'id': 147, 'nombre': '602'}, {'id': 148, 'nombre': '609'}, {'id': 149, 'nombre': '611'}, {'id': 150, 'nombre': '612'}, {'id': 151, 'nombre': '613'}, {'id': 152, 'nombre': '618'}, {'id': 153, 'nombre': '619'}, {'id': 154, 'nombre': '620'}, {'id': 155, 'nombre': '622'}, {'id': 156, 'nombre': '624'}, {'id': 157, 'nombre': '630'}, {'id': 158, 'nombre': '631'}, {'id': 159, 'nombre': '632'}, {'id': 160, 'nombre': '633'}, {'id': 161, 'nombre': '634'}, {'id': 162, 'nombre': '635'}, {'id': 163, 'nombre': '638'}, {'id': 164, 'nombre': '639'}, {'id': 165, 'nombre': '640'}, {'id': 166, 'nombre': '641'}, {'id': 167, 'nombre': '644'}, {'id': 168, 'nombre': '645'}, {'id': 169, 'nombre': '648'}, {'id': 170, 'nombre': '649'}, {'id': 171, 'nombre': '658'}, {'id': 172, 'nombre': '660'}, {'id': 173, 'nombre': '661'}, {'id': 174, 'nombre': '665'}, {'id': 175, 'nombre': '669'}, {'id': 176, 'nombre': '670'}, {'id': 177, 'nombre': '674'}, {'id': 178, 'nombre': '675'}, {'id': 179, 'nombre': '678'}, {'id': 180, 'nombre': '681'}, {'id': 181, 'nombre': '686'}, {'id': 182, 'nombre': '689'}, {'id': 183, 'nombre': '691'}, {'id': 184, 'nombre': '698'}]
    usuarios = [(di['id'], di['nombre']) for di in res]
    res1 = [{'id': 1, 'nombre': '2 Bayview'}, {'id': 2, 'nombre': '2 South Keys'}, {'id': 3, 'nombre': '5 Billings Bridge'}, {'id': 4, 'nombre': '6 Daly / Nicholas'}, {'id': 5, 'nombre': '6 Greenboro'}, {'id': 6, 'nombre': '6 Rideau'}, {'id': 7, 'nombre': '7 Brittany'}, {'id': 8, 'nombre': '7 Carleton'}, {'id': 9, 'nombre': '7 Parliament'}, {'id': 10, 'nombre': '7 Rideau'}, {'id': 11, 'nombre': '7 St. Laurent'}, {'id': 12, 'nombre': '7 St-Laurent'}, {'id': 13, 'nombre': '9 Rideau'}, {'id': 14, 'nombre': '10 Hurdman'}, {'id': 15, 'nombre': '10 Lyon'}, {'id': 16, 'nombre': '11 Lincoln Fields'}, {'id': 17, 'nombre': '11 Parliament/Parlement'}, {'id': 18, 'nombre': '12 Blair'}, {'id': 19, 'nombre': '12 Parliament'}, {'id': 20, 'nombre': '14 St. Laurent'}, {'id': 21, 'nombre': '14 Tunneys Pasture'}, {'id': 22, 'nombre': '15 Blair'}, {'id': 23, 'nombre': '15 Gatineau'}, {'id': 24, 'nombre': '16 Westboro'}, {'id': 25, 'nombre': '17 Gatineau'}, {'id': 26, 'nombre': '17 Terrasses'}, {'id': 27, 'nombre': '18 Parliament'}, {'id': 28, 'nombre': '18 St. Laurent'}, {'id': 29, 'nombre': '18 St-Laurent'}, {'id': 30, 'nombre': '19 Parliament'}, {'id': 31, 'nombre': '19 Parliament/Parlement'}, {'id': 32, 'nombre': '19 St. Laurent'}, {'id': 33, 'nombre': '19 Vanier'}, {'id': 34, 'nombre': '24 Beacon Hill'}, {'id': 35, 'nombre': '24 St. Laurent'}, {'id': 36, 'nombre': '24 St-Laurent'}, {'id': 37, 'nombre': '25 Blair'}, {'id': 38, 'nombre': '25 La CitÃ©'}, {'id': 39, 'nombre': '25 Millennium'}, {'id': 40, 'nombre': '26 Blair'}, {'id': 41, 'nombre': '26 Pineview'}, {'id': 42, 'nombre': '30 Blair'}, {'id': 43, 'nombre': '30 Millennium'}, {'id': 44, 'nombre': '33 Blair'}, {'id': 45, 'nombre': '33 Portobello'}, {'id': 46, 'nombre': '34 Blair'}, {'id': 47, 'nombre': '34 Renaud'}, {'id': 48, 'nombre': '35 Blair'}, {'id': 49, 'nombre': '35 Esprit'}, {'id': 50, 'nombre': '38 Blair'}, {'id': 51, 'nombre': '38 Jeane dâ€™Arc / Trim'}, {'id': 52, 'nombre': '38 Jeanne dArc / Trim'}, {'id': 53, 'nombre': '38 Trim'}, {'id': 54, 'nombre': '39 Blair'}, {'id': 55, 'nombre': '39 Millenium'}, {'id': 56, 'nombre': '39 Millennium'}, {'id': 57, 'nombre': '39 Trim'}, {'id': 58, 'nombre': '40 Greenboro'}, {'id': 59, 'nombre': '44 Billings Bridge'}, {'id': 60, 'nombre': '44 Hurdman'}, {'id': 61, 'nombre': '46 Billings Bridge'}, {'id': 62, 'nombre': '46 Hurdman'}, {'id': 63, 'nombre': '48 Elmvale'}, {'id': 64, 'nombre': '50 Lincoln Fields'}, {'id': 65, 'nombre': '51 Britannia'}, {'id': 66, 'nombre': '51 Brittania'}, {'id': 67, 'nombre': '53 Tunneys Pasture'}, {'id': 68, 'nombre': '55 Bayshore'}, {'id': 69, 'nombre': '55 Elmvale'}, {'id': 70, 'nombre': '56 King Edward'}, {'id': 71, 'nombre': '56 Tunneys Pasture'}, {'id': 72, 'nombre': '57 Bayshore'}, {'id': 73, 'nombre': '57 Tunneys Pasture'}, {'id': 74, 'nombre': '61 Stittsville'}, {'id': 75, 'nombre': '61 Terry Fox'}, {'id': 76, 'nombre': '63 Briarbrook via Innovation'}, {'id': 77, 'nombre': '63 Gatineau'}, {'id': 78, 'nombre': '63 Innovation'}, {'id': 79, 'nombre': '63 Legget'}, {'id': 80, 'nombre': '63 Tunneys Pasture'}, {'id': 81, 'nombre': '64 Morgans Grant via Innovation'}, {'id': 82, 'nombre': '64 Tunneys Pasture'}, {'id': 83, 'nombre': '66 Gatineau'}, {'id': 84, 'nombre': '66 Tunneyâ€™s Pasture'}, {'id': 85, 'nombre': '73 Tunneys Pasture'}, {'id': 86, 'nombre': '74 Riverview'}, {'id': 87, 'nombre': '74 Tunneys Pasture'}, {'id': 88, 'nombre': '75 Barrhaven Centre'}, {'id': 89, 'nombre': '75 Baseline'}, {'id': 90, 'nombre': '75 Gatineau'}, {'id': 91, 'nombre': '75 Tunneys Pasture'}, {'id': 92, 'nombre': '80 Tunneys Pasture'}, {'id': 93, 'nombre': '81 Clyde'}, {'id': 94, 'nombre': '81 Tunneys Pasture'}, {'id': 95, 'nombre': '83 Viewmount'}, {'id': 96, 'nombre': '84 Centrepointe'}, {'id': 97, 'nombre': '84 Tunneys Pasture'}, {'id': 98, 'nombre': '85 Bayshore'}, {'id': 99, 'nombre': '85 Gatineau'}, {'id': 100, 'nombre': '86 Baseline'}, {'id': 101, 'nombre': '86 Tunneys'}, {'id': 102, 'nombre': '87 Baseline'}, {'id': 103, 'nombre': '87 Tunneys Pasture'}, {'id': 104, 'nombre': '88 Hurdman'}, {'id': 105, 'nombre': '88 Terry Fox'}, {'id': 106, 'nombre': '90 Greenboro'}, {'id': 107, 'nombre': '90 Hurdman'}, {'id': 108, 'nombre': '92 Greenboro'}, {'id': 109, 'nombre': '92 Hurdman'}, {'id': 110, 'nombre': '93 Hurdman'}, {'id': 111, 'nombre': '93 Leitrim'}, {'id': 112, 'nombre': '96 Merivale'}, {'id': 113, 'nombre': '97 Airport'}, {'id': 114, 'nombre': '97 Hurdman'}, {'id': 115, 'nombre': '98 Hawthorne'}, {'id': 116, 'nombre': '98 Hurdman'}, {'id': 117, 'nombre': '111 Baseline'}, {'id': 118, 'nombre': '111 Carleton'}, {'id': 119, 'nombre': '141 Kaladar'}, {'id': 120, 'nombre': '225 Blair'}, {'id': 121, 'nombre': '225 Renaud'}, {'id': 122, 'nombre': '231 Blair'}, {'id': 123, 'nombre': '231 Meadowglen'}, {'id': 124, 'nombre': '232 Blair'}, {'id': 125, 'nombre': '234 Tenth Line'}, {'id': 126, 'nombre': '235 Gardenway'}, {'id': 127, 'nombre': '236 Blair'}, {'id': 128, 'nombre': '236 Esprit'}, {'id': 129, 'nombre': '237 Blair'}, {'id': 130, 'nombre': '251 Bells Corners'}, {'id': 131, 'nombre': '252 Fernbank'}, {'id': 132, 'nombre': '256 Tunneys Pasture'}, {'id': 133, 'nombre': '257 Bridlewood'}, {'id': 134, 'nombre': '257 Tunneys Pasture'}, {'id': 135, 'nombre': '262 Tunneys Pasture'}, {'id': 136, 'nombre': '262 West Ridge'}, {'id': 137, 'nombre': '266 Tunneys Pasture'}, {'id': 138, 'nombre': '267 Tunneys Pasture'}, {'id': 139, 'nombre': '270 Cedarview'}, {'id': 140, 'nombre': '270 Tunneys Pasture'}, {'id': 141, 'nombre': '271 Stoneway'}, {'id': 142, 'nombre': '272 Tunneys Pasture'}, {'id': 143, 'nombre': '273 Tunneys Pasture'}, {'id': 144, 'nombre': '277 Tunneys Pasture'}, {'id': 145, 'nombre': '278 Riverside South'}, {'id': 146, 'nombre': '278 Tunneys Pasture'}, {'id': 147, 'nombre': '284 Tunneys Pasture'}, {'id': 148, 'nombre': '291 Hurdman'}, {'id': 149, 'nombre': '294 Findlay Creek'}]
    usuarios1 = [(di['id'], di['nombre']) for di in res1]
    if request.method == 'POST':
        if request.form['submit_button'] == 'Do Something':
            bus = request.form['usuario']
            print(bus)
            scheduleroute(bus)
        elif request.form['submit_button'] == 'Do Something Else':
            bus1 = request.form['usuario1']
            cancel(bus1)
            return render_template("index.html",
                                   title="Occasional Transport: Ottawa Bus Edition",
                                   mastHead="Where's my @#$@ Bus?",
                                   statusLevel=STATUSLEVELS.OK,
                                   mastDescrip="Who knows. We do. Move along.",
                                   usuarios=usuarios,
                                   usuarios1=usuarios1,
                                   data=df)


    #if request.method == 'POST1':
    #    bus1 = request.form['usuario1']
    #    cancel(bus1)
    return render_template("index.html",
                           title="Occasional Transport: Ottawa Bus Edition",
                           mastHead="Where's my @#$@ Bus?",
                           statusLevel=STATUSLEVELS.OK,
                           mastDescrip="Who knows. We do. Move along.",
                           usuarios=usuarios,
                           usuarios1=usuarios1,
                           data=df)


def scheduleroute(route_id):
    print(f'alita route id ---------{route_id}---------')
    #CartoDB positron
    #Stamen Terrain
    m = folium.Map(width=900,height=650,location=[45.4215, -75.6972], left='17.5%', top='10%', tiles='CartoDB positron', zoom_start=13)
    marker_cluster = MarkerCluster().add_to(m)  # create marker clusters
    coordinates = []
    coordinates1 = []


    for k in r6:
        # k[1] has route_short
        if (k[1] == route_id):
            #r1 has all the stop details
            for l in r5:
                #if stop_id is same then plot
                if (k[0] == l[0] and l[4] == "1"):
                    print(k[0])
                    destination1 = l[3]
                    for j in r4:
                        if (l[6] == j[0]):
                            coordinates.append([float(j[1]), float(j[2])])
                if (k[0] == l[0] and l[4] == "1"):
                    break

    for k in r6:
        # k[1] has route_id
        if (k[1] == route_id):
            #r1 has all the stop details
            for l in r5:
                #if stop_id is same then plot
                if (k[0] == l[0] and l[4] == "0"):
                    print(k[0])
                    destination0= l[3]
                    for j in r4:
                        if (l[6] == j[0]):
                            coordinates1.append([float(j[1]) - 0.00007, float(j[2]) - 0.00007])
                if (k[0] == l[0] and l[4] == "0"):
                    break

    for k in r:
        if (k[1] == route_id and k[2] == "1"):
            for l in r1:
                if (k[3] == l[0]):
                    folium.Marker(location=[l[4],l[5]], tooltip=[l[2], 'Destination: ' + destination1],
                                  icon=folium.Icon(color='blue', icon='bus', prefix='fa')).add_to(marker_cluster)

        if (k[1] == route_id and k[2] == "0"):
            for l in r1:
                if (k[3] == l[0]):
                    folium.Marker(location=[l[4],l[5]], tooltip=[l[2], 'Destination: ' + destination0],
                                  icon=folium.Icon(color='red', icon='bus', prefix='fa')).add_to(marker_cluster)

    #print(coordinates)
    #print(coordinates1)
    my_PolyLine = folium.PolyLine(locations=coordinates,
            bubbling_mouse_events=True,
            color= "#2142c6",
            dash_array= None,
            dash_offset= None,
            fill_opacity= 0.2,
            fill_rule= "evenodd",
            line_cap= "round",
            line_join= "round",
            no_clip= False,
            opacity= 1.0,
            smooth_factor= 1.0,
            stroke= True,
            weight= 3)

    my_PolyLine1 = folium.PolyLine(locations=coordinates1, bubbling_mouse_events=True,
        color= "#db2c29",
        dash_array= None,
        dash_offset= None,
        fill_opacity= 0.2,
        fill_rule= "evenodd",
        line_cap= "round",
        line_join= "round",
        no_clip= False,
        opacity= 1.0,
        smooth_factor= 1.0,
        stroke= True,
        weight= 3,
        offset= 5)
    m.add_child(my_PolyLine)
    m.add_child(my_PolyLine1)
    m.save('templates//schedule.html')
    #return render_template("schedule.html")

#def usuarios1():
    # resultado de SELECT id, nombre FROM usuarios ORDER BY nombre
#    res = [{'id': 1, 'nombre': '2 Bayview'}, {'id': 2, 'nombre': '2 South Keys'}, {'id': 3, 'nombre': '5 Billings Bridge'}, {'id': 4, 'nombre': '6 Daly / Nicholas'}, {'id': 5, 'nombre': '6 Greenboro'}, {'id': 6, 'nombre': '6 Rideau'}, {'id': 7, 'nombre': '7 Brittany'}, {'id': 8, 'nombre': '7 Carleton'}, {'id': 9, 'nombre': '7 Parliament'}, {'id': 10, 'nombre': '7 Rideau'}, {'id': 11, 'nombre': '7 St. Laurent'}, {'id': 12, 'nombre': '7 St-Laurent'}, {'id': 13, 'nombre': '9 Rideau'}, {'id': 14, 'nombre': '10 Hurdman'}, {'id': 15, 'nombre': '10 Lyon'}, {'id': 16, 'nombre': '11 Lincoln Fields'}, {'id': 17, 'nombre': '11 Parliament'}, {'id': 18, 'nombre': '12 Blair'}, {'id': 19, 'nombre': '12 Parliament'}, {'id': 20, 'nombre': '14 St. Laurent'}, {'id': 21, 'nombre': '14 Tunneys Pasture'}, {'id': 22, 'nombre': '15 Blair'}, {'id': 23, 'nombre': '15 Gatineau'}, {'id': 24, 'nombre': '16 Westboro'}, {'id': 25, 'nombre': '17 Gatineau'}, {'id': 26, 'nombre': '17 Terrasses'}, {'id': 27, 'nombre': '18 Parliament'}, {'id': 28, 'nombre': '18 St. Laurent'}, {'id': 29, 'nombre': '18 St-Laurent'}, {'id': 30, 'nombre': '19 Parliament'}, {'id': 31, 'nombre': '19 Parliament/Parlement'}, {'id': 32, 'nombre': '19 St. Laurent'}, {'id': 33, 'nombre': '19 Vanier'}, {'id': 34, 'nombre': '24 Beacon Hill'}, {'id': 35, 'nombre': '24 St. Laurent'}, {'id': 36, 'nombre': '24 St-Laurent'}, {'id': 37, 'nombre': '25 Blair'}, {'id': 38, 'nombre': '25 La CitÃ©'}, {'id': 39, 'nombre': '25 Millennium'}, {'id': 40, 'nombre': '26 Blair'}, {'id': 41, 'nombre': '26 Pineview'}, {'id': 42, 'nombre': '30 Blair'}, {'id': 43, 'nombre': '30 Millennium'}, {'id': 44, 'nombre': '33 Blair'}, {'id': 45, 'nombre': '33 Portobello'}, {'id': 46, 'nombre': '34 Blair'}, {'id': 47, 'nombre': '34 Renaud'}, {'id': 48, 'nombre': '35 Blair'}, {'id': 49, 'nombre': '35 Esprit'}, {'id': 50, 'nombre': '38 Blair'}, {'id': 51, 'nombre': '38 Jeane dâ€™Arc / Trim'}, {'id': 52, 'nombre': '38 Jeanne dArc / Trim'}, {'id': 53, 'nombre': '38 Trim'}, {'id': 54, 'nombre': '39 Blair'}, {'id': 55, 'nombre': '39 Millenium'}, {'id': 56, 'nombre': '39 Millennium'}, {'id': 57, 'nombre': '39 Trim'}, {'id': 58, 'nombre': '40 Greenboro'}, {'id': 59, 'nombre': '44 Billings Bridge'}, {'id': 60, 'nombre': '44 Hurdman'}, {'id': 61, 'nombre': '46 Billings Bridge'}, {'id': 62, 'nombre': '46 Hurdman'}, {'id': 63, 'nombre': '48 Elmvale'}, {'id': 64, 'nombre': '50 Lincoln Fields'}, {'id': 65, 'nombre': '51 Britannia'}, {'id': 66, 'nombre': '51 Brittania'}, {'id': 67, 'nombre': '53 Tunneys Pasture'}, {'id': 68, 'nombre': '55 Bayshore'}, {'id': 69, 'nombre': '55 Elmvale'}, {'id': 70, 'nombre': '56 King Edward'}, {'id': 71, 'nombre': '56 Tunneys Pasture'}, {'id': 72, 'nombre': '57 Bayshore'}, {'id': 73, 'nombre': '57 Tunneys Pasture'}, {'id': 74, 'nombre': '61 Stittsville'}, {'id': 75, 'nombre': '61 Terry Fox'}, {'id': 76, 'nombre': '63 Briarbrook via Innovation'}, {'id': 77, 'nombre': '63 Gatineau'}, {'id': 78, 'nombre': '63 Innovation'}, {'id': 79, 'nombre': '63 Legget'}, {'id': 80, 'nombre': '63 Tunneys Pasture'}, {'id': 81, 'nombre': '64 Morgans Grant via Innovation'}, {'id': 82, 'nombre': '64 Tunneys Pasture'}, {'id': 83, 'nombre': '66 Gatineau'}, {'id': 84, 'nombre': '66 Tunneyâ€™s Pasture'}, {'id': 85, 'nombre': '73 Tunneys Pasture'}, {'id': 86, 'nombre': '74 Riverview'}, {'id': 87, 'nombre': '74 Tunneys Pasture'}, {'id': 88, 'nombre': '75 Barrhaven Centre'}, {'id': 89, 'nombre': '75 Baseline'}, {'id': 90, 'nombre': '75 Gatineau'}, {'id': 91, 'nombre': '75 Tunneys Pasture'}, {'id': 92, 'nombre': '80 Tunneys Pasture'}, {'id': 93, 'nombre': '81 Clyde'}, {'id': 94, 'nombre': '81 Tunneys Pasture'}, {'id': 95, 'nombre': '83 Viewmount'}, {'id': 96, 'nombre': '84 Centrepointe'}, {'id': 97, 'nombre': '84 Tunneys Pasture'}, {'id': 98, 'nombre': '85 Bayshore'}, {'id': 99, 'nombre': '85 Gatineau'}, {'id': 100, 'nombre': '86 Baseline'}, {'id': 101, 'nombre': '86 Tunneys'}, {'id': 102, 'nombre': '87 Baseline'}, {'id': 103, 'nombre': '87 Tunneys Pasture'}, {'id': 104, 'nombre': '88 Hurdman'}, {'id': 105, 'nombre': '88 Terry Fox'}, {'id': 106, 'nombre': '90 Greenboro'}, {'id': 107, 'nombre': '90 Hurdman'}, {'id': 108, 'nombre': '92 Greenboro'}, {'id': 109, 'nombre': '92 Hurdman'}, {'id': 110, 'nombre': '93 Hurdman'}, {'id': 111, 'nombre': '93 Leitrim'}, {'id': 112, 'nombre': '96 Merivale'}, {'id': 113, 'nombre': '97 Airport'}, {'id': 114, 'nombre': '97 Hurdman'}, {'id': 115, 'nombre': '98 Hawthorne'}, {'id': 116, 'nombre': '98 Hurdman'}, {'id': 117, 'nombre': '111 Baseline'}, {'id': 118, 'nombre': '111 Carleton'}, {'id': 119, 'nombre': '141 Kaladar'}, {'id': 120, 'nombre': '225 Blair'}, {'id': 121, 'nombre': '225 Renaud'}, {'id': 122, 'nombre': '231 Blair'}, {'id': 123, 'nombre': '231 Meadowglen'}, {'id': 124, 'nombre': '232 Blair'}, {'id': 125, 'nombre': '234 Tenth Line'}, {'id': 126, 'nombre': '235 Gardenway'}, {'id': 127, 'nombre': '236 Blair'}, {'id': 128, 'nombre': '236 Esprit'}, {'id': 129, 'nombre': '237 Blair'}, {'id': 130, 'nombre': '251 Bells Corners'}, {'id': 131, 'nombre': '252 Fernbank'}, {'id': 132, 'nombre': '256 Tunneys Pasture'}, {'id': 133, 'nombre': '257 Bridlewood'}, {'id': 134, 'nombre': '257 Tunneys Pasture'}, {'id': 135, 'nombre': '262 Tunneys Pasture'}, {'id': 136, 'nombre': '262 West Ridge'}, {'id': 137, 'nombre': '266 Tunneys Pasture'}, {'id': 138, 'nombre': '267 Tunneys Pasture'}, {'id': 139, 'nombre': '270 Cedarview'}, {'id': 140, 'nombre': '270 Tunneys Pasture'}, {'id': 141, 'nombre': '271 Stoneway'}, {'id': 142, 'nombre': '272 Tunneys Pasture'}, {'id': 143, 'nombre': '273 Tunneys Pasture'}, {'id': 144, 'nombre': '277 Tunneys Pasture'}, {'id': 145, 'nombre': '278 Riverside South'}, {'id': 146, 'nombre': '278 Tunneys Pasture'}, {'id': 147, 'nombre': '284 Tunneys Pasture'}, {'id': 148, 'nombre': '291 Hurdman'}, {'id': 149, 'nombre': '294 Findlay Creek'}]
#    usuarios1 = [(di['id'], di['nombre']) for di in res]
#    if request.method == 'POST':
#        bus1 = request.form['usuario1']
#        cancel(bus1)

#    return render_template("index.html",
#                           title="Occasional Transport: Ottawa Bus Edition",
#                           mastHead="Where's my @#$@ Bus?",
#                           statusLevel=STATUSLEVELS.OK,
#                           mastDescrip="Who knows. We do. Move along.",
#                           usuarios=usuarios,
#                           usuarios1=usuarios1)
    #return render_template('NewSchedule.html', usuarios1=usuarios1)

def cancel(cancel_id):
    print(f'alita cancel id {cancel_id}')
    #plot the map in given location
    #m = folium.Map(location=[45.4215, -75.6972], zoom_start=13)
    m = folium.Map(location=[45.4215, -75.6972], width=900, height=650,left='17.5%', top='10%', tiles='CartoDB positron', zoom_start=13)
    marker_cluster = MarkerCluster().add_to(m)  # create marker clusters
    coordinates = []
    coordinates1 = []
    print(f'route cacellations {cancel_id}')
    seq = 1
    # r7 has all the cancel_raw details
    for a in r7:
        # a[8] is route short name
        if (a[1] == cancel_id):
            can = a[8]
            stop_id = a[25]
            print(can + " id: " + stop_id)
            print(a[3][0:10])
            print(datetime.datetime.now().date().strftime("%Y-%m-%d"))
            #Identify day of the cancellation
            if a[3][0:10] == datetime.datetime.now().date().strftime("%Y-%m-%d"):
                print(a[3][0:9])
                print(datetime.datetime.now().date().strftime("%Y-%m-%d"))
                #identify time of the cancellation
                time_dst = datetime.datetime.strptime(a[5], '%H:%M')
                print(time_dst)
                time_next = time_dst + datetime.timedelta(0,int(a[7])*60)
                print(time_next.time())
                if (datetime.datetime.now().time() < time_next.time()):
                    # r8 is stop_list cancelled sequence
                    for b in r8:
                        if (int(b[2]) < seq):
                            break
                            # a[0] and b[0] is the Tweet ID
                        if (a[0] == b[0]):
                            #print("{lat: " + b[4] + ", long: " + b[5] + "},")
                            # b[2] is the number of the sequence
                            seq = int(b[2])
                            folium.Marker(location=[b[4], b[5]], tooltip=[a[12], b[3], 'Next trip: '+ a[7] + ' minutes later'],
                                        icon=folium.Icon(color='red', icon='bus', prefix='fa')).add_to(marker_cluster)


    #r has details of route_stops
    print(f'route {cancel_id}')

    # Identify the direction of the route
    for p in r:
        if (p[1] == can and p[3 == stop_id]):
            dir = p[2]
            print(p[2])
            break
   # for k in r:
        # k[1] has route_id
   #     if (k[1] == cancel_id and k[2] == dir):
            #r1 has all the stop details
   #         for l in r1:
                #if stop_id is same then plot
   #             if (k[3] == l[0]):
   #                 if l[2] in stop_name:
   #                     print('yes')
   #                     continue
   #                 print("{lat: " + l[4] + ", long: " + l[5] + "},")
                    #plots all the stops in the given route in blue colour
   #                 folium.Marker(location=[l[4], l[5]], tooltip=[l[2], l[1]],
   #                               icon=folium.Icon(color='blue', icon='bus', prefix='fa')).add_to(marker_cluster)

    for k in r6:
        # k[1] has route_short
        if (k[1] == can):
            #r1 has all the stop details
            for l in r5:
                #if stop_id is same then plot
                if (k[0] == l[0] and l[4] == dir):
                    print(k[0])
                    for j in r4:
                        if (l[6] == j[0]):
                            coordinates.append([float(j[1]), float(j[2])])
                if (k[0] == l[0] and l[4] == dir):
                    break

    my_PolyLine = folium.PolyLine(locations=coordinates,
                                  bubbling_mouse_events=True,
                                  color="#2142c6",
                                  dash_array=None,
                                  dash_offset=None,
                                  fill_opacity=0.2,
                                  fill_rule="evenodd",
                                  line_cap="round",
                                  line_join="round",
                                  no_clip=False,
                                  opacity=1.0,
                                  smooth_factor=1.0,
                                  stroke=True,
                                  weight=3)

    m.add_child(my_PolyLine)

    m.save('templates//cancel.html')
    #return render_template("cancel.html")

@app.route('/new', methods=['GET', 'POST'])
        #scheduleroute(bus)
    #return render_template('NewSchedule.html', usuario=usuario, usuarios1=usuarios1)
def usuarios1():

    # resultado de SELECT id, nombre FROM usuarios ORDER BY nombre
    res = [{'id': 1, 'nombre': '2 Bayview'}, {'id': 2, 'nombre': '2 South Keys'}, {'id': 3, 'nombre': '5 Billings Bridge'}, {'id': 4, 'nombre': '6 Daly / Nicholas'}, {'id': 5, 'nombre': '6 Greenboro'}, {'id': 6, 'nombre': '6 Rideau'}, {'id': 7, 'nombre': '7 Brittany'}, {'id': 8, 'nombre': '7 Carleton'}, {'id': 9, 'nombre': '7 Parliament'}, {'id': 10, 'nombre': '7 Rideau'}, {'id': 11, 'nombre': '7 St. Laurent'}, {'id': 12, 'nombre': '7 St-Laurent'}, {'id': 13, 'nombre': '9 Rideau'}, {'id': 14, 'nombre': '10 Hurdman'}, {'id': 15, 'nombre': '10 Lyon'}, {'id': 16, 'nombre': '11 Lincoln Fields'}, {'id': 17, 'nombre': '11 Parliament'}, {'id': 18, 'nombre': '12 Blair'}, {'id': 19, 'nombre': '12 Parliament'}, {'id': 20, 'nombre': '14 St. Laurent'}, {'id': 21, 'nombre': '14 Tunneys Pasture'}, {'id': 22, 'nombre': '15 Blair'}, {'id': 23, 'nombre': '15 Gatineau'}, {'id': 24, 'nombre': '16 Westboro'}, {'id': 25, 'nombre': '17 Gatineau'}, {'id': 26, 'nombre': '17 Terrasses'}, {'id': 27, 'nombre': '18 Parliament'}, {'id': 28, 'nombre': '18 St. Laurent'}, {'id': 29, 'nombre': '18 St-Laurent'}, {'id': 30, 'nombre': '19 Parliament'}, {'id': 31, 'nombre': '19 Parliament/Parlement'}, {'id': 32, 'nombre': '19 St. Laurent'}, {'id': 33, 'nombre': '19 Vanier'}, {'id': 34, 'nombre': '24 Beacon Hill'}, {'id': 35, 'nombre': '24 St. Laurent'}, {'id': 36, 'nombre': '24 St-Laurent'}, {'id': 37, 'nombre': '25 Blair'}, {'id': 38, 'nombre': '25 La CitÃ©'}, {'id': 39, 'nombre': '25 Millennium'}, {'id': 40, 'nombre': '26 Blair'}, {'id': 41, 'nombre': '26 Pineview'}, {'id': 42, 'nombre': '30 Blair'}, {'id': 43, 'nombre': '30 Millennium'}, {'id': 44, 'nombre': '33 Blair'}, {'id': 45, 'nombre': '33 Portobello'}, {'id': 46, 'nombre': '34 Blair'}, {'id': 47, 'nombre': '34 Renaud'}, {'id': 48, 'nombre': '35 Blair'}, {'id': 49, 'nombre': '35 Esprit'}, {'id': 50, 'nombre': '38 Blair'}, {'id': 51, 'nombre': '38 Jeane dâ€™Arc / Trim'}, {'id': 52, 'nombre': '38 Jeanne dArc / Trim'}, {'id': 53, 'nombre': '38 Trim'}, {'id': 54, 'nombre': '39 Blair'}, {'id': 55, 'nombre': '39 Millenium'}, {'id': 56, 'nombre': '39 Millennium'}, {'id': 57, 'nombre': '39 Trim'}, {'id': 58, 'nombre': '40 Greenboro'}, {'id': 59, 'nombre': '44 Billings Bridge'}, {'id': 60, 'nombre': '44 Hurdman'}, {'id': 61, 'nombre': '46 Billings Bridge'}, {'id': 62, 'nombre': '46 Hurdman'}, {'id': 63, 'nombre': '48 Elmvale'}, {'id': 64, 'nombre': '50 Lincoln Fields'}, {'id': 65, 'nombre': '51 Britannia'}, {'id': 66, 'nombre': '51 Brittania'}, {'id': 67, 'nombre': '53 Tunneys Pasture'}, {'id': 68, 'nombre': '55 Bayshore'}, {'id': 69, 'nombre': '55 Elmvale'}, {'id': 70, 'nombre': '56 King Edward'}, {'id': 71, 'nombre': '56 Tunneys Pasture'}, {'id': 72, 'nombre': '57 Bayshore'}, {'id': 73, 'nombre': '57 Tunneys Pasture'}, {'id': 74, 'nombre': '61 Stittsville'}, {'id': 75, 'nombre': '61 Terry Fox'}, {'id': 76, 'nombre': '63 Briarbrook via Innovation'}, {'id': 77, 'nombre': '63 Gatineau'}, {'id': 78, 'nombre': '63 Innovation'}, {'id': 79, 'nombre': '63 Legget'}, {'id': 80, 'nombre': '63 Tunneys Pasture'}, {'id': 81, 'nombre': '64 Morgans Grant via Innovation'}, {'id': 82, 'nombre': '64 Tunneys Pasture'}, {'id': 83, 'nombre': '66 Gatineau'}, {'id': 84, 'nombre': '66 Tunneyâ€™s Pasture'}, {'id': 85, 'nombre': '73 Tunneys Pasture'}, {'id': 86, 'nombre': '74 Riverview'}, {'id': 87, 'nombre': '74 Tunneys Pasture'}, {'id': 88, 'nombre': '75 Barrhaven Centre'}, {'id': 89, 'nombre': '75 Baseline'}, {'id': 90, 'nombre': '75 Gatineau'}, {'id': 91, 'nombre': '75 Tunneys Pasture'}, {'id': 92, 'nombre': '80 Tunneys Pasture'}, {'id': 93, 'nombre': '81 Clyde'}, {'id': 94, 'nombre': '81 Tunneys Pasture'}, {'id': 95, 'nombre': '83 Viewmount'}, {'id': 96, 'nombre': '84 Centrepointe'}, {'id': 97, 'nombre': '84 Tunneys Pasture'}, {'id': 98, 'nombre': '85 Bayshore'}, {'id': 99, 'nombre': '85 Gatineau'}, {'id': 100, 'nombre': '86 Baseline'}, {'id': 101, 'nombre': '86 Tunneys'}, {'id': 102, 'nombre': '87 Baseline'}, {'id': 103, 'nombre': '87 Tunneys Pasture'}, {'id': 104, 'nombre': '88 Hurdman'}, {'id': 105, 'nombre': '88 Terry Fox'}, {'id': 106, 'nombre': '90 Greenboro'}, {'id': 107, 'nombre': '90 Hurdman'}, {'id': 108, 'nombre': '92 Greenboro'}, {'id': 109, 'nombre': '92 Hurdman'}, {'id': 110, 'nombre': '93 Hurdman'}, {'id': 111, 'nombre': '93 Leitrim'}, {'id': 112, 'nombre': '96 Merivale'}, {'id': 113, 'nombre': '97 Airport'}, {'id': 114, 'nombre': '97 Hurdman'}, {'id': 115, 'nombre': '98 Hawthorne'}, {'id': 116, 'nombre': '98 Hurdman'}, {'id': 117, 'nombre': '111 Baseline'}, {'id': 118, 'nombre': '111 Carleton'}, {'id': 119, 'nombre': '141 Kaladar'}, {'id': 120, 'nombre': '225 Blair'}, {'id': 121, 'nombre': '225 Renaud'}, {'id': 122, 'nombre': '231 Blair'}, {'id': 123, 'nombre': '231 Meadowglen'}, {'id': 124, 'nombre': '232 Blair'}, {'id': 125, 'nombre': '234 Tenth Line'}, {'id': 126, 'nombre': '235 Gardenway'}, {'id': 127, 'nombre': '236 Blair'}, {'id': 128, 'nombre': '236 Esprit'}, {'id': 129, 'nombre': '237 Blair'}, {'id': 130, 'nombre': '251 Bells Corners'}, {'id': 131, 'nombre': '252 Fernbank'}, {'id': 132, 'nombre': '256 Tunneys Pasture'}, {'id': 133, 'nombre': '257 Bridlewood'}, {'id': 134, 'nombre': '257 Tunneys Pasture'}, {'id': 135, 'nombre': '262 Tunneys Pasture'}, {'id': 136, 'nombre': '262 West Ridge'}, {'id': 137, 'nombre': '266 Tunneys Pasture'}, {'id': 138, 'nombre': '267 Tunneys Pasture'}, {'id': 139, 'nombre': '270 Cedarview'}, {'id': 140, 'nombre': '270 Tunneys Pasture'}, {'id': 141, 'nombre': '271 Stoneway'}, {'id': 142, 'nombre': '272 Tunneys Pasture'}, {'id': 143, 'nombre': '273 Tunneys Pasture'}, {'id': 144, 'nombre': '277 Tunneys Pasture'}, {'id': 145, 'nombre': '278 Riverside South'}, {'id': 146, 'nombre': '278 Tunneys Pasture'}, {'id': 147, 'nombre': '284 Tunneys Pasture'}, {'id': 148, 'nombre': '291 Hurdman'}, {'id': 149, 'nombre': '294 Findlay Creek'}]
    usuarios1 = [(di['id'], di['nombre']) for di in res]
    if request.method == 'POST':
        bus = request.form.get('usuario')
        print(bus)
        #cancel(bus1)
    return render_template('NewSchedule.html', usuarios1=usuarios1)
# Historical Routes

@app.route('/updateDB')
def update():
    def execute_job():
        get_data()

    thread = threading.Thread(target=execute_job)
    thread.start()
    print("Uploading tweets in background")

    return redirect("/", code=302)


@app.route('/cancel/jan')
def jan():
    print('alita jan -----')
    m = folium.Map(location=[45.4215, -75.6972], zoom_start=13)
    marker_cluster = MarkerCluster().add_to(m)  # create marker clusters


    for k in r1:
        folium.Marker(location=[k[4], k[5]], tooltip=[k[2], k[1]],
                      icon=folium.Icon(color='blue', icon='bus', prefix='fa')).add_to(marker_cluster)

    for a in r2:
        for b in r3:
            if (a[0] == b[0]):
                if (b[1] < "2"):
                    folium.Marker(location=[a[3], a[4]], tooltip=[a[1], 'Cancellation:', b[1]],
                                  icon=folium.Icon(color='purple', icon='bus', prefix='fa')).add_to(marker_cluster)
                elif (b[1] >= "2" and b[1] < "4"):

                    folium.Marker(location=[a[3], a[4]], tooltip=[a[1], b[1], 'Cancellations'],
                                  icon=folium.Icon(color='orange', icon='bus', prefix='fa')).add_to(marker_cluster)
                elif (b[1] >= "4"):
                    folium.Marker(location=[a[3], a[4]], tooltip=[a[1], b[1]],
                                  icon=folium.Icon(color='red', icon='bus', prefix='fa')).add_to(marker_cluster)

    m.save('templates//jan_stops.html')
    return render_template("jan_stops.html")



@app.route('/cancel/feb')
def feb():
    print(f'alita feb cancel')
    m = folium.Map(location=[45.4215, -75.6972], zoom_start=13)
    marker_cluster = MarkerCluster().add_to(m)  # create marker clusters

    for k in r1:
        folium.Marker(location=[k[4], k[5]], tooltip=[k[2], k[1]],
                      icon=folium.Icon(color='blue', icon='bus', prefix='fa')).add_to(marker_cluster)

    for a in r2:
        for b in r3:
            if (a[0] == b[0]):
                if (b[1] < "2"):
                    folium.Marker(location=[a[3], a[4]], tooltip=[a[1], 'Cancellation:', b[1]],
                                  icon=folium.Icon(color='purple', icon='bus', prefix='fa')).add_to(marker_cluster)
                elif (b[1] >= "2" and b[1] < "4"):

                    folium.Marker(location=[a[3], a[4]], tooltip=[a[1], b[1], 'Cancellations'],
                                  icon=folium.Icon(color='orange', icon='bus', prefix='fa')).add_to(marker_cluster)
                elif (b[1] >= "4"):
                    folium.Marker(location=[a[3], a[4]], tooltip=[a[1], b[1]],
                                  icon=folium.Icon(color='red', icon='bus', prefix='fa')).add_to(marker_cluster)

    m.save('templates//feb_stops.html')
    return render_template("feb_stops.html")


#@app.route('/schedule/<route_id>')
#def scheduleroute(route_id):
#    print(f'alita route id ---------{route_id}---------')
    #CartoDB positron
    #Stamen Terrain
#    m = folium.Map(width=800,height=500,location=[45.4215, -75.6972], left='20.5%', top='10%', tiles='CartoDB positron', zoom_start=13)
#    marker_cluster = MarkerCluster().add_to(m)  # create marker clusters
#   coordinates = []
#    coordinates1 = []

#    for k in r:
#        if (k[1] == route_id and k[2] == "1"):
#            for l in r1:
#                if (k[3] == l[0]):

#                    print("{lat: " + l[4] + ", long: " + l[5] + "},")
#                    folium.Marker(location=[l[4],l[5]], tooltip=[l[2], l[1]],
#                                  icon=folium.Icon(color='blue', icon='bus', prefix='fa')).add_to(marker_cluster)

#        if (k[1] == route_id and k[2] == "0"):
#            for l in r1:
#                if (k[3] == l[0]):
#                    folium.Marker(location=[l[4],l[5]], tooltip=[l[2], l[1]],
#                                  icon=folium.Icon(color='red', icon='bus', prefix='fa')).add_to(marker_cluster)

#    for k in r6:
#        # k[1] has route_short
#        if (k[1] == route_id):
#            #r1 has all the stop details
#            for l in r5:
#                #if stop_id is same then plot
#                if (k[0] == l[0] and l[4] == "1"):
#                    print(k[0])
#                    for j in r4:
#                        if (l[6] == j[0]):
#                            coordinates.append([float(j[1]), float(j[2])])
#                if (k[0] == l[0] and l[4] == "1"):
#                    break

#    for k in r6:
#        # k[1] has route_id
#        if (k[1] == route_id):
#            #r1 has all the stop details
#            for l in r5:
#                #if stop_id is same then plot
#                if (k[0] == l[0] and l[4] == "0"):
#                    print(k[0])
#                    for j in r4:
#                        if (l[6] == j[0]):
#                            coordinates1.append([float(j[1]), float(j[2])])
#                if (k[0] == l[0] and l[4] == "0"):
#                    break

#    #print(coordinates)
#    #print(coordinates1)
#    my_PolyLine = folium.PolyLine(locations=coordinates,
#            bubbling_mouse_events=True,
#            color= "#2142c6",
#            dash_array= None,
#            dash_offset= None,
#            fill_opacity= 0.2,
#            fill_rule= "evenodd",
#            line_cap= "round",
#            line_join= "round",
#            no_clip= False,
#            opacity= 1.0,
#            smooth_factor= 1.0,
#            stroke= True,
#            weight= 3)

#    my_PolyLine1 = folium.PolyLine(locations=coordinates1, bubbling_mouse_events=True,
#        color= "#db2c29",
#        dash_array= None,
#        dash_offset= None,
#        fill_opacity= 0.2,
#        fill_rule= "evenodd",
#        line_cap= "round",
#        line_join= "round",
#        no_clip= False,
#        opacity= 1.0,
#        smooth_factor= 1.0,
#        stroke= True,
#        weight= 3)
#    m.add_child(my_PolyLine)
#    m.add_child(my_PolyLine1)
#    m.save('templates//schedule.html')
#    return render_template("schedule.html")



#@app.route('/cancel/<cancel_id>')
#def cancel(cancel_id):
#    print(f'alita cancel id {cancel_id}')
#    #plot the map in given location
#    #m = folium.Map(location=[45.4215, -75.6972], zoom_start=13)
#    m = folium.Map(location=[45.4215, -75.6972], width=600, height=400, tiles='CartoDB positron', zoom_start=12)
#    marker_cluster = MarkerCluster().add_to(m)  # create marker clusters
#    coordinates = []
#    coordinates1 = []
#    stop_name = []
#    print(f'route cacellations {cancel_id}')
#    seq = 1
#    # r7 has all the cancel_raw details
#    for a in r7:
#        # a[8] is route short name
#        if (a[1] == cancel_id):
#            # r8 is stop_list cancelled sequence
#            for b in r8:
#                if (int(b[2]) < seq):
#                    break
#                    # a[0] and b[0] is the Tweet ID
#                if (a[0] == b[0]):
#                    #print("{lat: " + b[4] + ", long: " + b[5] + "},")
#                    # b[2] is the number of the sequence
#                    seq = int(b[2])
#                    folium.Marker(location=[b[4], b[5]], tooltip=[a[12], b[3], 'Next trip: '+ a[7] + ' minutes later'],
#                                        icon=folium.Icon(color='red', icon='bus', prefix='fa')).add_to(marker_cluster)
#                    stop_name.append(b[3])

#    #r has details of route_stops
#    print(f'route {cancel_id}')

#    # Identify the direction of the route
#    for o in r1:
#        if (stop_name[0] == o[2]):
#            for p in r:
#                if (o[0] == p[3]):
#                    dir = p[2]
#                    print(p[2])
#                    break
#   # for k in r:
#        # k[1] has route_id
#   #     if (k[1] == cancel_id and k[2] == dir):
#            #r1 has all the stop details
#   #         for l in r1:
#                #if stop_id is same then plot
#   #             if (k[3] == l[0]):
#   #                 if l[2] in stop_name:
#  #                     print('yes')
#  #                     print('yes')
#  #                     print('yes')
#  #                     continue
#  #                 print("{lat: " + l[4] + ", long: " + l[5] + "},")
#                   #plots all the stops in the given route in blue colour
#  #                 folium.Marker(location=[l[4], l[5]], tooltip=[l[2], l[1]],
#  #                               icon=folium.Icon(color='blue', icon='bus', prefix='fa')).add_to(marker_cluster)
#
#   for k in r6:
#       # k[1] has route_short
#       if (k[1] == cancel_id):
#           #r1 has all the stop details
#           for l in r5:
#               #if stop_id is same then plot
#               if (k[0] == l[0] and l[4] == dir):
#                   print(k[0])
#                   for j in r4:
#                       if (l[6] == j[0]):
#                           coordinates.append([float(j[1]), float(j[2])])
#               if (k[0] == l[0] and l[4] == dir):
#                   break
#
#   my_PolyLine = folium.PolyLine(locations=coordinates,
#                                 bubbling_mouse_events=True,
#                                 color="#2142c6",
#                                 dash_array=None,
#                                 dash_offset=None,
#                                 fill_opacity=0.2,
#                                 fill_rule="evenodd",
#                                 line_cap="round",
#                                 line_join="round",
#                                 no_clip=False,
#                                 opacity=1.0,
#                                 smooth_factor=1.0,
#                                 stroke=True,
#                                 weight=3)

#   m.add_child(my_PolyLine)
#   print(stop_name)
#   m.save('templates//cancel.html')
#   return render_template("cancel.html")

@app.route('/detailed')
def latCan():
    return render_template("latestCancellation.html")

@app.route('/table')
def bootsTable():
    print(df)
    return render_template("table.html", data=df)

@app.route('/mapa')
def d3map():
    return render_template("dmap.html")

@app.before_first_request
def batch():
    def run_batch():
        while True:
            json = get_data()
            if json is not None:
                print("Uploading Tweets in background")
                time.sleep(900)

    thread = threading.Thread(target=run_batch)
    thread.start()

if __name__=="__main__":
    app.run(port=8000,debug=True)
