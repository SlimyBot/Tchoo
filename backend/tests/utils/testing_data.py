from typing import Any

import pytest
from sqlalchemy.orm import Session
from sae_backend.model.database.db_models import QuestionType, SurveySessionType, UserAffiliation
from sae_backend.model.database.operations import (
    create_group,
    add_question_to_survey,
    create_answer,
    create_question,
    create_session_template,
    create_survey,
    register_user,
    add_user_to_group,
    start_survey_session,
)

_ressources = {}


def _add_ressource(ressource_id: str, ressource):
    _ressources[ressource_id] = ressource


def get_ressource(ressource_id: str) -> Any:
    """
    Récupère une ressource de test.
    Une ressource de test est un objet qui est crée dans la base de données
    pour les tests et qui peut être utilisé dans plusieurs tests.
    C'est pour pouvoir récupérer des objets qui sont généré automatiquement par exemple,
    commes les ID.
    """
    try:
        return _ressources[ressource_id]
    except KeyError:
        pytest.fail(f"'{ressource_id}' is not a valid testing ressource")


# NOTE : ne pas utiliser les mêmes données pour plusieurs catégories de tests


def populate_database(db: Session):
    # test_users : Utilisateur pour tester le login
    initial_user = register_user(db, "Tester", "TheTester", "login_test@gmail.com", UserAffiliation.student)
    _add_ressource("initial_user_id", initial_user.id)

    # Utilisateurs pour tester les permissions
    register_user(db, "Teacher", "Man", "prof@univ-cotedazur.fr", UserAffiliation.teacher)
    register_user(db, "Student", "Man", "coco@univ-cotedazur.fr", UserAffiliation.student)

    # test question : question pour tester les routes de question
    user = register_user(db, "Question", "Man", "Question.man@gmail.com", UserAffiliation.teacher)

    create_survey(db, user.id, "test_survey", "test_subject")
    question1 = create_question(db, user.id, QuestionType.multiple_answers, "test_question", "test_answer")
    create_answer(db, user.id, question1.id, "test_answer", True)
    create_answer(db, user.id, question1.id, "test_answer2", True)
    create_answer(db, user.id, question1.id, "test_answer3", False)
    create_answer(db, user.id, question1.id, "test_answer4", False)

    survey2 = create_survey(db, user.id, "test_survey2", "test_subject2")
    question2 = create_question(db, user.id, QuestionType.single_answer, "test_question2", "test_answer")
    create_answer(db, user.id, question2.id, "test_answer5", True)
    create_answer(db, user.id, question2.id, "test_answer6", False)
    create_answer(db, user.id, question2.id, "test_answer7", False)
    add_question_to_survey(db, user.id, survey2.id, question2.id)

    survey3 = create_survey(db, user.id, "test_survey3", "test_subject3")
    add_question_to_survey(db, user.id, survey3.id, question1.id)
    add_question_to_survey(db, user.id, survey3.id, question2.id)

    survey5 = create_survey(db, user.id, "test_survey5", "test_subject5")
    question4 = create_question(db, user.id, QuestionType.multiple_answers, "test_question", "test_answer")
    add_question_to_survey(db, user.id, survey5.id, question4.id)
    question5 = create_question(db, user.id, QuestionType.multiple_answers, "test_question", "test_answer")
    add_question_to_survey(db, user.id, survey5.id, question5.id)

    # test delete
    create_question(db, user.id, QuestionType.single_answer, "test_question3", "test_answer")
    create_answer(db, user.id, question2.id, "test_answer8", False)
    create_survey(db, user.id, "test_survey4", "test_subject4")

    # test groups : groupe pour tester les routes de groupes
    user2 = register_user(db, "Group", "Man", "Group.man@gmail.com", UserAffiliation.teacher)
    user3 = register_user(db, "Added", "Member", "Added.Member@gmail.com", UserAffiliation.student)
    user4 = register_user(db, "Member", "ToRemove", "Member.ToRemove@gmail.com", UserAffiliation.student)
    create_group(db, user2.id, "test_group1", None)
    group2 = create_group(db, user2.id, "test_group2", 1)
    add_user_to_group(db, user2.id, group2.id, user4.id)
    add_user_to_group(db, user2.id, group2.id, user3.id)

    # Tests sessions
    session_user = register_user(db, "Session", "Man", "session.man@gmail.com", UserAffiliation.teacher)
    session_survey = create_survey(db, session_user.id, "Session testing survey", "It's about sessions!")

    session_question1 = create_question(
        db, session_user.id, QuestionType.multiple_answers, "Qu'est-ce une session ?", None
    )
    create_answer(db, session_user.id, session_question1.id, "Je ne sais pas", False)
    create_answer(db, session_user.id, session_question1.id, "Je ne sais pas mais plus long", False)
    create_answer(db, session_user.id, session_question1.id, "Un questionaire en live", True)
    add_question_to_survey(db, session_user.id, session_survey.id, session_question1.id)

    session_question2 = create_question(db, session_user.id, QuestionType.single_answer, "Est-ce que ?", None)
    create_answer(db, session_user.id, session_question2.id, "Oui", True)
    create_answer(db, session_user.id, session_question2.id, "Non", False)
    add_question_to_survey(db, session_user.id, session_survey.id, session_question2.id)

    _add_ressource("testing_session_survey_id", session_survey.id)

    other_session_user = register_user(db, "Session2", "Man2", "session.man2@gmail.com", UserAffiliation.teacher)
    other_session_survey = create_survey(db, other_session_user.id, "Session testing survey, the 2nd one", "yes")
    _add_ressource("other_testing_session_survey_id", other_session_survey.id)

    _add_ressource("session_man_id", session_user.id)
    _add_ressource("session_man2_id", other_session_user.id)

    # Tests pour les modèles de sessions
    create_session_template(
        db, session_user.id, session_survey.id, "A session template", SurveySessionType.auto_free, None, False
    )

    session_template = create_session_template(
        db, session_user.id, session_survey.id, "A nice session template", SurveySessionType.piloted, None, False
    )
    _add_ressource("testing_session_template_id", session_template.id)  # type: ignore

    session_template_edit_me = create_session_template(
        db, session_user.id, session_survey.id, "editme", SurveySessionType.auto_free, None, False
    )
    _add_ressource("testing_session_template_edit_id", session_template_edit_me.id)  # type: ignore

    session_template_delete_me = create_session_template(
        db, session_user.id, session_survey.id, "delete me", SurveySessionType.piloted, None, False
    )
    _add_ressource("testing_session_template_delete_id", session_template_delete_me.id)  # type: ignore

    started_session = start_survey_session(db, session_user.id, session_template.id)  # type: ignore
    _add_ressource("started_session_join_code", started_session.join_code)

    # Suite des tests de sessions une fois lancée
    running_session_user = register_user(db, "Running", "SessionMan", "running.man@gmail.com", UserAffiliation.teacher)
    running_session_survey = create_survey(db, running_session_user.id, "Running session survey", "We love to run!")

    running_session_question1 = create_question(
        db, running_session_user.id, QuestionType.multiple_answers, "Qu'est-ce une session ?", None
    )
    _add_ressource("first_question_id", running_session_question1.id)
    create_answer(db, running_session_user.id, running_session_question1.id, "Je ne sais pas", False)
    create_answer(db, running_session_user.id, running_session_question1.id, "Je ne sais pas mais plus long", False)
    first_answer = create_answer(
        db, running_session_user.id, running_session_question1.id, "Un questionaire en live", True
    )

    _add_ressource("first_answer_id", first_answer.id)  # type: ignore

    running_session_question2 = create_question(
        db, running_session_user.id, QuestionType.single_answer, "Est-ce que ?", None
    )
    answer1 = create_answer(db, running_session_user.id, running_session_question2.id, "Oui", True)
    answer2 = create_answer(db, running_session_user.id, running_session_question2.id, "Non", False)

    _add_ressource("running_session_answer1", answer1.id)  # type: ignore
    _add_ressource("running_session_answer2", answer2.id)  # type: ignore
    _add_ressource("second_question_id", running_session_question2.id)

    add_question_to_survey(db, running_session_user.id, running_session_survey.id, running_session_question1.id)
    add_question_to_survey(db, running_session_user.id, running_session_survey.id, running_session_question2.id)

    running_session_open_question1 = create_question(
        db, running_session_user.id, QuestionType.open, "Quel est le but de la vie ?", None
    )

    running_session_open_question2 = create_question(
        db, running_session_user.id, QuestionType.open_restricted, "Quel est ton mot favoris ?", None
    )

    _add_ressource("open_question_id", running_session_open_question1.id)
    _add_ressource("open_restricted_question_id", running_session_open_question2.id)

    add_question_to_survey(db, running_session_user.id, running_session_survey.id, running_session_open_question1.id)
    add_question_to_survey(db, running_session_user.id, running_session_survey.id, running_session_open_question2.id)

    running_session_template = create_session_template(
        db,
        running_session_user.id,
        running_session_survey.id,
        "Running session template",
        SurveySessionType.piloted,
        None,
        False,
    )

    running_session = start_survey_session(db, running_session_user.id, running_session_template.id)  # type: ignore
    _add_ressource("running_session_join_code", running_session.join_code)

    running_session_start_me = start_survey_session(
        db, running_session_user.id, running_session_template.id  # type: ignore
    )
    _add_ressource("running_session_start_me_join_code", running_session_start_me.join_code)

    results_testing_session = start_survey_session(
        db, running_session_user.id, running_session_template.id  # type: ignore
    )
    _add_ressource("results_testing_session_join_code", results_testing_session.join_code)

    # Groupes et modèles de sessions
    group_creator = register_user(db, "Group", "Creator", "michael@michaelson.com", UserAffiliation.teacher)
    group_user = register_user(db, "Mich", "dd", "jonnhy@peterson.com", UserAffiliation.student)

    auth_group = create_group(db, group_creator.id, "The best group ever!", None)
    _add_ressource("auth_group_id", auth_group.id)
    add_user_to_group(db, group_creator.id, group_user.id, auth_group.id)

    fun_survey = create_survey(db, group_creator.id, "adza", "stopitstopit")
    nice_template = create_session_template(
        db, group_creator.id, fun_survey.id, "Nice template", SurveySessionType.piloted, auth_group.id, False
    )
    nice_session = start_survey_session(db, group_creator.id, nice_template.id)  # type: ignore
    _add_ressource("nice_session_join_code", nice_session.join_code)
