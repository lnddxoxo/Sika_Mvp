from django.db import models
from datetime import date


class CoursHistorique(models.Model):
    ticker         = models.CharField(max_length=10)
    date           = models.DateField()
    ouverture      = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    plus_haut      = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    plus_bas       = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    cloture        = models.DecimalField(max_digits=12, decimal_places=2)
    volume         = models.IntegerField(default=0)
    valeur         = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    variation      = models.DecimalField(max_digits=6,  decimal_places=2, default=0)
    capitalisation = models.DecimalField(max_digits=25, decimal_places=2, null=True)

    class Meta:
        unique_together = ['ticker', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.ticker} — {self.date} — {self.cloture} FCFA"


class DonneesFondamentales(models.Model):
    ticker       = models.CharField(max_length=10, unique=True)
    nom_societe  = models.CharField(max_length=100)
    secteur      = models.CharField(max_length=50)
    benefice_net = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    actif_net    = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    nb_actions   = models.BigIntegerField(null=True)
    dividende    = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    notation     = models.CharField(max_length=10, blank=True)
    mise_a_jour  = models.DateField(auto_now=True)

    @property
    def bpa(self):
        if self.benefice_net and self.nb_actions and self.nb_actions > 0:
            return float(self.benefice_net) / self.nb_actions
        return None

    @property
    def actif_net_par_action(self):
        if self.actif_net and self.nb_actions and self.nb_actions > 0:
            return float(self.actif_net) / self.nb_actions
        return None

    def __str__(self):
        return f"{self.ticker} — {self.nom_societe}"


class SignalJournalier(models.Model):
    ticker     = models.CharField(max_length=10)
    date       = models.DateField(default=date.today)
    cours      = models.DecimalField(max_digits=12, decimal_places=2)

    # Technique
    rsi        = models.DecimalField(max_digits=6,  decimal_places=2, null=True)
    mm20       = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    mm50       = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    boll_sup   = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    boll_inf   = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    vol_ratio  = models.DecimalField(max_digits=6,  decimal_places=2, null=True)
    variation  = models.DecimalField(max_digits=6,  decimal_places=2, null=True)

    # Fondamental calculé
    per        = models.DecimalField(max_digits=8,  decimal_places=2, null=True)
    pbr        = models.DecimalField(max_digits=8,  decimal_places=2, null=True)
    dy         = models.DecimalField(max_digits=6,  decimal_places=2, null=True)
    roe        = models.DecimalField(max_digits=6,  decimal_places=2, null=True)

    # Moyennes sectorielles du jour (calculées dynamiquement)
    per_secteur        = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    pbr_secteur        = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    dy_secteur         = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    variation_secteur  = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    perf_vs_secteur    = models.DecimalField(max_digits=6, decimal_places=2, null=True)

    # Scores et signal
    score_fonda = models.IntegerField(default=0)
    score_tech  = models.IntegerField(default=0)
    signal      = models.CharField(max_length=20, default='NEUTRE')

    # Interprétations texte
    interp_rsi  = models.CharField(max_length=200, blank=True)
    interp_mm   = models.CharField(max_length=200, blank=True)
    interp_boll = models.CharField(max_length=200, blank=True)

    class Meta:
        unique_together = ['ticker', 'date']
        ordering = ['-score_tech', '-score_fonda']

    def __str__(self):
        return f"{self.ticker} — {self.date} — {self.signal}"