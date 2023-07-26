from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

import os

app = Flask(__name__)
# basedir = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + \
#     os.path.join(basedir, 'app.sqlite')

app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://fnzergzxycybba:465d500d8cc9b1afae5932d306add414d2a3e225cb3ee905373f1c4fdac377c5@ec2-44-206-204-65.compute-1.amazonaws.com:5432/d48v7f91vkks0g"

db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    progress = db.Column(db.Integer, nullable=False)

    def __init__(self, title, progress):
        self.title = title
        self.progress = progress


class TodoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'progress')


todo_schema = TodoSchema()
todos_schema = TodoSchema(many=True)


@app.route('/todos', methods=['GET'])
def get_todos():
    all_todos = Todo.query.all()
    result = todos_schema.dump(all_todos)
    return jsonify(result)


@app.route('/todo/<id>', methods=["GET"])
def get_todo(id):
    todo = Todo.query.get(id)
    return todo_schema.jsonify(todo)


@app.route('/todos', methods=['POST'])
def add_todo():
    title = request.json['title']
    progress = request.json['progress']
    new_todo = Todo(title, progress)
    db.session.add(new_todo)
    db.session.commit()
    return todo_schema.jsonify(new_todo)


@app.route('/todo/<id>', methods=["PUT"])
def update_todo(id):
    todo = Todo.query.get(id)
    title = request.json['title']
    progress = request.json['progress']
    todo.title = title
    todo.progress = progress
    db.session.commit()
    return todo_schema.jsonify(todo)


@app.route('/todo/<id>', methods=['DELETE'])
def delete_todo(id):
    todo = Todo.query.get(id)
    db.session.delete(todo)
    db.session.commit()
    return todo_schema.jsonify(todo)


if __name__ == '__main__':
    app.run(debug=True)
