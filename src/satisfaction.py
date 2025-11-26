from typing import Dict, List
import math

def satisfaction_individuelle(rang: int, taille: int) -> float:
    """
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
    
    #satisfaction moyenne des étudiants
    scores_etus = []
    for uni, etus in matching.items():
        for etu in etus:
            if etu not in prefs_etus:
                continue
            
            prefs_etu = prefs_etus[etu]
            taille_etu = len(prefs_etu)
            
            if uni not in prefs_etu:
                S_etu = 0.0
            else:
                rang_etu = prefs_etu.index(uni)
                S_etu = satisfaction_individuelle(rang_etu, taille_etu)
            
            scores_etus.append(S_etu)
    
    S_etu_global = sum(scores_etus) / len(scores_etus) if scores_etus else 0.0
    
    #satisfaction moyenne des universités
    scores_unis = []
    for uni, etus in matching.items():
        prefs_uni = prefs_unis[uni]
        taille_uni = len(prefs_uni)
        
        for etu in etus:
            if etu not in prefs_uni:
                S_uni = 0.0
            else:
                rang_uni = prefs_uni.index(etu)
                S_uni = satisfaction_individuelle(rang_uni, taille_uni)
            
            scores_unis.append(S_uni)
    
    S_uni_global = sum(scores_unis) / len(scores_unis) if scores_unis else 0.0
    
    return (S_etu_global + S_uni_global) / 2