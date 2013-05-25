import tfl_london
import jcdecaux
import keolis_rennes

modules = [tfl_london, jcdecaux, keolis_rennes]

cities = {}
for m in modules:
    for (k, v) in m.cities.iteritems():
        cities[k] = v

def update_all(options={}):
    """ Download data for all providers
    options should be a dict with a key for each provider, the corresponding
    value will be passed to the update method of the corresponding module
    """
    for m in modules:
        m_name = m.__name__.split('.')[-1]
        if options.has_key(m_name):
            o = options[m_name]
            m.update(o)
