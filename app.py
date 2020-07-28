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
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
#     os.path.join(basedir, 'app.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

# Recipe Table

class Recipes(db.Model):
    __tablename__ = "recipe"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    recipeImage = db.Column(db.String(999), nullable=False)
    ingredients = db.Column(db.String(9999), nullable=False)
    instructions = db.Column(db.String(9999), nullable=False)
    thumbsUp = db.Column(db.String(9999), nullable=False)
    thumbsDown = db.Column(db.String(9999), nullable=False)
    favorite = db.Column(db.String(99), nullable=False)


    def __init__(self, name, category, recipeImage, ingredients, instructions, thumbsUp, thumbsDown, favorite):
        self.name = name
        self.category = category
        self.recipeImage = recipeImage
        self.ingredients = ingredients
        self.instructions = instructions
        self.thumbsUp = thumbsUp
        self.thumbsDown = thumbsDown
        self.favorite = favorite


class RecipeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'category', 'recipeImage', 'ingredients', 'instructions', 'thumbsUp', 'thumbsDown', 'favorite')

recipe_schema = RecipeSchema()
recipes_schema = RecipeSchema(many=True)

# Comment Table

class Comments(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    recipeID = db.Column(db.String(9999), nullable=False)
    recipeComment = db.Column(db.String(9999), nullable=False)


    def __init__(self, name, recipeID, recipeComment):
        self.name = name
        self.recipeID = recipeID
        self.recipeComment = recipeComment

class CommentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'recipeID', 'recipeComment')

comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)


@app.route('/', methods=["GET"])
def home():
    return "<h1>Family Recipe DB</h1>"

@app.route('/wakeup', methods=['POST'])
def auth_user():
  return str("I am awake!")

# Recipe Endpoints

@app.route('/recipe', methods=['POST'])
def add_recipe():
    name = request.json['name']
    category = request.json['category']
    recipeImage = request.json['recipeImage']
    ingredients = request.json['ingredients']
    instructions = request.json['instructions']
    thumbsUp = request.json['thumbsUp']
    thumbsDown = request.json['thumbsDown']
    favorite = request.json['favorite']


    new_recipe = Recipes(name, category, recipeImage, ingredients, instructions, thumbsUp, thumbsDown, favorite)

    db.session.add(new_recipe)
    db.session.commit()

    recipe = Recipes.query.get(new_recipe.id)
    return recipe_schema.jsonify(recipe)


@app.route('/recipes', methods=["GET"])
def get_recipes():
    all_recipes = Recipes.query.all()
    result = recipes_schema.dump(all_recipes)

    return jsonify(result)


@app.route('/recipe/<id>', methods=['GET'])
def get_recipe(id):
    recipe = Recipe.query.get(id)

    result = recipe_schema.dump(recipe)
    return jsonify(result)


@app.route('/recipe/<id>', methods=['PATCH'])
def update_recipe(id):
    recipe = Recipes.query.get(id)

    new_name = request.json['name']
    new_category = request.json['category']
    new_recipeImage = request.json['recipeImage']
    new_ingredients = request.json['ingredients']
    new_instructions = request.json['instructions']
    new_thumbsUp = request.json['thumbsUp']
    new_thumbsDown = request.json['thumbsDown']
    new_favorite = request.json['favorite']

    user.name = new_name
    user.category = new_category
    user.recipeImage = new_recipeImage
    user.ingredients = new_ingredients
    user.instructions = new_instructions
    user.thumbsUp = new_thumbsUp
    user.thumbsDown = new_thumbsDown
    user.favorite = new_favorite

    db.session.commit()
    return recipe_schema.jsonify(recipe)

@app.route('/recipe/<id>', methods=['DELETE'])
def delete_recipe(id):
    record = Recipe.query.get(id)
    db.session.delete(record)
    db.session.commit()

    return jsonify('Item deleted')

# Comment endpoints

@app.route('/comment', methods=['POST'])
def add_comment():
    name = request.json['name']
    recipeID = request.json['recipeID']
    recipeComment = request.json['recipeComment']

    new_comment = Comments(name, recipeID, recipeComment)

    db.session.add(new_comment)
    db.session.commit()

    comment = Comments.query.get(new_comment.id)
    return comment_schema.jsonify(comment)


@app.route('/comments', methods=["GET"])
def get_comments():
    all_comments = Comments.query.all()
    result = comments_schema.dump(all_comments)

    return jsonify(result)


@app.route('/comment/<id>', methods=['GET'])
def get_comment(id):
    comment = Comment.query.get(id)

    result = comment_schema.dump(comment)
    return jsonify(result)


@app.route('/comment/<id>', methods=['PATCH'])
def update_comment(id):
    comment = Comments.query.get(id)

    new_name = request.jsos['name']
    new_recipeID = request.json['recipeID']
    new_recipeComment = request.json['recipeComment']

    user.name = new_name
    user.recipeID = new_recipeID
    user.recipeComment = new_recipeComment

    db.session.commit()
    return comment_schema.jsonify(comment)

@app.route('/comment/<id>', methods=['DELETE'])
def delete_comment(id):
    record = Comment.query.get(id)
    db.session.delete(record)
    db.session.commit()

    return jsonify('Item deleted')


if __name__ == "__main__":
    app.debug = True
    app.run()