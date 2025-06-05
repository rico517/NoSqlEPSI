# Structure du modèle de données - FlexiShop

## Collection : `produits`

Chaque document de la collection `produits` possède la structure suivante :

- **_id** : ObjectId (identifiant unique MongoDB)
- **nom** : string (nom du produit)
- **categorie** : string (catégorie du produit, ex : "Vêtements", "Puzzle", "Informatique")
- **prix** : number (prix du produit)
- **stock** : integer (quantité en stock, >= 0)
- **disponible** : boolean (disponibilité à la vente)
- **dateAjout** : date (date d'ajout du produit)
- **attributs** : objet/dictionnaire (propriétés spécifiques à la catégorie du produit, structure flexible)

### Exemple de document

```json
{
  "_id": "60d21b4667d0d8992e610c85",
  "nom": "T-shirt col rond",
  "categorie": "Vêtements",
  "prix": 19.99,
  "stock": 30,
  "disponible": true,
  "dateAjout": "2025-06-01T00:00:00",
  "attributs": {
    "taille": "M",
    "couleur": "Bleu",
    "genre": "Homme"
  }
}
```

### Remarques

- Le champ `attributs` permet d'ajouter dynamiquement des propriétés selon la catégorie (ex : `taille`, `couleur` pour les vêtements, `marque`, `connectivité` pour l'informatique, etc.).
- Ce modèle est volontairement flexible pour s'adapter à l'évolution des besoins métiers sans migration de schéma.
