import pytest
from typing import Generator
from sqlalchemy.engine import Connection

from essential_sqlalchemy.config import Config
from essential_sqlalchemy.db.engine import engine
from essential_sqlalchemy.db.metadata import metadata

from essential_sqlalchemy.crud.cookies_crud import Cookies
from essential_sqlalchemy.models.cookie import Cookie


@pytest.fixture(scope="session")
def connection() -> Generator[Connection, None, None]:
    Config.__config__.env_file = ".env.test"

    connection: Connection = engine.connect()
    metadata.create_all(bind=engine)

    yield connection

    metadata.drop_all(bind=engine)


def test_insert_one_cookie(connection: Connection) -> None:
    cookies = Cookies(connection)
    cookie = Cookie(
        cookie_name="choc chip",
        cookie_recipe_url="https://example.com/recipe/choc-chip",
        cookie_sku="choc_chip_123",
        quantity=25,
        unit_cost=12.25,
    )
    row = cookies.insert_one(cookie)
    assert row is not None


def test_insert_many_cookies(connection: Connection) -> None:
    cookies = Cookies(connection)
    cookie_list = [
        Cookie(
            **{
                "cookie_name": "peanut butter",
                "cookie_recipe_url": "http://some.aweso.me/cookie/peanut.html",
                "cookie_sku": "PB01",
                "quantity": 24,
                "unit_cost": 0.25,
            }
        ),
        Cookie(
            **{
                "cookie_name": "oatmeal raisin",
                "cookie_recipe_url": "http://some.okay.me/cookie/raisin.html",
                "cookie_sku": "EWW01",
                "quantity": 100,
                "unit_cost": 1.00,
            }
        ),
    ]

    result = cookies.insert_many(cookie_list)
    assert len(result.inserted_primary_key_rows) == 2
