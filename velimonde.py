from flask import Flask, render_template, abort, jsonify, flash
from flask.helpers import send_from_directory
import json
import time

# configuration
SECRET_KEY = 'dev key'
if __name__ == '__main__':
    DEBUG = True

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

cities = [ u'Amiens', u'Besancon', u'Bruxelles-Capitale', u'Cergy-Pontoise',
                u'Creteil', u'Goteborg', u'Ljubljana', u'Luxembourg',
                u'Lyon', u'Marseille', u'Mulhouse', u'Namur', u'Nancy',
                u'Nantes', u'Paris', u'Rouen', u'Santander', u'Seville', u'Stockholm',
                u'Toulouse', u'Toyama', u'Valence' ]

cities_lower = map(lambda x:x.lower(), cities)

output_formats = ['html', 'json']

def get_station_info(city, station_id):
    with open('data/{0}.json'.format(city)) as f:
        stations = json.load(f)
    for s in stations:
        if s['number'] == station_id:
            return s
    return None

# Try to find case insensitive match
def get_city_upper(city):
    index = cities_lower.index(city.lower())
    return cities[index]

@app.route('/')
def index():
    return render_template('index.html', initial_city='')

@app.route('/api')
def api_info():
    return render_template('api.html')

@app.route('/city/<city>')
def city_map(city):
    try:
        city_upper = get_city_upper(city)
        return render_template('index.html', initial_city=city_upper)
    except ValueError:
        flash('This city ({0}) does exist, please choose one below'.format(city))
        return render_template('cities.html', cities=cities)

@app.route('/city/<city>/<station_id>')
def station_info(city, station_id, format='html'):
    try:
        city_upper = get_city_upper(city)
        if format in output_formats:
            if station_id[-5:] == '.json':
                station_id = station_id[:-5]
                format = 'json'
            station_id = int(station_id)
            info = get_station_info(city_upper, station_id)
            if info:
                if format == 'json':
                    return jsonify(info)
                elif format == 'html':
                    return render_template('station.html', city=city_upper, info=info)
    except ValueError:
        pass
    abort(404)

@app.template_filter('tomin')
def epoch_to_minutes(s):
# jdecaux data uses msecs for epoch
    return int((time.time()*1000 - s)/60000)


if __name__ == '__main__':
# only for development, should be served by the webserver
    @app.route('/data/<path:filename>')
    def custom_static(filename):
        return send_from_directory('data', filename)

if __name__ == '__main__':
    app.run()
