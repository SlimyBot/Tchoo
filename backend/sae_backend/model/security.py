"""
Algorithmes de hashage de l'application.
Mots de passes et identidiants de session.
"""
import hashlib
import time

_inner_uniqueness_counter = 0


def _map_to_valid_chr_code(code: int) -> str:
    """
    Prend un code ASCII et le map à un caractère valide pour un code de session.
    Les caractères valides sont les caractères alphanumériques en minuscule et majuscule.

    Paramètres
    ----------

    code : int
        Code ASCII.

    Retour
    ------

    str
        Caractère valide.
    """
    while True:
        if code < 48:
            code += 48
        elif code > 122:
            code -= 122
        elif code > 90 and code < 97:
            code += 97
        elif code > 57 and code < 65:
            code += 65
        else:
            return chr(code)


def create_session_join_code(session_id: int) -> str:
    """
    Crée et renvoie un code adapté pour rejoindre une session.

    Paramètres
    ----------

    session_id : int
        Identifiant de la session.

    Retour
    ------

    str
        Code de session de 6 caractères.
    """
    global _inner_uniqueness_counter

    hash_obj = hashlib.sha1(str(time.time_ns()).encode("ascii"), usedforsecurity=False)
    hash_obj.update(str(session_id).encode("ascii"))
    hash_obj.update(str(_inner_uniqueness_counter).encode("ascii"))
    hashed_bytes = hash_obj.digest()

    _inner_uniqueness_counter += 1

    out = []
    for i in range(6):
        out.append(_map_to_valid_chr_code(hashed_bytes[i]))

    return "".join(out)
