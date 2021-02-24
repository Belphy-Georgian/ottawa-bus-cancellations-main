#OC Transpo API

import requests
from flask import json

# Globals
OCAPI_URL = 'https://api.octranspo1.com/v1.3/'
OCAPI_APPID = ''
OCAPI_APIKEY = ''

#Grabs API responce and returns working class code

# Typical Responce
#{
#   "GetRouteSummaryForStopResult": {
#       "StopNo": "1170",
#       "StopDescription": "WOODRIDGE / BAYSHORE PARK",
#       "Error": "",
#       "Routes": {
#           "Route": [
#               {
#                   "RouteNo": "85",
#                   "DirectionID": 0,
#                   "Direction": "",
#                   "RouteHeading": "Gatineau"
#               },
#               {
#                   "RouteNo": "658",
#                   "DirectionID": 0,
#                   "Direction": "",
#                   "RouteHeading": "Grandview"
#               },
#               {
#                   "RouteNo": "669",
#                   "DirectionID": 1,
#                   "Direction": "",
#                   "RouteHeading": "Bayshore"
#               }
#           ]
#       }
#   }
#}

def getStopInfo(stopID, routeID):
    TYPE = 'GetRouteSummaryForStop'

    x = requests.get(OCAPI_URL + TYPE +'?\
    appID=' + OCAPI_APPID + '&\
    apiKey=' + OCAPI_APIKEY + '&\
    stopNo=' + stopID + '&\
    routeNo=' + routeID + '&\
    format=json')

    return json.loads(x.text, None)

#{
#   "GetNextTripsForStopResult": {
#       "StopNo": "1170",
#       "StopLabel": "WOODRIDGE / BAYSHORE PARK",
#       "Error": "",
#       "Route": {
#           "RouteDirection": {
#               "RouteNo": "85",
#               "RouteLabel": "Gatineau",
#               "Direction": "",
#               "Error": "",
#               "RequestProcessingTime": "20201015130537",
#               "Trips": {
#                   "Trip": [
#                       {
#                           "TripDestination": "Gatineau",
#                           "TripStartTime": "13:18",
#                           "AdjustedScheduleTime": "15",
#                           "AdjustmentAge": "0.33",
#                           "LastTripOfSchedule": false,
#                           "BusType": "6EB - 60",
#                           "Latitude": "45.345741",
#                           "Longitude": "-75.809422",
#                           "GPSSpeed": "0.5"
#                       },
#                       {
#                           "TripDestination": "Gatineau",
#                           "TripStartTime": "13:33",
#                           "AdjustedScheduleTime": "30",
#                           "AdjustmentAge": "-1",
#                           "LastTripOfSchedule": false,
#                           "BusType": "6EB - 60",
#                           "Latitude": "",
#                           "Longitude": "",
#                           "GPSSpeed": ""
#                       },
#                       {
#                           "TripDestination": "Gatineau",
#                           "TripStartTime": "13:48",
#                           "AdjustedScheduleTime": "45",
#                           "AdjustmentAge": "-1",
#                           "LastTripOfSchedule": false,
#                           "BusType": "6EB - 60",
#                           "Latitude": "",
#                           "Longitude": "",
#                           "GPSSpeed": ""
#                       }
#                   ]
#               }
#           }
#       }
#   }
#}

def getNextTripsForStop(stopID, routeID):
    TYPE = 'GetNextTripsForStop'

    x = requests.get(OCAPI_URL + TYPE +'?\
    appID=' + OCAPI_APPID + '&\
    apiKey=' + OCAPI_APIKEY + '&\
    stopNo=' + stopID + '&\
    routeNo=' + routeID + '&\
    format=json')

    return json.loads(x.text, None)

#{
#   "GetRouteSummaryForStopResult": {
#       "StopNo": "7659",
#       "StopDescription": "BANK / FIFTH",
#       "Error": "",
#       "Routes": {
#           "Route": [
#               {
#                   "RouteNo": "6",
#                   "DirectionID": 1,
#                   "Direction": "",
#                   "RouteHeading": "Rockcliffe",
#                   "Trips": [
#                       {
#                           "TripDestination": "Rockcliffe",
#                           "TripStartTime": "12:46",
#                           "AdjustedScheduleTime": "8",
#                           "AdjustmentAge": "0.61",
#                           "LastTripOfSchedule": false,
#                           "BusType": "6EB - 60",
#                           "Latitude": "45.384656",
#                           "Longitude": "-75.677049",
#                           "GPSSpeed": "25.7"
#                       },
#                       {
#                           "TripDestination": "Rockcliffe",
#                           "TripStartTime": "13:01",
#                           "AdjustedScheduleTime": "24",
#                           "AdjustmentAge": "0.45",
#                           "LastTripOfSchedule": false,
#                           "BusType": "6EB - 60",
#                           "Latitude": "45.350191",
#                           "Longitude": "-75.652509",
#                           "GPSSpeed": "34.6"
#                       },
#                       {
#                           "TripDestination": "Rockcliffe",
#                           "TripStartTime": "13:16",
#                           "AdjustedScheduleTime": "35",
#                           "AdjustmentAge": "0.53",
#                           "LastTripOfSchedule": false,
#                           "BusType": "6EB - 60",
#                           "Latitude": "45.359847",
#                           "Longitude": "-75.658581",
#                           "GPSSpeed": "0.5"
#                       }
#                   ]
#               },
#               {
#                   "RouteNo": "7",
#                   "DirectionID": 1,
#                   "Direction": "",
#                   "RouteHeading": "St-Laurent",
#                   "Trips": [
#                       {
#                           "TripDestination": "St-Laurent",
#                           "TripStartTime": "13:09",
#                           "AdjustedScheduleTime": "13",
#                           "AdjustmentAge": "0.53",
#                           "LastTripOfSchedule": false,
#                           "BusType": "6EB - 60",
#                           "Latitude": "45.386659",
#                           "Longitude": "-75.695434",
#                           "GPSSpeed": "0.5"
#                       },
#                       {
#                           "TripDestination": "St-Laurent",
#                           "TripStartTime": "13:24",
#                           "AdjustedScheduleTime": "28",
#                           "AdjustmentAge": "-2",
#                           "LastTripOfSchedule": false,
#                           "BusType": "6EB - 60",
#                           "Latitude": "",
#                           "Longitude": "",
#                           "GPSSpeed": ""
#                       },
#                       {
#                           "TripDestination": "St-Laurent",
#                           "TripStartTime": "13:39",
#                           "AdjustedScheduleTime": "43",
#                           "AdjustmentAge": "-1",
#                           "LastTripOfSchedule": false,
#                           "BusType": " - ON",
#                           "Latitude": "",
#                           "Longitude": "",
#                           "GPSSpeed": ""
#                       }
#                   ]
#               }
#           ]
#       }
#   }
#}

def getNextTripsForStopAllRoutes(stopID):
    TYPE = 'GetNextTripsForStopAllRoutes'

    x = requests.get(OCAPI_URL + TYPE +'?\
    appID=' + OCAPI_APPID + '&\
    apiKey=' + OCAPI_APIKEY + '&\
    stopNo=' + stopID + '&\
    format=json')

    return json.loads(x.text, None)
    

if __name__=="__main__":
    print(getNextTripsForStopAllRoutes('7659'))
