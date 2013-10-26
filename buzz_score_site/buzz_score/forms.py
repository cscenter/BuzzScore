__author__ = 'nikita_kartashov'

from django import forms

SUPPORTED_LANGUAGES = (('en', 'en'), ('ru', 'ru'))
MAX_QUERY_LENGTH = 100
MIN_QUERY_LENGTH = 3
MAX_RESULTS = 1000


class EmotionalEvaluationForm (forms.Form):
    search_query = forms.CharField(MAX_QUERY_LENGTH, MIN_QUERY_LENGTH)
    search_language = forms.ChoiceField(widget=forms.RadioSelect, choices=SUPPORTED_LANGUAGES)