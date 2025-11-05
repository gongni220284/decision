
import random
import pandas as pd


def generer_preferences(nb_etudiants, nb_etablissements, capacite_etablissement):
    etudiants = [f"Etu{i+1}" for i in range(nb_etudiants)]
    etablissements = [f"Eta{j+1}" for j in range(nb_etablissements)]
    capacites = {etablissement: capacite_etablissement for etablissement in etablissements}
    
    # preferences des etudiants
    prefs_etudiants = {e: random.sample(etablissements, len(etablissements)) for e in etudiants}
    
    # preferences des etablissements
    prefs_etablissements = {e: random.sample(etudiants, len(etudiants)) for e in etablissements}
    
    return prefs_etudiants, prefs_etablissements, capacites


def gale_shapley(prefs_etudiants, prefs_etablissements, capacites):
    etudiants_libres = list(prefs_etudiants.keys()) 
    appariements = {e: [] for e in prefs_etablissements.keys()}  
    propositions_index = {e: 0 for e in prefs_etudiants.keys()} 

    while etudiants_libres:
        etu = etudiants_libres.pop(0)
        prefs = prefs_etudiants[etu]
        idx = propositions_index[etu]

        if idx < len(prefs):
            eta = prefs[idx] 
            propositions_index[etu] = idx + 1
            capacite = capacites[eta]

            # si l'établissement n'est pas plein, on accepte 
            if len(appariements[eta]) < capacite:
                appariements[eta].append(etu)
            else:
                # sinon,comparer les preferences
                appariements[eta].append(etu)
                appariements[eta].sort(key=lambda x: prefs_etablissements[eta].index(x))
                pire = appariements[eta].pop()  

                if pire != etu:
                    etudiants_libres.append(pire)
                else:
                    etudiants_libres.append(etu)
    return appariements


def calculer_satisfaction(appariements, prefs_etudiants, prefs_etablissements):
#satisfaction etudiant:(nombre totale-rang)/nombre totale
    satisfaction_etudiants = []
    satisfaction_etablissements = []

    # etudiant
    for etu in prefs_etudiants:
        for eta, etus in appariements.items():
            if etu in etus:
                rang = prefs_etudiants[etu].index(eta)
                satisfaction = (len(prefs_etudiants[etu]) - rang) / len(prefs_etudiants[etu])
                satisfaction_etudiants.append(satisfaction)
                break

    # etablissement
    for eta in prefs_etablissements:
        for etu in appariements[eta]:
            rang = prefs_etablissements[eta].index(etu)
            satisfaction = (len(prefs_etablissements[eta]) - rang) / len(prefs_etablissements[eta])
            satisfaction_etablissements.append(satisfaction)

    moy_etu = sum(satisfaction_etudiants) / len(satisfaction_etudiants) if satisfaction_etudiants else 0
    moy_eta = sum(satisfaction_etablissements) / len(satisfaction_etablissements) if satisfaction_etablissements else 0

    return moy_etu, moy_eta


def est_stable(appariements, prefs_etudiants, prefs_etablissements):
    for etu, prefs in prefs_etudiants.items():
        for eta in prefs:
            affecte = None
            for eta_temp, etus_list in appariements.items():
                if etu in etus_list:
                    affecte = eta_temp
                    break

            if affecte and prefs.index(eta) < prefs.index(affecte):
                capacite = len(appariements[eta])
                if capacite > 0:
                    pire_etu = appariements[eta][0]
                    pire_rang = prefs_etablissements[eta].index(pire_etu)

                    for s in appariements[eta][1:]:
                        s_rang = prefs_etablissements[eta].index(s)
                        if s_rang > pire_rang:
                            pire_rang = s_rang
                            pire_etu = s

                    etu_rang = prefs_etablissements[eta].index(etu)
                    if etu_rang < pire_rang:
                        return False, (etu, eta)
    return True, None
