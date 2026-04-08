import pandas as pd
import logging
from datetime import date, timedelta
from django.db.models import Avg

logger = logging.getLogger(__name__)

# --- CALCULS DES MOYENNES SECTORIELLES ---

def calculer_moyennes_sectorielles():
    """
    Calcule les moyennes PER/PBR/DY/ROE par secteur à partir des données RÉELLES.
    """
    from apps.scrapping.models import SignalJournalier
    from constants.brvm30 import BRVM30
    
    secteurs = {}
    # Grouper les données par secteur
    for ticker, info in BRVM30.items():
        secteur = info["secteur"]
        if secteur not in secteurs:
            secteurs[secteur] = {"pers": [], "pbrs": [], "dys": [], "roes": []}
        
        signal = SignalJournalier.objects.filter(ticker=ticker, date=date.today()).first()
        if signal:
            if signal.per: secteurs[secteur]["pers"].append(float(signal.per))
            if signal.pbr: secteurs[secteur]["pbrs"].append(float(signal.pbr))
            if signal.dy: secteurs[secteur]["dys"].append(float(signal.dy))
            if signal.roe: secteurs[secteur]["roes"].append(float(signal.roe))

    # Calculer les moyennes
    moyennes = {}
    for secteur, data in secteurs.items():
        moyennes[secteur] = {
            "per_moyen": round(sum(data["pers"])/len(data["pers"]), 2) if data["pers"] else None,
            "pbr_moyen": round(sum(data["pbrs"])/len(data["pbrs"]), 2) if data["pbrs"] else None,
            "dy_moyen": round(sum(data["dys"])/len(data["dys"]), 2) if data["dys"] else None,
            "roe_moyen": round(sum(data["roes"])/len(data["roes"]), 2) if data["roes"] else None,
        }
    return moyennes

def get_moyenne_secteur(secteur):
    DEFAUTS = {
        "Services financiers": {"per_moyen": 9.0, "pbr_moyen": 1.2, "dy_moyen": 7.0, "roe_moyen": 18.0},
        "Telecommunications": {"per_moyen": 14.0, "pbr_moyen": 3.5, "dy_moyen": 5.5, "roe_moyen": 20.0},
        "Energie": {"per_moyen": 12.0, "pbr_moyen": 2.0, "dy_moyen": 4.0, "roe_moyen": 15.0},
        "Agro-industrie": {"per_moyen": 10.0, "pbr_moyen": 1.8, "dy_moyen": 3.5, "roe_moyen": 14.0},
        "Consommation de base": {"per_moyen": 11.0, "pbr_moyen": 2.2, "dy_moyen": 3.8, "roe_moyen": 13.0},
        "Distribution": {"per_moyen": 9.0, "pbr_moyen": 1.5, "dy_moyen": 3.0, "roe_moyen": 12.0},
        "Transport": {"per_moyen": 7.0, "pbr_moyen": 1.0, "dy_moyen": 2.5, "roe_moyen": 10.0},
        "Industries": {"per_moyen": 9.5, "pbr_moyen": 1.6, "dy_moyen": 3.2, "roe_moyen": 11.0},
    }
    moyennes = calculer_moyennes_sectorielles()
    if secteur in moyennes and moyennes[secteur]["per_moyen"]:
        return moyennes[secteur]
    return DEFAUTS.get(secteur, {"per_moyen": 10.0, "pbr_moyen": 1.5, "dy_moyen": 4.0, "roe_moyen": 12.0})

# --- INDICATEURS TECHNIQUES ---

def calculer_rsi(ticker, periode=14):
    from apps.scrapping.models import CoursHistorique
    qs = CoursHistorique.objects.filter(ticker=ticker).order_by("date").values("cloture")
    if qs.count() < periode + 1: return None
    df = pd.DataFrame(list(qs))
    df["cloture"] = df["cloture"].astype(float)
    delta = df["cloture"].diff()
    gain = delta.clip(lower=0).rolling(periode).mean()
    perte = (-delta.clip(upper=0)).rolling(periode).mean()
    rsi = 100 - (100 / (1 + gain / perte))
    return round(float(rsi.iloc[-1]), 2)

def calculer_mm(ticker, periode=20):
    from apps.scrapping.models import CoursHistorique
    qs = CoursHistorique.objects.filter(ticker=ticker).order_by("date").values("cloture")
    if qs.count() < periode: return None
    df = pd.DataFrame(list(qs))
    mm = df["cloture"].astype(float).rolling(periode).mean()
    return round(float(mm.iloc[-1]), 2)

def calculer_bollinger(ticker, periode=20):
    from apps.scrapping.models import CoursHistorique
    qs = CoursHistorique.objects.filter(ticker=ticker).order_by("date").values("cloture")
    if qs.count() < periode: return None, None
    df = pd.DataFrame(list(qs))
    c = df["cloture"].astype(float)
    mm = c.rolling(periode).mean()
    std = c.rolling(periode).std()
    return (round(float((mm + 2*std).iloc[-1]), 2), round(float((mm - 2*std).iloc[-1]), 2))

def calculer_vol_ratio(ticker, periode=20):
    from apps.scrapping.models import CoursHistorique
    qs = CoursHistorique.objects.filter(ticker=ticker).order_by("date").values("volume")
    if qs.count() < 2: return None
    df = pd.DataFrame(list(qs))
    moy = float(df["volume"].rolling(periode).mean().iloc[-1])
    if moy == 0: return None
    return round(float(df["volume"].iloc[-1]) / moy, 2)

# --- SYSTEME DE SCORING ---

def score_rsi(rsi):
    if rsi is None: return 0
    if rsi < 25: return 30
    if rsi < 30: return 25
    if rsi < 40: return 15
    if rsi < 50: return 8
    if rsi < 70: return 0
    return -20

def score_mm(cours, mm20, mm50):
    if not mm20 or not cours: return 0
    if mm50 and cours > mm20 > mm50: return 25
    if cours > mm20: return 15
    return -10

def score_bollinger(cours, boll_sup, boll_inf, mm20):
    if not cours: return 0
    if boll_inf and cours <= boll_inf: return 20
    if boll_sup and cours >= boll_sup: return -20
    return 0

def score_volume(vol_ratio):
    if vol_ratio is None: return 0
    if vol_ratio > 2.0: return 20
    if vol_ratio > 1.0: return 8
    return 0

def calculer_score_tech(rsi, mm20, mm50, boll_sup, boll_inf, cours, vol_ratio):
    s = 50 
    s += score_rsi(rsi)
    s += score_mm(cours, mm20, mm50)
    s += score_bollinger(cours, boll_sup, boll_inf, mm20)
    s += score_volume(vol_ratio)
    return max(0, min(100, s))

def calculer_score_fonda(per, pbr, dy, roe, div_pts, endettement, secteur):
    moy = get_moyenne_secteur(secteur)
    s = 50
    if per and moy.get("per_moyen"):
        r = per / moy["per_moyen"]
        if r < 0.80: s += 20
        elif r > 1.30: s -= 10
    if pbr:
        if pbr < 1.00: s += 15
        elif pbr > 3.00: s -= 5
    if dy and moy.get("dy_moyen"):
        r = dy / moy["dy_moyen"]
        if r > 1.2: s += 15
    return max(0, min(100, s))

# --- GENERATION DES SIGNAUX ---

def signal_global(score_fonda, score_tech):
    score_final = (score_tech * 0.60) + (score_fonda * 0.40)
    if score_final >= 65: return "ACHETER"
    if score_final >= 40: return "ATTENDRE"
    return "EVITER"

def calculer_signal_ticker(ticker):
    from apps.scrapping.models import CoursHistorique, SignalJournalier, DonneesFondamentales
    from constants.brvm30 import BRVM30
    
    dernier = CoursHistorique.objects.filter(ticker=ticker).order_by("-date").first()
    if not dernier: return None
    
    cours = float(dernier.cloture)
    var = float(dernier.variation)
    sect = BRVM30.get(ticker, {}).get("secteur", "Inconnu")
    
    try: fonda = DonneesFondamentales.objects.get(ticker=ticker)
    except: fonda = None

    rsi = calculer_rsi(ticker)
    mm20 = calculer_mm(ticker, 20)
    mm50 = calculer_mm(ticker, 50)
    b_sup, b_inf = calculer_bollinger(ticker)
    vol_ratio = calculer_vol_ratio(ticker)

    per = round(cours / fonda.bpa, 2) if fonda and fonda.bpa else None
    pbr = round(cours / fonda.actif_net_par_action, 2) if fonda and fonda.actif_net_par_action else None
    dy = round((float(fonda.dividende) / cours) * 100, 2) if fonda and fonda.dividende and cours > 0 else None
    
    moy = get_moyenne_secteur(sect)
    s_tech = calculer_score_tech(rsi, mm20, mm50, b_sup, b_inf, cours, vol_ratio)
    s_fonda = calculer_score_fonda(per, pbr, dy, None, 5, None, sect)
    signal = signal_global(s_fonda, s_tech)

    SignalJournalier.objects.update_or_create(
        ticker=ticker, date=date.today(),
        defaults={
            "cours": cours, "variation": var,
            "rsi": rsi, "mm20": mm20, "mm50": mm50,
            "boll_sup": b_sup, "boll_inf": b_inf, "vol_ratio": vol_ratio,
            "per": per, "pbr": pbr, "dy": dy,
            "per_secteur": moy.get("per_moyen"),
            "dy_secteur": moy.get("dy_moyen"),
            "score_fonda": s_fonda, "score_tech": s_tech, "signal": signal,
        }
    )
    return signal

def calculer_tous_les_signaux():
    from constants.brvm30 import BRVM30_TICKERS
    for t in BRVM30_TICKERS:
        try:
            calculer_signal_ticker(t)
        except Exception as e:
            logger.error(f"Erreur sur le ticker {t}: {e}")