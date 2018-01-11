import django_filters
from dal import autocomplete
from .models import SkosConcept, SkosConceptScheme


django_filters.filters.LOOKUP_TYPES = [
    ('', '---------'),
    ('exact', 'Is equal to'),
    ('iexact', 'Is equal to (case insensitive)'),
    ('not_exact', 'Is not equal to'),
    ('lt', 'Lesser than/before'),
    ('gt', 'Greater than/after'),
    ('gte', 'Greater than or equal to'),
    ('lte', 'Lesser than or equal to'),
    ('startswith', 'Starts with'),
    ('endswith', 'Ends with'),
    ('contains', 'Contains'),
    ('icontains', 'Contains (case insensitive)'),
    ('not_contains', 'Does not contain'),
]


class SkosConceptFilter(django_filters.FilterSet):

    pref_label = django_filters.ModelMultipleChoiceFilter(
        widget=autocomplete.Select2Multiple(url='vocabs-ac:skosconcept-autocomplete'),
        queryset=SkosConcept.objects.all(),
        lookup_expr='icontains',
        label='PrefLabel',
        help_text=False,
    )

    scheme = django_filters.ModelMultipleChoiceFilter(
        queryset=SkosConceptScheme.objects.all(),
        lookup_expr='icontains',
        label='in SkosConceptScheme',
        help_text=False,
    )

    class Meta:
        model = SkosConcept
        fields = '__all__'
