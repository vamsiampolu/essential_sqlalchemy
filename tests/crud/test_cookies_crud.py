import pytest
from typing import Generator
from sqlalchemy.engine import Connection, Engine

from essential_sqlalchemy.config import Config
from essential_sqlalchemy.db.engine import get_engine
from essential_sqlalchemy.db.metadata import metadata

from essential_sqlalchemy.crud.cookies_crud import Cookies
from essential_sqlalchemy.models.cookie import Cookie


@pytest.fixture(scope="session")
def config() -> Generator[Config, None, None]:
    Config.__config__.env_file = ".env.test"
    config = Config(DB_NAME="cookie_shop_test")
    yield config


@pytest.fixture(scope="session")
def engine(config: Config) -> Generator[Engine, None, None]:
    engine = get_engine(config)
    yield engine


@pytest.fixture(scope="session")
def connection(engine: Engine) -> Generator[Connection, None, None]:
    connection: Connection = engine.connect()
    yield connection


@pytest.fixture(scope="function", autouse=True)
def manage_tables(engine: Engine) -> Generator:
    metadata.create_all(bind=engine)
    yield metadata.tables.keys()
    print("dropping tables")
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


def test_cookies_count(connection: Connection) -> None:
    cookies = Cookies(connection=connection)
    assert cookies.get_cookie_rows_count() == 0


def has_n_items(items: list | set, n: int) -> bool:
    return len(items) == n


def are_cookies_equal_excluding_id(cookie: Cookie, other: Cookie) -> bool:
    exclude = {"cookie_id"}
    return cookie.copy(exclude=exclude) == other.copy(exclude=exclude)


def lists_have_same_values_ignoring_order_of_elements(
    list_a: list, list_b: list
) -> bool:
    diff = set(list_a) ^ set(list_b)
    return len(list_a) == len(list_b) and len(diff) == 0


def test_get_all(connection: Connection) -> None:
    cookies = Cookies(connection=connection)
    cookie = Cookie(
        cookie_name="choc chip",
        cookie_recipe_url="https://example.com/recipe/choc-chip",
        cookie_sku="choc_chip_123",
        quantity=25,
        unit_cost=12.25,
    )

    cookies.insert_one(cookie)

    cookies_list = cookies.get_all()

    assert len(cookies_list) == 1
    assert are_cookies_equal_excluding_id(cookies_list[0], cookie)


def test_get_one(connection: Connection) -> None:
    cookies = Cookies(connection)
    cookie = Cookie(
        cookie_name="white chip",
        cookie_recipe_url="https://example.com/recipe/white-chip",
        cookie_sku="white_choc_213",
        quantity=41,
        unit_cost=7.50,
    )
    cookies.insert_one(cookie)

    actual = cookies.get_one()
    assert are_cookies_equal_excluding_id(actual, cookie)


def test_get_all_no_records(connection: Connection) -> None:
    cookies = Cookies(connection)
    assert len(cookies.get_all()) == 0


def test_get_all_cookie_name_and_quantity(connection: Connection) -> None:
    cookies = Cookies(connection)
    cookie = Cookie(
        cookie_name="vanilla raspberry",
        cookie_recipe_url="https://example.com/recipe/vanilla_raspberry",
        cookie_sku="white_ras_444",
        quantity=35,
        unit_cost=16.00,
    )

    cookies.insert_many([cookie])

    cookie_labels = cookies.get_all_cookie_name_and_quantity()
    assert cookie_labels == [{"cookie_name": "vanilla raspberry", "quantity": 35}]


def test_get_all_cookie_name_and_quantity_no_records(connection: Connection) -> None:
    cookies = Cookies(connection)
    assert len(cookies.get_all_cookie_name_and_quantity()) == 0


def test_find_one_by_name_cookie_exists(connection: Connection) -> None:
    cookies = Cookies(connection)

    triple_choc_cookie = Cookie(
        cookie_name="triple choc",
        cookie_recipe_url="https://example.com/recipe/triple_choc",
        cookie_sku="triple_choc_350",
        quantity=42,
        unit_cost=10.00,
    )
    choc_chip_cookie = Cookie(
        cookie_name="choc chip",
        cookie_recipe_url="https://example.com/recipe/choc_chip",
        cookie_sku="choc_chip_123",
        quantity=25,
        unit_cost=12.50,
    )

    cookies.insert_one(triple_choc_cookie)
    cookies.insert_one(choc_chip_cookie)

    actual = cookies.find_one_by_name("choc chip")

    print(actual)

    assert actual is not None

    assert are_cookies_equal_excluding_id(actual, choc_chip_cookie)


def test_find_one_by_name_cookie_does_not_exist(connection: Connection) -> None:
    cookies = Cookies(connection)

    transaction = connection.begin()

    cookie = Cookie(
        cookie_name="vanilla raspberry",
        cookie_recipe_url="https://example.com/recipe/vanilla_raspberry",
        cookie_sku="white_ras_444",
        quantity=35,
        unit_cost=16.00,
    )

    cookies.insert_one(cookie)
    transaction.commit()

    actual = cookies.find_one_by_name("choc chip")

    assert actual is None


def test_get_top_n_cookies_by_quantity(connection: Connection) -> None:
    cookies = Cookies(connection)

    inventory_list = [
        Cookie(
            cookie_name="choc chip",
            cookie_recipe_url="http://some.yum.my/cookie/choc-chip.html",
            cookie_sku="CC01",
            quantity=225,
            unit_cost=0.40,
        ),
        Cookie(
            cookie_name="peanut_butter",
            cookie_recipe_url="http://some.aweso.me/cookie/peanut.html",
            cookie_sku="PB01",
            quantity=24,
            unit_cost=0.25,
        ),
        Cookie(
            cookie_name="oatmeal_raisin",
            cookie_recipe_url="http://some.okay.me/cookie/raisin.html",
            cookie_sku="EWW01",
            quantity=100,
            unit_cost=1.00,
        ),
    ]

    top_2_cookies = [
        Cookie(
            cookie_name="choc chip",
            cookie_recipe_url="http://some.yum.my/cookie/choc-chip.html",
            cookie_sku="CC01",
            quantity=225,
            unit_cost=0.40,
        ),
        Cookie(
            cookie_name="oatmeal_raisin",
            cookie_recipe_url="http://some.okay.me/cookie/raisin.html",
            cookie_sku="EWW01",
            quantity=100,
            unit_cost=1.00,
        ),
    ]

    transaction = connection.begin()
    cookies.insert_many(inventory_list)
    transaction.commit()

    top_cookies = cookies.get_top_n_cookies_by_quantity(2)

    print(top_cookies[0].json())

    assert are_cookies_equal_excluding_id(top_cookies[0], top_2_cookies[0])
    assert are_cookies_equal_excluding_id(top_cookies[1], top_2_cookies[1])


def test_get_top_n_cookies_with_less_than_n_records(connection: Connection) -> None:
    cookies = Cookies(connection)

    inventory_list = [
        Cookie(
            cookie_name="choc chip",
            cookie_recipe_url="http://some.yum.my/cookie/choc-chip.html",
            cookie_sku="CC01",
            quantity=225,
            unit_cost=0.40,
        ),
        Cookie(
            cookie_name="oatmeal_raisin",
            cookie_recipe_url="http://some.okay.me/cookie/raisin.html",
            cookie_sku="EWW01",
            quantity=100,
            unit_cost=1.00,
        ),
    ]

    transaction = connection.begin()
    cookies.insert_many(inventory_list)
    transaction.commit()

    top_cookies = cookies.get_top_n_cookies_by_quantity(3)

    assert len(top_cookies) == 2


def test_get_cookies_with_name_like(connection: Connection) -> None:
    cookies = Cookies(connection)

    cookie = Cookie(
        cookie_name="vanilla raspberry",
        cookie_recipe_url="https://example.com/recipe/vanilla_raspberry",
        cookie_sku="white_ras_444",
        quantity=35,
        unit_cost=16.00,
    )

    transaction = connection.begin()
    cookies.insert_one(cookie)
    transaction.commit()

    matched_cookies = cookies.get_cookie_with_name_like("ras")

    assert matched_cookies[0].cookie_name == "vanilla raspberry"


def test_get_cookies_with_name_like_no_matches(connection: Connection) -> None:
    cookies = Cookies(connection)

    cookie = Cookie(
        cookie_name="vanilla raspberry",
        cookie_recipe_url="https://example.com/recipe/vanilla_raspberry",
        cookie_sku="white_ras_444",
        quantity=35,
        unit_cost=16.00,
    )

    transaction = connection.begin()
    cookies.insert_one(cookie)
    transaction.commit()

    matched_cookies = cookies.get_cookie_with_name_like("choc")

    assert len(matched_cookies) == 0


def test_get_cookies_with_name_like_multiple_matches(connection: Connection) -> None:
    cookies = Cookies(connection)

    inventory_list = [
        Cookie(
            cookie_name="choc chip",
            cookie_recipe_url="http://some.yum.my/cookie/choc-chip.html",
            cookie_sku="CC01",
            quantity=225,
            unit_cost=0.40,
        ),
        Cookie(
            cookie_name="oatmeal raisin",
            cookie_recipe_url="http://some.okay.me/cookie/raisin.html",
            cookie_sku="EWW01",
            quantity=100,
            unit_cost=1.00,
        ),
        Cookie(
            cookie_name="triple choc",
            cookie_recipe_url="http://some.yum.my/cookie/triple-choc.html",
            cookie_sku="TC01",
            quantity=400,
            unit_cost=0.75,
        ),
    ]

    transaction = connection.begin()
    cookies.insert_many(inventory_list)
    transaction.commit()

    matched_cookies = cookies.get_cookie_with_name_like("choc")
    cookie_names = [item.cookie_name for item in matched_cookies]

    assert lists_have_same_values_ignoring_order_of_elements(
        cookie_names, ["choc chip", "triple choc"]
    )
