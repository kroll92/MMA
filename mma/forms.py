from django.forms import ModelForm, modelformset_factory
from .models import Event, Fight, Fighter, FightHighlight, Article, Bet
from django import forms

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location']

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

class BetForm(forms.ModelForm):
    CHOICES = (
        ('fighter1_win', 'Fighter 1 Win'),
        ('draw', 'Draw'),
        ('fighter2_win', 'Fighter 2 Win'),
    )

    choice = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())

    class Meta:
        model = Bet
        fields = ['fight', 'points']

    def __init__(self, event=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if event:
            fights = event.fights.all()
            choices = [(fight.id, f"{fight.fighter1.name} vs {fight.fighter2.name}") for fight in fights]
            self.fields['fight'].choices = choices
