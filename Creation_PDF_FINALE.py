# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 09:20:49 2024

@author: Silver
"""
#Partie Structure
from fpdf import FPDF
import os
import numpy as np
from PIL import Image
import json

###____________________________________________________________________Classe pour la séléction des ETP____________________________________________________________________###  
class PG:
    #Classe PG qui prend en entrée la liste classée des secteurs préféré (en numéro)
    def __init__(self,pref):
        self.pref = pref
        
    
    #Programme qui permet la séléction aléatoire et le shuffle des etp recommandées
    def affectation(self,Id):
        self.tab = []
        places = [4,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
        for i in range(len(self.pref)):
            espace = 7
            secteur = Secteurs[self.pref[i]-1]
            n = len(secteur)
            if(n < places[i]):
                places[i+1] += places[i]-n
                places[i] = n
            #indice -1 car on rajoute la proba après le reste
            poids = [float(subtable[-1]) for subtable in secteur]
            poids = [x/sum(poids) for x in poids]
            for k in range(len(poids)):
                if poids[k] == 0 and (len(self.tab)<espace): 
                    places[i] -= 1
                    espace-=1
                    self.tab.append(secteur[k])
            index = []
            for k in range(n): index.append(k)
            rand = np.random.choice(index, places[i], replace=False, p=poids)
            for j in range(places[i]):
                if(len(self.tab)<espace):
                    self.tab.append(secteur[rand[j]])
        
        np.random.shuffle(self.tab)
        for i,test in enumerate(self.tab):
            for j,test_2 in enumerate(self.tab):
                if j != i and test == test_2:
                    print("ERREUR")
                    print(Id)
                    

###____________________________________________________________________Classe pour la création du PDF____________________________________________________________________###  
class PDF(FPDF):
    #Création de l'entête du PDF
    def header(self):
        largeur = 210
        longueur_rectangle_entete = 32.3
        pages_avant = 13
        
        self.set_margins(0,0,0)
    
        #Définition de la couleur pour les remplissages
        self.set_fill_color(142,40,98)
        os.chdir(r'C:/Users/Silver/Desktop/PJT FORUM AM/Logo')
        self.image("logo_forum_am.png",0,0,largeur,longueur_image)
        os.chdir(r'C:/Users/Silver/Desktop/PJT FORUM AM/Police')
        #Création d'un réctangle rempli, de largeur page
        self.rect(0,0,largeur,longueur_rectangle_entete,"F")
        # Police Arial gras 15
        self.set_font('Aharoni', '', 24)
        # Titre
        self.set_fill_color(243,146,0)
        self.set_x(0)
        self.set_y(14.3)
        self.set_text_color(255,255,255)
        self.cell(109.3,18, 'Votre Parcours Forum AM', new_x="RIGHT", new_y="TOP", align='C', fill=True)
        
        self.set_xy(135,0.7)
        self.set_font('Aptos', '', 11)
        string = nom +' | Id n° : ' + Id + ' Page %s' % (self.page_no()+pages_avant)
        
        #Prise en compte de la taille du nom et de l'ID
        if (self.get_string_width(string) + 135 < largeur):
            self.cell(73.6,7.3,string,new_x="RIGHT", new_y="TOP", align='C', fill=False)
        else :
            self.cell(73.6+largeur-(self.get_string_width(string) + 135) ,7.3,string,new_x="RIGHT", new_y="TOP", align='C', fill=False)
            
        self.set_x(12.2)
        self.set_y(0.7)
        self.set_font('Aptos', '', 11)
        self.cell(91.6,7.3, 'Test d’Orientation Professionnelle pour Ingénieurs', new_x="RIGHT", new_y="TOP", align='C', fill= False)
        
        
        
    #Tentative de création d'une fonction qui permet d'écrire avec gras et liens
    def mixed_text(self,text,w,l,site,police,siz):
        #rapport_police_milli = 0.375
        Symbole_gras = "<g>"
        Symbole_fin_gras = "<\g>"
        nb_c = len(text)
        indice_lettre = 0
        debut = 0
        while nb_c-3 >indice_lettre+debut:
            
            if text[debut+indice_lettre:debut+indice_lettre+3]==Symbole_gras :
                debut+=3
                lengh = 0
                gras = True
                while gras and nb_c-3 >debut+indice_lettre+lengh:
                    lengh+=1
                    if text[debut + indice_lettre+lengh:debut +indice_lettre+lengh+3]==Symbole_fin_gras :
                        gras = False
                self.cell(self.get_string_width(text[debut:debut+indice_lettre-3]),l,text[debut:debut+indice_lettre-3], new_x="RIGHT", new_y="TOP", align='C', fill= False)
                pdf.set_font(police, "B", size = siz)
                self.cell(self.get_string_width(text[debut+indice_lettre:debut+indice_lettre+lengh]),l,text[debut+indice_lettre:debut+indice_lettre+lengh], new_x="RIGHT", new_y="TOP", align='C', fill= False)
                pdf.set_font(police, "", size = siz)
                debut = debut+indice_lettre+lengh+3
                indice_lettre =0  
                
                
            indice_lettre +=1 
            
        self.cell(self.get_string_width(text[debut:]),l,text[debut:], new_x="RIGHT", new_y="TOP", align='C', fill= False)
         
    # Fonction pour centrer le texte dans un cadre donné
    def draw_text_in_box(self, x, y, w, h, text, max_font_size=12, min_font_size=3):
        font_size = max_font_size

        # On essaie de gérer les retours à la ligne sans modifier la taille de la police
        while font_size >= min_font_size:
            self.set_font('Aptos', 'B', font_size)
            # Diviser le texte en lignes qui tiennent dans la largeur du cadre
            lines = self.wrap_text(text, w)

            # Calculer la hauteur totale nécessaire pour toutes les lignes
            total_text_height = len(lines) * (font_size * 0.4)

            # Si le texte tient dans la hauteur du cadre, on l'affiche centré
            if total_text_height <= h:
                # Centrer verticalement
                start_y = y + (h - total_text_height) / 2
                self.set_xy(x, start_y)
                
                # Imprimer chaque ligne centrée horizontalement
                for line in lines:
                    
                    line_width = self.get_string_width(line)
                    while font_size >= min_font_size and line_width>w:
                        font_size-=1
                        self.set_font('Aptos', 'B', font_size)
                        line_width = self.get_string_width(line)
                for line in lines:
                    line_width = self.get_string_width(line)
                    #Le -2 est ajouté manuellement pour centrer mais c'est probablement une idée de merde
                    start_x = x + (w - line_width-2) / 2
                    self.set_xy(start_x, self.get_y())
                    self.cell(line_width, font_size * 0.4, line, ln=True)

                break
            else:
                # Si le texte ne tient pas, réduire la taille de la police
                font_size -= 1
                
    def draw_text_in_box2(self, x, y, w, h, text, max_font_size=8, min_font_size=5):
        font_size = max_font_size

        # On essaie de gérer les retours à la ligne sans modifier la taille de la police
        while font_size >= min_font_size:
            self.set_font('Aptos', '', font_size)
            # Diviser le texte en lignes qui tiennent dans la largeur du cadre
            lines = self.wrap_text(text, w)

            # Calculer la hauteur totale nécessaire pour toutes les lignes
            total_text_height = len(lines) * (font_size * 0.4)

            # Si le texte tient dans la hauteur du cadre, on l'affiche centré
            if total_text_height <= h:
                # Centrer verticalement
                start_y = y + (h - total_text_height-2) / 2
                self.set_xy(x, start_y)
                
                lengh = 0
                while lengh <len(lines[0]) and lines[0][:lengh] not in Liste_sec :
                    lengh +=1
                line_width = self.get_string_width(lines[0])
                self.set_xy(x, self.get_y())
                self.set_font('Aptos', 'B', font_size)
                self.cell(self.get_string_width(lines[0][:lengh+1]), font_size * 0.4, lines[0][:lengh+1])
                
                self.set_font('Aptos', '', font_size)
                self.cell(self.get_string_width(lines[0][lengh+1:]), font_size * 0.4, lines[0][lengh+1:], ln=True)
                # Imprimer chaque ligne centrée horizontalement
                for line in lines[1:]:
                    
                    line_width = self.get_string_width(line)
                    start_x = x 
                    self.set_xy(start_x, self.get_y())
                    self.cell(line_width, font_size * 0.4, line, ln=True)

                break
            else:
                # Si le texte ne tient pas, réduire la taille de la police
                font_size -= 1
        
                
    # Fonction pour diviser le texte en lignes adaptées à la largeur du cadre sans couper les mots
    def wrap_text(self, text, max_width):
        words = text.split(' ')
        lines = []
        current_line = ''
        
        for word in words:
            # Ajouter le mot courant à la ligne actuelle
            test_line = current_line + word + ' '
            line_width = self.get_string_width(test_line)

            # Si la ligne dépasse la largeur maximale, ajouter la ligne actuelle aux lignes et recommencer
            if line_width > max_width and current_line:
                lines.append(current_line.strip())  # Ajouter la ligne et supprimer les espaces inutiles
                current_line = word + ' '  # Commencer une nouvelle ligne avec le mot actuel
            else:
                current_line = test_line
        
        # Ajouter la dernière ligne si elle n'est pas vide
        if current_line.strip():
            lines.append(current_line.strip())
        
        return lines
    
    def tableau(self,xo,yo,Liste_etp,Liste_logo,liste_description):
        os.chdir(r'C:/Users/Silver/Desktop/PJT FORUM AM/Logo')
        titre = [" ","Logo","Entreprise","Description/Secteur"]
        Tabl = [titre]
        

        for a in range(7):
            Tabl.append([" "," ",Liste_etp[a]," "])
        largeur = 186.9
        hauteur = 14.9
        column_dim = [16.2,25.8,23,largeur-16.2-25.8-22.8]
        dim_image = 13.7
        x = xo
        y = yo       
        x_l = xo
        y_l = yo
        x_desc = xo
        y_desc = yo
        self.set_xy(x,y)
        for i in range(8):
        #On a 7 ligne et l'entete
            for j in range(4):
            #on a 4 colonnes
                if i == 0:
                    self.set_font("aptos","B",size = 12)
                    
                elif j == 0:
                    self.set_font("aptos","B",size = 12)
                    self.set_text_color(0,0,0)
                    
                    self.image("Point_localisation.png",xo+1.3,yo+15.4+(i-1)*hauteur,dim_image,dim_image)
                    
                    x_l,y_l = self.get_x(),self.get_y()
                    self.set_xy(xo+5.9,yo+16.2+(i-1)*hauteur)
                    #dimensions choisi avec le ppt
                    self.cell(4.44,7.6,str(i),align= "C")
                    self.set_xy(x_l,y_l)
                    
                elif j == 1:
                    
                    self.image(Liste_logo[i-1][0],21+11.2-(Liste_logo[i-1][1]-17.5)/2,yo+(i)*hauteur,Liste_logo[i-1][1],Liste_logo[i-1][2])
                    
                elif j == 2:
                    self.set_font("aptos","B",size = 12)
                    self.set_text_color(0,0,0)
                    a= self.get_x()
                    b = self.get_y()
                    self.draw_text_in_box(a,b,column_dim[j],hauteur,Tabl[i][j])
                    self.set_xy(a,b)
                    self.cell(column_dim[j],hauteur,"",border = 1,new_x="RIGHT", new_y="TOP", align= "C")
                    
                    continue
                else :
                    self.set_font("aptos","",size = 8)
                    self.set_text_color(0,0,0)
                    x_desc,y_desc = self.get_x(),self.get_y()
                    self.set_xy(x_desc+1,y_desc+1)
                    self.draw_text_in_box2(self.get_x(),self.get_y(),column_dim[-1]-2,hauteur,Liste_sec[i-1] + " " +liste_description[i-1])
                    #self.multi_cell(column_dim[-1]-2,4, liste_description[i-1],align= "L")
                    self.set_xy(x_desc,y_desc)
                    
                self.cell(column_dim[j],hauteur,Tabl[i][j],border = 1,new_x="RIGHT", new_y="TOP", align= "C")
            y += hauteur
            self.set_y(y)
            self.set_x(x)
        os.chdir(r'C:/Users/Silver/Desktop/PJT FORUM AM/Police')
        
    #Fonction pour souligner du texte       
    def underline_text(self, x, y,a,b, text,l):
        #a et b correspondent à la position absolue du début du texte à souligner, x y sont les positions par rapport au curseur
        self.cell(x, y, text, link=l)
        self.line(a+1, b + self.font_size, a + self.get_string_width(text)+1, b + self.font_size)

    def pointeur_tableau(self, liste_etp, liste_coordonnes, x_coordonne_carte, y_coordonne_carte):
        taille_pointeur = 11.0
        position_point_pointeur = (11 / 2, 11)
        position_chiffre_point = (-2.25, -2 * 11 / 3 - 2.26)
        self.set_text_color(0, 0, 0)
        
        # Création d'une liste avec les coordonnées et les indices originaux
        liste_avec_indices = [(index, coord) for index, coord in enumerate(liste_coordonnes)]
        
        # Tri des coordonnées uniquement par Y, tout en conservant les indices originaux
        liste_triee = sorted(liste_avec_indices, key=lambda item: item[1][1])
        
        os.chdir(r'C:/Users/Silver/Desktop/PJT FORUM AM/Logo')
        
        for (original_index, coord) in liste_triee:
            # Positionnement de l'image du pointeur
            self.image(
                "Point_localisation_2.png",
                x_coordonne_carte + coord[0] - position_point_pointeur[0],
                y_coordonne_carte + coord[1] - position_point_pointeur[1],
                taille_pointeur,
                taille_pointeur
            )
            
            # Positionnement du numéro en fonction de l'indice original
            self.set_xy(
                x_coordonne_carte + coord[0] + position_chiffre_point[0],
                y_coordonne_carte + coord[1] + position_chiffre_point[1]
            )
            self.set_font("aptos", "B", size=12)
            self.cell(
                self.get_string_width(str(original_index + 1)),
                12 * 0.4,
                text=str(original_index + 1),
            )




###____________________________________________________________________________Fonction utile_______________________________________________________________________________###   
def convertion(L):
    M = L.copy()
    for i in range(len(L)):
        if L[i] == "Agriculture, sylviculture et pêche":
            M[i] = 11
        elif L[i] == "Industrie extractive, raffinage":
            M[i] = 7
        elif L[i] == "Industrie agroalimentaire (IAA)":
            M[i] = 11
        elif L[i] == "Industrie chimique":
            M[i] = 7
        elif L[i] == "Industrie pharmaceutique":
            M[i] = 14
        elif L[i] == "Plastique, produits non métalliques":
            M[i] = 8
        elif L[i] == "Siderurgie, Fonderie":
            M[i] = 8
        elif L[i] == "Produits informatiques, électroniques, et optiques":
            M[i] = 13
        elif L[i] == "Luxe et textile":
            M[i] = 12
        elif L[i] == "Equipements électriques":
            M[i] = 13
        elif L[i] == "Machines, armements":
            M[i] = 1
        elif L[i] == "Automobile":
            M[i] = 2
        elif L[i] == "Aéronautique":
            M[i] = 1
        elif L[i] == "Spatial":
            M[i] = 1
        elif L[i] == "Ferroviaire et naval":
            M[i] = 2
        elif L[i] == "Electricité, Gaz":
            M[i] = 7
        elif L[i] == "Eau, assainissement, gestion des déchets":
            M[i] = 7
        elif L[i] == "Construction, BTP":
            M[i] = 4
        elif L[i] == "Commerce, réparation":
            M[i] = 3
        elif L[i] == "Transport, logistique, entreposage":
            M[i] = 2
        elif L[i] == "Télécoms":
            M[i] = 9
        elif L[i] == "Médias, publicitaires, événementiel":
            M[i] = 5
        elif L[i] == "Banques, assurances, établissements financiers":
            M[i] = 3
        elif L[i] == "Audit, Conseil en stratégie et management":
            M[i] = 5
        elif L[i] == "Enseignement et recherche":
            M[i] = 6
        elif L[i] == "Administration (hors enseignement et recherche)":
            M[i] = 3
        elif L[i] == "Conseil, logiciels et services informatique":
            M[i] = 9
        elif L[i] == "Société d'ingénierie":
            M[i] = 10
    N = []
    for test in M:
        if test not in N :
            N.append(test)
    return N
        
      
        
 
###____________________________________________________________________BDD ET DONNEES STABLES____________________________________________________________________###  
#On se place là où il ya les bdd
os.chdir(r'C:/Users/Silver/Desktop/PJT FORUM AM/BDD')

#BDD Eleves
nom_fichier = "BDD_eleve.json"  # Remplacez par le chemin de votre fichier .json


#Liste des secteurs pour y associer des numéro
Liste_secteur = ["Aéronautique, Spatial, Défense",
                 "Automobile, Transport",
                 "Banque, finance, services",
                 "BTP, Immobilier",
                 "Conseil",
                 "Ecole, Formation, Recherche",
                 "Energie, Chimie, Environnement",
                 "Industrie, Maintenance, Métallurgie, Plasturgie",
                 "Informatique, IT, Telecom",
                 "Ingénierie, Etudes techniques",
                 "Logistique, Agroalimentaire",
                 "Luxe",
                 "Robotique, Electronique",
                 "Santé"]
"""
#Ceci est la liste des secteurs fourni par TOPI
Liste_secteur = ["Agriculture, sylviculture et pêche",
                 "Industrie extractive, raffinage",
                 "Industrie agroalimentaire (IAA)",
                 "Industrie chimique",
                 "Industrie pharmaceutique",
                 "Plastique, produits non métalliques",
                 "Siderurgie, Fonderie",
                 "Produits informatiques, électroniques, et optiques",
                 "Luxe et textile",
                 "Equipements électriques",
                 "Machines, armements",
                 "Automobile",
                 "Aéronautique",
                 "Spatial",
                 "Ferroviaire et naval",
                 "Electricité, Gaz",
                 "Eau, assainissement, gestion des déchets",
                 "Construction, BTP",
                 "Commerce, réparation",
                 "Transport, logistique, entreposage",
                 "Télécoms",
                 "Médias, publicitaires, événementiel",
                 "Banques, assurances, établissements financiers",
                 "Audit, Conseil en stratégie et management",
                 "Enseignement",
                 "Administration (hors enseignement et recherche)",
                 "Conseil, logiciels et services informatique",
                 "Société d'ingénierie"]
"""
#On ouvre la BDD ETP et on refait le tableau sous forme de liste sur python
Secteurs = []
for j in Liste_secteur:
    Secteurs.append([])
    
fichier = open("bdd_etp_a_exporter.txt",'r')
ligne = fichier.read().splitlines()
#Séparation des colonnes et ajout de la ligne dans la bonne partie du tableau Secteurs
for i in range(len(ligne)):
    ligne[i]= ligne[i].split("\t")
    Secteurs[Liste_secteur.index(ligne[i][1])].append(ligne[i])

#######_______________________________________________________________________Fonction définie ici_ car dépend de la longueur qu'on veut_________________________________________________________________#########
    def importer_json_et_extraire_listes(nom_fichier):
        """
        Importe un fichier JSON contenant une liste de dictionnaires
        et extrait les données en listes distinctes pour chaque clé.
    
        Args:
            nom_fichier (str): Le chemin du fichier JSON.
    
        Returns:
            dict: Un dictionnaire où chaque clé correspond à une liste des valeurs associées.
        """
        try:
            # Lire le fichier JSON
            with open(nom_fichier, 'r', encoding='utf-8') as fichier:
                data = json.load(fichier)
        
            # Extraire les données en listes distinctes
            Nom = []
            Prenom = []
            Email = []
            ID = []
            Liste_secteur_interet = []
            for entry in data:
                for clé, valeur in entry.items():
                    if clé == "prenom":
                        Prenom.append(valeur)
                    elif clé == "nom":
                        Nom.append(valeur)
                    elif clé == "email":
                        Email.append(valeur)
                    elif clé == "identifiant":
                        ID.append(valeur)
                    elif clé == "ranked_secteurs":
                        L = []
                        for couple_secteur in valeur:
                            if len(L)<19:
                                L.append(couple_secteur[0])
                            else : break
                        Liste_secteur_interet.append(L)
            
            return Prenom,Nom,Email,ID,Liste_secteur_interet
    
        except FileNotFoundError:
            print(f"Le fichier {nom_fichier} n'existe pas.")
            return {}
        except json.JSONDecodeError:
            print(f"Erreur lors de la lecture du fichier JSON {nom_fichier}.")
            return {}
        except ValueError as e:
            print(e)
            return {}
    Prenoms,Noms,Email,Identifiants,Liste_secteur_interets = importer_json_et_extraire_listes(nom_fichier)
#
#Exemple format etp
"""
Secteurs = [[("Limagrin",0.5,[1,7],)]]
"""           
###____________________________________________________________________Attribution aux PG____________________________________________________________________###

for index_PDF_PG in range(len(Noms)):
    nom = Noms[index_PDF_PG] + " " + Prenoms[index_PDF_PG]
    Id = Identifiants[index_PDF_PG]
    Recomendations = Liste_secteur_interets[index_PDF_PG]
    Reco_converti = convertion(Recomendations)
    Student = PG(Reco_converti)
    Student.affectation(Id)
    Liste_e = [i[0] for i in Student.tab]
    Liste_desc = [i[2] for i in Student.tab]
    Liste_sec = [i[1] for i in Student.tab]
    Liste_coord = [(float(i[3])*210/1654,float(i[4])*262.8/2070) for i in Student.tab]#A MODIFIER EN FONCTION DE LA BDD mais j'imagine que ça sera en position 6
    Liste_lo = []
    
    ###____________________________________________________________________Dimensionnement des logo____________________________________________________________________###  
    #On se pace là où il a les logo
    os.chdir(r'C:/Users/Silver/Desktop/PJT FORUM AM/Logo')
    # Petite fonction pour chopper les dimensions des images
    
    def get_image_dimensions(image_name):
        # Ouvrir l'image
        with Image.open(image_name) as img:
            # Obtenir les dimensions (largeur, hauteur)
            width, height = img.size
        return width, height
    
    def dimensionnement(x,y):
        if x == y :
            return (14.9,14.9)
        else:
            return (x/y*14.9,14.9)
    #On récupére les logo des entreprises concernées et on a adapte les dimensions
    for k in Student.tab:
        rim = get_image_dimensions(str(k[0])+".png")
        dim = dimensionnement(rim[0],rim[1])
        Liste_lo.append([str(k[0])+".png",dim[0],dim[1]])
        
    
    ###________________________________________________________________________Définition du PDF________________________________________________________________________###  
    # Création d'une instance de la classe PDF
    os.chdir(r'C:/Users/Silver/Desktop/PJT FORUM AM/Police')
    pdf = PDF()
    
    #Implémentation des polices nécessaires
    pdf.add_font("Aharoni","","ahronbd.ttf")
    pdf.add_font("Aptos","","fonnts.com-aptos.ttf")
    pdf.add_font("Aptos","B","fonnts.com-aptos-black.ttf")
    
    #Longueur de l'image AM
    longueur_image = 210
    largeur = 210
    
    
    # Définir la police
    pdf.set_font("aptos", size=14)
    
    
    #texte de bienvenue séparé en plusieur pour les mots en gras
    texte = " correspondant le mieux avec votre profil d’ingénieur pour vous permettre de vous orienter lors du jour J.\n \n Vous pouvez utiliser les résultats de ce test pour vous préparer au mieux pour votre venue au Forum. Pour plus d’informations sur les entreprises nous vous donnons rendez-vous sur notre application forum AM (disponible sur Play Store et App Store) ainsi que sur notre site web " 
    texte2 = "\n \n Au plaisir de vous voir préparés le 20 novembre au Parc Floral.\n \n Cordialement, \n \n L’équipe Forum AM et TOPI"
    
    
    pdf.add_page()
    pdf.set_x(0)
    pdf.set_y(41.6)
    
    os.chdir(r'C:/Users/Silver/Desktop/PJT FORUM AM/Police')
    #Rédaction et positionnement des différents élément du texte
    pdf.set_xy(7.2,41.6)
    pdf.set_font("aptos", size = 14)
    pdf.set_text_color(0,0,0)
    pdf.set_margins(7.2,0,210-7.2-195.7)
    pdf.write(6.21,"Le TOPI s’associe au Forum Arts et Métiers pour vous proposer un parcours d’entreprises \n")
    
    pdf.set_xy(pdf.get_x(),pdf.get_y())
    pdf.set_font("aptos", "B", size = 14)
    pdf.write(6.21,"correspondant le mieux avec votre profil d’ingénieur")
    
    pdf.set_xy(pdf.get_x(),pdf.get_y())
    pdf.set_font("aptos", size = 14)
    pdf.write(6.21,texte)
    
    pdf.set_xy(pdf.get_x(),pdf.get_y())
    pdf.set_font("aptos", size = 14)
    pdf.set_text_color(0,0,255)
    pdf.underline_text(0,6.21,pdf.get_x(),pdf.get_y(),"forum-am.fr",'http://forum-am.fr')
    
    pdf.set_xy(pdf.get_x(),pdf.get_y())
    pdf.set_font("aptos", size = 14)
    pdf.set_text_color(0,0,0)
    pdf.write(6.21,texte2)
    pdf.tableau(11.9,143.2,Liste_e,Liste_lo,Liste_desc)
    
    #_____________________________________________________________________Page avec la carte____________________________________________________________________#
    pdf.add_page()
    os.chdir(r'C:/Users/Silver/Desktop/PJT FORUM AM/Carte')
    
    x_c = 0 #position de l'image prise sur le pptx
    y_c = 33.3#position de l'image prise sur le pptx
    l_c = 210
    L_c = 262.8
    pdf.image("Carte_forum.png",x_c,y_c,l_c,L_c)
    pdf.pointeur_tableau(Liste_e, Liste_coord,x_c,y_c)
    
    
    ###____________________________________________________________________Création du PDF____________________________________________________________________###  
    # Enregistrement du PDF
    
    os.chdir(r'C:/Users/Silver/Desktop/PJT FORUM AM/PDF')
    pdf_output_path = Id+".pdf"
    if os.path.exists(pdf_output_path):
        print("Existe déjà")
    pdf.output(pdf_output_path)
    
    # Vérification si le fichier a été enregistré avec succès
    if not os.path.exists(pdf_output_path):
        print("Erreur lors de la création du PDF")
