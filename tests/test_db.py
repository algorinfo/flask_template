# pylint: disable=unused-argument
from changeme.db.sql import SQL
from changeme.models.users import User


def _insert_user(db) -> User:
    user = User(
        email="test@test.com",
        password="test"
    )

    db.add(user)
    # commit(db)
    db.commit()
    return user


def test_db_User(clean_db, db):
    _insert_user(db)

    user = db.query(User).first()

    assert user.email == "test@test.com"
    assert user.check_password("test") == True
