# Gestionnaire de tâches — Flask

Petite application de gestion de tâches développée avec **Flask** : une API JSON et une interface web (template HTML) qui utilise cette même API en arrière-plan. Elle expose :

- `GET /tasks` — liste toutes les tâches (JSON)
- `POST /tasks` — ajoute une tâche (`{"title": "..."}`)
- `PATCH /tasks/<id>` — modifie une tâche (`{"title": "..."}` et/ou `{"done": true}`)
- `DELETE /tasks/<id>` — supprime une tâche
- `GET /` — page d'accueil HTML : ajouter/cocher/supprimer une tâche depuis le navigateur (utilise `/web/tasks/...` en interne)

Les tâches sont stockées dans une base **MySQL** (persistante entre les redémarrages) quand l'app tourne via Docker. En local sans Docker, en l'absence de la variable `DATABASE_URL`, l'app utilise une base **SQLite en mémoire** — pratique pour développer/tester sans dépendre d'un serveur MySQL, mais tout est perdu à l'arrêt.

## Structure du projet

```
projet-flask/
├── app/
│   ├── app.py               # application Flask (create_app + routes API et web)
│   ├── models.py            # modèle SQLAlchemy Task
│   └── templates/
│       └── index.html       # page d'accueil (liste des tâches)
├── tests/
│   └── test_app.py          # suite de tests pytest
├── wsgi.py                   # point d'entrée pour gunicorn
├── requirements.txt
├── Dockerfile
├── compose.yml                # service api + service db (MySQL)
├── Makefile
├── COMMANDES.md               # détail de chaque commande + résultat attendu
└── README.md
```

## Commandes

Chaque commande existe sous deux formes : le raccourci `make` (pratique en local) et la commande brute équivalente (à utiliser telle quelle dans un pipeline CI, ou si `make` n'est pas disponible). Détail complet et résultat attendu de chacune : voir **[COMMANDES.md](COMMANDES.md)**.

| Action                              | `make`             | Commande brute (CI)                                              |
| ------------------------------------ | ------------------ | ----------------------------------------------------------------- |
| Installer les dépendances            | `make install`      | `pip install -r requirements.txt`                                  |
| Lancer les tests                     | `make test`         | `pytest -v` (ou `pytest --junitxml=report.xml` pour un rapport CI) |
| Lancer le serveur de dev             | `make run`          | `FLASK_APP=wsgi.py flask run --port 5001`                          |
| Construire l'image Docker            | `make docker-build` | `docker compose build`                                             |
| Démarrer les conteneurs (api + db)   | `make up`           | `docker compose up -d --build`                                     |
| Voir les logs                        | `make logs`         | `docker compose logs -f`                                           |
| Arrêter les conteneurs               | `make down`         | `docker compose down`                                              |
| Nettoyer (venv, caches, rapports)    | `make clean`        | `rm -rf .venv .pytest_cache **/__pycache__ report.xml`             |

`make install` et `make run` passent par un environnement virtuel (`.venv/bin/...`) — inutile sur un runner CI, qui installe directement dans son propre environnement isolé, d'où les commandes brutes sans `.venv/bin/`.

### Base de données MySQL (Docker)

Identifiants définis dans `compose.yml` (à usage local/dev uniquement) :

| Variable              | Valeur     |
| --------------------- | ---------- |
| `MYSQL_DATABASE`      | `tasks`    |
| `MYSQL_USER`          | `taskuser` |
| `MYSQL_PASSWORD`      | `taskpass` |
| `MYSQL_ROOT_PASSWORD` | `rootpass` |

Les données sont conservées dans le volume Docker `db-data` : elles survivent à un `docker compose restart` ou `down` (sans `-v`). Pour repartir d'une base vide :

```bash
docker compose down -v
```

## Exemples d'appels API et interface web

Voir [COMMANDES.md](COMMANDES.md) pour la liste complète (GET/POST/PATCH/DELETE + interface web).
