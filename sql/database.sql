CREATE DATABASE IF NOT EXISTS wordpress_db;

USE wordpress_db;

CREATE TABLE IF NOT EXISTS ventes (
    id_vente INT PRIMARY KEY,
    date DATE,
    produit VARCHAR(100),
    categorie VARCHAR(100),
    quantite INT,
    prix_unitaire DECIMAL(10,2),
    ville VARCHAR(100)
);
