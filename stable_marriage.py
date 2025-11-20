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
                # sinon, comparer les preferences
                appariements[eta].append(etu)
                appariements[eta].sort(key=lambda x: prefs_etablissements[eta].index(x))
                pire = appariements[eta].pop()  

                if pire != etu:
                    etudiants_libres.append(pire)
                else:
                    etudiants_libres.append(etu)
    return appariements


def top_k(appariements, prefs_etudiants, k):
    nb_etudiants = len(prefs_etudiants)
    count = 0
    etu_eta = {}
    for eta, etudiants_acceptes in appariements.items():
        for etu in etudiants_acceptes:
            etu_eta[etu] = eta

    for etu, prefs in prefs_etudiants.items():
        # obtient l'établissement assigné à l'étudiant
        eta_assigne = etu_eta.get(etu)
        if eta_assigne is not None:
            rang = prefs.index(eta_assigne) 
            if rang + 1 <= k: 
                count += 1
    
    tk = count / nb_etudiants
    return tk


def calculer_satisfaction(appariements, prefs_etudiants, prefs_etablissements):
    etu_eta = {}
    for eta, etudiants_acceptes in appariements.items():
        for etu in etudiants_acceptes:
            etu_eta[etu] = eta
    
    # Satisfaction moyenne des étudiants
    satisfactions_etudiants = []
    for etu, prefs in prefs_etudiants.items():
        eta_assigne = etu_eta.get(etu)

        if eta_assigne is not None:
            r_i = prefs.index(eta_assigne)
            n_i = len(prefs)
            if n_i > 1:
                s_i = (n_i - 1 - r_i) / (n_i - 1)
            else:
                s_i = 1.0  
            satisfactions_etudiants.append(s_i)
        else:
            # Étudiant non assigné 
            satisfactions_etudiants.append(0.0)
    
    nb_etudiants = len(prefs_etudiants)
    S_etudiants = sum(satisfactions_etudiants) / nb_etudiants
    satisfactions_par_etablissement = []
    
    for eta, etudiants_acceptes in appariements.items():
        if len(etudiants_acceptes) > 0:
            prefs = prefs_etablissements[eta]
            satisfactions_eta = []
            
            for etu in etudiants_acceptes:
                r_s = prefs.index(etu)
                n_s = len(prefs)
                if n_s > 1:
                    s_s = (n_s - 1 - r_s) / (n_s - 1)
                else:
                    s_s = 1.0
                satisfactions_eta.append(s_s)
            
            satisfactions_par_etablissement.append(sum(satisfactions_eta) / len(satisfactions_eta))
        else:
            # Établissement sans étudiant
            satisfactions_par_etablissement.append(0.0)
    
    nb_etablissements = len(prefs_etablissements)
    S_etablissements = sum(satisfactions_par_etablissement) / nb_etablissements
    
    if S_etudiants > 0 and S_etablissements > 0:
        H = (2 * S_etudiants * S_etablissements) / (S_etudiants + S_etablissements)
    else:
        H = 0
    
    return S_etudiants, S_etablissements, H


def calculer_frustration(appariements, prefs_etudiants, prefs_etablissements):
    etu_eta = {}
    for eta, etudiants_acceptes in appariements.items():
        for etu in etudiants_acceptes:
            etu_eta[etu] = eta
    
    frustrations = []
    
    for etu, prefs in prefs_etudiants.items():
        eta_assigne = etu_eta.get(etu)
        
        if eta_assigne is not None:
            rank_assigned = prefs.index(eta_assigne)
            A_i_rejected = set(prefs[:rank_assigned])
        else:
            # Étudiant non assigné -> tous les établissements sont "rejetés"
            A_i_rejected = set(prefs)
        
        B_i = set()
        for eta_rejected in A_i_rejected:
            students_accepted = appariements[eta_rejected]
            eta_prefs = prefs_etablissements[eta_rejected]
            
            # Vérifier si l'étudiant est dans les préférences de cet établissement
            if etu in eta_prefs:
                etu_rank = eta_prefs.index(etu)
                for etu_accepted in students_accepted:
                    if etu_accepted in eta_prefs:
                        accepted_rank = eta_prefs.index(etu_accepted)
                        if etu_rank < accepted_rank:
                            B_i.add(eta_rejected)
                            break  
        
        if len(A_i_rejected) > 0:
            f_i = len(B_i) / len(A_i_rejected)
        else:
            f_i = 0.0  
        
        frustrations.append(f_i)
    
    nb_etudiants = len(prefs_etudiants)
    F_bar = sum(frustrations) / nb_etudiants
    F = 1 - F_bar
    
    return F_bar, F


def score_global(appariements, prefs_etudiants, prefs_etablissements, k, alpha, beta, gamma):
    # Vérifier que les poids somment à 1
    if abs(alpha + beta + gamma - 1) > 1e-9:
        raise ValueError(f"La somme des poids doit être égale à 1 (actuel: {alpha + beta + gamma})")
    
    tk = top_k(appariements, prefs_etudiants, k)
    
    S_etudiants, S_etablissements, H = calculer_satisfaction(
        appariements, prefs_etudiants, prefs_etablissements
    )
    
    F_bar, F = calculer_frustration(
        appariements, prefs_etudiants, prefs_etablissements
    )
    
    score_global = alpha * tk + beta * H + gamma * F
    
    resultats = {
        'Top_k': tk,
        'Satisfaction_etudiants': S_etudiants,
        'Satisfaction_etablissements': S_etablissements,
        'Harmonic_mean': H,
        'Frustration_rate': F_bar,
        'Non_frustration': F,
        'Global_score': score_global,
        'Weight_alpha': alpha,
        'Weight_beta': beta,
        'Weight_gamma': gamma,
        'k_value': k
    }
    
    return score_global, resultats


    