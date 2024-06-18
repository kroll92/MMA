from django.contrib import admin
from .models import Article, Event, Fighter, Fight, FighterStats, FightHighlight

admin.site.register(Article)
admin.site.register(Event)
admin.site.register(Fighter)
admin.site.register(Fight)
admin.site.register(FighterStats)
admin.site.register(FightHighlight)