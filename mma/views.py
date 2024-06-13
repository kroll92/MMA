from django.shortcuts import render, get_object_or_404
from .models import Article
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import Event, Fight, Fighter
from .forms import EventForm, FightFormSet, FighterForm
from django.views.generic import DetailView

def index(request):
    return render(request, 'index.html')


def aktualnosci(request):
    return render(request, 'aktualnosci.html')


def events(request):
    return render(request, 'events.html')


def skroty_walk(request):
    return render(request, 'skroty_walk.html')


def fighters(request):
    all_fighters = Fighter.objects.all()
    return render(request, 'fighters.html', {'fighters': all_fighters})

class FighterDetailView(DetailView):
    model = Fighter
    template_name = 'fighter_detail.html'

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
    return render(request, 'aktualnosci.html', {'articles': articles})


def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    return render(request, 'article_detail.html', {'article': article})



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
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm()
        formset = FightFormSet(queryset=Fight.objects.none())
    return render(request, 'add_event.html', {'form': form, 'formset': formset})

from django.shortcuts import render
from .forms import FighterStatsForm


def create_fighter(request):
    if request.method == 'POST':
        form = FighterStatsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fighters')  # redirect to fighter's listing after successful creation
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