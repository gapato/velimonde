## Vélimonde

#### Overview

Rather stupid webapp showing location and availability of automated bike rental stations.

#### TODO

* Be very kind and try to make it behave OK on hand-held thingies
* Option to disable background to save bandwidth
* Move away from jQuery
* Etc.

#### Demo

You can check [the demo](http://velimonde.oknaj.eu/) out.

Some say there's a [REST API](http://velimonde.oknaj.eu/api) you can use to access a city or station
directly.

#### Getting your own rolling

* Get the code.
* Create the ``data`` folder in the Vélimonde root folder.
* Get your API hey [here](https://developer.jcdecaux.com/) and put it into the ``update_stations`` file
(if you use git you probably want to use a copy of that file).
* Setup whatever cron program you use to run ``python update_stations`` periodically. Make sure to ``chdir``
to the Vélimonde root folder.
* Setup your webserver, and ensure that the ``static`` and ``data`` folders are served directly. Those are
separated to make it easier to setup ``Expires`` headers since ``data/*`` is updated much more frequently.
Note that ``cities.json`` has a different format than the one served by JCDecaux to speed up lookups.

### Licence

This work is license under the likable [WTFPL](http://www.wtfpl.net/txt/copying/).

#### The software within, many thanks to them!

* [Cookies.js](https://github.com/ScottHamper/Cookies), by Scott Hamper
* [LeafletJS](http://leafletjs.com/)
* [Flask](http://flask.pocoo.org/)
* [Tango icon theme](http://tango.freedesktop.org/Tango_Desktop_Project)
* [jQuery](http://jquery.com/)

#### The data within, many thanks to them too!

Real time data:
* [JCDecaux](https://developer.jcdecaux.com/), under ODC-BY, CC-BY 2.0 license.
* [Transport for London](http://www.tfl.gov.uk/businessandpartners/syndication/default.aspx), licensing does not allow distribution.
* [Keolis Rennes](http://data.keolis-rennes.com/)

Map courtesy of [OpenStreetMap](http://osm.org/) contributors and [OpenCycleMap](http://www.opencyclemap.org/).
