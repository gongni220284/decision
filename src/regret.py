from pathlib import Path
from typing import List, Dict

def regret_etudiants(matching, matching_ideal, prefs_etus):
    assign = {etu: uni for uni, etus in matching.items() for etu in etus}
    assign_ideal = {etu: uni for uni, etus in matching_ideal.items() for etu in etus}

    regrets = []

    for etu, prefs in prefs_etus.items():
        n = len(prefs)

        uni = assign.get(etu)
        rank = prefs.index(uni) if uni in prefs else n - 1

        ideal_uni = assign_ideal.get(etu)
        ideal_rank = prefs.index(ideal_uni) if ideal_uni in prefs else n - 1

        regret = (rank - ideal_rank) / (n - 1)

        regrets.append(regret)

    return sum(regrets) / len(regrets)



def regret_universites(matching, matching_ideal, prefs_unis):
    regrets = []

    for uni, prefs in prefs_unis.items():
        n = len(prefs)

        accepted = matching.get(uni, [])
        accepted_ideal = matching_ideal.get(uni, [])

        rank = max((prefs.index(s) for s in accepted), default=n - 1)
        rank_opt = max((prefs.index(s) for s in accepted_ideal), default=n - 1)

        regret = (rank - rank_opt) / (n - 1)
        regrets.append(regret)

    return sum(regrets) / len(regrets)


def regret_global(
    matching: Dict[str, List[str]],
    matching_ideal_uni: Dict[str, List[str]],
    prefs_etus: Dict[str, List[str]],
    prefs_unis: Dict[str, List[str]]
):
    r_etu = regret_etudiants(matching, matching, prefs_etus)
    r_uni = regret_universites(matching, matching_ideal_uni, prefs_unis)

    print(r_etu)
    print(r_uni)
    

    return (r_etu, r_uni, (r_etu + r_uni) / 2)
