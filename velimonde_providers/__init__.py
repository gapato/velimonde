import tfl_london
import jcdecaux
import keolis_rennes
import lacub_bordeaux

plugins = [tfl_london, jcdecaux, keolis_rennes, lacub_bordeaux]

def get_cities(plugin_name_list=[]):
    """ Return a dict containing the cities of plugins matching the input list,
    defaults to all cities with no input argument
    """
    if plugin_name_list == []:
        plugin_name_list = map(lambda m:m.__name__.split('.')[-1], plugins)
    cities = {}
    for p in plugins:
        p_name = p.__name__.split('.')[-1]
        if p_name in plugin_name_list:
            for (k, v) in p.cities.iteritems():
                cities[k] = v
    return cities

def update_all(options={}):
    """ Download data for all providers
    options should be a dict with a key for each provider, the corresponding
    value will be passed to the update method of the corresponding plugin
    """
    for p in plugins:
        p_name = p.__name__.split('.')[-1]
        if options.has_key(p_name):
            o = options[p_name]
            p.update(o)
