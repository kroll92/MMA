from django.db import models
from django.utils import timezone
from django import forms
from django.urls import reverse


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
        return reverse('fighter-details', args=[str(self.id)])

    def __str__(self):
        return self.name

class Fight(models.Model):
    fighter1 = models.ForeignKey(Fighter, on_delete=models.CASCADE, related_name="fighter1")
    fighter2 = models.ForeignKey(Fighter, on_delete=models.CASCADE, related_name="fighter2")


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    fights = models.ManyToManyField(Fight)

class FighterStats(models.Model):
    fighter = models.OneToOneField(Fighter, on_delete=models.CASCADE)

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
        return self.fighter.name


