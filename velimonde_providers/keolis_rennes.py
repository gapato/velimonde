# encoding: utf-8
#
# Keolis Rennes
# http://data.keolis-rennes.com/
#

# update options
#   api_key : Keolis API key (required)

import urllib2
import json
import sys
import os
import datetime

cities = { u'Rennes'             : { 'country': 'FR' } }

#Unused for now
info = {
    'provider' : 'Keolis Rennes',                          # name of the data provider
    'info_url' : '',                                       # where to get info (users) where applicable
    'dev_info_url' :  'http://data.keolis-rennes.com/' ,   # where to get more info (developers)
    'logo_filename' :  ''                                  # logo file which should be located under
                                                           # static/imgs/logos
}

def update(options={}):
    api_key = options['api_key']
    if api_key:
        url = 'http://data.keolis-rennes.com/json/?version=2.0&key={0}&cmd=getbikestations'.format(api_key)
        try:
            r = urllib2.urlopen(url)
            in_json  = json.load(r)
            out_json = _reformat_json(in_json)
            with open(u'data/Rennes.json', 'w') as f:
                json.dump(out_json, f, separators=(',',':'));
        except:
            sys.stderr.write(u'Failed to retrieve data for Rennes ({1} plugin)'.format(k, __name__).encode('utf-8'))
    else:
        sys.stderr.write('Keolis Rennes API key not defined in options dict')

def _reformat_json(data):

    got_first = False

    try:
        status = data['opendata']['answer']['status']['@attributes']['code']
        if not status == '0':
            raise ValueError
    except:
        raise ValueError

    stations = []
    for s in data['opendata']['answer']['data']['station']:
        bikes  = int(s['bikesavailable'])
        stands = int(s['slotsavailable'])

        # A bit of a ugly hack because we want to forget about timezones
        # but datetime seems too dumb for that...
        # Since timestamps seem to be all the same, do the parsing once only.
        if not got_first:
            # Get the date and get the offset 'by hand', datetime does not handle ISO 8601 properly
            # The timestamp is now using UTC time
            last_update = datetime.datetime.strptime(s['lastupdate'][:-6], '%Y-%m-%dT%H:%M:%S')
            offset = datetime.timedelta(hours=int(s['lastupdate'][-6:-3]))
            last_update = last_update - offset

            #  Format it, forcing it to be considered UTC time,
            # not too sure how portable this is though...
            if os.environ.has_key('TZ'):
                tz = os.environ['TZ']
            os.environ['TZ'] = 'UTC'
            last_update = int(last_update.strftime('%s'))*1000
            try:
                os.environ['TZ'] = tz
            except NameError:
                os.environ.pop('TZ')
            got_first = True
        station = {
            'id'              : int(s['number']),
            'name'            : s['name'],
            'position'        : {
                'lat': float(s['latitude']),
                'lng': float(s['longitude'])
                },
            'open'            : s['state'] == '1',
            'bike_stands'     : stands+bikes,
            'available_bikes' : bikes,
            'last_update'     : last_update
        }
        stations.append(station)
    return stations

