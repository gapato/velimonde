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
#    'country'  : (2 letters ISO 3166)' }}
# the local name is the one displayed beside the map
# see http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2
cities = {
    u'Amiens'             : { 'country': 'FR' } ,
    u'Besancon'           : { 'country': 'FR' } ,
    u'Bruxelles-Capitale' : { 'country': 'FR' } ,
    u'Cergy-Pontoise'     : { 'country': 'FR' } ,
    u'Créteil'            : { 'country': 'FR' } ,
    u'Göteborg'           : { 'country': 'SE' } ,
    u'Ljubljana'          : { 'country': 'SI' } ,
    u'Luxembourg'         : { 'country': 'LU' } ,
    u'Lyon'               : { 'country': 'FR' } ,
    u'Marseille'          : { 'country': 'FR' } ,
    u'Mulhouse'           : { 'country': 'FR' } ,
    u'Namur'              : { 'country': 'BE' } ,
    u'Nancy'              : { 'country': 'FR' } ,
    u'Nantes'             : { 'country': 'FR' } ,
    u'Paris'              : { 'country': 'FR' } ,
    u'Rouen'              : { 'country': 'FR' } ,
    u'Santander'          : { 'country': 'ES' } ,
    u'Sevilla'            : { 'country': 'ES' } ,
    u'Stockholm'          : { 'country': 'SE' } ,
    u'Toulouse'           : { 'country': 'FR' } ,
    u'富山市'             : { 'country': 'JP' } ,
    u'Valencia'           : { 'country': 'ES' }
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
                with open(u'data/{0}.json'.format(k).encode('utf-8'), 'w') as f:
                    json.dump(out_json, f, separators=(',',':'));
            except:
                sys.stderr.write(u'Failed to retrieve data for {0} ({1} plugin)'.format(k, __name__).encode('utf-8'))
    else:
        sys.stderr.write('JCDecaux API key not defined in options dict')

def _reformat_json(data):
    stations = []
    for s in data:
        try:
            position = { 'lat' : round(s['position']['lat'], 6), 'lng' : round(s['position']['lng'], 6) }
        except:
            position = { 'lat' : 0, 'lng' : 0 }
        station = {
            'id'              : s['number'],
            'name'            : s['name'],
            'position'        : position,
            'open'            : s['status'] == 'OPEN',
            'bike_stands'     : s['bike_stands'],
            'available_bikes' : s['available_bikes'],
            'last_update'     : s['last_update']
        }
        stations.append(station)
    return stations

