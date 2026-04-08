from django.db import models
from datetime import date
from utils.calcul_t3 import calculer_t3
from constants.concours import CONCOURS


class Transaction(models.Model):

    TYPE_CHOICES  = [('achat', 'Achat'), ('vente', 'Vente')]
    ORDRE_CHOICES = [('marche', 'Au marché'), ('limite', 'À cours limité')]

    ticker           = models.CharField(max_length=10)
    type_transaction = models.CharField(max_length=10, choices=TYPE_CHOICES)
    type_ordre       = models.CharField(max_length=10, choices=ORDRE_CHOICES, default='marche')
    quantite         = models.IntegerField()
    prix_execution   = models.DecimalField(max_digits=12, decimal_places=2)
    date_transaction = models.DateField(default=date.today)
    date_t3          = models.DateField(null=True, blank=True)
    frais_courtage   = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    montant_total    = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    stop_loss        = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    objectif_1       = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    objectif_2       = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    objectif_3       = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    justification    = models.TextField(blank=True)
    cloturee         = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        montant_brut        = self.quantite * float(self.prix_execution)
        self.frais_courtage = round(montant_brut * CONCOURS['frais_courtage'], 2)
        self.montant_total  = round(montant_brut + self.frais_courtage, 2)
        if not self.date_t3:
            self.date_t3 = calculer_t3(self.date_transaction)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.ticker} — {self.type_transaction} — {self.date_transaction}"