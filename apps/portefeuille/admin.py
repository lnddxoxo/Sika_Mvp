from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display  = ['ticker', 'type_transaction', 'quantite', 'prix_execution',
                     'frais_courtage', 'montant_total', 'date_transaction', 'date_t3',
                     'stop_loss', 'objectif_1', 'objectif_2', 'objectif_3', 'cloturee']
    list_filter   = ['type_transaction', 'cloturee', 'ticker']
    search_fields = ['ticker']
    ordering      = ['-date_transaction']
    readonly_fields = ['frais_courtage', 'montant_total', 'date_t3']
    # → frais, montant et T+3 calculés automatiquement à la sauvegarde
    # → readonly pour ne pas les modifier manuellement