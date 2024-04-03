from .extensions import db
from datetime import datetime

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<User {self.email}>'

class Model(db.Model):
    model_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    

class Dataset(db.Model):
    dataset_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)


class Node(db.Model):
    node_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    cpu_cores = db.Column(db.Integer, nullable=False)
    gpu_cores = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(128), nullable=False)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    model_id = db.Column(db.Integer, db.ForeignKey('model.model_id'), nullable=False)
    dataset_id = db.Column(db.Integer, db.ForeignKey('dataset.dataset_id'), nullable=False)
    status = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    result = db.Column(db.Text, nullable=True)

class ProjectNode(db.Model):
    project_node_id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    node_id = db.Column(db.Integer, db.ForeignKey('node.node_id'), nullable=False)
    status = db.Column(db.String(128), nullable=True)