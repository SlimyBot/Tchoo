"""
Routes API en rapport avec les résultats d'un questionnaire.
"""
import json
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...model.api.auth import only_teacher_allowed, student_or_teacher_allowed
from ...model.database.db_models import User, UserAffiliation
from ...model.database import get_db
from ...model.database.operations import get_saved_results, add_name_to_players, add_name_to_player


router = APIRouter()


@router.get("/get_end_survey/{join_code}")
def get_end_survey(
    db: Annotated[Session, Depends(get_db)],
    active_user: Annotated[User, Depends(only_teacher_allowed)],
    join_code: str,
):
    """
    Récupère les résultats de tout les joueurs.
    """
    survey_results = get_saved_results(db, join_code)
    score_players = get_score_all_players(survey_results)
    if score_players == "Aucun resultat":
        return score_players
    else:
        sort_players = sort_scores_players(score_players)
        return add_name_to_players(db, sort_players)


@router.get("/get_player_details/{id_player}/{join_code}")
def get_player_details(
    db: Annotated[Session, Depends(get_db)],
    active_user: Annotated[User, Depends(student_or_teacher_allowed)],
    id_player: str,
    join_code: str,
):
    """
    Récupère les résultats d'un joueur.
    """
    # si l'utilisateur est un étudiant, il ne peut voir que ses résultats (et pas ceux des autres)
    if active_user.affiliation == UserAffiliation.student and active_user.id != int(id_player):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Student cannot see the results of another student",
        )

    survey_results = get_saved_results(db, join_code)
    info_player = get_info_player(survey_results, id_player)

    return add_name_to_player(db, info_player)


def get_score_all_players(results: str) -> list | str:
    """
    Récupère le score de chaque joueur

    Paramètres
    ----------
    results : str
        Le résultat du questionnaire.

    Retour
    ------
    list | str
        le score de chaque joueur ou 'Aucun résultat'
    """
    json_data = json.loads(results)
    infos_players = []

    for player_id, player_info in json_data.items():
        if player_id is not None and player_id != "null":
            id_player = player_id
            correctly_answered = sum(
                1
                for question_info in player_info.values()
                if "correctly_answered" in question_info and question_info["correctly_answered"]
            )

            infos_players.append({"id_player": id_player, "correctly_answered": correctly_answered})

    if not infos_players:
        return "Aucun resultat"
    else:
        return infos_players


def sort_scores_players(infos_players: list) -> list:
    """
    Trie les joueurs en fonctions de leur score par ordre décroissant

    Paramètres

    ----------

    infos_joueurs : list
        Liste des joueurs et leur score

    Retour
    ------

    list
        Liste des joueurs et leur score triée par ordre décroissant
    """

    return sorted(infos_players, key=lambda x: x["correctly_answered"], reverse=True)


def get_top3_players(infos_players: list) -> list:
    """
    Récupère les 3 premiers joueurs

    Paramètres

    ----------

    infos_joueurs : list
        Liste des joueurs et leur score

    Retour
    ------

    list
        3 premiers joueurs
    """
    return infos_players[:3]


def get_info_player(infos_players, id_player):
    json_data = json.loads(infos_players)
    if id_player not in json_data:
        return None

    infos_player = {"id_player": id_player, "questions_answers": []}

    for question_id, question_info in json_data[id_player].items():
        question_answer = {
            "question_id": question_id,
            "question_text": question_info.get("question_text", ""),
            "answers_text": question_info.get("answers_text", []),
            "correctly_answered": question_info.get("correctly_answered", None),
        }
        infos_player["questions_answers"].append(question_answer)

    return infos_player
