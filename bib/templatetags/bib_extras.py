import json
from django import template
from bib.models import ZotItem
register = template.Library()


@register.inclusion_tag('bib/tags/zotitem.html')
def bib_quote(item):
    values = {}
    bib = json.loads(item.zot_bibtex.replace("'", '"'))
    quote = "{} ({}), {}, {}".format(
            bib['author'],
            bib['year'],
            bib['title'],
            bib['pages']
        )
    values['quote'] = quote
    values['object'] = item
    return values
