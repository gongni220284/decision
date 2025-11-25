# rotation_poset.py
from pathlib import Path
from typing import List, Dict
from copy import deepcopy
from algorithms import gale_shapley_etudiant_optimal
def build_shortlists(matching, prefs_students, prefs_unis):
    """
    Construit les shortlists (réduction des listes de préférence).
    Algorithme d'Irving : on supprime tous les partenaires impossibles.
    """
    S = deepcopy(prefs_students)
    U = deepcopy(prefs_unis)

    inv = {s: u for u, lst in matching.items() for s in lst}

    #  pour chaque étudiant, on coupe les universités en dessous de son match
    for s, prefs in S.items():
        u = inv.get(s)
        if u in prefs:
            cut = prefs.index(u)
            S[s] = prefs[:cut+1]

    #  pour chaque université, coupe sous le plus mauvais étudiant accepté
    for u, prefs in U.items():
        lst = matching[u]
        if lst:
            ranking = U[u]
            worst = max(lst, key=lambda x: ranking.index(x))
            cut = ranking.index(worst)
            U[u] = ranking[:cut+1]

    return S, U


def find_rotations(short_students, short_unis, matching):
    inv = {s: u for u, lst in matching.items() for s in lst}
    rotations = []

    for s in short_students.keys():
        u = inv[s]
        prefs = short_students[s]
        idx = prefs.index(u)

        if idx + 1 < len(prefs):
            # le suivant dans la shortlist
            u_next = prefs[idx + 1]

            # trouver celui qui bloque s->u_next
            ranking = short_unis[u_next]
            # étudiant préféré à u_next dans son worst-case
            s_next = ranking[-1]  # le pire dans la shortlist

            rotations.append([(s, u, u_next, s_next)])

    return rotations


def eliminate_rotation(matching, rotation, prefs_students, prefs_unis, capacities):
    """
    Élimine une rotation (dans version simplifiée : une rotation élémentaire).
    On force chaque s → u_next et relance GS restreint.
    """
    new_prefs = deepcopy(prefs_students)

    # Forcer la préférence du student vers u_next
    for (s, u, u_next, s_next) in rotation:
        # Placer u_next en premier
        lst = new_prefs[s]
        if u_next in lst:
            lst.remove(u_next)
        new_prefs[s] = [u_next] + lst

    # Relancer GS avec les prefs modifiées
    return gale_shapley_etudiant_optimal(new_prefs, prefs_unis, capacities)


def enumerate_all_stable_matchings(prefs_students, prefs_unis, capacities):

    match_opt = gale_shapley_etudiant_optimal(prefs_students, prefs_unis, capacities)
    short_s, short_u = build_shortlists(match_opt, prefs_students, prefs_unis)
    rotations = find_rotations(short_s, short_u, match_opt)

    all_matchings = {str(match_opt): match_opt}

    frontier = [match_opt]

    while frontier:
        m = frontier.pop()

        s_short, u_short = build_shortlists(m, prefs_students, prefs_unis)
        rots = find_rotations(s_short, u_short, m)

        for rot in rots:
            new_m = eliminate_rotation(m, rot, prefs_students, prefs_unis, capacities)
            key = str(new_m)
            if key not in all_matchings:
                all_matchings[key] = new_m
                frontier.append(new_m)

    return list(all_matchings.values())


