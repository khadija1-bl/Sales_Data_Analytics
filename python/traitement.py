import pandas as pd
import mysql.connector

donnees = pd.read_csv("../data/ventes.csv")

print(donnees)

print(donnees.head())

print(donnees.shape)

print(donnees.info())

print(donnees.isnull().sum())

print("Nombre de doublons :")
print(donnees.duplicated().sum())

print(donnees.dtypes)

donnees['date'] = pd.to_datetime(donnees['date'])
print(donnees.dtypes)

donnees['chiffre_affaires'] = donnees['quantite'] * donnees['prix_unitaire']
print(donnees)

ca_total = donnees['chiffre_affaires'].sum()
print("Chiffre d'affaires total :", ca_total, "DH")

ca_ville = donnees.groupby('ville')['chiffre_affaires'].sum()
print(ca_ville)

ventes_produit = donnees.groupby('produit')['quantite'].sum()
print(ventes_produit)

ventes_produit = donnees.groupby('produit')['quantite'].sum()
ventes_triees = ventes_produit.sort_values(ascending=False)
print(ventes_triees)

donnees.to_csv("../data/ventes_nettoyees.csv", index=False)
print("Les données ont été enregistrées avec succès !")

connexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="wordpress_db"
)

curseur = connexion.cursor()

requete = """
INSERT INTO ventes
(id_vente, date, produit, categorie, quantite, prix_unitaire, ville)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

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

curseur.executemany(requete, valeurs)

connexion.commit()

print(curseur.rowcount, "ventes ajoutées avec succès !")

curseur.close()
connexion.close()

