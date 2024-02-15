"""
Codes des évenements socket.io
"""

## Renvoyé par session_connect

# Le propriétaire de la session rejoind sa session
OWNER_JOINS_SESSION = ("owner_join", "Bienvenu, propriétaire de la session")

# Utilisateur déjà connecté a la session
USER_ALREADY_JOINED = ("already_joined", "Deja connecté a la session")

# Un utilisateur rejoind la session
USER_JOINS_SESSION = ("join", "Bienvenu dans la session, utilisateur")

# L'utilisateur n'a pas le droit de rejoindre la session
USER_NOT_ALLOWED = ("join_not_allowed", "Pas de droit de rejoindre la session")

# La session n'est pas joignable
SESSION_NOT_JOINABLE = ("not_joinable", "La session n'existe pas, a déjà commencé ou est finie")


## Renvoyé par initiate_next_question

# Un utilisteur tente de passer à la prochaine question
NEXT_QUESTION_NOT_OWNER = ("refused", "Vous n'êtes pas le propriétaire de la session")

# Fin du questionaire de question, il n'y a pas de question suivante
NO_MORE_QUESTIONS = "no_more_questions", "Fin du questionaire"

# Passage à la question suivante
NEXT_QUESTION = ("next_question", "Passage à la question suivante")


## Renvoyé par user_answer

# L'ID de réponse ne correspond pas
ANSWER_DOES_NOT_EXIST = ("answer_does_not_exist", "Une réponse choisi n'existe pas")


## Renvoyé par user_open_answer

# La réponse ouverte est trop longue (+ de 1 mots alors qu'elle ne devrait pas)
OPEN_ANSWER_TOO_LONG = ("open_answer_too_long", "Seule une réponse d'un seul mot est autorisé pour cette question")

# Cette question n'est pas une réponse ouverte
NOT_OPEN_ANSWER = ("not_open_answer", "La question n'accepte pas de réponses ouvertes")


## Renvoyé par les deux ci-dessus

# Un utilisateur répond
ANSWER_SAVED = ("answer_saved", "Réponse enregistrée")


## Renvoyé par end_session

# Un utilisateur tente d'arrêter la session
END_SESSION_NOT_OWNER = NEXT_QUESTION_NOT_OWNER

# La session prend fin
SESSION_ENDS = ("session_ends", "Fin de session")
