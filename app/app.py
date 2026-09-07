import os

from flask import Flask, jsonify, render_template, request

from app.models import Task, db


def create_app(config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", "sqlite:///:memory:"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    if config:
        app.config.update(config)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    @app.get("/")
    def home():
        return render_template("index.html", tasks=Task.query.all())

    @app.get("/tasks")
    def list_tasks():
        return jsonify([task.to_dict() for task in Task.query.all()])

    @app.post("/tasks")
    def create_task():
        task = Task(title=request.get_json()["title"])
        db.session.add(task)
        db.session.commit()
        return jsonify(task.to_dict()), 201

    return app
