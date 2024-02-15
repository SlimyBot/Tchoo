"""
Opérations asyncrones sur la base de données.
"""
from asyncio import gather
from itertools import groupby, chain
from typing import Sequence
import json

from async_lru import alru_cache
from sqlalchemy import Row, or_, select, delete, and_, update, literal_column
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.expression import func
from sqlalchemy.ext.asyncio import AsyncSession

from .exceptions import AnswerDoesNotExist, NotAnOpenAnswer, OpenAnswerTooLong
from ..db_models import (
    Answer,
    AuthorisedGroup,
    GroupMember,
    OpenAnswer,
    Question,
    QuestionType,
    Results,
    Survey,
    SurveyQuestion,
    SurveyResults,
    SurveySession,
    SurveySessionTemplate,
    User,
    SessionParticipant,
    Group,
)


async def is_session_owner(sess: AsyncSession, email: str, join_code: str) -> bool:
    """
    Verifie si un utilisateur est le propriétaire de la session auquel appartiens le code.
    """

    stmt = (
        select(func.count(User.id))
        .join(Survey, User.id == Survey.user_id)
        .join(SurveySessionTemplate, Survey.id == SurveySessionTemplate.survey_id)
        .join(SurveySession)
        .where(User.email == email)
        .where(SurveySession.join_code == join_code)
    )
    owner_count = (await sess.execute(stmt)).scalar()

    return owner_count is not None and owner_count >= 1


async def can_join_session(sess: AsyncSession, email: str, join_code: str) -> bool:
    """
    Vérifie si un utilisateur à le droit de rejoindre une session.
    """

    # Si le questionaire est public, c'est facile...
    stmt = select(SurveySessionTemplate.is_public).join(SurveySession).where(SurveySession.join_code == join_code)
    is_public = (await sess.execute(stmt)).scalar()

    if is_public:
        return True

    # Si c'est pas publique, il faut vérifier si l'utilisateur fait partie du groupe
    # TODO : vérifier si groupe de groupe
    check_stmt = (
        select(func.count())
        .select_from(SurveySession)
        .join(SurveySessionTemplate)
        .join(AuthorisedGroup)
        .join(Group)
        .join(GroupMember)
        .join(User)
        .where(SurveySession.join_code == join_code)
        .where(User.email == email)
    )

    relationship_count = (await sess.execute(check_stmt)).scalar()

    return relationship_count == 1


@alru_cache()
async def _fetch_user_and_session(sess: AsyncSession, email: str, join_code: str) -> tuple[int, int]:
    user_query = sess.execute(select(User.id).where(User.email == email))
    session_query = sess.execute(select(SurveySession.id).where(SurveySession.join_code == join_code))

    user_id, session_id = await gather(user_query, session_query)

    return user_id.scalar_one(), session_id.scalar_one()


async def join_session(sess: AsyncSession, email: str, join_code: str):
    """
    Enregistre un utilisateur comme faisant partie d'une session.
    """

    user_id, session_id = await _fetch_user_and_session(sess, email, join_code)

    part = SessionParticipant(session_id=session_id, user_id=user_id)

    sess.add(part)
    await sess.commit()
    await sess.refresh(part)


async def leave_session(sess: AsyncSession, email: str, join_code: str):
    """
    Fait quitter un utilisateur d'une session
    """

    user_id, session_id = await _fetch_user_and_session(sess, email, join_code)

    await sess.execute(
        delete(SessionParticipant)
        .where(SessionParticipant.user_id == user_id)
        .where(SessionParticipant.session_id == session_id)
    )
    await sess.commit()


async def is_in_session(sess: AsyncSession, email: str, join_code: str) -> bool:
    """
    Vérifie si un utilisateur est présent dans une session.
    """

    user_id, session_id = await _fetch_user_and_session(sess, email, join_code)

    count = (
        await sess.execute(
            select(func.count(SessionParticipant.session_id))
            .where(SessionParticipant.user_id == user_id)
            .where(SessionParticipant.session_id == session_id)
        )
    ).scalar_one()

    return count != 0


async def users_in_session(sess: AsyncSession, join_code: str) -> Sequence[User]:
    """
    Renvoie la liste de tout les utilisateurs qui sont présent dans une session.
    """

    stmt = select(User).join(SessionParticipant).join(SurveySession).where(SurveySession.join_code == join_code)

    users = (await sess.execute(stmt)).scalars().all()
    return users


async def all_questions_in_order(sess: AsyncSession, join_code: str) -> Sequence[Question]:
    """
    Renvoie la liste de toutes les questions dans l'ordre dans lesquelles elles doivent être
    jouées dans le questionaire.
    Pour l'instant l'ordre des question est determiné par leurs ID.
    """
    stmt = (
        select(Question)
        .join(SurveyQuestion)
        .join(Survey)
        .join(SurveySessionTemplate)
        .join(SurveySession)
        .where(SurveySession.join_code == join_code)
        .order_by(Question.id)
    )

    questions = (await sess.execute(stmt)).scalars().all()
    return questions


async def next_question(sess: AsyncSession, join_code: str) -> tuple[Question, Sequence[Answer]] | tuple[None, None]:
    """
    Renvoie la prochaine question accompagné de ses réponses possibles à jouer lors du questionaire.

    Renvoie None, None si il n'y a pas de prochaine question.
    """
    survey_session = (
        await sess.execute(select(SurveySession).where(SurveySession.join_code == join_code))
    ).scalar_one()
    all_questions = await all_questions_in_order(sess, join_code)

    if survey_session.current_question_id is None:  # début du questionaire
        question = all_questions[0]
    else:
        current_question_index = next(
            (
                i
                for i, question in enumerate(all_questions)
                if question.id == survey_session.current_question_id  # type: ignore
            ),
            None,
        )
        question = (
            None
            if current_question_index is None or current_question_index + 1 == len(all_questions)
            else all_questions[current_question_index + 1]
        )

    if question is None:  # fin des questions
        return None, None

    answers = (await sess.execute(select(Answer).where(Answer.question_id == question.id))).scalars().all()

    # Save the current question
    await sess.execute(
        update(SurveySession).where(SurveySession.join_code == join_code).values(current_question_id=question.id)
    )
    await sess.commit()

    return question, answers


async def save_user_answer(sess: AsyncSession, email: str, join_code: str, answer_ids: list[int]):
    """
    Enregistre la ou les réponses d'un utilisateur (question type QCM).
    """

    user_id, session_id = await _fetch_user_and_session(sess, email, join_code)

    sess.add_all(Results(user_id=user_id, session_id=session_id, answer_id=aid) for aid in answer_ids)

    try:
        await sess.flush()
    except IntegrityError as e:
        raise AnswerDoesNotExist(e)

    await sess.commit()


async def save_user_open_answer(sess: AsyncSession, email: str, join_code: str, question_id: int, text: str):
    """
    Enregistre le texte d'une réponse ouverte d'un utilisateur.
    """

    question_type = (await sess.execute(select(Question.type).where(Question.id == question_id))).scalar_one()

    if question_type == QuestionType.open_restricted and (size := len(text.split())) > 1:
        raise OpenAnswerTooLong(f"{size} words instead of 1")

    if question_type in {QuestionType.multiple_answers, QuestionType.single_answer}:
        raise NotAnOpenAnswer(question_type)

    user_id, session_id = await _fetch_user_and_session(sess, email, join_code)

    answer = OpenAnswer(text=text, question_id=question_id, user_id=user_id, session_id=session_id)

    sess.add(answer)
    await sess.commit()


async def has_user_answered(sess: AsyncSession, email: str, join_code: str, question_id: int) -> bool:
    """
    Vérifie si un utilisateur à déjà répondu a une question (type QCM).
    """

    user_id, session_id = await _fetch_user_and_session(sess, email, join_code)

    stmt = (
        select(func.count())
        .select_from(Results)
        .join(Answer)
        .join(Question)
        .where(Results.user_id == user_id)
        .where(Results.session_id == session_id)
        .where(Question.id == question_id)
    )

    results = (await sess.execute(stmt)).scalar_one()

    return results > 0


async def has_user_participated(sess: AsyncSession, email: str, join_code: str) -> bool:
    """
    Vérifie si un utilisateur à déjà participé à une session.
    """
    stmt = (
        select(func.count())
        .select_from(Results)
        .join(User)
        .join(SurveySession)
        .where(User.email == email)
        .where(SurveySession.join_code == join_code)
    )

    results_count = (await sess.execute(stmt)).scalar_one()

    return results_count > 0


async def save_session_results(sess: AsyncSession, join_code: str) -> str:
    """
    Sauvagarde (imprime) les résultats d'une session de questionaire qui
    viens de se terminer.
    """

    stmt_multiple_answers = (
        select(
            SurveySession.id, Question.id, Results.user_id, Question.text, Answer.text, Answer.is_correct, Question.type
        )
        .join(SurveyQuestion)
        .join(Survey)
        .join(SurveySessionTemplate)
        .join(SurveySession)
        .outerjoin(Results)
        .outerjoin(Answer, and_(Answer.id == Results.answer_id, Question.id == Answer.question_id))
        .where(SurveySession.join_code == join_code)
        .where(or_(Question.type == QuestionType.multiple_answers, Question.type == QuestionType.single_answer))
        .order_by(Results.user_id, Question.user_id)
    )

    stmt_open = (
        select(
            SurveySession.id,
            Question.id,
            OpenAnswer.user_id,
            Question.text,
            OpenAnswer.text,
            literal_column("0"),
            Question.type,
        )
        .join(SurveyQuestion)
        .join(Survey)
        .join(SurveySessionTemplate)
        .join(SurveySession)
        .outerjoin(OpenAnswer, and_(OpenAnswer.question_id == Question.id, OpenAnswer.session_id == SurveySession.id))
        .where(SurveySession.join_code == join_code)
        .where(or_(Question.type == QuestionType.open, Question.type == QuestionType.open_restricted))
        .order_by(OpenAnswer.user_id, Question.user_id)
    )

    res_multiple_answers, res_open = await gather(sess.execute(stmt_multiple_answers), sess.execute(stmt_open))

    res_multiple_answers = res_multiple_answers.all()
    res_open = res_open.all()

    filtered_rows = filter(lambda r: r[2] is not None, chain(res_multiple_answers, res_open))

    all_results = sorted(filtered_rows, key=lambda r: r[2])

    out = {}
    for user_id, user_group in groupby(all_results, lambda r: r[2]):
        user_results = {}
        questions = sorted(user_group, key=lambda r: r[1])
        for question_id, question_group in groupby(questions, lambda r: r[1]):
            user_question_rows = list(question_group)

            question_result = {
                "question_text": user_question_rows[0][3],
                "answers_text": [r[4] for r in user_question_rows if r[4] is not None],
            }

            if user_question_rows[0][6] in {QuestionType.multiple_answers, QuestionType.single_answer}:
                question_result["correctly_answered"] = await _check_multiple_correctly_answered(
                    sess, question_id, user_question_rows
                )

            user_results[question_id] = question_result

        out[user_id] = user_results

    serialised = json.dumps(out)

    results = SurveyResults(session_id=res_multiple_answers[0][0], saved_results=serialised)
    sess.add(results)

    await sess.commit()

    return serialised


async def _check_multiple_correctly_answered(
    sess: AsyncSession, question_id: int, user_question_rows: list[Row[tuple[int, int, int, str, str, bool, str]]]
) -> bool:
    """
    Helper qui determine si on a répondu correctement à une question de type QCM.
    """
    all_answers = [r[5] for r in user_question_rows]
    answers_given = list(set(all_answers))

    if len(answers_given) == 1:
        is_correctly_answered = bool(answers_given[0])

    else:
        # Si une réponse fausse a été donnée
        if False in answers_given:
            is_correctly_answered = False

            # Si True est la seule réponse autre que None retenue, il faut vérifier si il existe d'autres réponses
            # True non répondues
        else:
            nb_correct_answers = (
                await sess.execute(
                    select(func.count())
                    .select_from(Answer)
                    .join(Question)
                    .where(Answer.is_correct)
                    .where(Question.id == question_id)
                )
            ).scalar_one()
            nb_true_answers = sum(1 for a in all_answers if a)

            if nb_correct_answers == nb_true_answers:
                is_correctly_answered = True
            else:
                is_correctly_answered = False
    return is_correctly_answered


async def is_session_joinable(sess: AsyncSession, join_code: str) -> bool:
    """
    Determine si une session de questionaire est joignable :
        - elle existe
        - elle n'est pas en cours d'être jouée
        - elle n'est pas finie (pas de réponses enregistrées)
    """
    session = (
        await sess.execute(select(SurveySession).where(SurveySession.join_code == join_code))
    ).scalar_one_or_none()

    if session is None:
        return False

    if session.has_started:  # type: ignore
        return False

    saved_results_count = (
        await sess.execute(
            select(func.count(SurveyResults.id)).join(SurveySession).where(SurveySession.join_code == join_code)
        )
    ).scalar_one_or_none()

    return saved_results_count == 0


async def start_survey_session(sess: AsyncSession, join_code: str):
    """
    Marque une session comme ayant démarée
    """
    await sess.execute(update(SurveySession).where(SurveySession.join_code == join_code).values(has_started=True))
    await sess.commit()
