from rest_framework import renderers
from django.template.loader import render_to_string
import rdflib
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef, RDFS, ConjunctiveGraph
from rdflib.namespace import DC, FOAF, RDFS, SKOS
from .models import *


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
		metadata = Metadata.objects.all()
		g = rdflib.Graph()
		SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
		DC = Namespace("http://purl.org/dc/elements/1.1/")
		DCT = Namespace("http://purl.org/dc/terms/")
		RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
		OWL = Namespace("http://www.w3.org/2002/07/owl#")
		VOCABS = Namespace("https://vocabs.acdh.oeaw.ac.at/testthesaurus/")
		g.bind('skos', SKOS)
		g.bind('dc', DC)
		g.bind('dct', DCT)
		g.bind('rdfs', RDFS)
		g.bind('owl', OWL)
		for obj in data['results']:
			# to force different base URI, e.g. VOCABS
			# concept = URIRef(VOCABS + str(obj['id']))
			concept = URIRef(str(obj['url'][:-12]))
			g.add((concept, RDF.type, SKOS.Concept))
			g.add((concept, SKOS.prefLabel, Literal(obj['pref_label'], lang=obj['pref_label_lang'])))
			g.add((concept, SKOS.notation, Literal(obj['notation'])))
			# test modelling fake main Schema relations
			for x in metadata[:1]:
				mainConceptScheme = URIRef(x.indentifier)
				g.add((mainConceptScheme, RDF.type, SKOS.ConceptScheme))
				g.add((mainConceptScheme, DC.title, Literal(x.title)))
				g.add((mainConceptScheme, RDFS.label, Literal(x.title)))
				g.add((mainConceptScheme, DC.description, Literal(x.description, lang=x.description_lang)))
				g.add((mainConceptScheme, OWL.versionInfo, Literal(x.version)))
				g.add((mainConceptScheme, DC.rights, Literal(x.license)))
				g.add((mainConceptScheme, DCT.created, Literal(x.date_created)))
				g.add((mainConceptScheme, DCT.modified, Literal(x.date_modified)))
				g.add((mainConceptScheme, DCT.issued, Literal(x.date_issued)))
				# each concept must have skos:inScheme mainConceptScheme
				g.add((concept, SKOS.inScheme, mainConceptScheme))
				# accessing lists todo

			# remodelling ConceptScheme into Skos Collection
			if obj['scheme']:
				for x in obj['scheme']:
					collection = URIRef(str(x['namespace'][:-12]) +str(x['legacy_id']))
					g.add((collection, RDF.type, SKOS.Collection))
					if x['dc_title']:
						g.add((collection, SKOS.prefLabel, Literal(x['dc_title'], lang='en')))
					if x['dct_creator']:
						g.add((collection, DC.creator, Literal(x['dct_creator'])))
					if x['has_concepts']:
						for y in x['has_concepts']:
							g.add((collection, SKOS.member, URIRef(y[:-12])))
			if obj['definition']:
				g.add((concept, SKOS.definition, Literal(obj['definition'], lang=obj['definition_lang'])))
			# modelling labels
			if obj['other_label']:
				for x in obj['other_label']:
					if x['label_type'] == 'prefLabel':
						g.add((concept, SKOS.prefLabel, Literal(x['label'], lang=x['isoCode'])))
					elif x['label_type'] == 'altLabel':
						g.add((concept, SKOS.altLabel, Literal(x['label'], lang=x['isoCode'])))
					elif x['label_type'] == 'hiddenLabel':
						g.add((concept, SKOS.hiddenLabel, Literal(x['label'], lang=x['isoCode'])))
					# if x['label_type'] is not set then we make it altLabel
					else:
						g.add((concept, SKOS.altLabel, Literal(x['label'], lang=x['isoCode'])))
			# modelling broader/narrower relationships
			if obj['skos_broader']:
				for x in obj['skos_broader']:
					g.add((concept, SKOS.broader, URIRef(str(x[:-12]))))
					# g.add((concept, SKOS.broader, URIRef(x.source.get_vocabs_uri())))
			if obj['narrower']:
				for x in obj['narrower']:
					g.add((concept, SKOS.narrower, URIRef(str(x[:-12]))))
					# declaring top concepts of main scheme
					g.add((concept, SKOS.topConceptOf, URIRef(mainConceptScheme)))
					g.add((mainConceptScheme, SKOS.hasTopConcept, URIRef(concept)))
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




