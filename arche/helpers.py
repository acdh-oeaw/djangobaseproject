from .models import Collection


def path2cols(path, separator="_"):
    """takes a splittable string and creates nested collections"""
    counter = 1
    current = 0
    cols = []
    final_cols = []
    for x in reversed(path.split(separator)):
        col, _ = Collection.objects.get_or_create(
            has_title=x
        )
        cols.append(col)
    while counter != len(cols):
        current_col = cols[current]
        parent_col = cols[counter]
        current_col.part_of = parent_col
        current_col.save()
        counter += 1
        current += 1
        final_cols.append(current_col)
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
