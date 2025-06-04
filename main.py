import os
from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId
import json

# Configuration de la connexion MongoDB
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "flexishopDB"

# Initialisation de l'application FastAPI
app = FastAPI(
    title="FlexiShop API",
    description="API pour la gestion d'une plateforme e-commerce avec des produits aux structures hétérogènes",
    version="1.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Classe pour gérer les ObjectId de MongoDB
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

# Modèles Pydantic
class AttributsModel(BaseModel):
    class Config:
        extra = "allow"  # Permet des champs supplémentaires dynamiques

class ProduitBase(BaseModel):
    nom: str
    categorie: str
    prix: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    disponible: bool
    attributs: Dict[str, Any]

class ProduitCreate(ProduitBase):
    dateAjout: Optional[datetime] = None

    class Config:
        schema_extra = {
            "example": {
                "nom": "T-shirt col rond",
                "categorie": "Vêtements",
                "prix": 19.99,
                "stock": 30,
                "disponible": True,
                "attributs": {
                    "taille": "M",
                    "couleur": "Bleu",
                    "genre": "Homme"
                }
            }
        }

class ProduitUpdate(BaseModel):
    nom: Optional[str] = None
    categorie: Optional[str] = None
    prix: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    disponible: Optional[bool] = None
    attributs: Optional[Dict[str, Any]] = None

    class Config:
        schema_extra = {
            "example": {
                "prix": 24.99,
                "stock": 15,
                "attributs": {
                    "couleur": "Rouge"
                }
            }
        }

class ProduitDB(ProduitBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    dateAjout: datetime

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: lambda dt: dt.isoformat()}
        schema_extra = {
            "example": {
                "_id": "60d21b4667d0d8992e610c85",
                "nom": "T-shirt col rond",
                "categorie": "Vêtements",
                "prix": 19.99,
                "stock": 30,
                "disponible": True,
                "dateAjout": "2025-06-01T00:00:00",
                "attributs": {
                    "taille": "M",
                    "couleur": "Bleu",
                    "genre": "Homme"
                }
            }
        }

# Classe pour les réponses de statistiques
class StatResponse(BaseModel):
    data: Any

# Fonction pour se connecter à MongoDB
def get_db():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    return db

# Initialisation de la base de données avec les données de test
@app.on_event("startup")
async def startup_db_client():
    try:
        db = get_db()
        # Vérifier si la collection existe et contient des données
        if "produits" not in db.list_collection_names() or db.produits.count_documents({}) == 0:
            # Charger les données initiales depuis le fichier JSON
            with open("init_data.json", "r") as file:
                produits = json.load(file)
                
            # Convertir les dates de chaîne en objets datetime
            for produit in produits:
                if "dateAjout" in produit:
                    produit["dateAjout"] = datetime.fromisoformat(produit["dateAjout"])
            
            # Insérer les données
            if produits:
                db.produits.insert_many(produits)
                print(f"Base de données initialisée avec {len(produits)} produits")
    except Exception as e:
        print(f"Erreur lors de l'initialisation de la base de données: {e}")

# Routes API

# Route pour récupérer tous les produits (avec filtres optionnels)
@app.get("/produits", response_model=List[ProduitDB], tags=["Produits"])
async def get_produits(
    categorie: Optional[str] = None,
    disponible: Optional[bool] = None,
    prix_min: Optional[float] = None,
    prix_max: Optional[float] = None,
    skip: int = 0,
    limit: int = 100
):
    db = get_db()
    
    # Construction du filtre
    filtre = {}
    if categorie:
        filtre["categorie"] = categorie
    if disponible is not None:
        filtre["disponible"] = disponible
    
    # Filtre de prix
    if prix_min is not None or prix_max is not None:
        filtre["prix"] = {}
        if prix_min is not None:
            filtre["prix"]["$gte"] = prix_min
        if prix_max is not None:
            filtre["prix"]["$lte"] = prix_max
    
    # Exécution de la requête
    produits = list(db.produits.find(filtre).skip(skip).limit(limit))
    return produits

# Route pour récupérer un produit par son ID
@app.get("/produits/{id}", response_model=ProduitDB, tags=["Produits"])
async def get_produit(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID de produit invalide")
    
    db = get_db()
    produit = db.produits.find_one({"_id": ObjectId(id)})
    
    if produit is None:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    
    return produit

# Route pour ajouter un nouveau produit
@app.post("/produits", response_model=ProduitDB, status_code=status.HTTP_201_CREATED, tags=["Produits"])
async def create_produit(produit: ProduitCreate):
    db = get_db()
    
    # Définir la date d'ajout si non fournie
    if not produit.dateAjout:
        produit.dateAjout = datetime.now()
    
    # Conversion en dictionnaire et insertion
    produit_dict = produit.dict()
    result = db.produits.insert_one(produit_dict)
    
    # Récupérer le produit créé
    created_produit = db.produits.find_one({"_id": result.inserted_id})
    return created_produit

# Route pour mettre à jour un produit
@app.put("/produits/{id}", response_model=ProduitDB, tags=["Produits"])
async def update_produit(id: str, produit: ProduitUpdate):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID de produit invalide")
    
    db = get_db()
    
    # Filtrer les champs non None
    update_data = {k: v for k, v in produit.dict().items() if v is not None}
    
    # Gestion spéciale pour les attributs (mise à jour partielle)
    if "attributs" in update_data and update_data["attributs"]:
        # Récupérer les attributs existants
        existing_produit = db.produits.find_one({"_id": ObjectId(id)})
        if not existing_produit:
            raise HTTPException(status_code=404, detail="Produit non trouvé")
        
        # Fusionner les attributs existants avec les nouveaux
        existing_attrs = existing_produit.get("attributs", {})
        for key, value in update_data["attributs"].items():
            existing_attrs[key] = value
        
        # Remplacer par les attributs fusionnés
        update_data["attributs"] = existing_attrs
    
    # Exécuter la mise à jour si des données sont présentes
    if update_data:
        result = db.produits.update_one(
            {"_id": ObjectId(id)},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Produit non trouvé")
    
    # Récupérer le produit mis à jour
    updated_produit = db.produits.find_one({"_id": ObjectId(id)})
    return updated_produit

# Route pour supprimer un produit
@app.delete("/produits/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Produits"])
async def delete_produit(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID de produit invalide")
    
    db = get_db()
    result = db.produits.delete_one({"_id": ObjectId(id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    
    return None

# Routes pour les statistiques

# Valeur totale du stock par catégorie
@app.get("/stats/valeur-stock", response_model=StatResponse, tags=["Statistiques"])
async def get_valeur_stock():
    db = get_db()
    
    pipeline = [
        { 
            "$match": { "disponible": True }
        },
        {
            "$project": {
                "categorie": 1,
                "valeurStock": { "$multiply": ["$prix", "$stock"] }
            }
        },
        {
            "$group": {
                "_id": "$categorie",
                "valeurTotale": { "$sum": "$valeurStock" }
            }
        },
        {
            "$sort": { "valeurTotale": -1 }
        }
    ]
    
    result = list(db.produits.aggregate(pipeline))
    
    # Formater les résultats
    formatted_result = [
        {"categorie": item["_id"], "valeurTotale": round(item["valeurTotale"], 2)}
        for item in result
    ]
    
    return {"data": formatted_result}

# Top 3 des catégories les plus chères (prix moyen)
@app.get("/stats/top-categories", response_model=StatResponse, tags=["Statistiques"])
async def get_top_categories():
    db = get_db()
    
    pipeline = [
        {
            "$group": {
                "_id": "$categorie",
                "prixMoyen": { "$avg": "$prix" },
                "nbProduits": { "$sum": 1 }
            }
        },
        {
            "$sort": { "prixMoyen": -1 }
        },
        {
            "$limit": 3
        }
    ]
    
    result = list(db.produits.aggregate(pipeline))
    
    # Formater les résultats
    formatted_result = [
        {
            "categorie": item["_id"], 
            "prixMoyen": round(item["prixMoyen"], 2),
            "nbProduits": item["nbProduits"]
        }
        for item in result
    ]
    
    return {"data": formatted_result}

# Répartition des produits selon leur disponibilité
@app.get("/stats/repartition-disponibilite", response_model=StatResponse, tags=["Statistiques"])
async def get_repartition_disponibilite():
    db = get_db()
    
    # Compter le nombre total de produits
    total_produits = db.produits.count_documents({})
    
    pipeline = [
        {
            "$group": {
                "_id": "$disponible",
                "count": { "$sum": 1 },
                "categories": { "$addToSet": "$categorie" }
            }
        }
    ]
    
    result = list(db.produits.aggregate(pipeline))
    
    # Formater les résultats
    formatted_result = [
        {
            "disponible": "Disponible" if item["_id"] else "Non disponible",
            "count": item["count"],
            "pourcentage": round((item["count"] / total_produits) * 100, 2),
            "categories": item["categories"]
        }
        for item in result
    ]
    
    return {"data": formatted_result}

# Point d'entrée principal
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
