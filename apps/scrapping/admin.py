from django.contrib import admin
from .models import CoursHistorique, DonneesFondamentales, SignalJournalier

@admin.register(CoursHistorique)
class CoursHistoriqueAdmin(admin.ModelAdmin):
    list_display  = ['ticker', 'date', 'cloture', 'variation', 'volume', 'capitalisation']
    list_filter   = ['ticker', 'date']
    search_fields = ['ticker']
    ordering      = ['-date']

@admin.register(DonneesFondamentales)
class DonneesFondamentalesAdmin(admin.ModelAdmin):
    list_display  = ['ticker', 'nom_societe', 'secteur', 'benefice_net', 'nb_actions', 'dividende']
    search_fields = ['ticker', 'nom_societe']

@admin.register(SignalJournalier)
class SignalJournalierAdmin(admin.ModelAdmin):
    list_display  = ['ticker', 'date', 'cours', 'score_fonda', 'score_tech', 'signal', 'rsi', 'per', 'dy', 'vol_ratio']
    list_filter   = ['signal', 'date']
    search_fields = ['ticker']
    ordering      = ['-score_tech', '-score_fonda']