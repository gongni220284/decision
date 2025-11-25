from pathlib import Path
from typing import Dict, List


def frustration_etudiants(matching: Dict[str, List[str]], prefs_etus: Dict[str, List[str]], prefs_unis: Dict[str, List[str]]):

    etu_eta = {
        etu: eta
        for eta, etus in matching.items()
        for etu in etus
    }

    frustrations = []

    for etu, prefs in prefs_etus.items():
        eta_assigne = etu_eta.get(etu)

        # A_i : établissements préférés au match reçu
        if eta_assigne is not None:
            rank_assigned = prefs.index(eta_assigne)
            A_i = prefs[:rank_assigned]
        else:
            A_i = prefs[:]

        A_i = set(A_i)
        B_i = set()

        for eta in A_i:
            accepted = matching.get(eta, [])
            eta_prefs = prefs_unis[eta]

            if etu not in eta_prefs:
                continue

            rank_etu = eta_prefs.index(etu)

            for other in accepted:
                if other in eta_prefs:
                    if rank_etu < eta_prefs.index(other):
                        B_i.add(eta)
                        break

        f_i = len(B_i) / len(A_i) if A_i else 0.0
        frustrations.append(f_i)

    F_bar = sum(frustrations) / len(prefs_etus)
    F = 1 - F_bar
    return F_bar, F

def frustration_etablissements(matching: Dict[str, List[str]], prefs_etus: Dict[str, List[str]], prefs_unis: Dict[str, List[str]]):
    etu_eta = {
        etu: eta
        for eta, etus in matching.items()
        for etu in etus
    }

    frustrations = []

    for eta, eta_prefs in prefs_unis.items():
        accepted = matching.get(eta, [])
        A_j = set()
        B_j = set()

        # A_j : étudiants que l’établissement préfère à au moins un accepté
        for etu in eta_prefs:
            for other in accepted:
                if other in eta_prefs and eta_prefs.index(etu) < eta_prefs.index(other):
                    A_j.add(etu)
                    break

        # B_j : parmi A_j, ceux qui préfèrent cet établissement à leur match actuel
        for etu in A_j:
            prefs = prefs_etus[etu]
            assigned_eta = etu_eta.get(etu)
            if assigned_eta is None or prefs.index(eta) < prefs.index(assigned_eta):
                B_j.add(etu)

        f_j = len(B_j) / len(A_j) if A_j else 0.0
        frustrations.append(f_j)

    F_bar = sum(frustrations) / len(prefs_unis)
    F = 1 - F_bar
    return F_bar, F


def score_global_frustration(
    appariements,
    prefs_etudiants,
    prefs_etablissements,
    alpha=0.5
):


    Fbar_etu, stab_etu = frustration_etudiants(
        appariements, prefs_etudiants, prefs_etablissements
    )

    Fbar_uni, stab_uni = frustration_etablissements(
        appariements, prefs_etudiants, prefs_etablissements
    )

    score = alpha * stab_etu + (1 - alpha) * stab_uni

    return score, Fbar_etu, stab_etu, Fbar_uni, stab_uni





