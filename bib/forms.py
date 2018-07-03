from dal import autocomplete
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import *


class ReferenceForm(forms.ModelForm):
    class Meta:
        model = Reference
        fields = "__all__"
        widgets = {'zotero_item': autocomplete.ModelSelect2(url='bib-ac:book-autocomplete')}

    def __init__(self, *args, **kwargs):
        super(ReferenceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.add_input(Submit('submit', 'save'),)
