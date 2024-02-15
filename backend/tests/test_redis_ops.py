import pytest
from redis import ConnectionError

from sae_backend.model.redis_operations import get_redis_session, join_session, leave_session, nb_users_in_session


@pytest.fixture
async def redis_client():
    async with get_redis_session() as client:
        try:
            await client.ping()
        except ConnectionError:
            pytest.skip("No Redis server reacheable")

        return client


@pytest.mark.asyncio
async def test_full_redis_session_flow(redis_client):
    client = await redis_client

    join_code = "H3lPm3"

    await client.delete(f"{join_code}:users")

    assert await nb_users_in_session(client, join_code) == 0, "Too many users in session"

    await join_session(client, "hello", join_code)
    assert await nb_users_in_session(client, join_code) == 1, "There isn't one user in the session"

    await join_session(client, "joe", join_code)
    assert await nb_users_in_session(client, join_code) == 2, "There isn't two users in the session"

    await leave_session(client, "hello", join_code)
    assert await nb_users_in_session(client, join_code) == 1, "There isn't one user in the session"

    await leave_session(client, "joe", join_code)
    assert await nb_users_in_session(client, join_code) == 0, "Too many users in session"
