from flask import Flask, jsonify, render_template, request


def create_app():
    app = Flask(__name__)
    tasks = []

    @app.get("/")
    def home():
        return render_template("index.html", tasks=tasks)

    @app.get("/tasks")
    def list_tasks():
        return jsonify(tasks)

    @app.post("/tasks")
    def create_task():
        task = {"id": len(tasks) + 1, "title": request.get_json()["title"]}
        tasks.append(task)
        return jsonify(task), 201

    return app
