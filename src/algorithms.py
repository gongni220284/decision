import json
import random
from pathlib import Path
from typing import Dict, List
import typer
from utils import load_data_from_json
from datetime import datetime

app = typer.Typer()



def gale_shapley_etudiant_otimal(prefs_etus: Dict[str, List[str]],
                                 prefs_unis: Dict[str, List[str]],
                                 capacities: Dict[str, int]) -> Dict[str, List[str]]:
    
    free = list(prefs_etus.keys())

    next_dem =  {s: 0 for s in prefs_etus}
    matching = {u: [] for u in prefs_unis}

    while free:
        etu = free.pop(0)
        prefs = prefs_etus[etu]

        if next_dem[etu] >= len(prefs): continue

        uni = prefs[next_dem[etu]]
        next_dem[etu] += 1

        if len(matching[uni]) < capacities[uni]:
            matching[uni].append(etu)
        else:
            classement = prefs_unis[uni]
            pire = max(matching[uni], key = lambda x: classement.index(x))

            if classement.index(etu) < classement.index(pire):
                matching[uni].remove(pire)
                matching[uni].append(etu)
                free.append(pire)
            else: free.append(etu)

    return matching


def gale_shapley_university_optimal(prefs_etus: Dict[str, List[str]],
                                    prefs_unis: Dict[str, List[str]],
                                    capacities: Dict[str, int]) -> Dict[str, List[str]]:
    
    free = list(prefs_unis.keys())
    next_dem = {u: 0 for u in prefs_unis}
    matching = {u: [] for u in prefs_unis}
    etus_assign = {s: None for s in prefs_etus}

    while free:
        uni = free.pop(0)
        if next_dem[uni] >= len(prefs_unis[uni]):
            continue

        etu = prefs_unis[uni][next_dem[uni]]
        next_dem[uni] += 1

        current = etus_assign[etu]

        if current is None:
            etus_assign[etu] = uni
            matching[uni].append(etu)
        else:
            classement = prefs_etus[etu]
            if classement.index(uni) < classement.index(current):
                matching[current].remove(etu)
                matching[uni].append(etu)
                etus_assign[etu] = uni
                free.append(current)
            else:
                free.append(uni)

    return matching

def est_stable(matching: Dict[str, List[str]],
               prefs_etus: Dict[str, List[str]],
               prefs_unis: Dict[str, List[str]]):

    # affectation étu -> uni
    assigned = {}
    for uni, etus in matching.items():
        for s in etus:
            assigned[s] = uni

    for etu, prefs in prefs_etus.items():
        assigned_uni = assigned.get(etu)

        for uni in prefs:
            if uni == assigned_uni:
                break

            assigned_list = matching[uni]
            classement = prefs_unis[uni]

            if not assigned_list:
                return False, (etu, uni)

            pire = max(assigned_list, key=lambda x: classement.index(x))

            if classement.index(etu) < classement.index(pire):
                return False, (etu, uni)

    return True, None

