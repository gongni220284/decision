from typing import Dict, List
import math

def satisfaction_individuelle(rang: int, taille: int) -> float:
    """
    Convertit un rang (0-indexé) et la taille de la liste
    en une satisfaction normalisée entre 0 et 1 :
    S = (n - r - 1) / (n - 1)
    """
    if taille <= 1:
        return 1.0
    return (taille - rang - 1) / (taille - 1)


def satisfaction_croisee_globale(
    matching: Dict[str, List[str]],
    prefs_etus: Dict[str, List[str]],
    prefs_unis: Dict[str, List[str]]
) -> float:
    """
    Calcule un score global de satisfaction croisée
    entre étudiants et universités, basé sur la moyenne
    harmonique des satisfactions individuelles.

    Retourne un score entre 0 et 1.
    """

    scores_pairs = []

    for uni, etus in matching.items():
        prefs_uni = prefs_unis[uni]
        taille_uni = len(prefs_uni)

        for etu in etus:
            # Si l'étudiant n'a pas de préférences, on ignore
            if etu not in prefs_etus:
                continue

            prefs_etu = prefs_etus[etu]
            taille_etu = len(prefs_etu)

            # Rang de l'université dans la liste de l'étudiant
            if uni not in prefs_etu:
                # L'étudiant n'a pas classé cette université : satisfaction nulle côté étudiant
                S_etu = 0.0
            else:
                rang_etu = prefs_etu.index(uni)
                S_etu = satisfaction_individuelle(rang_etu, taille_etu)

            # Rang de l'étudiant dans la liste de l'université
            if etu not in prefs_uni:
                S_uni = 0.0
            else:
                rang_uni = prefs_uni.index(etu)
                S_uni = satisfaction_individuelle(rang_uni, taille_uni)

            if S_etu <= 0 or S_uni <= 0:
                S_cross = 0.0
            else:
                S_cross = 2 * S_etu * S_uni / (S_etu + S_uni)

            scores_pairs.append(S_cross)

    if not scores_pairs:
        return 0.0

    return sum(scores_pairs) / len(scores_pairs)
