from jose import JWTError
from socketio import AsyncNamespace

from sae_backend.model.database.async_.exceptions import AnswerDoesNotExist, NotAnOpenAnswer, OpenAnswerTooLong

from ...model.database.async_ import AsyncSessionLocal
from ...model.database.async_ import operations as pg_ops
from ...model import redis_operations as redis_ops

from ...model.api.auth import get_email_from_jwt
from ...model.socket_manager import manager
from .codes import (
    ANSWER_DOES_NOT_EXIST,
    ANSWER_SAVED,
    END_SESSION_NOT_OWNER,
    NEXT_QUESTION,
    NO_MORE_QUESTIONS,
    NEXT_QUESTION_NOT_OWNER,
    NOT_OPEN_ANSWER,
    OPEN_ANSWER_TOO_LONG,
    OWNER_JOINS_SESSION,
    SESSION_ENDS,
    SESSION_NOT_JOINABLE,
    USER_ALREADY_JOINED,
    USER_JOINS_SESSION,
    USER_NOT_ALLOWED,
)


class SessionNamespace(AsyncNamespace):  # pragma: no cover
    async def on_connect(self, sid, environ, auth):
        """
        Connexion aux websockets. L'utilisateur doit être authentifié.
        """
        try:
            email = get_email_from_jwt(auth)
        except JWTError as e:
            await self.emit("connect_error", str(e), to=sid)
            return await self.disconnect(sid)

        if email is None:
            return await self.disconnect(sid)

        # lien entre le sid et l'adresse mail
        await self.save_session(sid, {"email": email})

    async def on_disconnect(self, sid):
        """
        Déconnexion aux websockets.
        """
        session = await self.get_session(sid)

        if "join_code" not in session:
            return

        async with redis_ops.get_redis_session() as client:
            await redis_ops.leave_session(client, session["email"], session["join_code"])

        await self.emit("user_leave", session["email"], room=session["join_code"])

    async def on_session_connect(self, sid, join_code):
        """
        Demande de connexion à une session.
        """
        async with self.session(sid) as session:
            async with AsyncSessionLocal() as sess:
                if not await pg_ops.is_session_joinable(sess, join_code):
                    return SESSION_NOT_JOINABLE

                email = session["email"]

                if await pg_ops.is_session_owner(sess, email, join_code):
                    self.enter_room(sid, join_code)
                    session["join_code"] = join_code
                    session["is_owner"] = True
                    async with redis_ops.get_redis_session() as client:
                        await redis_ops.set_session_sid_owner(client, join_code, sid)
                    return OWNER_JOINS_SESSION

                if await pg_ops.can_join_session(sess, email, join_code):
                    async with redis_ops.get_redis_session() as client:
                        if await redis_ops.is_in_session(client, email, join_code):
                            return USER_ALREADY_JOINED

                        self.enter_room(sid, join_code)
                        session["join_code"] = join_code
                        await redis_ops.join_session(client, email, join_code)

                        await self.emit("user_join", email, room=join_code)
                        return USER_JOINS_SESSION

                return USER_NOT_ALLOWED

    async def on_initiate_next_question(self, sid):
        """
        Ordre de démarrage de la session ou de passage à la prochaine question,
        initié par le propriétaire de la session.
        """

        session: dict = await self.get_session(sid)

        if not session.get("is_owner", False):
            return NEXT_QUESTION_NOT_OWNER

        join_code = session["join_code"]

        async with AsyncSessionLocal() as sess:
            await pg_ops.start_survey_session(sess, join_code)

            question, answers = await pg_ops.next_question(sess, join_code)

        if question is None:
            return NO_MORE_QUESTIONS

        if answers is not None:  # question ouverte
            formated_answers = [{"text": a.text, "id": a.id} for a in answers]
        else:
            formated_answers = None  # TODO : penser au cas question qcm sans réponses

        data = {
            "question": {"text": question.text, "media": question.media, "id": question.id},
            "type": question.type.value,  # type: ignore
            "answers": formated_answers,
        }

        await self.emit("next_question", data, room=join_code)

        return NEXT_QUESTION

    async def on_user_answer(self, sid, answer_ids: list[int]):
        """
        Reçois la réponse a une question d'un utilsateur à une session.
        """

        session: dict = await self.get_session(sid)

        email = session["email"]
        join_code = session["join_code"]

        try:
            async with AsyncSessionLocal() as sess:
                await pg_ops.save_user_answer(sess, email, join_code, answer_ids)
        except AnswerDoesNotExist:
            return ANSWER_DOES_NOT_EXIST

        await self.emit("user_answered", email, room=join_code)

        return ANSWER_SAVED

    async def on_user_open_answer(self, sid, question_id: int, text: str):
        """
        Reçois la réponse à une question ouverte d'un utilisateur à une session.
        """

        session: dict = await self.get_session(sid)

        email = session["email"]
        join_code = session["join_code"]

        try:
            async with AsyncSessionLocal() as sess:
                await pg_ops.save_user_open_answer(sess, email, join_code, question_id, text)
        except OpenAnswerTooLong:
            return OPEN_ANSWER_TOO_LONG
        except NotAnOpenAnswer:
            return NOT_OPEN_ANSWER

        await self.emit("user_answered", email, room=join_code)

        async with redis_ops.get_redis_session() as client:
            owner_sid = await redis_ops.get_session_sid_owner(client, join_code)
        await self.emit("user_open_answered", text, to=owner_sid)

        return ANSWER_SAVED

    async def on_end_session(self, sid):
        """
        Ordre de fin de la session, initié par le propriétaire de session.
        Tout le monde est déconnecté.
        """

        session: dict = await self.get_session(sid)

        if not session.get("is_owner", False):
            return END_SESSION_NOT_OWNER

        join_code = session["join_code"]

        async with AsyncSessionLocal() as sess:
            await pg_ops.save_session_results(sess, join_code)

        await self.emit("session_end", None, room=join_code, skip_sid=sid)

        for user_sid, _ in manager.get_participants(self.namespace, join_code):
            if user_sid != sid:
                await self.disconnect(user_sid)

        await self.close_room(join_code)

        return SESSION_ENDS
