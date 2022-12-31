from essential_sqlalchemy.db.create_tables import create_tables, engine
from essential_sqlalchemy.schemas.cookies import cookies
from essential_sqlalchemy.schemas.users import users

from essential_sqlalchemy.crud.cookies_crud import Cookies, Cookie

print("foobar")
create_tables()

connection = engine.connect()

cookies = Cookies(connection=connection)
# cookie = Cookie(
#     cookie_name="chocolate chip",
#     cookie_recipe_url="http://some.aweso.me/cookie/recipe.html",
#     cookie_sku="CC01",
#     quantity=12,
#     unit_cost=0.50,
# )

# result = cookies.insert_one(cookie)
# print(result)

# cookie_records = cookies.get_all()
# print(cookie_records)

cookies.get_all_cookie_name_and_quantity()

inventory_list = [
    {
        'cookie_name': 'peanut butter',
        'cookie_recipe_url': 'http://some.aweso.me/cookie/peanut.html',
        'cookie_sku': 'PB01',
        'quantity': '24',
        'unit_cost': '0.25'
    },
    {
        'cookie_name': 'oatmeal raisin',
        'cookie_recipe_url': 'http://some.okay.me/cookie/raisin.html',
        'cookie_sku': 'EWW01',
        'quantity': '100',
        'unit_cost': '1.00'
    }
]


def dict_to_model(obj):
    return Cookie(**obj)

def model_to_json(obj):
    return obj.json()

# cookie_models = list(map(dict_to_model, inventory_list))

# cookies.insert_many(cookie_models)

cookie_details = cookies.get_all_cookie_name_and_quantity()
print(cookie_details)

choco_chip = cookies.find_one_by_name('chocolate chip')
print(choco_chip.json())