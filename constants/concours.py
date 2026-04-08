from datetime import date

CONCOURS = {
    # ── DATES ──────────────────────────────────────────────
    'debut':                     date(2026, 4, 7),
    'deadline_1ere_transaction': date(2026, 4, 18),  # URGENT — sinon élimination
    'deadline_80pct':            date(2026, 5, 8),   # 80% investi + 4 secteurs + obligations
    'deadline_justifications':   date(2026, 5, 8),   # envoyer justifications avril à l'arbitre
    'debut_liberte':             date(2026, 5, 9),   # liberté totale sur l'allocation
    'dernier_achat':             date(2026, 5, 31),  # T+3 = vendable le 5 juin max
    'cloture':                   date(2026, 6, 8),   # TOUT VENDRE avant 14h59

    # ── CAPITAL ────────────────────────────────────────────
    'capital_initial':           20_000_000,
    'bonus_fille':                  500_000,         # équipe avec au moins 1 fille
    'capital_reel':              20_500_000,         # capital_initial + bonus_fille

    # ── RÈGLES INVESTISSEMENT ──────────────────────────────
    'min_investi_pct':           0.80,               # 80% du capital avant le 8 mai
    'min_actions_fcfa':          13_120_000,         # 64% en actions BRVM
    'min_obligations_fcfa':       3_280_000,         # 16% en obligations UMOA
    'max_par_action_pct':        0.10,               # max 10% du portefeuille par action
    'min_secteurs':              4,                  # minimum 4 secteurs différents

    # ── FRAIS ──────────────────────────────────────────────
    'frais_courtage':            0.013,              # 1.3% à l'achat ET à la vente
    'frais_aller_retour':        0.026,              # 2.6% total aller-retour

    # ── SÉANCE ─────────────────────────────────────────────
    'heure_ouverture':           '09:00',
    'heure_cloture':             '14:59',            # FAQ dit 14h59 pas 15h00

    # ── ORDRES ─────────────────────────────────────────────
    'validite_ordre_jours':      7,                  # ordre purgé après 1 semaine
    'ordre_purge_si_limite':     True,               # purgé si limite 10% atteinte

    # ── CLASSEMENT ─────────────────────────────────────────
    'classement_sur':            'liquidites',       # pas la valeur du portefeuille
    'classement_calcule':        'chaque_soir',      # après clôture chaque jour

    # ── PRIMES HEBDOMADAIRES ───────────────────────────────
    'prime_1er':                 10_000,             # FCFA réels chaque lundi
    'prime_2eme':                 5_000,
    'prime_3eme':                 2_500,

    # ── PHASE ──────────────────────────────────────────────
    'phase':                     'virtuel',          # changer en 'reel' le 8 juin
    'impot_pv':                  0,                  # 0 en virtuel, 0.01 en réel
    'retenue_dividende':         0,                  # 0 en virtuel, 0.10 en réel

    # ── TRADING RÉEL (après qualification) ─────────────────
    'debut_reel':                date(2026, 6, 8),
    'fin_reel':                  date(2026, 7, 10),
    'capital_reel_phase2':       1_000_000,          # 1M FCFA réel par équipe
    'elimination_perte_reel':    0.25,               # -25% = élimination
}