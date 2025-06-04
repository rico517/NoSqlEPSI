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
    },
    {
        nom: "Robe d'été Fleurie",
        categorie: "Vêtements",
        prix: 29.99,
        stock: 75,
        disponible: true,
        dateAjout: new Date(),
        attributs: {
            taille: "S",
            couleur: "Jaune",
            genre: "Femme"
        }
    },
    {
        nom: "Jean Slim Noir",
        categorie: "Vêtements",
        prix: 49.90,
        stock: 60,
        disponible: true,
        dateAjout: new Date(),
        attributs: {
            taille: "30",
            couleur: "Noir",
            genre: "Homme"
        }
    },
    {
        nom: "Chaussettes de Sport (lot de 3)",
        categorie: "Vêtements",
        prix: 9.99,
        stock: 120,
        disponible: true,
        dateAjout: new Date(),
        attributs: {
            taille: "39-42",
            couleur: "Blanc",
            genre: "Mixte"
        }
    },
    {
        nom: "Pull en Laine Doux",
        categorie: "Vêtements",
        prix: 39.99,
        stock: 40,
        disponible: true,
        dateAjout: new Date(),
        attributs: {
            taille: "L",
            couleur: "Gris Chiné",
            genre: "Femme"
        }
    },
    {
        nom: "Puzzle 500 pièces Animaux de la Forêt",
        categorie: "Puzzle",
        prix: 12.00,
        stock: 80,
        disponible: true,
        dateAjout: new Date(),
        attributs: {
            nbPieces: 500,
            difficulté: "Moyen",
            format: "Portrait"
        }
    },
    {
        nom: "Puzzle 3D Tour Eiffel",
        categorie: "Puzzle",
        prix: 22.50,
        stock: 30,
        disponible: true,
        dateAjout: new Date(),
        attributs: {
            nbPieces: 216,
            difficulté: "Moyen",
            format: "3D"
        }
    },
    {
        nom: "Puzzle Enfant Dinosaures 100 pièces",
        categorie: "Puzzle",
        prix: 9.95,
        stock: 90,
        disponible: true,
        dateAjout: new Date(),
        attributs: {
            nbPieces: 100,
            difficulté: "Facile",
            format: "Paysage"
        }
    },
    {
        nom: "Souris Gamer Optique",
        categorie: "Informatique",
        prix: 45.00,
        stock: 35,
        disponible: true,
        dateAjout: new Date(),
        attributs: {
            marque: "LogiTech",
            connectivité: "Filaire USB",
            dpi: "12000"
        }
    },
    {
        nom: "Clavier Mécanique RGB",
        categorie: "Informatique",
        prix: 120.00,
        stock: 20,
        disponible: true,
        dateAjout: new Date(),
        attributs: {
            marque: "Corsair",
            connectivité: "USB-C",
            typeSwitch: "Cherry MX Red"
        }
    },
    {
        nom: "Écran PC 27 pouces QHD",
        categorie: "Informatique",
        prix: 299.99,
        stock: 15,
        disponible: true,
        dateAjout: new Date(),
        attributs: {
            marque: "Samsung",
            connectivité: "HDMI, DisplayPort",
            resolution: "2560x1440"
        }
    },
    {
        nom: "SSD Externe 1To Portable",
        categorie: "Informatique",
        prix: 99.00,
        stock: 45,
        disponible: false,
        dateAjout: new Date(),
        attributs: {
            marque: "Crucial",
            connectivité: "USB 3.2",
            capacité: "1To"
        }
    },
    {
        nom: "Le Seigneur des Anneaux - Intégrale",
        categorie: "Livres",
        prix: 35.00,
        stock: 50,
        disponible: true,
        dateAjout: new Date(),
        attributs: {
            auteur: "J.R.R. Tolkien",
            genreLitteraire: "Fantasy",
            nbPages: 1216
        }
    },
    {
        nom: "1984",
        categorie: "Livres",
        prix: 8.90,
        stock: 70,
        disponible: true,
        dateAjout: new Date(),
        attributs: {
            auteur: "George Orwell",
            genreLitteraire: "Dystopie",
            nbPages: 328
        }
    },
    {
        nom: "Poêle Antiadhésive 24cm",
        categorie: "Cuisine",
        prix: 25.99,
        stock: 65,
        disponible: true,
        dateAjout: new Date(),
        attributs: {
            materiau: "Aluminium forgé",
            capacite: "24cm diamètre",
            compatibleInduction: true
        }
    },
    {
        nom: "Set de 5 Couteaux de Cuisine Professionnel",
        categorie: "Cuisine",
        prix: 79.50,
        stock: 25,
        disponible: true,
        dateAjout: new Date(),
        attributs: {
            materiau: "Acier Inoxydable",
            nbPieces: 5,
            typeManche: "Ergonomique"
        }
    }
]);