var map;
var marks_layer_group;
var epoch;
var current_city;

var cookie_domain = 'velimonde.oknaj.eu';
var cookie_expire = 3600*24*30;

var refetch_delay = 1000 * 60 * 5; // 5 minutes

var refetch_timer_id;

var cities;

var CityControl = L.Control.extend({
    options: {
        position: 'topcenter',
        title: 'city',
        cities: {"Paris":{"country":"FR"}}
    },

    initialize: function(cities) {
        if (cities) {
            this.options.cities = cities;
        }
    },

    onAdd: function (map) {
        this._initLayout();
        this._update();

        return this._container;
    },

    // shameless copy from Leaflet/control/Control.Layers
    _initLayout: function() {

        var $controlContainer = $(map._controlContainer);
        if ($controlContainer.children('.leaflet-top.leaflet-center').length == 0) {
            $controlContainer.append('<div class="leaflet-top leaflet-center"></div>');
            map._controlCorners.topcenter = $controlContainer.children('.leaflet-top.leaflet-center').first()[0];
        }

        var className = 'leaflet-control-cities',
            container = this._container = L.DomUtil.create('div', className);

        //Makes this work on IE10 Touch devices by stopping it from firing a mouseout event when the touch is released
        container.setAttribute('aria-haspopup', true);

        if (!L.Browser.touch) {
            L.DomEvent.disableClickPropagation(container);
            L.DomEvent.on(container, 'mousewheel', L.DomEvent.stopPropagation);
        } else {
            L.DomEvent.on(container, 'click', L.DomEvent.stopPropagation);
        }

        var form = this._form = L.DomUtil.create('form', className + '-list');

        L.DomEvent.on(container, 'mouseover', this._expand, this).on(container, 'mouseout', this._collapse, this);

        var link = this._layersLink = L.DomUtil.create('a', className + '-toggle', container);
        link.href = '#';
        link.title = 'cities';
        link.innerHTML = 'Choose a city';

        if (L.Browser.touch) {
            L.DomEvent
            .on(link, 'click', L.DomEvent.stopPropagation)
            .on(link, 'click', L.DomEvent.preventDefault)
            .on(link, 'click', this._expand, this);
        } else {
            L.DomEvent.on(link, 'focus', this._expand, this);
        }

        this._map.on('movestart', this._collapse, this);

        this._cities_list = L.DomUtil.create('div', className + '-base', form);

        container.appendChild(form);
    },

    _update: function () {
        if (!this._container) {
            return;
        }

        this._cities_list.innerHTML = '';

        for (name in this.options.cities) {
            obj = this.options.cities[name];
            this._addItem(name, obj);
        }
    },

    _addItem: function (name, obj) {
        city_div = document.createElement('div');
        c = obj['country'];
        city_div.innerHTML =  name + '<span class="velimonde-country">'
            +'<img src="/static/img/flags/'+c+'.png" alt="'+c+'" title="'+c+'"></span>';
        city_div.className = 'leaflet-control-cities-entry';
        city_div.cityId = name;
        L.DomEvent.on(city_div, 'click', this._onItemClick);
        this._cities_list.appendChild(city_div);
    },

    _onItemClick: function () {
        switch_city(this.cityId);
    },

    _expand: function () {
        $('#splash').hide();
        L.DomUtil.addClass(this._container, 'leaflet-control-cities-expanded');
    },

    _collapse: function () {
        this._container.className = this._container.className.replace(' leaflet-control-cities-expanded', '');
    }

});

function map_init() {
    map = L.map('map');
    if (Cookies.enabled) {
        default_city = Cookies.get('default_city');
    }
    $.getJSON('/static/cities.json', function(data) {
        cities = eval(data);
        if (VELIMONDE_INIT_CITY != '') {
            switch_city(VELIMONDE_INIT_CITY);
        } else if (default_city) {
                switch_city(default_city);
        } else {
            reset_to_world();
        }
        L.tileLayer('http://{s}.tile.opencyclemap.org/cycle/{z}/{x}/{y}.png', {
                attribution: '<div class="velimonde-sample velimonde-full"></div> ~full '
                + '<div class="velimonde-sample velimonde-empty"></div> ~empty '
                + '<div class="velimonde-sample velimonde-ok"></div> OK '
                + '<div class="velimonde-sample velimonde-closed"></div> closed '
                + '| <a href="/api">API</a> '
                + '| <a href="/licensing">Licensing</a>',
                opacity: 0.5
                }).addTo(map);
        map.addControl(new CityControl(cities));
    });
}

function add_station(i, s) {
    if (s.position.lat == 0 && s.position.lng ==0)
    {
        return;
    }
    if (s.open) {
        if (s.available_bikes <= 3) {
            color = '#F55';
        } else if ((s.bike_stands - s.available_bikes) <= 3) {
            color = '#55F';
        } else {
            color = '#0C0';
        }
    } else {
        color = '#000';
    }
    mark = new L.Circle([s.position.lat, s.position.lng], 10, {color: color, opacity: 0.7, fillOpacity: 1, weight: 10});
    popup_text  = '<div class="station-info">';
    popup_text += '<div class="station-name">';
    popup_text += '<a href="/city/'+current_city+'/'+s.id+'">'+s.name+'</a></div>';
    if (!s.open) {
        popup_text += '<p class="station-status">This station is CLOSED!</p>';
    }
    popup_text += '<span class="station-available-stands">'+s.available_bikes+'</span>';
    popup_text += '<span class="station-separator">/</span>';
    popup_text += '<span class="station-total-stands">'+s.bike_stands+'</span> bikes here';
    popup_text += '</div>';
    popup_text += '<div class="station-update-time">';
    utcSeconds = s.last_update;
    d = new Date(0); // The 0 there is the key, which sets the date to the epoch
    d.setUTCSeconds(utcSeconds/1000);
    popup_text += 'updated at '+lpad(d.getHours(),2)+':'+lpad(d.getMinutes(),2);
    popup_text += '</div>';
    mark.bindPopup(popup_text);
    mark.addTo(marks_layer_group);
}

function reset_to_world() {
    map.fitWorld();
    $('#splash').show();
}

function switch_city(name) {


    if (name == 'world') {
        reset_to_world();
        return;
    }

    current_city = name;

    if (cities[name]) {

        window.clearInterval(refetch_timer_id);

        fetch_stations(name, true);

        if (Cookies.enabled) {
            Cookies.set('default_city',  name);
        }
        $('#splash').hide();

        refetch_timer_id = window.setInterval( function() {
            fetch_stations(name, false);
        }, refetch_delay);
    } else {
        Cookies.set('default_city', 'world');
        reset_to_world();
    }
};

function load_stations(data, fit_map) {
    if (data) {
        epoch = (new Date).getTime();
        if (marks_layer_group) {
            marks_layer_group.clearLayers();
        } else {
            marks_layer_group = new L.FeatureGroup();
            marks_layer_group.addTo(map);
        }
        var stations = eval(data);
        $.each(stations, add_station);
        if (fit_map) {
            map.fitBounds(marks_layer_group.getBounds());
        }
    }
}


function fetch_stations(name, fit_map) {
    $('#loading').show();
    $.ajax({url: '/data/'+name+'.json'}).done(function(data) {
        load_stations(data, fit_map);
    }).always( function(){
        $('#loading').hide();
    });
}

var lpad = function(value, padding) {
    var zeroes = "0";
    for (var i = 0; i < padding; i++) { zeroes += "0"; }
    return (zeroes + value).slice(padding * -1);
}

$(document).ready(function () {

    if (Cookies.enabled) {
        Cookies.default = {
            expires: cookie_expire,
            domain:  cookie_domain
        };
    }

    map_init();

});
