from django import forms
from .models import *



class adminForm(forms.ModelForm):
    class Meta:
        model = admin
        fields = [

            'username',
            'password',

        ]


class ttnForm(forms.ModelForm):
    class Meta:
        model = TTN
        fields = [

            'ttn_no'
        ]


class TestResultsForm(forms.ModelForm):
    class Meta:
        model = TestResults
        fields = [

            'email',
            'full_name',
            'age',
            'gender',
            'address',
            'postcode',
            'ttn_code',
            'test_result',

        ]