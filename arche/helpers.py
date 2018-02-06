from .models import Collection


def path2cols(path, separator="_"):
    """takes a splittable string and creates nested collections"""
    counter = 1
    current = 0
    cols = []
    path_parts = path.split(separator)[:-1]
    path_length = len(path_parts)
    prefix = path_length
    for x in reversed(path_parts):
        col_title = '/'.join(path_parts[0:prefix])
        col, _ = Collection.objects.get_or_create(
            has_title=col_title
        )
        cols.append(col)
        prefix = prefix - 1
    while counter != len(cols):
        current_col = cols[current]
        parent_col = cols[counter]
        current_col.part_of = parent_col
        current_col.save()
        counter += 1
        current += 1
    return cols


def create_acdhids(resource, joiner="/", base_url='https://id.acdh.oeaw.ac.at'):
    """
    Endpoint to process text from the ACDH internal json standard

    param *resource*: a Collection or Resource object:
    param *joiner*: a string which is used to join the identifiers components with default: '/')
    param *base_url*: a base url of the identifier with default 'https://id.acdh.oeaw.ac.at'
    """
    path = "{}".format(resource.part_of)
    name = "{}".format(resource.has_title)
    acdhid = joiner.join([base_url, path, name])
    return acdhid
