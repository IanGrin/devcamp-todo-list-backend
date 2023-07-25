from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

import os

app = Flask(__name__)
# basedir = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + \
#     os.path.join(basedir, 'app.sqlite')

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://xfbgoobatvybmy:61c896f2979511f0211ac9b19346627f4120272cfe5fa61781c86b1298aaf3e4@ec2-34-202-127-5.compute-1.amazonaws.com:5432/da84p4rs433fi5' + os.path.join(basedir, 'app.sqlite')

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
