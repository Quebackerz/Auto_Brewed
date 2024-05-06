#Coded in python 3.10.12
"""
Pour que le script fonctionne bien :
1- Changer le nom du fichier de SPS pour : input.csv.
    1.1- Le nom du fichier doit etre en minuscule toujours.
2- La bonne version de python doit etre installe et les modules requis aussi.
3- La personne qui roule le script doit aimer le cafe et l'HOMME CAFE 
"""

import csv
import time
from datetime import datetime 
from datetime import timedelta 
#import datetime

print("""\

        /~~~~~~~~/|
       / /######/ / |
      / /______/ /  |
     ============ /||
     |__________|/ ||
      |\__,,__/    ||
      | __,,__     ||
      |_\====/%____||    Auto_Brewed, pour l'HOMME CAFE
      | /~~~~\ %  / |
     _|/      \%_/  |
    | |        | | /
    |__\______/__|/
    ~~~~~~~~~~~~~~
    
"Coffee is a language in itself." - Jackie Chan
                    """)

#Demander le bon numero de facture a entrer et la date de facturation
Num_Facture = int(input("Entrer le prochain numero de facture :"))-1# Au debut je dois faire -1 parce qu'au premier tour il ajoute 1.
Maison_Mere = input("(1) Loblaws Inc.: \n (2) Sobeys Québec Inc.: \n (3) Metro Richelieu INC.: \n Entrer la maison mere : ")
Date_Facturation_Statique = input("Entre la date de facturation (YYYY-MM-DD) :")
Date_Facturation_Statique = datetime.strptime(Date_Facturation_Statique, '%Y-%m-%d')

if Maison_Mere == "1": Maison_Mere = "Loblaws Inc.:"
if Maison_Mere == "2": Maison_Mere = "Sobeys Québec Inc.:"
if Maison_Mere == "3": Maison_Mere = "Metro Richelieu INC.:"

Message = "Dépots directs:\n Caisse Desjardins \n 30500-815-095-372-9 \n Veuillez envoyer la confirmation du dépôt. \n\n For direct deposits: \n Caisse Desjardins \n 30500-815-095-372-9 \n 30500-815-095-372-9 \n Please send payment confirmation. \n Veuillez noter que les crédits expirent après 12 mois. \n Please note credit memos expire 12 months."

# Calcul de 30 jours pour la date d'Echeance 
#Date_Echeance_Statique = input("Entre la date d'echeance (YYYY-MM-DD) :")
Date_Echeance_Statique = Date_Facturation_Statique + timedelta(days=30) 

print
#Declaration des variables statiques
timestr = time.strftime("%Y_%m_%d-%H_%M")
Fichier_Output_csv  = "output_" + timestr + ".csv"
Taxes = "Exempt"
Current_PO = ""
Current_PO_row = "" 
#Ouvrir le fichier de Source a traiter
with open('input.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    
    for row in csv_reader:
        # Si c'est la premiere ligne, entrer le titre des colonnes
        if line_count == 0:
            # Ecrire la premiere ligne dans le fichier
            with open(Fichier_Output_csv, 'a') as output_file:
                Line_Output = 'No de facture,Client,Date de facturation,Échéance,Modalités,Lieu,Message Affiché sur la facture,Article (produit/service),Description de l’article,Quantité de l’article,Taux de l’article,Montant de l’article,Code de taxe de l’article,Montant de la taxe de l’article\n'
                output_file.write(Line_Output)
            line_count += 1
        # Si ce n'est pas la premiere ligne, prendre les valeurs des champs et ecrire dans le bon format pour le output.    
        else:
            with open(Fichier_Output_csv, 'a') as output_file:
                Montant_Article = ""
                Current_PO_row = row[0]
                # Increment pour le numero de facture, par contre il ne doit changer que quand le PO change
                if Current_PO != Current_PO_row: Num_Facture += 1; Current_PO = Current_PO_row
                # Si la quantitee de l'article n'est pas vide, faire le calcul du montant 
                if row[13] != "": Montant_Article = float(row[13]) * float(row[15])
                # Si la ligne "Unit of mesure" est egal a "case" Ajouter "CAISSE DE" devant la description du produit.
                Description_Produit = row[20]
                if row[14] == 'Case': Description_Produit = "CAISSE DE " + str(row[20])
                #Changer la description de l'article pour le UPC et GTIN, si la ligne n'est pas vide
                Article_Description=""
                if row[16] != "":Article_Description = 'UPC: ' + row[16] + " GTIN: " + row[95] 
                # Quickbook magic pour ecrire la premiere commande sur la meme ligne.
                Hold = "True" # Tant que cette variable est vrai, ne pas ecrire les variables sur la ligne, mais les garder en memoire dans une variable.
                if row[62] != "": 
                    Client = row[62]
                    Date_Facturation = Date_Facturation_Statique.strftime('%Y-%m-%d')
                    Date_Echeance = Date_Echeance_Statique.strftime('%Y-%m-%d')
                    Modalites = "Net 30"
                    Memo = "PO:" + row[0] + Message
                    Hold="True"
                  
                # Ecrire la ligne dans le fichier output
                if row[20] !="" :
                        Line_Output = str(Num_Facture) + ","+ Maison_Mere + Client + "," + str(Date_Facturation) + "," + str(Date_Echeance) +  ","+ Modalites + "," + "," + Memo + "," + Description_Produit + "," + Article_Description + "," + row[13] + "," + row[15] + "," + str(Montant_Article) + "," + Taxes + "," + "\n"
                        output_file.write(Line_Output)
                        Client = ""
                        Date_Facturation = ""
                        Date_Echeance = ""
                        Modalites = ""
                        Memo = ""
                        Hold="False"
            line_count += 1 
    print(f' {line_count} lignes transformees. Voir le fichier Output.csv pour importer dans Quickbooks !')
    
   
  
"""
00- Input:row / Output:Colonne
-------------------------------------------------------
01- Not_Available:Manual / No de facture*
02- Ship to Name:62 / Client*
03- Not_Available:Manual / Date de facturation*
04- Not_Available:Manual / Échéance
05- Not_Available:Manual / Modalités
06- Vide ? / Lieu
07- PO Number:0 / Mémo
08- Product/Item Description:20 / Article (produit/service)	
09- (UPC:16 + GTIN:95) / Description de l’article	
10- Qty Ordered:13/ Quantité de l’article	
11- Unit Price:15 / Taux de l’article* 
12- (Qty Ordered * Unit Price):calculated / Montant de l’article* 
13- Not_Available:Static/ Code de taxe de l’article	
14- Vide?/ Montant de la taxe de l’article
"""
