import json
from typing import Any

import pytest
from sae_backend.model.database.async_.exceptions import NotAnOpenAnswer, OpenAnswerTooLong

from sae_backend.model.database.async_.operations import (
    all_questions_in_order,
    can_join_session,
    has_user_answered,
    has_user_participated,
    is_session_joinable,
    is_session_owner,
    join_session,
    leave_session,
    next_question,
    save_session_results,
    save_user_answer,
    save_user_open_answer,
    start_survey_session,
    users_in_session,
    is_in_session,
)

from .utils.testing_data import get_ressource
from .utils.testing_database import TestingAsyncSession


@pytest.fixture
def join_code() -> str:
    return get_ressource("running_session_join_code")


@pytest.fixture
def nice_join_code() -> str:
    return get_ressource("nice_session_join_code")


@pytest.mark.asyncio
async def test_is_session_owner(join_code: str):
    async with TestingAsyncSession() as sess:
        assert await is_session_owner(sess, "running.man@gmail.com", join_code)
        assert not await is_session_owner(sess, "session.man2@gmail.com", join_code)


@pytest.mark.asyncio
async def test_can_join_session(join_code: str):
    async with TestingAsyncSession() as sess:
        assert await can_join_session(sess, "session.man2@gmail.com", join_code)


@pytest.mark.asyncio
async def test_can_join_session_authorised(nice_join_code: str):
    async with TestingAsyncSession() as sess:
        assert await can_join_session(sess, "jonnhy@peterson.com", nice_join_code)


@pytest.mark.asyncio
async def test_can_join_session_unauthorised(nice_join_code: str):
    async with TestingAsyncSession() as sess:
        assert not await can_join_session(sess, "session.man2@gmail.com", nice_join_code)


@pytest.mark.asyncio
async def test_session_lifecycle(join_code: str):
    async with TestingAsyncSession() as sess:
        assert len(await users_in_session(sess, join_code)) == 0

        assert await can_join_session(sess, "session.man2@gmail.com", join_code)

        await join_session(sess, "session.man2@gmail.com", join_code)
        assert len(await users_in_session(sess, join_code)) == 1

        assert await is_in_session(sess, "session.man2@gmail.com", join_code)

        assert await can_join_session(sess, "session.man@gmail.com", join_code)

        await join_session(sess, "session.man@gmail.com", join_code)
        assert len(await users_in_session(sess, join_code)) == 2

        await leave_session(sess, "session.man2@gmail.com", join_code)
        assert len(await users_in_session(sess, join_code)) == 1

        assert not await is_in_session(sess, "session.man2@gmail.com", join_code)


@pytest.mark.asyncio
async def test_is_session_joinable(join_code: str):
    async with TestingAsyncSession() as sess:
        assert await is_session_joinable(sess, join_code)


@pytest.mark.asyncio
async def test_session_not_joinable():
    async with TestingAsyncSession() as sess:
        assert not await is_session_joinable(sess, "FaK3C0de")


@pytest.mark.asyncio
async def test_all_questions(join_code: str):
    async with TestingAsyncSession() as sess:
        nb_questions = len(await all_questions_in_order(sess, join_code))
        assert nb_questions == 4, nb_questions


@pytest.mark.asyncio
async def test_next_question(join_code: str):
    next_question_id = get_ressource("first_question_id")

    async with TestingAsyncSession() as sess:
        question = (await next_question(sess, join_code))[0]
        assert question is not None
        assert question.id == next_question_id

        # On va jusqu"a la fin du questionaire
        guard = 0
        while question is not None:
            question = (await next_question(sess, join_code))[0]
            guard += 1
            assert guard < 500, "next_question does not circulate to the next question"


@pytest.mark.asyncio
async def test_save_questions(join_code: str):
    question2_id = get_ressource("second_question_id")
    answer1_id = get_ressource("running_session_answer1")
    answer2_id = get_ressource("running_session_answer2")

    async with TestingAsyncSession() as sess:
        assert not await has_user_answered(sess, "session.man@gmail.com", join_code, question2_id)
        assert not await has_user_answered(sess, "session.man2@gmail.com", join_code, question2_id)

        await save_user_answer(sess, "session.man2@gmail.com", join_code, [answer1_id])
        await save_user_answer(sess, "session.man@gmail.com", join_code, [answer1_id, answer2_id])

        assert await has_user_answered(sess, "session.man@gmail.com", join_code, question2_id)
        assert await has_user_answered(sess, "session.man2@gmail.com", join_code, question2_id)

        assert await has_user_participated(sess, "session.man@gmail.com", join_code)


@pytest.mark.asyncio
async def test_start_survey_session():
    to_start_join_code = get_ressource("running_session_start_me_join_code")

    async with TestingAsyncSession() as sess:
        assert await is_session_joinable(sess, to_start_join_code)

        await start_survey_session(sess, to_start_join_code)

        assert not await is_session_joinable(sess, to_start_join_code)


@pytest.mark.asyncio
async def test_save_open_answer(join_code: str):
    open_question_id = get_ressource("open_question_id")
    open_restricted_question_id = get_ressource("open_restricted_question_id")

    async with TestingAsyncSession() as sess:
        await save_user_open_answer(
            sess, "session.man@gmail.com", join_code, open_question_id, "La vie est très complexe."
        )

        await save_user_open_answer(sess, "session.man@gmail.com", join_code, open_restricted_question_id, "Joie")


@pytest.mark.asyncio
async def test_save_open_answer_too_long(join_code: str):
    open_restricted_question_id = get_ressource("open_restricted_question_id")

    async with TestingAsyncSession() as sess:
        with pytest.raises(OpenAnswerTooLong):
            await save_user_open_answer(
                sess, "session.man@gmail.com", join_code, open_restricted_question_id, "Malheur et soufrances"
            )


@pytest.mark.asyncio
async def test_save_not_open_answer(join_code: str):
    question2_id = get_ressource("second_question_id")

    async with TestingAsyncSession() as sess:
        with pytest.raises(NotAnOpenAnswer):
            await save_user_open_answer(sess, "session.man@gmail.com", join_code, question2_id, "Malheur et soufrances")


@pytest.mark.asyncio
async def test_save_results():
    join_code = get_ressource("results_testing_session_join_code")

    question1_id = get_ressource("first_question_id")
    first_answer_id = get_ressource("first_answer_id")
    question2_id = get_ressource("second_question_id")
    answer1_id = get_ressource("running_session_answer1")
    answer2_id = get_ressource("running_session_answer2")
    open_question_id = get_ressource("open_question_id")
    open_restricted_question_id = get_ressource("open_restricted_question_id")

    async with TestingAsyncSession() as sess:
        # Première question type QCM
        await save_user_answer(sess, "session.man@gmail.com", join_code, [first_answer_id])

        # Seconde question type QCM
        await save_user_answer(sess, "session.man2@gmail.com", join_code, [answer1_id])
        await save_user_answer(sess, "session.man@gmail.com", join_code, [answer1_id, answer2_id])

        # Troisième question type ouverte
        await save_user_open_answer(sess, "session.man@gmail.com", join_code, open_question_id, "Plusieurs mots ici")
        await save_user_open_answer(sess, "session.man2@gmail.com", join_code, open_question_id, "La campagne est cool")

        # Quatrième question type ouverte
        await save_user_open_answer(sess, "session.man@gmail.com", join_code, open_restricted_question_id, "One!")

        # Sauvegarde de tout ça
        res_json = await save_session_results(sess, join_code)

    results: dict[str, dict[str, Any]] = json.loads(res_json)

    session_man_id = get_ressource("session_man_id")
    session_man2_id = get_ressource("session_man2_id")

    assert len(results) == 2, len(results)

    session_man_results = results[str(session_man_id)]
    session_man2_results = results[str(session_man2_id)]

    assert len(session_man_results) == 4
    assert len(session_man2_results) == 3

    assert session_man_results[str(question1_id)]["correctly_answered"]
    assert not session_man2_results[str(question1_id)]["correctly_answered"]

    assert not session_man_results[str(question2_id)]["correctly_answered"]
    assert session_man2_results[str(question2_id)]["correctly_answered"]
    assert len(session_man_results[str(question2_id)]["answers_text"]) == 2

    with pytest.raises(KeyError):
        session_man_results[str(open_question_id)]["correctly_answered"]

    assert session_man_results[str(open_question_id)]["answers_text"][0] == "Plusieurs mots ici"
