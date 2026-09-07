# Commandes du projet

Liste de toutes les commandes disponibles et de ce qu'elles produisent. Toutes s'exécutent depuis le dossier `projet-flask/`.

Chaque commande est donnée sous deux formes :
- le raccourci **`make`**, pratique en local (utilise l'environnement virtuel `.venv/`) ;
- la **commande brute équivalente**, à coller telle quelle dans un pipeline CI (`.github/workflows/ci.yml`) ou si `make` n'est pas installé — un runner CI installe directement dans son propre environnement isolé, donc pas besoin de `.venv/bin/...`.

## En local (sans Docker)

### `make install`

```bash
make install
```
Crée l'environnement virtuel Python (`.venv/`) et installe Flask, pytest, gunicorn, Flask-SQLAlchemy, PyMySQL, cryptography, **ruff** et **mypy** (via `requirements-dev.txt`, qui inclut `requirements.txt`).

**Résultat** : un dossier `.venv/` créé, aucune sortie particulière à part le log de `pip install`.

**Commande brute (CI)** :
```bash
pip install -r requirements-dev.txt
```
En CI, si le job ne fait que lancer les tests (pas de lint), `pip install -r requirements.txt` suffit — `requirements-dev.txt` n'est utile que pour `ruff`/`mypy`.

### `make test`

```bash
make test
```
Lance la suite de tests avec `pytest -v`.

**Résultat** :
```
tests/test_app.py::test_list_tasks_starts_empty PASSED
tests/test_app.py::test_create_task_returns_it_with_an_id PASSED
...
11 passed in 0.4s
```
Utilise SQLite en mémoire (pas besoin de MySQL qui tourne).

**Commande brute (CI)** :
```bash
pytest -v
```
Pour générer un rapport exploitable par `actions/upload-artifact` en CI (format JUnit) :
```bash
pytest --junitxml=report.xml
```

### `make lint`

```bash
make lint
```
Analyse le code avec **Ruff** (style, imports non triés, syntaxe obsolète — config dans `pyproject.toml`).

**Résultat** :
```
All checks passed!
```
Si des problèmes sont trouvés, Ruff les liste avec le fichier/la ligne concernés (code de sortie non nul).

**Commande brute (CI)** :
```bash
ruff check .
```

### `make typecheck`

```bash
make typecheck
```
Vérifie les types avec **mypy** sur `app/` et `wsgi.py` (config dans `pyproject.toml`).

**Résultat** :
```
Success: no issues found in 4 source files
```

**Commande brute (CI)** :
```bash
mypy app wsgi.py
```

### `make quality`

```bash
make quality
```
Enchaîne `make lint` puis `make typecheck` — pratique pour tout vérifier d'un coup avant de pousser.

**Commande brute (CI)** :
```bash
ruff check . && mypy app wsgi.py
```

### `make run`

```bash
make run
```
Démarre le serveur de développement Flask sur http://127.0.0.1:5001.

**Résultat** : le terminal reste occupé (`Ctrl+C` pour arrêter), affiche `Running on http://127.0.0.1:5001`. Les données sont en SQLite mémoire : tout est perdu à l'arrêt.

**Commande brute** :
```bash
FLASK_APP=wsgi.py flask run --port 5001
```

## Avec Docker

### `make up`

```bash
make up
```
Construit l'image et démarre les conteneurs `api` (Flask + gunicorn) et `db` (MySQL 8). L'API attend que MySQL réponde (`healthcheck`) avant de démarrer.

**Résultat** : deux conteneurs `projet-flask-api-1` et `projet-flask-db-1` en cours d'exécution. L'app est accessible sur http://localhost:5001. Les données sont dans le volume Docker `db-data` (persistantes).

**Commande brute (CI)** :
```bash
docker compose up -d --build
```

### `make logs`

```bash
make logs
```
Affiche les logs des deux conteneurs en continu.

**Résultat** : flux des logs de `api` (requêtes gunicorn) et `db` (MySQL). `Ctrl+C` pour quitter (ne stoppe pas les conteneurs).

**Commande brute** :
```bash
docker compose logs -f
```

### `make down`

```bash
make down
```
Arrête et supprime les conteneurs `api` et `db` (le réseau aussi).

**Résultat** : conteneurs supprimés, mais le volume `db-data` est conservé — les données MySQL survivent.

**Commande brute (CI)** :
```bash
docker compose down
```

### `make docker-build`

```bash
make docker-build
```
Reconstruit l'image `api` sans démarrer de conteneur.

**Résultat** : utile après avoir modifié `requirements.txt` ou le code, pour préparer l'image avant un `make up`.

**Commande brute (CI)** :
```bash
docker compose build
```

### Réinitialiser complètement la base MySQL

```bash
docker compose down -v
```

**Résultat** : supprime aussi le volume `db-data` — toutes les tâches enregistrées disparaissent. Le prochain `make up` (ou `docker compose up -d --build`) repart d'une base vide.

## Nettoyage

### `make clean`

```bash
make clean
```
Supprime `.venv/`, les caches pytest/Python/Ruff/mypy (`.pytest_cache`, `.ruff_cache`, `.mypy_cache`, `__pycache__`) et `report.xml`.

**Résultat** : dossier du projet remis à l'état "juste après un clone git" (hors Docker).

**Commande brute** :
```bash
rm -rf .venv .pytest_cache .ruff_cache .mypy_cache **/__pycache__ report.xml
```

## Utiliser l'API en ligne de commande (`curl`)

Le port dépend de comment l'app tourne : **5001** que ce soit via `make run` ou `make up`.

### Lister les tâches

```bash
curl http://localhost:5001/tasks
```
**Résultat** :
```json
[{"id": 1, "title": "Acheter du pain", "done": false}]
```

### Ajouter une tâche

```bash
curl -X POST http://localhost:5001/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Acheter du pain"}'
```
**Résultat** (code 201) :
```json
{"id": 1, "title": "Acheter du pain", "done": false}
```

### Marquer une tâche comme faite (ou la renommer)

```bash
curl -X PATCH http://localhost:5001/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"done": true}'
```
**Résultat** (code 200) :
```json
{"id": 1, "title": "Acheter du pain", "done": true}
```
Renvoie 404 si l'id n'existe pas.

### Supprimer une tâche

```bash
curl -X DELETE http://localhost:5001/tasks/1
```
**Résultat** : code 204, pas de contenu. Renvoie 404 si l'id n'existe pas.

## Utiliser l'interface web (navigateur)

L'application n'est pas qu'une API : la page d'accueil est un vrai template HTML (`app/templates/index.html`) qui appelle les mêmes routes en interne via des formulaires.

Ouvrir http://localhost:5001/ (ou http://127.0.0.1:5001/ en local) :

- Champ texte + bouton **Ajouter** → crée une tâche (`POST /web/tasks`, formulaire HTML)
- Case ☐ / ☑ à gauche de chaque tâche → bascule fait / à faire (`POST /web/tasks/<id>/toggle`)
- Croix ✕ à droite → supprime la tâche (`POST /web/tasks/<id>/delete`)

Chaque action recharge la page (redirection vers `/`) avec la liste à jour.
