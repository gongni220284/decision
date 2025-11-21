from typing import Dict, List
from pathlib import Path
import typer
from utils import load_data_from_json
import random
from algorithms import gale_shapley_etudiant_otimal, gale_shapley_university_optimal, est_stable
import json
import datetime


app = typer.Typer()


@app.command()
def main(
    etudiants_json: Path = typer.Argument(..., help="Chemin du fichier JSON contenant les noms des étudiants."),
    etablissements_json: Path = typer.Argument(..., help="Chemin du fichier JSON contenant les noms des établissements."),
    output_dir: Path = typer.Option("./results", help="Dossier de sortie pour sauvegarder les préférences.")
):

    etudiants_data = load_data_from_json(etudiants_json)
    etudiants = etudiants_data["nom"]

    universite_data = load_data_from_json(etablissements_json)
    universites = [u["nom"] for u in universite_data["etablissements_superieurs_francais_complet"]]

    nb_etudiants = typer.prompt(f"Nombre d'étudiants à utiliser (max {len(etudiants)})", type=int)
    nb_uni = typer.prompt(f"Nombre d'établissements à utiliser (max {len(universites)})", type=int)
    capacite = typer.prompt("Capacité de chaque établissement", type=int)

    selec_etu = random.sample(etudiants, nb_etudiants)
    selec_uni = random.sample(universites, nb_uni)

    # Génération des préférences aléatoires
    prefs_etudiants = {
        etu: random.sample(selec_uni, len(selec_uni))
        for etu in selec_etu
    }
    prefs_uni = {
        uni: random.sample(selec_etu, len(selec_etu))
        for uni in selec_uni
    }

    capacites = {uni: capacite for uni in selec_uni}

    typer.secho("\n--- Aperçu des préférences générées ---", fg=typer.colors.CYAN)
    for s, prefs in list(prefs_etudiants.items())[:5]:
        print(f"{s} : {prefs}")
    for e, prefs in list(prefs_uni.items())[:5]:
        print(f"{e} : {prefs}")
    typer.secho("\n--- Exécution de Gale–Shapley (étudiant-optimal) ---", fg=typer.colors.GREEN)
    matching_etudiant_opt = gale_shapley_etudiant_otimal(
        prefs_etudiants, prefs_uni, capacites
    )
    stable_e, _ = est_stable(matching_etudiant_opt, prefs_etudiants, prefs_uni)
    typer.echo(f"Stable (étudiant-optimal) : {stable_e}")
    

    typer.secho("\n--- Exécution de Gale–Shapley (université-optimal) ---", fg=typer.colors.GREEN)
    matching_universite_opt = gale_shapley_university_optimal(
        prefs_etudiants, prefs_uni, capacites
    )
    stable_u, _ = est_stable(matching_universite_opt, prefs_etudiants, prefs_uni)
    typer.echo(f"Stable (université-optimal) : {stable_u}")


    # -------------------------------
    #  CALCUL DES SCORES
    # -------------------------------

    typer.secho("\n--- Calcul des scores ---", fg=typer.colors.MAGENTA)

    from score import score_final

    score_etud_opt = score_final(
        matching_etudiant_opt,
        matching_universite_opt,
        prefs_etudiants,
        prefs_uni,
        k=3,
        alpha=0.4,
        beta=0.3,
        gamma=0.3
    )

    score_univ_opt = score_final(
        matching_universite_opt,
        matching_etudiant_opt,
        prefs_etudiants,
        prefs_uni,
        k=3,
        alpha=0.4,
        beta=0.3,
        gamma=0.3
    )

    typer.echo("\nScore étudiant-optimal :")
    typer.echo(score_etud_opt)

    typer.echo("\nScore université-optimal :")
    typer.echo(score_univ_opt)


    # -------------------------------
    #  PREPARATION POUR VISUALISATION
    # -------------------------------

    results = [
        {
            "label": "Étudiant-optimal",
            "score_final": score_etud_opt["score_final"],
            "topk_global": score_etud_opt["topk_global"],
            "satisfaction_croisee": score_etud_opt["satisfaction_croisee"],
            "regret_global": score_etud_opt["regret_global"],
            "optimalité": score_etud_opt["optimality"]
        },
        {
            "label": "Université-optimal",
            "score_final": score_univ_opt["score_final"],
            "topk_global": score_univ_opt["topk_global"],
            "satisfaction_croisee": score_univ_opt["satisfaction_croisee"],
            "regret_global": score_univ_opt["regret_global"],
            "optimalité": score_univ_opt["optimality"]
        }
    ]


    # -------------------------------
    # VISUALISATIONS
    # -------------------------------

    typer.secho("\n--- Visualisations ---", fg=typer.colors.BLUE)

    from visualisation import (
        plot_satisfaction_vs_scorefinal,
        plot_score_vs_weights, 
        # plot_components_vs_weights, 
        plot_matching_components, 
        plot_score_vs_weights_recompute
    )

    # Scatter Satisfaction vs Score Final
    plot_satisfaction_vs_scorefinal(results)
    plot_score_vs_weights_recompute(
    score_final,
    matching_etudiant_opt,      # matching à analyser
    matching_etudiant_opt,      # matching idéal côté étudiants
    matching_universite_opt,    # matching idéal côté universités
    prefs_etudiants,
    prefs_uni,
    k=3,
    step=0.1
)
    # # Variation du score final selon alpha, beta, gamma = 1 - alpha - beta
    # plot_score_vs_weights(
    #     score_final,
    #     matching_etudiant_opt,     # ou choisir matching à visualiser
    #     prefs_etudiants,
    #     prefs_uni,
    #     k=3,
    #     steps=11
    # )

    # plot_components_vs_weights(results)
    # plot_matching_components(results)
    # plot_score_vs_weights(results)


    typer.secho("\n--- Fin ---", fg=typer.colors.BRIGHT_GREEN)
        # ----------------- Sauvegarde -----------------
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(f"{output_dir}/{timestamp}")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "preference_et_resultats.json"

    out_data = {
        "preferences": {
            "etudiants": prefs_etudiants,
            "etablissements": prefs_uni,
            "capacites": capacites
        },
        "matchings": {
            "etudiant_optimal": matching_etudiant_opt,
            "universite_optimal": matching_universite_opt
        },
        "scores": {
            "student_optimal": score_etud_opt,
            "university_optimal": score_univ_opt
        }
    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(out_data, f, ensure_ascii=False, indent=2)

    typer.secho(f"\nRésultats sauvegardés dans : {output_path}", fg=typer.colors.GREEN)

    from rotation_poset import enumerate_all_stable_matchings

    matchings = enumerate_all_stable_matchings(
            prefs_etudiants, prefs_uni, capacites
    )

    print("Nombre total de matchings stables :", len(matchings))
    for m in matchings:
        print(m)



if __name__ == "__main__":
    app()