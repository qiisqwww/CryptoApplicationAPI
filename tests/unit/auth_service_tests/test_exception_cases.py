import pytest

from src.application.services import AuthService, UserWasNotFoundException


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "username, password",
    [
        ("unregistered_user", "does_not_matter"),
        ("user3", "abra_kadabra")
    ]
)
async def test_authenticate_user_was_not_found(
        username: str,
        password: str,
        auth_service: AuthService,
        monkeypatch
) -> None:
    with pytest.raises(UserWasNotFoundException):
        await auth_service.authenticate(username, password)
