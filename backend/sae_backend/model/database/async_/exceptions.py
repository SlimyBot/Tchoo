"""
Erreurs pouvant être déclencché lors des sessions.
"""


class SessionException(Exception):
    """
    Exception de base pour tout ce qui est lié aux sessions.
    """


class AnswerDoesNotExist(SessionException):
    """
    Si un ID de réponse n'existe pas.
    """


class NotAnOpenAnswer(SessionException):
    """
    Si on tente de répondre ouvertement à une question de type QCM.
    """


class OpenAnswerTooLong(SessionException):
    """
    Si une réponse à une question ouverte avec un seul mot autorisé.
    """
