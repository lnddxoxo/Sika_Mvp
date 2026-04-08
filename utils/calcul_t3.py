from datetime import date, timedelta

def calculer_t3(date_transaction):
    """T+3 jours ouvrés BRVM (lundi-vendredi)."""
    jours = 0
    d = date_transaction
    while jours < 3:
        d += timedelta(days=1)
        if d.weekday() < 5:  # 0-4 correspondent à Lundi-Vendredi
            jours += 1
    return d