# Requêtes MongoDB utilisées dans l'API FlexiShop

## 1. Récupérer tous les produits avec filtres optionnels

```python
filtre = {}
if categorie:
    filtre["categorie"] = categorie
if disponible is not None:
    filtre["disponible"] = disponible
if prix_min is not None or prix_max is not None:
    filtre["prix"] = {}
    if prix_min is not None:
        filtre["prix"]["$gte"] = prix_min
    if prix_max is not None:
        filtre["prix"]["$lte"] = prix_max

produits = db.produits.find(filtre).skip(skip).limit(limit)
```

---

## 2. Récupérer un produit par son ID

```python
produit = db.produits.find_one({"_id": ObjectId(id)})
```

---

## 3. Ajouter un nouveau produit

```python
result = db.produits.insert_one(produit_dict)
```

---

## 4. Mettre à jour un produit

```python
result = db.produits.update_one(
    {"_id": ObjectId(id)},
    {"$set": update_data}
)
```

---

## 5. Supprimer un produit

```python
result = db.produits.delete_one({"_id": ObjectId(id)})
```

---

## 6. Valeur totale du stock par catégorie (Aggregation Pipeline)

```python
pipeline = [
    { "$match": { "disponible": True } },
    { "$project": { "categorie": 1, "valeurStock": { "$multiply": ["$prix", "$stock"] } } },
    { "$group": { "_id": "$categorie", "valeurTotale": { "$sum": "$valeurStock" } } },
    { "$sort": { "valeurTotale": -1 } }
]
result = db.produits.aggregate(pipeline)
```

---

## 7. Top 3 des catégories les plus chères (prix moyen)

```python
pipeline = [
    { "$group": { "_id": "$categorie", "prixMoyen": { "$avg": "$prix" }, "nbProduits": { "$sum": 1 } } },
    { "$sort": { "prixMoyen": -1 } },
    { "$limit": 3 }
]
result = db.produits.aggregate(pipeline)
```

---

## 8. Répartition des produits selon leur disponibilité

```python
pipeline = [
    { "$group": { "_id": "$disponible", "count": { "$sum": 1 }, "categories": { "$addToSet": "$categorie" } } }
]
result = db.produits.aggregate(pipeline)
```

---

## 9. Compter le nombre total de produits

```python
total_produits = db.produits.count_documents({})
```