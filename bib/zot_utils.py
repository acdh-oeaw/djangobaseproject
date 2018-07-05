from pyzotero import zotero
from django.conf import settings
from . models import ZotItem


def items_to_dict(library_id, library_type, api_key, limit=15, since_version=None):

    """
    returns a dict with keys 'error' containing possible error-msgs,
    'items' a list of fetched zotero items and
    'bibs' a list of dicts ready for creating ZotItem objects
    """

    zot = zotero.Zotero(library_id, library_type, api_key)
    result = {}
    error = None
    itmes = None
    bibs = []
    if since_version:
        try:
            items = zot.everything(zot.top(since=since_version))
            bibtexs = zot.everything(zot.top(format='bibtex', since=since_version))
        except Exception as e:
            error = "{}".format(e)
            items = None
            bibtexs = None
    elif limit:
        try:
            items = zot.top(limit=limit)
            bibtexs = zot.everything(zot.top(format='bibtex', limit=limit))
        except Exception as e:
            error = "{}".format(e)
            items = None
            bibtexs = None
    else:
        try:
            items = zot.everything(zot.top())
            bibtexs = zot.everything(zot.top(format='bibtex'))
        except Exception as e:
            error = "{}".format(e)
            items = None
            bibtexs = None

    result['items'] = items
    result['error'] = error
    result['bibtexs'] = bibtexs

    if items:
        bibs = []
        c = 0
        for x in items:
            bib = {}
            bib['key'] = "{}".format(x['data'].get('key'))
            bib['creators'] = "{}".format(x['data'].get('creators'))
            bib['date'] = "{}".format(x['data'].get('date'))
            bib['itemType'] = "{}".format(x['data'].get('itemType'))
            bib['title'] = "{}".format(x['data'].get('title'))
            bib['publicationTitle'] = "{}".format(x['data'].get('publicationTitle'))
            bib['dateModified'] = "{}".format(x['data'].get('dateModified'))
            bib['pages'] = "{}".format(x['data'].get('pages'))
            bib['version'] = "{}".format(x['data'].get('version'))
            bib['version'] = "{}".format(x['data'].get('version'))
            bib['zot_html_link'] = "{}".format(x['links']['alternate']['href'])
            bib['zot_api_link'] = "{}".format(x['links']['self']['href'])
            if bibtexs:
                bib['zot_bibtex'] = "{}".format(bibtexs.entries[c])
            bibs.append(bib)
            c += 1

    result['bibs'] = bibs
    return result


def create_zotitem(bib_item, get_bibtex=False):
    """
    takes a dict with bib info created by 'items_to_dict'
    and creates/updates a ZotItem object
    """
    x = bib_item
    temp_item, _ = ZotItem.objects.get_or_create(
        zot_key=x['key']
    )
    temp_item.zot_creator = x['creators']
    temp_item.zot_date = x['date']
    temp_item.zot_item_type = x['itemType']
    temp_item.zot_title = x['title']
    temp_item.zot_pub_title = x['publicationTitle']
    temp_item.date_modified = x['dateModified']
    temp_item.zot_pages = x['pages']
    temp_item.zot_version = x['version']
    temp_item.zot_html_link = x['zot_html_link']
    temp_item.zot_api_link = x['zot_api_link']
    temp_item.zot_bibtex = x['zot_bibtex']
    if get_bibtex:
        temp_item.save(get_bibtex=True)
    else:
        temp_item.save()
    return temp_item
