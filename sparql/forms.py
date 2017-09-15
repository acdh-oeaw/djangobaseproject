from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class QueryForm(forms.Form):
    query = forms.CharField(
        required=False,
        widget=forms.Textarea()
    )

    def __init__(self, *args, **kwargs):
        super(QueryForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.add_input(Submit('submit', 'query'),)
