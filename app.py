from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_heroku import Heroku
from environs import Env
import psycopg2
import os

app = Flask(__name__)
CORS(app)
heroku = Heroku(app)

env = Env()
env.read_env()
DATABASE_URL = env("DATABASE_URL")

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'app.sqlite')
# app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Recipes(db.Model):
    __tablename__ = "recipe"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    ingredients = db.Column(db.String(9999), nullable=False)
    instructions = db.Column(db.String(9999), nullable=False)
    thumbsUp = db.Column(db.String(9999), nullable=False)
    thumbsDown = db.Column(db.String(9999), nullable=False)


    def __init__(self, name, highScore):
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions
        self.thumbsUp = thumbsUp
        self.thumbsDown = thumbsDown

class ScoreSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'ingredients', 'instructions', 'thumbsUp', 'thumbsDown')

recipe_schema = ScoreSchema()
recipes_schema = ScoreSchema(many=True)

@app.route('/', methods=["GET"])
def home():
    return "<h1>Family Recipe DB</h1>"

@app.route('/wakeup', methods=['POST'])
def auth_user():
  return str("I am awake!")

@app.route('/score', methods=['POST'])
def add_score():
    name = request.json['name']
    ingredients = request.json['ingredients']
    instructions = request.json['instructions']
    thumbsUp = request.json['thumbsUp']
    thumbsDown = request.json['thumbsDown']


    new_recipe = Recipes(name, ingredients, instructions, thumbsUp, thumbsDown)

    db.session.add(new_recipe)
    db.session.commit()

    recipe = Recipes.query.get(new_recipe.id)
    return recipe_schema.jsonify(recipe)


@app.route('/recipes', methods=["GET"])
def get_receipes():
    all_recipes = Recipes.query.all()
    result = recipes_schema.dump(all_recipes)

    return jsonify(result)


@app.route('/recipe/<id>', methods=['GET'])
def get_recipe(id):
    recipe = Recipe.query.get(id)

    result = recipe_schema.dump(recipe)
    return jsonify(result)


@app.route('/recipe/<id>', methods=['PATCH'])
def update_user(id):
    recipe = Recipes.query.get(id)

    new_name = request.json['name']
    new_ingredients = request.json['ingredients']
    new_instructions = request.json['instructions']
    new_thumbsUp = request.json['thumbsUp']
    new_thumbsDown = request.json['thumbsDown']

    user.name = new_name
    user.ingredients = new_ingredients
    user.instructions = new_instructions
    user.thumbsUp = new_thumbsUp
    user.thumbsDown = thumbsDown

    db.session.commit()
    return recipe_schema.jsonify(recipe)

@app.route('/recipe/<id>', methods=['DELETE'])
def delete_recipe(id):
    record = Recipe.query.get(id)
    db.session.delete(record)
    db.session.commit()

    return jsonify('Item deleted')


if __name__ == "__main__":
    app.debug = True
    app.run()