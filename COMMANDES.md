# Commandes du projet

Liste de toutes les commandes disponibles et de ce qu'elles produisent. Toutes s'exécutent depuis le dossier `projet-flask/`.

## En local (sans Docker)

### `make install`

Crée l'environnement virtuel Python (`.venv/`) et installe Flask, pytest, gunicorn, Flask-SQLAlchemy, PyMySQL, cryptography.

**Résultat** : un dossier `.venv/` créé, aucune sortie particulière à part le log de `pip install`.

### `make test`

Lance la suite de tests avec `pytest -v`.

**Résultat** :
```
tests/test_app.py::test_list_tasks_starts_empty PASSED
tests/test_app.py::test_create_task_returns_it_with_an_id PASSED
...
11 passed in 0.4s
```
Utilise SQLite en mémoire (pas besoin de MySQL qui tourne).

### `make run`

Démarre le serveur de développement Flask sur http://127.0.0.1:5001.

**Résultat** : le terminal reste occupé (`Ctrl+C` pour arrêter), affiche `Running on http://127.0.0.1:5001`. Les données sont en SQLite mémoire : tout est perdu à l'arrêt.

## Avec Docker

### `make up`

Construit l'image et démarre les conteneurs `api` (Flask + gunicorn) et `db` (MySQL 8). L'API attend que MySQL réponde (`healthcheck`) avant de démarrer.

**Résultat** : deux conteneurs `projet-flask-api-1` et `projet-flask-db-1` en cours d'exécution. L'app est accessible sur http://localhost:5001. Les données sont dans le volume Docker `db-data` (persistantes).

### `make logs`

Affiche les logs des deux conteneurs en continu (`docker compose logs -f`).

**Résultat** : flux des logs de `api` (requêtes gunicorn) et `db` (MySQL). `Ctrl+C` pour quitter (ne stoppe pas les conteneurs).

### `make down`

Arrête et supprime les conteneurs `api` et `db` (le réseau aussi).

**Résultat** : conteneurs supprimés, mais le volume `db-data` est conservé — les données MySQL survivent.

### `make docker-build`

Reconstruit l'image `api` sans démarrer de conteneur (`docker compose build`).

**Résultat** : utile après avoir modifié `requirements.txt` ou le code, pour préparer l'image avant un `make up`.

### Réinitialiser complètement la base MySQL

```bash
docker compose down -v
```

**Résultat** : supprime aussi le volume `db-data` — toutes les tâches enregistrées disparaissent. Le prochain `make up` repart d'une base vide.

## Nettoyage

### `make clean`

Supprime `.venv/`, les caches pytest/Python (`.pytest_cache`, `__pycache__`) et `report.xml`.

**Résultat** : dossier du projet remis à l'état "juste après un clone git" (hors Docker).

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

Ouvrir http://localhost:5001/ (ou http://127.0.0.1:5001/ en local) :

- Champ texte + bouton **Ajouter** → crée une tâche (`POST /web/tasks`, formulaire HTML)
- Case ☐ / ☑ à gauche de chaque tâche → bascule fait / à faire (`POST /web/tasks/<id>/toggle`)
- Croix ✕ à droite → supprime la tâche (`POST /web/tasks/<id>/delete`)

Chaque action recharge la page (redirection vers `/`) avec la liste à jour.
