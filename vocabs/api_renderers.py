from rest_framework import renderers
from django.template.loader import render_to_string
import rdflib
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef, RDFS, ConjunctiveGraph
from rdflib.namespace import DC, FOAF, RDFS, SKOS


class RDFRenderer(renderers.BaseRenderer):
	media_type = 'text/xml'
	format = 'xml'

	def render(self, data, media_type=None, renderer_context=None):
		data = render_to_string(
			"vocabs/RDF_renderer.xml", {'data': data, 'renderer_context': renderer_context})

		return data


class SKOSRenderer(renderers.BaseRenderer):
	media_type = 'text/xml'
	format = 'rdf'

	def render(self, data, media_type=None, renderer_context=None):
		g = rdflib.Graph()
		SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
		DC = Namespace("http://purl.org/dc/elements/1.1/")
		RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
		VOCABS = Namespace("https://vocabs.acdh.oeaw.ac.at/testthesaurus/")
		g.bind('skos', SKOS)
		g.bind('dc', DC)
		g.bind('rdfs', RDFS)
		for obj in data['results']:
			# to force different base URI, e.g. VOCABS
			# concept = URIRef(VOCABS + str(obj['id']))
			concept = URIRef(str(obj['url'][:-12]))
			g.add((concept, RDF.type, SKOS.Concept))
			g.add((concept, SKOS.prefLabel, Literal(obj['pref_label'], lang=obj['pref_label_lang'])))
			g.add((concept, SKOS.notation, Literal(obj['notation'])))
			if obj['definition'] != '':
				g.add((concept, SKOS.definition, Literal(obj['definition'], lang=obj['definition_lang'])))
			# modelling labels
			# modelling broader/narrower relationships
			if obj['skos_broader']:
				for x in obj['skos_broader']:
					g.add((concept, SKOS.broader, URIRef(str(x[:-12]))))
					# g.add((concept, SKOS.broader, URIRef(x.source.get_vocabs_uri())))
			if obj['narrower']:
				for x in obj['narrower']:
					g.add((concept, SKOS.narrower, URIRef(str(x[:-12]))))
			if obj['skos_narrower']:
				for x in obj['skos_narrower']:
					g.add((concept, SKOS.narrower, URIRef(str(x[:-12]))))
			if obj['broader']:
				for x in obj['broader']:
					g.add((concept, SKOS.broader, URIRef(str(x[:-12]))))
			# modelling matches
			if obj['skos_related']:
				for x in obj['skos_related']:
					g.add((concept, SKOS.related, URIRef(str(x[:-12]))))
			if obj['related']:
				for x in obj['related']:
					g.add((concept, SKOS.related, URIRef(str(x[:-12]))))

			if obj['skos_broadmatch']:
				for x in obj['skos_broadmatch']:
					g.add((concept, SKOS.broadMatch, URIRef(str(x[:-12]))))
			if obj['narrowmatch']:
				for x in obj['narrowmatch']:
					g.add((concept, SKOS.narrowMatch, URIRef(str(x[:-12]))))
		result = g.serialize(format="pretty-xml")
		return result




