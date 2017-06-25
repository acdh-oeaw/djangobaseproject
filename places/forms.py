# -*- coding: utf-8 -*-
from django import forms
from crispy_forms.helper import FormHelper
from .models import Place


class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(PlaceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class PlaceFormCreate(forms.ModelForm):
    class Meta:
        model = Place
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(PlaceFormCreate, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
