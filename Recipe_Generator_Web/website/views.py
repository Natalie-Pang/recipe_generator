import json
from flask import Blueprint, render_template, request

views = Blueprint('views', __name__)

def load_recipes_from_json():
    json_path = r'D:\Projects\Recipe_Generator_Web\website\recipe.json'
    with open(json_path, 'r') as json_file:
        return json.load(json_file)

@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        selected_age = int(request.form.get('age'))
        selected_gender = request.form.get('gender')
        selected_weight = int(request.form.get('weight'))
        selected_height = int(request.form.get('height'))

        if selected_gender == 'M':
            calorie_needs = (66.5 + 13.8 * selected_weight + 5 * selected_height / 6.8 * selected_age)
        else:
            calorie_needs = (655.1 + 9.6 * selected_weight + 1.9 * selected_height / 4.7 * selected_age)

        return render_template('home.html', calorie_needs=calorie_needs)

    return render_template('home.html')


@views.route('/recipe/', methods=['GET', 'POST'])
def recipe():
    recipes = load_recipes_from_json()

    if request.method == 'POST':
        selected_ingredients = request.form.getlist('ingredients')
        selected_allergies = request.form.getlist('allergies')
        selected_health_issues = request.form.getlist('health_issue')

        matching_recipes = []

        if selected_ingredients:
            for recipe in recipes:
                if all(ingredient in recipe['ingredients'] for ingredient in selected_ingredients):
                    if any(allergies in recipe['allergies'] for allergies in selected_allergies):
                        continue
                    if any(health_issue in recipe['health_issue'] for health_issue in selected_health_issues):
                        continue
                    matching_recipes.append(recipe)
        else:
            matching_recipes = []

        return render_template('recipe.html', recipes=matching_recipes)

    return render_template('recipe.html', recipes=recipes)


@views.route('/advice/')
def advice():
     return render_template('advice.html')