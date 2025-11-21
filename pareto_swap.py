from stable_marriage import est_stable

def pareto_swap_stable(appariements, prefs_etudiants, prefs_etablissements):
    # Construire affectation e -> s
    affectation = {}
    for eta, etus in appariements.items():
        for e in etus:
            affectation[e] = eta

    etudiants = list(affectation.keys())

    for i in range(len(etudiants)):
        for j in range(i+1, len(etudiants)):
            e1, e2 = etudiants[i], etudiants[j]
            s1, s2 = affectation[e1], affectation[e2]

            # Vérifier si swap est un Pareto-improvement côté élèves
            if (prefs_etudiants[e1].index(s2) < prefs_etudiants[e1].index(s1) and
                prefs_etudiants[e2].index(s1) < prefs_etudiants[e2].index(s2)):

                # Test nouveau matching
                nouveau = {eta: list(etu_list) for eta, etu_list in appariements.items()}
                nouveau[s1] = [e2]
                nouveau[s2] = [e1]

                # Vérifier stabilité
                if est_stable(nouveau, prefs_etudiants, prefs_etablissements):
                    print(f"\n✔ Swap stable trouvé : {e1} ↔ {e2}")
                    return nouveau

    print("\nAucun Pareto swap stable possible.")
    return appariements