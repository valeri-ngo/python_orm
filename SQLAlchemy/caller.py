"""
1. pip install sqlalchemy
2. pip install alembic
3. pip install psycopg2
4. Create DB
5. Create Base class
6. alembic init alembic
7. Update target_metadata
8. Configure DB url
9. Create engine
10. Create sessionmaker
"""

from typing import Any

from sqlalchemy import Row, RowMapping, Sequence, create_engine, delete, select, update
from sqlalchemy.orm import sessionmaker

from models import Recipe, Chef
from helpers import handle_session


engine = create_engine(f"postgresql+psycopg2://postgres:password@localhost/sqlalchemy")
Session = sessionmaker(bind=engine)
session = Session()


@handle_session(session)
def create_recipe(name: str, ingredients: str, instructions: str) -> None:
    recipe = Recipe(
        name=name,
        ingredients=ingredients,
        instructions=instructions
    )

    session.add(recipe)


@handle_session(session)
def update_recipe_by_name(name: str, new_name: str,  new_ingredients: str, new_instructions: str) -> None:
    """
    UPDATE recipe
    SET
        name = new_name,
        igredients = new_ingredients,
        instructions = new_instructions
    WHERE
        name = <name>;
    """

    session.execute(
        update(Recipe)
        .where(Recipe.name == name)
        .values(
            name = new_name,
            ingredients = new_ingredients,
            instructions = new_instructions
        )
    )

# # Update a recipe by name
# update_recipe_by_name(
#     name="Spaghetti Carbonara",
#     new_name="Carbonara Pasta",
#     new_ingredients="Pasta, Eggs, Guanciale, Cheese",
#     new_instructions="Cook the pasta, mix with eggs, guanciale, and cheese"
# )

# # Query the updated recipe 
# updated_recipe = session.query(Recipe).filter_by(name="Carbonara Pasta").first()

# # Print the updated recipe details
# print("Updated Recipe Details:")
# print(f"Name: {updated_recipe.name}")
# print(f"Ingredients: {updated_recipe.ingredients}")
# print(f"Instructions: {updated_recipe.instructions}")


@handle_session(session)
def delete_recipe_by_name(name: str) -> None:
    """
    DELETE FROM recipe
    WHERE name = <name>;
    """

    session.execute(
        delete(Recipe).where(Recipe.name == name)
    )

# # Delete a recipe by name
# delete_recipe_by_name("Carbonara Pasta")

# # Query all recipes
# recipes = session.query(Recipe).all()

# # Loop through each recipe and print its details
# for recipe in recipes:
#     print(f"Recipe name: {recipe.name}")

@handle_session(session, autoclose=False)
def get_recipes_by_ingredient(ingredient_name: str) -> Sequence[Row[Any] | RowMapping | Any]:
    """
    SELECT
        *
    FROM recipe
    WHERE
        ingredients ILIKE "%ingredient_name%";
    """

    return session.scalars(
        select(Recipe).where(
            Recipe.ingredients.ilike(f"%{ingredient_name}%")
        )
    ).all()


@handle_session(session)
def swap_recipe_ingredients_by_name(first_recipe_name: str, second_recipe_name: str) -> None:
    first_recipe = session.scalars(
        select(Recipe)
        .where(Recipe.name == first_recipe_name)
        .with_for_update()      # Locks the record until transaction is finished
    ).one()

    second_recipe = session.scalars(
        select(Recipe)
        .where(Recipe.name == second_recipe_name)
        .with_for_update()      # Locks the record until transaction is finished
    ).one()

    first_recipe.ingredients, second_recipe.ingredients = second_recipe.ingredients, first_recipe.ingredients

# # Delete all objects (recipes) from the database
# session.query(Recipe).delete()
# session.commit()

# # Create the first recipe
# create_recipe("Pancakes", "Flour, Eggs, Milk", "Mix and cook on a griddle")

# # Create the second recipe
# create_recipe("Waffles", "Flour, Eggs, Milk, Baking Powder", "Mix and cook in a waffle iron")

# # Now, swap their ingredients
# swap_recipe_ingredients_by_name("Pancakes", "Waffles")

# recipe1 = session.query(Recipe).filter_by(name="Pancakes").first()
# recipe2 = session.query(Recipe).filter_by(name="Waffles").first()
# print(f"Pancakes ingredients {recipe1.ingredients}")
# print(f"Waffles ingredients {recipe2.ingredients}")

@handle_session(session)
def relate_recipe_with_chef_by_name(recipe_name: str, chef_name: str):
    recipe = session.scalars(
        select(Recipe)
        .where(Recipe.name == recipe_name)
    ).one()     # Recipe(...)

    if recipe.chef:
        raise Exception(f"Recipe: {recipe_name} already has a related chef")

    chef = session.scalars(
        select(Chef)
        .where(Chef.name == chef_name)
    ).one()

    recipe.chef = chef

    return f"Related recipe {recipe_name} with chef {chef_name}"

# # Create a recipe instance for Bulgarian Musaka
# musaka_recipe = Recipe(
#     name="Musaka",
#     ingredients="Potatoes, Ground Meat, Onions, Eggs, Milk, Cheese, Spices",
#     instructions="Layer potatoes and meat mixture, pour egg and milk mixture on top, bake until golden brown."
# )

# # Create a Bulgarian chef instances
# bulgarian_chef1 = Chef(name="Ivan Zvezdev")
# bulgarian_chef2 = Chef(name="Uti Buchvarov")

# # Add the recipe instance to the session
# session.add(musaka_recipe)

# # Add the chef instances to the session
# session.add(bulgarian_chef1)
# session.add(bulgarian_chef2)

# # Commit the changes to the database
# session.commit()

# print(relate_recipe_with_chef_by_name("Musaka", "Ivan Zvezdev"))
# print(relate_recipe_with_chef_by_name("Musaka", "Chef Uti"))


@handle_session(session)
def get_recipes_with_chef() -> str:
    """
    SELECT
        recipe.name,
        chef.name
    FROM
        recipe
    JOIN
        chef
    ON
        chef.id = recipe.chef_id
    """

    recipies = session.execute(
        select(Recipe.name, Chef.name).join(Recipe.chef)
    ).all()     # [("Pancakes", "Uti"), (...)]

    return '\n'.join(
        f"Recipe: {recipe_name} made by chef: {chef_name}"
        for recipe_name, chef_name in recipies
    )

# # Delete all objects (recipes and chefs) from the database
# session.query(Recipe).delete()
# session.query(Chef).delete()
# session.commit()

# # Create chef instances
# chef1 = Chef(name="Gordon Ramsay")
# chef2 = Chef(name="Julia Child")
# chef3 = Chef(name="Jamie Oliver")
# chef4 = Chef(name="Nigella Lawson")

# # Create recipe instances associated with chefs
# recipe1 = Recipe(name="Beef Wellington", ingredients="Beef fillet, Puff pastry, Mushrooms, Foie gras", instructions="Prepare the fillet and encase it in puff pastry.")
# recipe1.chef = chef1

# recipe2 = Recipe(name="Boeuf Bourguignon", ingredients="Beef, Red wine, Onions, Carrots", instructions="Slow-cook the beef with red wine and vegetables.")
# recipe2.chef = chef2

# recipe3 = Recipe(name="Spaghetti Carbonara", ingredients="Spaghetti, Eggs, Pancetta, Cheese", instructions="Cook pasta, mix ingredients.")
# recipe3.chef = chef3

# recipe4 = Recipe(name="Chocolate Cake", ingredients="Chocolate, Flour, Sugar, Eggs", instructions="Bake a delicious chocolate cake.")
# recipe4.chef = chef4

# recipe5 = Recipe(name="Chicken Tikka Masala", ingredients="Chicken, Yogurt, Tomatoes, Spices", instructions="Marinate chicken and cook in a creamy tomato sauce.")
# recipe5.chef = chef3

# session.add_all([chef1, chef2, chef3, chef4, recipe1, recipe2, recipe3, recipe4, recipe5])
# session.commit()
# print(get_recipes_with_chef())