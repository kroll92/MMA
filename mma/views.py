from django.shortcuts import render, get_object_or_404
from .models import Article
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import Event, Fight, Fighter, FightHighlight, Fight, Bet, BetPoints
from .forms import EventForm, FightFormSet, FighterForm, FightHighlightForm, ArticleForm, BetForm
from django.views.generic import DetailView
from django.urls import reverse
from django.views import View
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'index.html')


def aktualnosci(request):
    return render(request, 'aktualnosci.html')


def events(request):
    return render(request, 'events.html')




def fighters(request):
    all_fighters = Fighter.objects.all()
    return render(request, 'fighters.html', {'fighters': all_fighters})

class FighterDetailView(DetailView):
    model = Fighter
    template_name = 'fighter_detail.html'
    context_object_name = 'fighter'

def organizacje(request):
    return render(request, 'organizacje.html')




def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')

    return render(request, 'login.html')


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})



def aktualnosci(request):
    articles = Article.objects.all()
    return render(request, 'article_list.html', {'articles': articles})


def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    return render(request, 'article_detail.html', {'article': article})

def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('aktualnosci')
    else:
        form = ArticleForm()
    return render(request, 'add_article.html', {'form': form})

def article_list(request):
    articles = Article.objects.all()
    return render(request, 'article_list.html', {'articles': articles})




def add_event(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        formset = FightFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            event = form.save(commit=False)
            event.save()
            fights = formset.save(commit=False)
            for fight in fights:
                fight.save()
                event.fights.add(fight)
            return redirect('event_list')
    else:
        form = EventForm()
        formset = FightFormSet(queryset=Fight.objects.none())
    return render(request, 'add_event.html', {'form': form, 'formset': formset})

def event_list(request):
    events = Event.objects.prefetch_related('fights').all()
    return render(request, 'event_list.html', {'events': events})

class EventDetailView(DetailView):
    model = Event
    template_name = 'event_detail.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.object
        context['form'] = BetForm()
        return context

from django.shortcuts import render
from .forms import FighterStatsForm


def create_fighter(request):
    if request.method == 'POST':
        form = FighterStatsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fighters')
    else:
        form = FighterStatsForm()

    return render(request, 'create_fighter.html', {'form': form})

def add_fighter(request):
    if request.method == 'POST':
        form = FighterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fighters')
    else:
        form = FighterForm()
    return render(request, 'add_fighter.html', {'form': form})

class FightHighlightListView(View):
    def get(self, request):
        highlights = FightHighlight.objects.all()
        form = FightHighlightForm()
        return render(request, 'fight_highlights_list.html', {'highlights': highlights, 'form': form})

    def post(self, request):
        form = FightHighlightForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('fight_highlights_list'))
        highlights = FightHighlight.objects.all()
        return render(request, 'fight_highlights_list.html', {'highlights': highlights, 'form': form})


class EventDetailView(DetailView):
    model = Event
    template_name = 'event_detail.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.get_object()
        context['form'] = BetForm(event=event)
        return context

@login_required
def bet_on_fight(request, fight_id):
    fight = get_object_or_404(Fight, pk=fight_id)
    user = request.user

    if request.method == 'POST':
        form = BetForm(request.POST)
        if form.is_valid():
            choice = form.cleaned_data['choice']
            points = form.cleaned_data['points']
            bet_points = BetPoints.objects.get_or_create(user=user)[0]

            if points > bet_points.points:
                error_message = "You don't have enough points."
                return render(request, 'bet_on_fight.html', {'fight': fight, 'error_message': error_message})

            if choice == 'fighter1_win':
                points += 1
            elif choice == 'fighter2_win':
                points += 1


            bet = Bet(user=user, fight=fight, points=points)
            bet.save()

            bet_points.points -= points
            bet_points.save()

            return redirect('event_detail', pk=fight.event.pk)

    else:
        form = BetForm()

    return render(request, 'bet_on_fight.html', {'fight': fight, 'form': form})

def bet_ranking(request):
    ranking = BetPoints.objects.order_by('-points')
    return render(request, 'bet_ranking.html', {'ranking': ranking})




def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    form = BetForm(instance=event)
    return render(request, 'event_detail.html', {'event': event, 'form': form})