## Vélimonde

### Overview

Rather stupid webapp showing location and availability of automated bike rental stations.
This works for cities which have some kind of partnership with JCDecaux for deployment.

### TODO

* Be very kind and try to make it behave OK on hand-held thingies
* Option to disable background to save bandwidth
* Find a better background (no need for freaking _buildings_ to be on there) and stop leeching OSM.org
* Etc.

### Demo

You can check [the demo](http://velimonde.oknaj.eu/) out.

Some say there's a [REST API](http://velimonde.oknaj.eu/api) you can use to access a city or station
directly.

### Getting your own rolling

* Get the code.
* Create the ``data`` folder in the Vélimonde root folder.
* Get your API hey [here](https://developer.jcdecaux.com/) and put it into the ``update_stations`` file
(if you use git you probably want to use a copy of that file).
* Setup whatever cron program you use to run ``python update_stations`` periodically. Make sure to ``chdir``
to the Vélimonde root folder.
* Setup your webserver, and ensure that the ``static`` and ``data`` folders are served directly. Those are
separated to make it easier to setup ``Expires`` headers since ``data/*`` is updated much more frequently.


### Things within

* [Cookies.js](https://github.com/ScottHamper/Cookies), by Scott Hamper
* [LeafletJS](http://leafletjs.com/)
* [Flask](http://flask.pocoo.org/)

### Licence

This work is license under the likable [WTFPL](http://www.wtfpl.net/txt/copying/).

The real-time data is available at [developer.jcdecaux.com](https://developer.jcdecaux.com/) under ODC-BY, CC-BY 2.0 license.
If you want to serve the data yourself (you can, so you should), you need to get _your very own_ API key and make the data available under
``/static/cities.json`` for the list of areas available, and ``/data/<city_name>.json`` for the stations in each area.
Note that ``cities.json`` has a different format than the one served by JCDecaux to speed up lookups.

Map courtesy of [OpenStreetMap](http://osm.org/).
