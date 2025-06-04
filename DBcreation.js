// Creation de la base de données "flexishopDB" et de la collection "produits"

// Creation de la base de données "flexishopDB"
use flexishopDB;

// Creation de la collection "produits" en inserant des produits d'exemple
db.produits.insertMany([
    {
        nom: "T-shirt Cool",
        categorie: "Vêtements",
        prix: 19.99,
        stock: 100,
        disponible: true,
        dateAjout: new Date(),
        attributs: {
            taille: "M",
            couleur: "Bleu",
            genre: "Homme"
        }
    },
    {
        nom: "Puzzle 1000 pièces",
        categorie: "Puzzle",
        prix: 15.50,
        stock: 50,
        disponible: true,
        dateAjout: new Date(),
        attributs: {
            nbPieces: 1000,
            difficulté: "Difficile",
            format: "Paysage"
        }
    },
    {
        nom: "Casque sans fil",
        categorie: "Informatique",
        prix: 89.99,
        stock: 25,
        disponible: true,
        dateAjout: new Date(),
        attributs: {
            marque: "TechSound",
            connectivité: "Bluetooth",
            autonomie: "20h"
        }
    }
]);