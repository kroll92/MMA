from django.forms import ModelForm, modelformset_factory
from .models import Event, Fight, Fighter


class FightForm(ModelForm):
    class Meta:
        model = Fight
        fields = ['fighter1', 'fighter2']


FightFormSet = modelformset_factory(
    Fight,
    fields=('fighter1', 'fighter2',),
    extra=6,
    max_num=6
)


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location']

from django import forms
from .models import FighterStats


class FighterStatsForm(forms.ModelForm):
    fighter = forms.ModelChoiceField(queryset=Fighter.objects.all())
    class Meta:
        model = FighterStats
        fields = '__all__'

class FighterForm(forms.ModelForm):
    class Meta:
        model = Fighter
        fields = ['name']

