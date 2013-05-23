# encoding: utf-8
#
# JCDecaux
# http://developer.jcdecaux.com/
#

# update options
#   api_key : JCDecaux API key (required)

import urllib2
import json
import sys

# cities = { 'local name' : {
#    'position' : {'lat' : float, 'lng' : float},
#    'zoom'     : (int) zoom level,
#    'country'  : (3 letters ISO 3166)' }}
# the position and zoom level should be tuned so the city can fit on a regular screen
# the local name is the one displayed beside the map
# see http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2
cities = {
    u'Amiens'             : { 'country': 'FR', 'position' : {'lat':49.894607,'lng':2.293525},'zoom':14  } ,
    u'Besancon'           : { 'country': 'FR', 'position' : {'lat':47.239006,'lng':6.023297},'zoom':14  } ,
    u'Bruxelles-Capitale' : { 'country': 'FR', 'position' : {'lat':50.844646,'lng':4.346638},'zoom':12  } ,
    u'Cergy-Pontoise'     : { 'country': 'FR', 'position' : {'lat':49.034661,'lng':2.058477},'zoom':13  } ,
    u'Créteil'            : { 'country': 'FR', 'position' : {'lat':48.780811,'lng':2.461560},'zoom':15  } ,
    u'Göteborg'           : { 'country': 'SE', 'position' : {'lat':57.703207,'lng':11.965785},'zoom':14 } ,
    u'Ljubljana'          : { 'country': 'SI', 'position' : {'lat':46.063643,'lng':14.505987},'zoom':13 } ,
    u'Luxembourg'         : { 'country': 'LU', 'position' : {'lat':49.607873,'lng':6.130114},'zoom':13  } ,
    u'Lyon'               : { 'country': 'FR', 'position' : {'lat':45.759679,'lng':4.836130},'zoom':13  } ,
    u'Marseille'          : { 'country': 'FR', 'position' : {'lat':43.285016,'lng':5.374460},'zoom':13  } ,
    u'Mulhouse'           : { 'country': 'FR', 'position' : {'lat':47.749453,'lng':7.335134},'zoom':14  } ,
    u'Namur'              : { 'country': 'BE', 'position' : {'lat':50.465618,'lng':4.862695},'zoom':14  } ,
    u'Nancy'              : { 'country': 'FR', 'position' : {'lat':48.688552,'lng':6.178222},'zoom':14  } ,
    u'Nantes'             : { 'country': 'FR', 'position' : {'lat':47.218516,'lng':-1.554515},'zoom':13 } ,
    u'Paris'              : { 'country': 'FR', 'position' : {'lat':48.856866,'lng':2.352190},'zoom':12  } ,
    u'Rouen'              : { 'country': 'FR', 'position' : {'lat':49.435455,'lng':1.094127},'zoom':14  } ,
    u'Santander'          : { 'country': 'ES', 'position' : {'lat':43.457442,'lng':-3.834411},'zoom':13 } ,
    u'Sevilla'            : { 'country': 'ES', 'position' : {'lat':37.378683,'lng':-5.967722},'zoom':13 } ,
    u'Stockholm'          : { 'country': 'SE', 'position' : {'lat':59.330761,'lng':18.061310},'zoom':13 } ,
    u'Toulouse'           : { 'country': 'FR', 'position' : {'lat':43.604462,'lng':1.444247},'zoom':13  } ,
    u'富山市'             : { 'country': 'JP', 'position' : {'lat':36.694954,'lng':137.209582},'zoom':14} ,
    u'Valencia'           : { 'country': 'ES', 'position' : {'lat':39.478539,'lng':-0.375338},'zoom':13 }
}

# Unused for now
info = {
    'provider' : 'JCDecaux',                               # name of the data provider
    'info_url' : '',                                       # where to get info (users) where applicable
    'dev_info_url' :  'http://developer.jcdecaux.com/' ,   # where to get more info (developers)
    'logo_filename' :  ''                                  # logo file which should be located under
                                                           # static/imgs/logos
}

_provider_ids = {
    u'Amiens'             : 'Amiens',
    u'Besancon'           : 'Besancon',
    u'Bruxelles-Capitale' : 'Bruxelles-Capitale',
    u'Cergy-Pontoise'     : 'Cergy-Pontoise',
    u'Créteil'            : 'Creteil',
    u'Göteborg'           : 'Goteborg',
    u'Ljubljana'          : 'Ljubljana',
    u'Luxembourg'         : 'Luxembourg',
    u'Lyon'               : 'Lyon',
    u'Marseille'          : 'Marseille',
    u'Mulhouse'           : 'Mulhouse',
    u'Namur'              : 'Namur',
    u'Nancy'              : 'Nancy',
    u'Nantes'             : 'Nantes',
    u'Paris'              : 'Paris',
    u'Rouen'              : 'Rouen',
    u'Santander'          : 'Santander',
    u'Sevilla'            : 'Seville',
    u'Stockholm'          : 'Stockholm',
    u'Toulouse'           : 'Toulouse',
    u'富山市'             : 'Toyama',
    u'Valencia'           : 'Valence'
}

def update(options={}):
    """Download the data for each cities, storing it in json format in data/<name>.json
    It should be an array of dicts, each with the following keys:
        id              : (int) the ID of the station, must be unique for the city
        name            : (string) the name of the station (usually tied to location)
        position        : (dict) a dict with 'lat' and 'lng' keys, the latitude and longitude, as floats
        open            : (bool) whether the station is available
        bike_stands     : (int) the total number of stands, or docks, available at this station
        available_bikes : (int) the number of bikes available at this station
        last_update     : (int) the unix time of the last data update, in msecs
    """
    api_key = options['api_key']
    if api_key:
        c_info_url_format = "https://api.jcdecaux.com/vls/v1/stations?contract={0}&apiKey="+api_key
        for k, v in cities.iteritems():
            url = c_info_url_format.format(_provider_ids[k])
            try:
                r = urllib2.urlopen(url)
                in_json  = json.load(r)
                out_json = _reformat_json(in_json)
                with open(u'data/{0}.json'.format(k), 'w') as f:
                    json.dump(out_json, f, separators=(',',':'));
            except:
                sys.stderr.write('Failed to retrieve data for {0} ({1} plugin)'.format(k, __name__))
    else:
        sys.stderr.write('JCDecaux API key not defined in options dict')

def _reformat_json(data):
    stations = []
    for s in data:
        station = {
            'id'              : s['number'],
            'name'            : s['name'],
            'position'        : s['position'],
            'open'            : s['status'] == 'OPEN',
            'bike_stands'     : s['bike_stands'],
            'available_bikes' : s['available_bikes'],
            'last_update'     : s['last_update']
        }
        stations.append(station)
    return stations

