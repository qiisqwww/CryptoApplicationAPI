from src.application.utils import PasswdUtils
from src.entities import User

__all__ = [
    "users_list",
]


users_list: list[User] = [
    User(
        id=1,
        username="user1",
        email="user1@gmail.com",
        hashed_password=PasswdUtils.hashed_password("user1")
    ),
    User(
        id=2,
        username="user2",
        email="user2@gmail.com",
        hashed_password=PasswdUtils.hashed_password("user2")
    ),
    User(
        id=3,
        username="user3",
        email="user3@gmail.com",
        hashed_password=PasswdUtils.hashed_password("user3")
    ),
    User(
        id=4,
        username="user4",
        email="user4@gmail.com",
        hashed_password=PasswdUtils.hashed_password("user4")
    )
]
