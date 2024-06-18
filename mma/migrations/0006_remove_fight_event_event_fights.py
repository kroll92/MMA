# Generated by Django 5.0.6 on 2024-06-18 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mma', '0005_remove_event_fights_fight_event'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fight',
            name='event',
        ),
        migrations.AddField(
            model_name='event',
            name='fights',
            field=models.ManyToManyField(related_name='events', to='mma.fight'),
        ),
    ]