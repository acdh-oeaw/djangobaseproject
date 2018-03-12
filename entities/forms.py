# -*- coding: utf-8 -*-
from django import forms
from dal import autocomplete
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Place, AlternativeName, Institution, Person


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = "__all__"
        widgets = {
            'belongs_to_institution': autocomplete.ModelSelect2(
                url='entities-ac:institution-autocomplete'),
            'place_of_birth': autocomplete.ModelSelect2(url='entities-ac:place-autocomplete'),
            'alt_names': autocomplete.ModelSelect2Multiple(
                url='entities-ac:altname-autocomplete'),
        }

    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.add_input(Submit('submit', 'save'),)


class InstitutionForm(forms.ModelForm):
    class Meta:
        model = Institution
        fields = "__all__"
        widgets = {
            'location': autocomplete.ModelSelect2(url='entities-ac:place-autocomplete'),
            'parent_institution': autocomplete.ModelSelect2(
                url='entities-ac:institution-autocomplete'),
            'alt_names': autocomplete.ModelSelect2Multiple(
                url='entities-ac:altname-autocomplete'),
        }

    def __init__(self, *args, **kwargs):
        super(InstitutionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.add_input(Submit('submit', 'save'),)


class AlternativeNameForm(forms.ModelForm):
    class Meta:
        model = AlternativeName
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(AlternativeNameForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.add_input(Submit('submit', 'save'),)


class AlternativeNameFormCreate(forms.ModelForm):
    class Meta:
        model = AlternativeName
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(AlternativeNameFormCreate, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = "__all__"
        widgets = {
            'part_of': autocomplete.ModelSelect2(url='entities-ac:place-autocomplete'),
            'alt_names': autocomplete.ModelSelect2Multiple(
                url='entities-ac:altname-autocomplete'),
        }

    def __init__(self, *args, **kwargs):
        super(PlaceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class PlaceFormCreate(forms.ModelForm):
    class Meta:
        model = Place
        fields = "__all__"
        widgets = {
            'part_of': autocomplete.ModelSelect2(url='entities-ac:place-autocomplete'),
            'alt_names': autocomplete.ModelSelect2Multiple(
                url='entities-ac:altname-autocomplete'),
        }

    def __init__(self, *args, **kwargs):
        super(PlaceFormCreate, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
