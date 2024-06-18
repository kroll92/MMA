from django.shortcuts import get_object_or_404
from .models import Article
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import Event, Fight, Fighter, FightHighlight, Fight, Article
from .forms import EventForm, FightFormSet, FighterForm, FightHighlightForm, ArticleForm, FighterSearchForm
from django.views.generic import DetailView, DeleteView
from django.urls import reverse, reverse_lazy
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


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


def fighter_detail(request, fighter_id):
    fighter = get_object_or_404(Fighter, pk=fighter_id)
    return render(request, 'fighter_detail.html', {'fighter': fighter})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'error_message': 'Nieprawidłowe dane logowania'})

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


def logout_view(request):
    logout(request)
    return redirect('index')


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
            print(f"Event '{event.title}' saved successfully with {event.fights.count()} fights.")
            return redirect('event_list')
        else:
            print("Form or formset is invalid.")
            print(form.errors)
            print(formset.errors)
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


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'event_detail.html', {'event': event})


from .models import Article
from .forms import ArticleForm


@login_required
def edit_article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('article_detail', article_id=article.id)
    else:
        form = ArticleForm(instance=article)

    return render(request, 'edit_article.html', {'form': form, 'article': article})


class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy('article_list')  # Przekierowanie na listę artykułów po usunięciu
    template_name = 'article_confirm_delete.html'


def search_fighters(request):
    form = FighterSearchForm(request.GET)
    fighters = []

    if form.is_valid():
        search_query = form.cleaned_data['search_query']
        fighters = Fighter.objects.filter(name__icontains=search_query)

    return render(request, 'search_fighters.html', {'form': form, 'fighters': fighters})
