import pandas as pd
import mysql.connector

# Lire le fichier CSV
donnees = pd.read_csv("../data/ventes.csv")

# Afficher les données
print(donnees)

# Afficher les 5 premières lignes
print(donnees.head())

# Afficher le nombre de lignes et de colonnes
print(donnees.shape)

# Afficher les informations sur les colonnes
print(donnees.info())

# Vérifier les valeurs manquantes
print(donnees.isnull().sum())


# Vérifier les doublons
print("Nombre de doublons :")
print(donnees.duplicated().sum())

# Vérifier les types de données
print(donnees.dtypes)

# Convertir la colonne date en format datetime
# Vérifier le nouveau type
donnees['date'] = pd.to_datetime(donnees['date'])
print(donnees.dtypes)

# Calculer le chiffre d'affaires de chaque vente
# Afficher les résultats
donnees['chiffre_affaires'] = donnees['quantite'] * donnees['prix_unitaire']
print(donnees)


# Calculer le chiffre d'affaires total
# Afficher le résultat
ca_total = donnees['chiffre_affaires'].sum()
print("Chiffre d'affaires total :", ca_total, "DH")

# Calculer le chiffre d'affaires par ville
# Afficher les résultats
ca_ville = donnees.groupby('ville')['chiffre_affaires'].sum()
print(ca_ville)


# Calculer la quantité totale vendue par produit
# Afficher les résultats
ventes_produit = donnees.groupby('produit')['quantite'].sum()
print(ventes_produit)


# Trier les produits du plus vendu au moins vendu
# Afficher les résultats
ventes_produit = donnees.groupby('produit')['quantite'].sum()
ventes_triees = ventes_produit.sort_values(ascending=False)
print(ventes_triees)



# Enregistrer les données transformées
donnees.to_csv("../data/ventes_nettoyees.csv", index=False)
print("Les données ont été enregistrées avec succès !")


# Connexion à MySQL
connexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="wordpress_db"
)

# Créer un curseur
curseur = connexion.cursor()

# Requête SQL pour insérer les ventes
requete = """
INSERT INTO ventes
(id_vente, date, produit, categorie, quantite, prix_unitaire, ville)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

# Préparer les données
valeurs = []

for _, ligne in donnees.iterrows():
    valeurs.append((
        int(ligne['id_vente']),
        ligne['date'].date(),
        str(ligne['produit']),
        str(ligne['categorie']),
        int(ligne['quantite']),
        float(ligne['prix_unitaire']),
        str(ligne['ville'])
    ))

# Insérer toutes les ventes
curseur.executemany(requete, valeurs)

# Valider les modifications
connexion.commit()

print(curseur.rowcount, "ventes ajoutées avec succès !")

# Fermer la connexion
curseur.close()
connexion.close()

