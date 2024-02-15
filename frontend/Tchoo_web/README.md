# Tchoo_web

This template should help get you started developing with Vue 3 in Vite.

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur) + [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=Vue.vscode-typescript-vue-plugin).

## Customize configuration

See [Vite Configuration Reference](https://vitejs.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Compile and Minify for Production

```sh
npm run build
```

### Personalisation du projet

Les couleurs du projet sont définies dans le fichier [`src/assets/main.css`](src/assets/main.css). 
Pour les modifier, il suffit de changer les valeurs des variables CSS.

Les fond d'écran sont définis présents dans le dossier [`src/components/icons`](src/components/icons).
Pour que les changer, il suffit de remplacer les images présentes dans ce dossier.
Attention, les images doivent être au format `.png`. Et avoir le même nom que les images présentes dans le dossier. (Sensible à la casse)
5760x4096 est la taille recommandée pour les images.

Il est possible d'empecher les usagers de l'application à pouvoir changer le thème. Pour cela, il suffit de
mettre la variable `VITE_ALLOW_CHANGE_THEME` à `0` dans le fichier [.env](.env) avant de compiler le projet.
