# Rapport NoSQL EPSI

## Choix de modélisation

- Utilisation de MongoDB avec une base `flexishopDB` et une collection unique `produits`.
- Chaque produit possède des champs communs (`nom`, `categorie`, `prix`, `stock`, `disponible`, `dateAjout`) et un champ `attributs` (objet/dictionnaire) pour stocker les propriétés spécifiques à chaque catégorie.
- Ce schéma flexible permet d'ajouter facilement de nouveaux types de produits avec des attributs différents sans modifier la structure globale.

## Difficultés rencontrées

- Pas de difficultés particulières rencontrées sur la réalisation de ce TP, tout s'est globalement bien déroulé

## Logique des requêtes

- Récupération des produits avec filtres optionnels (catégorie, disponibilité, fourchette de prix).
- Ajout, modification (y compris fusion des attributs) et suppression de produits via des routes REST.
- Statistiques avancées via des agrégations MongoDB :
  - Valeur totale du stock par catégorie (`/stats/valeur-stock`).
  - Top 3 des catégories avec le prix moyen le plus élevé (`/stats/top-categories`).
  - Répartition des produits selon leur disponibilité (`/stats/repartition-disponibilite`).