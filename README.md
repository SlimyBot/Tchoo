# Equipe2a

## TCHOO : Questionnaires en lignes

Tchoo est un site de questionnaires en lignes conçus pour les professeurs et leurs élèves. Créez vos questionaires, projetez-les sur un écran et impliquez vottre classe !

## Auteurs et responsables
Chef de projet : Raphaël Caldwell

Développeurs : Eloi Terrol, Lucas Schiavetti, Mathieu Da Vinha, Mattys Lemoine, Maxance Viola, Santiago Di Fede

Enseignant responsable : Gxxxxxx RXX

## Instructions pour installer et lancer le projet

Afin de lancer notre projet, vous devez avoir Docker ainsi que Docker Compose **v2** installé sur votre machine. La version 24 est recomandée (version api `1.43`), mais cela devrait fonctionner avec des versions plus anciennes, jusqu'à version api `1.12` au minimum.

Ensuite, créez un fichier `.env` dans le repertoire [`backend/`](./backend/) du projet. Vous trouverez un modèle [ici](./backend/README.md).

Finalement, une fois que vous avez cloné le dépôt, exécutez la commande suivante depuis la racine du projet :

```sh
docker compose up -d --build
```

Cela va contruire et lancer l'application sur le port 3000 (par default).

L'application sera accessible à l'adresse suivante : [http://localhost:3000](http://localhost:3000).

La documentation auto-générée suivant le modèle d'OpenAPI est disponible à l'adresse : [http://localhost:3000/api/docs](http://localhost:3000/api/docs).

Pour un déployement en production, il est conseillé de modifier le fichier [docker-compose.yml](./docker-compose.yml) en fonction de vos besoin.

## License

Voir [la license](./LICENCE).
