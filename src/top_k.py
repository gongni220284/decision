from pathlib import Path
from typing import Dict, List


def top_k_etus(matching: Dict[str, List[str]],
               prefs_etus: Dict[str, List[str]],
               k: int):
    nb_etus = len(prefs_etus)
    scores = []
    etu_uni = {}
    for uni, etus in matching.items():
        for etu in etus:
            etu_uni[etu] = uni

    for etu, prefs in prefs_etus.items():
        uni_assign = etu_uni.get(etu)

        if uni_assign is not None:
            rang = prefs.index(uni_assign)

            if rang < k:
                # Score pondéré selon le rang
                score = 1 - (rang / k)
            else:
                score = 0

            scores.append(score)
        else:
            scores.append(0)

    return sum(scores) / nb_etus

def top_k_unis(matching: Dict[str, List[str]],
               prefs_unis: Dict[str, List[str]],
               k: int):
    
    scores = []
    print(type(prefs_unis))
    for uni, prefs in prefs_unis.items():
        etudiants = matching.get(uni, [])
        for etu in etudiants:
            classement = prefs.index(etu)

            if classement < k:
                score = 1 - (classement / k)
            else: 
                score = 0

            scores.append(score)

    return sum(scores) / len(scores) if scores else 0

def top_k_global(matching: Dict[str, List[str]],
                 prefs_unis: Dict[str, List[str]],
                 prefs_etus: Dict[str, List[str]],
                 k: int = 3, alpha: float = 0.9):
    score_etu = top_k_etus(matching, prefs_etus, k)
    score_uni = top_k_unis(matching, prefs_unis, k)
 
    score = alpha * score_etu + (1 - alpha) * score_uni

    return score, score_etu, score_uni

