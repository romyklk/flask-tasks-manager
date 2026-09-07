import os

from flask import Flask, jsonify, redirect, render_template, request, url_for

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

    @app.patch("/tasks/<int:task_id>")
    def update_task(task_id):
        task = db.session.get(Task, task_id)
        if task is None:
            return jsonify({"error": "Tâche introuvable"}), 404
        data = request.get_json()
        if "title" in data:
            task.title = data["title"]
        if "done" in data:
            task.done = data["done"]
        db.session.commit()
        return jsonify(task.to_dict())

    @app.delete("/tasks/<int:task_id>")
    def delete_task(task_id):
        task = db.session.get(Task, task_id)
        if task is None:
            return jsonify({"error": "Tâche introuvable"}), 404
        db.session.delete(task)
        db.session.commit()
        return "", 204

    @app.post("/web/tasks")
    def web_create_task():
        title = request.form.get("title", "").strip()
        if title:
            db.session.add(Task(title=title))
            db.session.commit()
        return redirect(url_for("home"))

    @app.post("/web/tasks/<int:task_id>/toggle")
    def web_toggle_task(task_id):
        task = db.session.get(Task, task_id)
        if task is not None:
            task.done = not task.done
            db.session.commit()
        return redirect(url_for("home"))

    @app.post("/web/tasks/<int:task_id>/delete")
    def web_delete_task(task_id):
        task = db.session.get(Task, task_id)
        if task is not None:
            db.session.delete(task)
            db.session.commit()
        return redirect(url_for("home"))

    return app
