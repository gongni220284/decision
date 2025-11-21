import matplotlib.pyplot as plt
import numpy as np


def plot_satisfaction_vs_scorefinal(results):
    avg_satisf = [(r["topk_global"] + r["satisfaction_croisee"]) / 2 for r in results]
    scoref = [r["score_final"] for r in results]
    labels = [res.get("label", f"M{i}") for i, res in enumerate(results)]

    plt.figure()
    for x, y, label in zip(avg_satisf, scoref, labels):
        plt.scatter([x], [y])
        plt.text(x, y, label)

    plt.xlabel("Average Satisfaction (Top-K + Satisfaction Croisée)")
    plt.ylabel("Score Final")
    plt.title("Satisfaction vs Score Final")
    plt.grid(True)
    plt.show()




def plot_score_vs_weights(
    score_fn,
    matching,
    matching_ideal_etu,
    matching_ideal_uni,
    prefs_etus,
    prefs_unis,
    k=3,
    steps=21
):
    """
    Calcule et affiche la variation du score final
    en fonction de alpha et beta (gamma = 1 - alpha - beta).
    """

    alphas = np.linspace(0, 1, steps)
    betas  = np.linspace(0, 1, steps)

    A, B, Scores = [], [], []

    for a in alphas:
        for b in betas:
            g = 1 - a - b
            if g < 0:
                continue

            res = score_fn(
                matching,
                matching_ideal_etu,
                matching_ideal_uni,
                prefs_etus,
                prefs_unis,
                k,
                a, b, g
            )

            A.append(a)
            B.append(b)
            Scores.append(res["score_final"])

    A = np.array(A)
    B = np.array(B)
    Scores = np.array(Scores)

    plt.figure(figsize=(10, 7))
    scatter = plt.scatter(A, B, c=Scores, cmap="viridis")
    plt.colorbar(scatter, label="Score final")

    plt.xlabel("alpha (poids Top-K)")
    plt.ylabel("beta (poids Satisfaction croisée)")
    plt.title("Variation du Score Final\n(gamma = 1 - alpha - beta)")
    plt.grid(True)
    plt.show()


# def plot_score_vs_weights(score_fn, matching, prefs_etus, prefs_unis, k=3, steps=11):
#     alphas = np.linspace(0, 1, steps)
#     betas = np.linspace(0, 1, steps)

#     pts = []
#     vals = []

#     for a in alphas:
#         for b in betas:
#             g = 1 - a - b
#             if g >= 0:
#                 res = score_fn(matching, prefs_etus, prefs_unis, k, a, b, g)
#                 pts.append((a, b))
#                 vals.append(res["score_final"])

#     pts = np.array(pts)
#     vals = np.array(vals)

#     plt.figure()
#     sc = plt.scatter(pts[:, 0], pts[:, 1], c=vals)
#     plt.xlabel("alpha")
#     plt.ylabel("beta")
#     plt.title("Final Score for alpha, beta (gamma = 1 - alpha - beta)")
#     plt.colorbar(sc, label="Final Score")
#     plt.grid(True)
#     plt.show()
# import matplotlib.pyplot as plt
# import numpy as np

# def plot_components_vs_weights(results):
#     """
#     results : liste d'objets retournés par score_final
#     """

#     # Extraction des valeurs
#     alphas = np.array([r["details"]["alpha"] for r in results])
#     betas  = np.array([r["details"]["beta"]  for r in results])
#     gammas = np.array([r["details"]["gamma"] for r in results])

#     topk_vals       = np.array([r["topk_global"]           for r in results])
#     cross_vals      = np.array([r["satisfaction_croisee"]  for r in results])
#     optimality_vals = np.array([r["optimalite"]            for r in results])
#     final_vals      = np.array([r["score_final"]           for r in results])

#     # --- PLOTS ---

#     titles = [
#         "Top-K global",
#         "Satisfaction croisée",
#         "Optimalité (1 - regret)",
#         "Score final"
#     ]
    
#     datasets = [
#         topk_vals,
#         cross_vals,
#         optimality_vals,
#         final_vals
#     ]

#     plt.figure(figsize=(14, 12))

#     for i, (title, data) in enumerate(zip(titles, datasets)):
#         plt.subplot(2, 2, i+1)

#         scatter = plt.scatter(alphas, betas, c=data, cmap="viridis")
#         plt.colorbar(scatter, label=title)

#         plt.xlabel("alpha")
#         plt.ylabel("beta")
#         plt.title(f"{title}\n(gamma = 1 - alpha - beta)")
#         plt.grid(True)

#     plt.tight_layout()
#     plt.show()


import matplotlib.pyplot as plt
import numpy as np

def plot_matching_components(results):
    labels = [r["label"] for r in results]

    # Extraire les scores
    topk_vals = [r["topk_global"] for r in results]
    cross_vals = [r["satisfaction_croisee"] for r in results]
    optimal_vals = [r["optimalité"] for r in results]
    final_vals = [r["score_final"] for r in results]

    x = np.arange(len(labels))
    width = 0.20

    plt.figure(figsize=(12, 6))

    plt.bar(x - 1.5*width, topk_vals, width, label="Top-K")
    plt.bar(x - 0.5*width, cross_vals, width, label="Satisfaction croisée")
    plt.bar(x + 0.5*width, optimal_vals, width, label="Optimalité (1 - regret)")
    plt.bar(x + 1.5*width, final_vals, width, label="Score final")

    plt.xticks(x, labels)
    plt.ylim(0, 1)
    plt.ylabel("Valeur")
    plt.title("Comparaison des composantes entre matchings")
    plt.legend()
    plt.grid(True, axis="y", linestyle="--", alpha=0.6)

    plt.show()


def plot_score_vs_weights_recompute(
    score_fn,
    matching,
    matching_ideal_etu,
    matching_ideal_uni,
    prefs_etus,
    prefs_unis,
    k=3,
    step=0.1
):
    """
    Recalcule le score final pour toutes les valeurs de alpha, beta
    avec un step donné (par exemple 0.1).
    gamma = 1 - alpha - beta
    """
    from score import score_final
    alphas = np.arange(0, 1 + step, step)
    betas  = np.arange(0, 1 + step, step)

    A, B, Scores = [], [], []

    for a in alphas:
        for b in betas:
            g = 1 - a - b
            if g < 0:
                continue  # gamma ne peut pas être négatif

            res = score_final(
                matching_ideal_etu,
                matching_ideal_uni,
                prefs_etus,
                prefs_unis,
                k,
                a, b, g
            )

            A.append(a)
            B.append(b)
            Scores.append(res["score_final"])

    # Convertir en numpy
    A = np.array(A)
    B = np.array(B)
    Scores = np.array(Scores)

    # --- Heatmap Scatter ---
    plt.figure(figsize=(10, 7))
    scatter = plt.scatter(A, B, c=Scores, cmap="viridis", s=200, edgecolors='black')

    plt.colorbar(scatter, label="Score final")
    plt.xlabel("alpha (poids Top-K)")
    plt.ylabel("beta (poids Satisfaction croisée)")
    plt.title(f"Variation du Score Final\n(step = {step}, gamma = 1 - alpha - beta)")
    plt.grid(True)
    plt.show()
