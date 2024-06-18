from django.db import models
from django.utils import timezone
from django import forms
from django.urls import reverse
from django.contrib.auth.models import User


class Article(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='articles/')
    content = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Events(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class Fighter(models.Model):
    name = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse('fighter_detail', args=[str(self.id)])

    def __str__(self):
        return self.name

class Fight(models.Model):
    fighter1 = models.ForeignKey(Fighter, on_delete=models.CASCADE, related_name="fighter1")
    fighter2 = models.ForeignKey(Fighter, on_delete=models.CASCADE, related_name="fighter2")

    def __str__(self):
        return f" {self.fighter1} vs. {self.fighter2}"

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    fights = models.ManyToManyField(Fight, related_name='events')

    def __str__(self):
        return self.title

class FighterStats(models.Model):
    WEIGHT_CLASSES = [
        ('Musza', 'Musza – 56 kg'),
        ('Kogucia', 'Kogucia – 61 kg'),
        ('Piórkowa', 'Piórkowa – 65 kg'),
        ('Lekka', 'Lekka – 70 kg'),
        ('Półśrednia', 'Półśrednia – 77 kg'),
        ('Średnia', 'Średnia – 84 kg'),
        ('Półciężka', 'Półciężka – 93 kg'),
        ('Ciężka', 'Ciężka – powyżej 93 kg'),
    ]

    ORGANIZATIONS = [
        ('UFC', 'UFC'),
        ('ONE FC', 'ONE FC'),
        ('ACA', 'ACA'),
    ]

    fighter = models.OneToOneField(Fighter, on_delete=models.CASCADE)
    weight_class = models.CharField(max_length=20, choices=WEIGHT_CLASSES, default='Musza')
    organization = models.CharField(max_length=50, choices=ORGANIZATIONS, default='UFC')

    win_streak = models.IntegerField()
    knockout_wins = models.IntegerField()
    submission_wins = models.IntegerField()

    sig_strikes_landed = models.IntegerField()
    sig_strikes_attempted = models.IntegerField()

    takedowns_landed = models.IntegerField()
    takedowns_attempted = models.IntegerField()

    sig_strikes_landed_per_min = models.DecimalField(max_digits=5, decimal_places=2)
    sig_strikes_absorbed_per_min = models.DecimalField(max_digits=5, decimal_places=2)

    takedown_avg_per_15_min = models.DecimalField(max_digits=5, decimal_places=2)
    submission_avg_per_15_min = models.DecimalField(max_digits=5, decimal_places=2)

    sig_strike_defense = models.DecimalField(max_digits=5, decimal_places=2)
    takedown_defense = models.DecimalField(max_digits=5, decimal_places=2)

    knockdown_avg = models.DecimalField(max_digits=5, decimal_places=2)
    avg_fight_time = models.DurationField()

    def __str__(self):
        return f"{self.fighter.name} {self.fighter.name}"

    def __str__(self):
        return self.fighter.name

class FightHighlight(models.Model):
    title = models.CharField(max_length=200)
    youtube_url = models.URLField()

    def __str__(self):
        return self.title
