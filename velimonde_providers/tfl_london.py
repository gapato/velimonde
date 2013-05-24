#
# Transport for London - Barclays Bike Hire
# http://www.tfl.gov.uk/businessandpartners/syndication/default.aspx
#

# update options
#   url : the URL of the data feed (required)

import urllib2
import xml.etree.ElementTree as ET
import json

cities = {'London' : {'country':  'GB' }}

info = {
    'provider' : 'Transport for London',                                                     # name of the data provider
    'info_url' : 'http://www.tfl.gov.uk/roadusers/cycling/14808.aspx',                       # where to get info (users)
    'dev_info_url' :  'http://www.tfl.gov.uk/businessandpartners/syndication/default.aspx' , # where to get more info (developers)
    'logo_filename' :  ''                                                                    # logo file which should be located under
                                                                                             # static/imgs/logos
}

def update(options={}):
    url = options['url']
    if url:
        try:
            r = urllib2.urlopen(url)

            root = ET.fromstring(r.read())
            out_json = _format_to_json(root)

            with open('data/London.json', 'w') as f:
                json.dump(out_json, f)
        except:
            sys.stderr.write(u'Failed to retrieve data for {0} ({1} plugin)'.format(k, __name__))
    else:
        sys.stderr.write('TfL feed url not defined in options dict')

def _format_to_json(root):
    stations = [];
    last_update = int(root.attrib['lastUpdate'])
    for s_xml in root:
        station = {'last_update' : last_update, 'open': True}
        position = {}
        for t in s_xml:
            if t.tag == 'id':
                station['id'] = int(t.text)
            if t.tag == 'locked' and t.text == 'true':
                station['open'] = False
            if t.tag == 'installed' and t.text == 'false':
                station['open'] = False
            if t.tag == 'nbBikes':
                station['available_bikes'] = int(t.text)
            if t.tag == 'nbDocks':
                station['bike_stands'] = int(t.text)
            if t.tag == 'name':
                station['name'] = t.text
            if t.tag == 'lat':
                position['lat'] = float(t.text)
            if t.tag == 'long':
                position['lng'] = float(t.text)
        station['position'] = position
        stations.append(station)
    return json.dumps(stations, separators=(',',':'))
