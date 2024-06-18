from django.forms import ModelForm, modelformset_factory
from .models import Event, Fight, Fighter, FightHighlight, Article
from django import forms
from django.forms import modelformset_factory
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location']

FightFormSet = modelformset_factory(Fight, fields=['fighter1', 'fighter2'], extra=1)


class FightForm(forms.ModelForm):
    class Meta:
        model = Fight
        fields = ['fighter1', 'fighter2']

FightFormSet = modelformset_factory(
    Fight,
    form=FightForm,
    extra=6,
    max_num=6)


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


class FightHighlightForm(forms.ModelForm):
    class Meta:
        model = FightHighlight
        fields = ['title', 'youtube_url']

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'image', 'content', 'published_date']


class FighterSearchForm(forms.Form):
    search_query = forms.CharField(label='Wyszukaj zawodnika', max_length=100)