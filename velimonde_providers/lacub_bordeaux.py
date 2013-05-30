#
# LACUB - Bordeaux
# http://data.lacub.fr/
#

# update options
#   url : the URL of the data feed (required)

import urllib2
import xml.etree.ElementTree as ET
import json
import sys
import re
import datetime

cities = {'Bordeaux' : {'country':  'FR' }}

info = {
    'provider' : 'LACUB',                                                                    # name of the data provider
    'info_url' : 'http://www.lacub.fr/le-velo-dans-la-cub/pieton-velo',                      # where to get info (users)
    'dev_info_url' :  'http://data.lacub.fr/' ,                                              # where to get more info (developers)
    'logo_filename' :  ''                                                                    # logo file which should be located under
                                                                                             # static/imgs/logos
}

def update(options={}):
    if options.has_key('api_key'):
        key = options['api_key']
        url = 'http://data.lacub.fr/wfs?key={0}&REQUEST=GetFeature&TYPENAME=CI_VCUB_P&service=wfs&VERSION=1.1.0&SRSNAME=EPSG%3A4326'.format(key)

        try:
            r = urllib2.urlopen(url)

            response = r.read()
            root = ET.fromstring(response)
            out_json = _format_to_json(root)

            with open('data/Bordeaux.json', 'w') as f:
                json.dump(out_json, f, separators=(',',':'))
        except:
            sys.stderr.write(u'Failed to retrieve data for Bordeaux ({0} plugin)'.format(__name__))
    else:
        sys.stderr.write('LACUB feed url not defined in options dict')

def _format_to_json(root):
    tag_prefix_re = re.compile('({.*})?')
    stations = [];
    for s_xml in root.getchildren()[1:]:
        epoch = int(datetime.datetime.now().strftime('%s')) * 1000
        station = {'last_update' : epoch} # No easy/quick way to get timezone/DST
        for t in s_xml[0]:
            tag_name = tag_prefix_re.sub('', t.tag)
            if tag_name == 'boundedBy':
                continue
            if tag_name == 'GID':
                station['id'] = int(t.text)
            if tag_name == 'locked' and t.text == 'true':
                station['open'] = False
            if tag_name == 'installed' and t.text == 'false':
                station['open'] = False
            if tag_name == 'NBVELOS':
                station['available_bikes'] = int(t.text)
            if tag_name == 'NBPLACES':
                free_stands = int(t.text)
            if tag_name == 'ETAT':
                station['open'] = t.text == 'CONNECTEE'
            if tag_name == 'NOM':
                station['name'] = t.text
            if tag_name == 'msGeometry':
                (lat, lng) = t[0][0].text.split(' ')
                position = { 'lat' : round(float(lat), 6), 'lng' : round(float(lng), 6) }
                station['position'] = position
        station['bike_stands'] = free_stands + station['available_bikes']
        stations.append(station)
    return stations
