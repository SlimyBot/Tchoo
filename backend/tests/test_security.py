from sae_backend.model.security import create_session_join_code


def test_session_code_unique():
    codes = []
    for _ in range(50):
        codes.append(create_session_join_code(18))

    assert len(list(set(codes))) == len(codes), "Duplication de code"
