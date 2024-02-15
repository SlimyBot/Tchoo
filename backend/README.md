# Backend du projet

## Configuration du fichier .env

Pour pouvoir lancer le backend de notre application, créer un fichier `.env` dans ce repertoire selon le modèle suivant :

```bash
SECRET_KEY=f8e0e677c61e84545f094f501f309192f9297a1b50ca3e37a05883f7358774df

POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres
POSTGRES_SERVER=localhost

REDIS_URL=redis://localhost:6379

DEPLOY_MODE=dev # remplacer par "prod" lors de la mise en production
```

Changez ces variable lors d'un deployement en production.

Vous pouvez générer une clé secrete avec [OpenSSL](https://www.openssl.org/) :

```sh
$ openssl rand -hex 32

c0d7b4fed229a25851b3cc268ff0c90...
```
