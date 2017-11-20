from .models import Collection


def path2cols(path, separator="_"):
    """takes a splittable string and creates nested collections"""
    counter = 1
    current = 0
    cols = []
    final_cols = []
    for x in path.split(separator)[::-1]:
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

    return final_cols
