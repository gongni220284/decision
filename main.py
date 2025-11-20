from stable_marriage import *

def main():
    print("=== Simulateur de l'algorithme du mariage stable ===\n")

    nb_etudiants = int(input("Nombre d'étudiants : "))
    nb_etablissements = int(input("Nombre d'établissements : "))
    capacite = int(input("Capacité par établissement : "))
    

    print("\nGénération des préférences...")
    prefs_etudiants, prefs_etablissements, capacites = generer_preferences(
        nb_etudiants, nb_etablissements, capacite
    )

    print("--- Préférences des étudiants ---")
    print(prefs_etudiants)
    
    print("\n--- Préférences des établissements ---")
    print(prefs_etablissements)
    
    
    print("Exécution de Gale-Shapley...\n")
    appariements = gale_shapley(prefs_etudiants, prefs_etablissements, capacites)


    print("--- Appariements ---")
    for etab, etus in appariements.items():
        print(f"{etab} : {etus}")


    k = int(input("Valeur de k pour Top-k : "))
    print(f"Top-{k} : {top_k(appariements, prefs_etudiants, k)}")
    
    alpha = float(input("Poids α (Top-k) : "))
    beta = float(input("Poids β (Satisfaction) : "))
    gamma = float(input("Poids γ (Non-frustration) : "))


    print("\n--- Résultats ---")
    score, resultats = score_global(
        appariements, prefs_etudiants, prefs_etablissements,
        k, alpha, beta, gamma
    )
    
    print(f"Score global : {score:.4f}")
    print(f"Top-{k} : {resultats['Top_k']:.4f}")
    print(f"Satisfaction étudiants : {resultats['Satisfaction_etudiants']:.4f}")
    print(f"Satisfaction établissements : {resultats['Satisfaction_etablissements']:.4f}")
    print(f"Moyenne harmonique : {resultats['Harmonic_mean']:.4f}")
    print(f"Taux de frustration : {resultats['Frustration_rate']:.4f}")
    print(f"Non-frustration : {resultats['Non_frustration']:.4f}")

if __name__ == "__main__":
    main()