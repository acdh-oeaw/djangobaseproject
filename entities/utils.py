from rdflib import Graph, Namespace
from rdflib.term import URIRef


def get_coordinates(gnd_id):
    """ takes a GeoNames-ID and returns a dict with lat, lng """
    g = Graph()
    WSG84 = Namespace('http://www.w3.org/2003/01/geo/wgs84_pos#')
    try:
        parsed = g.parse("https://www.geonames.org/{}/about.rdf".format(gnd_id))
    except Exception as e:
        print(e)
        return None
    if parsed:
        lat = [x for x in parsed.subject_objects(WSG84.lat)][0][1].value
        lng = [x for x in parsed.subject_objects(WSG84.long)][0][1].value
        return {"lat": lat, "lng": lng}
    else:
        return None
