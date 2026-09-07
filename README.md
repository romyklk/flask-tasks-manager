# Gestionnaire de tâches — API Flask

Petite API REST développée avec **Flask**, pour le TP7 (Capstone Sujet 1). Elle expose :

- `GET /tasks` — liste toutes les tâches (JSON)
- `POST /tasks` — ajoute une tâche (`{"title": "..."}`)
- `GET /` — page d'accueil HTML qui affiche la liste des tâches

Les tâches sont stockées dans une base **MySQL** (persistante entre les redémarrages) quand l'app tourne via Docker. En local sans Docker (`make run` / `make test`), en l'absence de la variable `DATABASE_URL`, l'app utilise une base **SQLite en mémoire** — pratique pour développer/tester sans dépendre d'un serveur MySQL, mais tout est perdu à l'arrêt.

## Structure du projet

```
projet-flask/
├── app/
│   ├── app.py               # application Flask (create_app + routes)
│   ├── models.py            # modèle SQLAlchemy Task
│   └── templates/
│       └── index.html       # page d'accueil (liste des tâches)
├── tests/
│   └── test_app.py          # suite de tests pytest
├── wsgi.py                   # point d'entrée pour gunicorn
├── requirements.txt
├── Dockerfile
├── compose.yml                # service api + service db (MySQL)
└── Makefile
```

## Commandes — en local (sans Docker)

Installer l'environnement virtuel et les dépendances :

```bash
make install
```

Lancer les tests :

```bash
make test
```

Lancer le serveur de développement Flask (http://127.0.0.1:5001) :

```bash
make run
```

## Commandes — avec Docker

Construire les images et démarrer les conteneurs `api` + `db` (http://localhost:5001) :

```bash
make up
```

L'API attend que MySQL soit prêt (`healthcheck` dans `compose.yml`) avant de démarrer.

Voir les logs des conteneurs :

```bash
make logs
```

Arrêter et supprimer les conteneurs :

```bash
make down
```

Reconstruire l'image seule (sans démarrer) :

```bash
make docker-build
```

### Base de données MySQL

Identifiants définis dans `compose.yml` (à usage local/dev uniquement) :

| Variable            | Valeur     |
| ------------------- | ---------- |
| `MYSQL_DATABASE`    | `tasks`    |
| `MYSQL_USER`        | `taskuser` |
| `MYSQL_PASSWORD`    | `taskpass` |
| `MYSQL_ROOT_PASSWORD` | `rootpass` |

Les données sont conservées dans le volume Docker `db-data` : elles survivent à un `docker compose restart` ou `down` (sans `-v`). Pour repartir d'une base vide :

```bash
docker compose down -v
```

## Nettoyage

Supprime l'environnement virtuel, les caches Python et les rapports de tests générés :

```bash
make clean
```

## Exemples d'appels

```bash
# Lister les tâches
curl http://localhost:5001/tasks

# Ajouter une tâche
curl -X POST http://localhost:5001/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Acheter du pain"}'
```
