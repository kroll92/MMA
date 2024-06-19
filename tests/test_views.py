from datetime import timezone

import pytest
from django.test import Client

@pytest.mark.django_db
def test_index_view(client):
    response = client.get(reverse('index'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_index_template(client):
    response = client.get(reverse('index'))
    assert 'index.html' in [template.name for template in response.templates]


@pytest.mark.django_db
def test_aktualnosci_template(client):
    response = client.get(reverse('article_list'))
    assert 'article_list.html' in [template.name for template in response.templates]

@pytest.mark.django_db
def test_aktualnosci_view(client):
    response = client.get(reverse('aktualnosci'))
    assert response.status_code == 200


@pytest.fixture
def create_fighters():
    fighters = [
        Fighter.objects.create(name='Fighter 1'),
        Fighter.objects.create(name='Fighter 2'),
        Fighter.objects.create(name='Fighter 3'),
    ]
    return fighters


@pytest.mark.django_db
def test_fighters_view(client: Client, create_fighters):
    url = reverse('fighters')
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.context['fighters']) == len(create_fighters)

    for fighter in create_fighters:
        assert fighter.name in str(response.content)


import pytest


@pytest.mark.django_db
def test_fighter_get_absolute_url():
    fighter = Fighter.objects.create(name='Test Fighter')
    expected_url = reverse('fighter_detail', args=[str(fighter.id)])

    assert fighter.get_absolute_url() == expected_url


import pytest

from mma.views import fighter_detail

from django.contrib.auth.models import User


@pytest.mark.django_db
def test_fighter_detail_view():
    user = mixer.blend(User)

    fighter = mixer.blend(Fighter, name='Test Fighter')

    factory = RequestFactory()

    url = reverse('fighter_detail', args=[fighter.id])

    request = factory.get(url)

    response = fighter_detail(request, fighter.id)

    assert response.status_code == 200


from django.test import TestCase

from mma.views import aktualnosci


class AktualnosciViewTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_aktualnosci_view_with_empty_list(self):
        request = self.factory.get('/aktualnosci/')
        response = aktualnosci(request)

        self.assertEqual(response.status_code, 200)

    def test_aktualnosci_view_with_articles(self):
        article1 = Article.objects.create(title='Artykuł 1', content='Treść artykułu 1')
        article2 = Article.objects.create(title='Artykuł 2', content='Treść artykułu 2')

        request = self.factory.get('/aktualnosci/')
        response = aktualnosci(request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Artykuł 1')
        self.assertContains(response, 'Artykuł 2')


from django.test import TestCase

from django.http import Http404
from mma.views import article_detail


class ArticleDetailViewTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_article_detail_view_with_existing_article(self):
        article = Article.objects.create(title='Test Article', content='Content of the test article')

        request = self.factory.get('/articles/1/')
        response = article_detail(request, article.id)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Article')
        self.assertContains(response, 'Content of the test article')

    def test_article_detail_view_with_nonexistent_article(self):
        request = self.factory.get('/articles/999/')
        with self.assertRaises(Http404):
            article_detail(request, 999)


import pytest
from mma.forms import ArticleForm, FighterStatsForm


@pytest.mark.django_db
def test_add_article_view_rendering_form():
    client = Client()

    response = client.get(reverse('add_article'))

    assert response.status_code == 200

    assert 'form' in response.context
    assert isinstance(response.context['form'], ArticleForm)


import pytest

@pytest.mark.django_db
def test_add_article_view_invalid_form():
    client = Client()

    form_data = {
        'title': '',
        'content': 'Test content for the article',
    }
    response = client.post(reverse('add_article'), form_data)

    assert response.status_code == 200

    assert 'form' in response.context
    assert response.context['form'].errors


import pytest
from mma.models import Article


@pytest.mark.django_db
def test_article_list_view_rendering():
    Article.objects.create(title='Article 1', content='Content of article 1')
    Article.objects.create(title='Article 2', content='Content of article 2')

    client = Client()

    response = client.get(reverse('article_list'))

    assert response.status_code == 200

    content = response.content.decode('utf-8')
    assert 'Article 1' in content
    assert 'Article 2' in content

@pytest.mark.django_db
def test_article_list_view():
    client = Client()

    article1 = Article.objects.create(title='Article 1', content='Content for article 1')
    article2 = Article.objects.create(title='Article 2', content='Content for article 2')
    article3 = Article.objects.create(title='Article 3', content='Content for article 3')

    response = client.get(reverse('article_list'))

    assert response.status_code == 200

    assert 'articles' in response.context
    assert len(response.context['articles']) == 3

    assert article1 in response.context['articles']
    assert article2 in response.context['articles']
    assert article3 in response.context['articles']


import pytest
from django.utils import timezone
from mma.models import Fight


@pytest.mark.django_db
def test_add_event_view(client):
    url = reverse('add_event')
    response = client.get(url)

    assert response.status_code == 200
    assert 'form' in response.context

    event_data = {
        'title': 'Test Event',
        'description': 'Test Description',
        'date': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),  # Przykładowa data
        'location': 'Test Location',
    }

    fighter1 = Fighter.objects.create(name='Fighter 1')
    fighter2 = Fighter.objects.create(name='Fighter 2')
    fight_formset_data = {
        'form-TOTAL_FORMS': '1',
        'form-INITIAL_FORMS': '0',
        'form-MIN_NUM_FORMS': '0',
        'form-MAX_NUM_FORMS': '1000',
        'form-0-fighter1': fighter1.id,
        'form-0-fighter2': fighter2.id,
    }

    post_data = {**event_data, **fight_formset_data}

    response = client.post(url, post_data)

    if response.status_code == 200:
        print(response.context['form'].errors)
        print(response.context['formset'].errors)

    assert response.status_code == 302
    assert Event.objects.filter(title='Test Event').exists()


@pytest.mark.django_db
def test_event_list_view_status_and_template(client):
    url = reverse('event_list')
    response = client.get(url)

    assert response.status_code == 200
    assert 'event_list.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_event_list_contains_events(client):
    Event.objects.create(title='Event 1', description='Description 1', date='2024-06-01 12:00', location='Location 1')
    Event.objects.create(title='Event 2', description='Description 2', date='2024-06-02 12:00', location='Location 2')

    url = reverse('event_list')
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.context['events']) == 2
    assert 'Event 1' in response.content.decode()
    assert 'Event 2' in response.content.decode()


@pytest.mark.django_db
def test_event_detail_view_status_and_template(client):
    event = Event.objects.create(
        title='Test Event',
        description='Test Description',
        date='2024-06-01 12:00',
        location='Test Location'
    )

    url = reverse('event_detail', kwargs={'pk': event.id})
    response = client.get(url)

    assert response.status_code == 200
    assert 'event_detail.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_event_detail_view_correct_data(client):
    fighter1 = Fighter.objects.create(name='Fighter 1')
    fighter2 = Fighter.objects.create(name='Fighter 2')
    fight = Fight.objects.create(fighter1=fighter1, fighter2=fighter2)

    event = Event.objects.create(
        title='Test Event',
        description='Test Description',
        date='2024-06-01 12:00',
        location='Test Location'
    )
    event.fights.add(fight)

    url = reverse('event_detail', kwargs={'pk': event.id})
    response = client.get(url)

    assert response.status_code == 200
    assert response.context['event'].title == 'Test Event'
    assert response.context['event'].description == 'Test Description'
    assert response.context['event'].date.strftime('%Y-%m-%d %H:%M') == '2024-06-01 12:00'
    assert response.context['event'].location == 'Test Location'
    assert response.context['event'].fights.count() == 1
    assert response.context['event'].fights.first() == fight


@pytest.mark.django_db
def test_create_fighter_get_request(client):
    url = reverse('create_fighter')
    response = client.get(url)

    assert response.status_code == 200
    assert isinstance(response.context['form'], FighterStatsForm)
    assert 'create_fighter.html' in [template.name for template in response.templates]


import pytest

from django.test import Client
from mma.models import Fighter, FighterStats, FightHighlight


@pytest.mark.django_db
def test_create_fighter_post_invalid_data(client):
    url = reverse('create_fighter')
    data = {
        'name': 'Test Fighter',
        'weight_class': 'InvalidWeightClass',
        'organization': 'UFC',
        'win_streak': 5,
        'knockout_wins': 3,
        'submission_wins': 2,
        'sig_strikes_landed': 150,
        'sig_strikes_attempted': 200,
        'takedowns_landed': 10,
        'takedowns_attempted': 15,
        'sig_strikes_landed_per_min': 3.50,
        'sig_strikes_absorbed_per_min': 2.75,
        'takedown_avg_per_15_min': 1.50,
        'submission_avg_per_15_min': 0.75,
        'sig_strike_defense': 60.0,
        'takedown_defense': 70.0,
        'knockdown_avg': 0.50,
        'avg_fight_time': '00:15:30',
    }

    response = client.post(url, data)

    assert response.status_code == 200

    assert isinstance(response.context['form'], FighterStatsForm)

    assert response.context['form'].errors


@pytest.mark.django_db
def test_fight_highlight_list_view_get(client):
    highlight1 = FightHighlight.objects.create(title='Highlight 1',
                                               youtube_url='https://www.youtube.com/watch?v=video1')
    highlight2 = FightHighlight.objects.create(title='Highlight 2',
                                               youtube_url='https://www.youtube.com/watch?v=video2')

    url = reverse('fight_highlights_list')
    response = client.get(url)

    assert response.status_code == 200

    assert highlight1.title in str(response.content)
    assert highlight2.title in str(response.content)


@pytest.mark.django_db
def test_fight_highlight_list_view_post(client):
    form_data = {
        'title': 'New Highlight',
        'youtube_url': 'https://www.youtube.com/watch?v=newvideo'
    }

    url = reverse('fight_highlights_list')

    response = client.post(url, form_data)

    assert response.status_code == 302

    assert FightHighlight.objects.filter(title='New Highlight').exists()


import pytest
from django.urls import reverse
from django.test import RequestFactory
from mixer.backend.django import mixer
from mma.models import Event


@pytest.mark.django_db
def test_event_detail_view(client):
    event = Event.objects.create(
        title='Sample Event',
        description='Sample description',
        date='2024-06-20 15:30',
        location='Sample location'
    )

    url = reverse('event_detail', kwargs={'pk': event.pk})

    response = client.get(url)

    assert response.status_code == 200

    print(response.content.decode('utf-8'))

    expected_content = 'Sample Event'
    assert expected_content in response.content.decode('utf-8')

@pytest.mark.django_db
def test_event_detail_view_not_found(client):
    url = reverse('event_detail', args=[9999])  # nieistniejące ID
    response = client.get(url)
    assert response.status_code == 404


@pytest.fixture
def article():
    return mixer.blend('mma.Article')


@pytest.mark.django_db
def test_edit_article_view_form(client, article):
    # Utwórz użytkownika i zaloguj go
    user = User.objects.create_user(username='testuser', password='password')
    client.login(username='testuser', password='password')

    url = reverse('edit_article', args=[article.pk])
    response = client.get(url)

    # Sprawdź, czy uzyskano poprawny kod odpowiedzi
    assert response.status_code == 200

    # Sprawdź zawartość odpowiedzi
    content = response.content.decode('utf-8')
    assert '<form' in content
    assert 'title' in content
    assert 'content' in content


@pytest.mark.django_db
def test_edit_article_view_redirect(client, article):
    url = reverse('edit_article', args=[article.pk])
    response = client.get(url)

    # Sprawdź, czy uzyskano przekierowanie do logowania
    assert response.status_code == 302
    assert '/accounts/login/' in response.url


import pytest
from django.urls import reverse
from django.test import Client
from mixer.backend.django import mixer
from mma.models import Article
@pytest.fixture
def article():
    return mixer.blend('mma.Article')

@pytest.mark.django_db
def test_delete_article_view(client, article):
    url = reverse('delete_article', args=[article.pk])
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_delete_article_redirect(client, article):
    url = reverse('delete_article', args=[article.pk])
    response = client.post(url)
    assert response.status_code == 302
    assert response.url == reverse('article_list')

from mma.forms import FighterSearchForm

@pytest.mark.django_db
def test_search_fighters_form_in_context(client):
    response = client.get(reverse('fighter_search') + '?search_query=John')
    assert 'form' in response.context
    assert isinstance(response.context['form'], FighterSearchForm)

@pytest.mark.django_db
def test_search_fighters_results(client):
    fighter = mixer.blend(Fighter, name='John Doe')
    response = client.get(reverse('fighter_search') + '?search_query=John')
    assert fighter.name in str(response.content)

