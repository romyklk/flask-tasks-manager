# Gestionnaire de tâches — API Flask

Petite API REST développée avec **Flask**, pour le TP7 (Capstone Sujet 1). Elle expose deux routes :

- `GET /tasks` — liste toutes les tâches
- `POST /tasks` — ajoute une tâche (`{"title": "..."}`)

Les tâches sont stockées en mémoire (pas de base de données) : elles sont perdues à chaque redémarrage du serveur.

## Structure du projet

```
projet-flask/
├── app/
│   └── app.py          # application Flask (create_app + routes)
├── tests/
│   └── test_app.py     # suite de tests pytest
├── wsgi.py              # point d'entrée pour gunicorn
├── requirements.txt
├── Dockerfile
├── compose.yml
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

Construire l'image et démarrer le conteneur (http://localhost:5001) :

```bash
make up
```

Voir les logs du conteneur :

```bash
make logs
```

Arrêter et supprimer le conteneur :

```bash
make down
```

Reconstruire l'image seule (sans démarrer) :

```bash
make docker-build
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
