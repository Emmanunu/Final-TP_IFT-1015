# Emmanuelle Pilon & Alessia Muresan 
# 12.12.2023
# Ce programme implémente le jeu "addiction solitaire". Il s'exécute dans
# l'environnement du navigateur web. Les cartes sont brassées et placées sur
# une grille de quatre rangées avec 13 cartes par rangée. Le but du jeu est de
# placer les cartes en séquence sur les quatre rangées, c'est-à-dire en ordre
# du 2 au roi, et par sorte. Au début, les quatre as sont enlevés pour créer
# quatre trous. Les cartes peuvent être déplacées une à la fois et celles qui
# peuvent bouger prennent la couleur lime. Les cartes 2 peuvent être déplacées
# seulement sur un trou dans la première colonne et les cartes du 3 au roi
# peuvent aller dans un trou qui est à la droite de la carte de même couleur
# qui la précède. Lorsqu'il n'y a plus de déplacements possibles, les cartes
# qui ne sont pas encore placées à la bonne place peuvent être mélangées à 3
# reprises maximum, et il y a aussi un bouton "Nouvelle partie", pour
# recommencer la parte autant de fois que désiré. 

import math
import random

# ----------------------------------Algo---------------------------------------
# La fonction brassement_des_cartes prend un paramètre 'paq_mel' qui est un
# tableau de nombre, et un paramètre 'bool_paq' qui est une liste de nombres.
# Cette fonction brasse aléatoirement les cartes, selon la technique dmd
# (dans tableaux), donc qui retourne un tableau mélangé
def brassement_des_cartes(paq_mel, bool_paq):
    longueur = len(paq_mel)
    # Itère le tableau à l'envers, en commençant par le dernier élément
    for i in range(longueur - 1, 0, -1):
        # Vérifie si la carte à la position i n'est pas déjà bien placée
        if not bool_paq[i]:
            j = math.floor(random.random() * (i + 1))
            if not bool_paq[j]:
                paq_mel[i], paq_mel[j] = paq_mel[j], paq_mel[i]
    return paq_mel

# La fonction position_des_trous prend un paramètre 'paquet' qui est un
# tableau de nombre. Cette fonction calcul la position des 4 trous dans 
# le paquet.
def position_des_trous(paquet):  
    # 4 trous, retourne leurs positions
    trou_paq = []
    pos = 0
    # Itère à traver chaque carte du paquet
    for carte in paquet:
        # Si la carte est un as, un trou est créé
        if carte in [0, 1, 2, 3]:
            trou_paq.append(pos)
        pos += 1

    # paquet = paquet mélangé / trou_paq = position des 4 trous 
    return trou_paq


# La fonction tri prend en paramètre 'cartes', qui est une liste de tableaux
# de nombres pour les 4 sortes du jeu de carte. Cette fonction trie le
# paquet de carte selon les 4 sortes: coeur, pique, trèfle et carreaux.
def tri(cartes):
    # Création de 4 tableaux vides
    paq = []
    for _ in range(4):
        paq.append([])
    # Itère à travers chacune des cartes du tableau de nombres
    for carte in cartes:
        # Détermine la sorte de la carte, en utilisant l'opérateur modulo
        sorte = carte % 4
        # Ajoute la carte dans le tableau correspondant à la bonne sorte 
        paq[sorte].append(carte)
    # Retourne la liste de tableaux
    return paq

# La fonction verif_cartes prend en paramètre 'paquet', qui est un tableau de
# nombres, 'paq_bra' qui est un tableau de nombres du paquet brassé, et
# 'bool_paq' qui est une liste qui simule la position des cartes. Cette
# fonction vérifie si les cartes sont bien placées et utilise des valeurs
# booléenes (True ou False). 
def verif_cartes(paquet, paq_bra, bool_paq):
    for carte in paquet:
        if paquet[carte] == paq_bra[carte]:
            bool_paq.pop(carte)
            bool_paq.insert(carte, True)  
    
    return bool_paq

# La fonction poss_bra prend en paramètre 'dcp_bra' (décompte brassement) qui
# est un nombre entier qui calcule le nombre de brassements. Cette fonction
# fait le brassement des cartes, récupère la position des trous, met à jour
# l'affichage avec le html et met à jour les déplacements possibles après le
# brassage.
def poss_bra(dcp_bra):
    # Décrémentation du nombre de brassements disponibles. (maximum 3)
    dcp_bra -= 1

    # Brassement à nouveau, comme souhaiter par le joueur
    paq_bra = brassement_des_cartes(copy_paquet, bool_paq)
    # Calcul des nouveaux trous
    pos_trous = position_des_trous(paq_bra)
    # Réinitialisation des cartes sur la page web
    html(paq_bra, paquet, dcp_bra, pos_trous)
    # Calculs les déplacements possibles
    deplacements(paquet, paq_bra, pos_trous, tab_sortes, bool_paq, dcp_bra)
    return dcp_bra

# La fonction deplacements prend en paramètres 'paquet' qui est un tableau de
# nombres, 'paq_bra' qui est un tableau de nombres du paquet brassé, 'trous' 
# qui est la liste des trous dans le paquet brassé, 'tab_sortes' qui est un
# tableau de tableaux avec les cartes triées par sortes, 'bool_paq' qui est
# une liste qui simule la position des cartes et 'dcp_bra' qui est un nombre
# entier qui représente le nombre de brassements. Cette fonction gère les
# déplacements possibles des cartes dans le jeu.
def deplacements(paquet, paq_bra, trous, tab_sortes, bool_paq, dcp_bra):
    # Créer le tableau des cartes biens placées
    bool_paq = verif_cartes(paquet, paq_bra, bool_paq)

    # Tableau temporaire qui stocke toutes les possibilités d'échange
    global cartes_limes
    cartes_limes = []

    # Variable à itération
    pos_deux = 0                                        
    
    # Vérification de 2 trous côte à côte
    pos_trou = 0
    for blanc in trous:
        if blanc + 1 in trous:
            trous.pop(pos_trou + 1)
            pos_trou += 1
    
    # Première conddition pour les cartes '2'
    for trou in trous:
        if trou in [0, 13, 26, 39]: 
            pos_deux = 0                               
            for carte in paq_bra:
                # Cherche les deux dans le paquet brassé
                if carte in paquet[4:8]: 
                    if not bool_paq[carte]: 
                        # Ajout du trou ainsi que la carte deux (pouvant être
                        # échangée) 
                        cartes_limes.append([trou, pos_deux])  
                pos_deux += 1  
                if pos_deux > 51:
                    continue

        # Deuxième condition ('3' à 'roi')
        pos_carte = trou + 1
    
        if trou not in [0, 13, 26, 39]:
            # Trouver la sorte du trou
            for sorte in range(4):
                if pos_carte >=  51:
                    break
                carte_ana = paq_bra[trou - 1]
                tab_sorte = tab_sortes[sorte]
                if carte_ana in tab_sorte:
                    # Si la sorte est trouvée, itérer à travers les cartes de
                    # cette sorte dans les cartes à droite 
                    for carte in paq_bra[trou + 1:]:
                        if carte in tab_sorte and carte_ana < carte:
                            if not bool_paq[pos_carte]:
                                cartes_limes.append([trou, pos_carte])
                        pos_carte += 1

    # Affiche le bouton de brassage optionnel si des déplacements sont 
    # possibles
    if len(cartes_limes) > 0 and dcp_bra > 0:
        brass_opt.setAttribute("style", "display:inline")

    # Affiche le bouton de brassage obligatoire s'il n'y a pas de 
    # déplacements possibles 
    elif len(cartes_limes) == 0 and dcp_bra > 0:
        brass_obl.setAttribute("style", "display:inline")

    # Affiche le message qu'il n'y a plus de brassements possibles si le
    # compteur est à 0, donc si les 3 brassements ont été faits.
    elif dcp_bra == 0:
        brass_fini.setAttribute("style", "display:inline")
        # Si il ni a plus de brassements disponible et il n'y a plus de 
        # cartes limes à déplacer, la partie est terminée
        if len(cartes_limes) == 0:
            brass_fini.setAttribute("style", "display:none")
            perdu_msg.setAttribute("style", "display:inline")

    # Si le paquet du jeux est égale au paquet initiale, alors le toutes 
    # les cartes sont bien placées et le joueur à gagné
    elif bool_paq == [True] * 52:
        gagne_msg.setAttribute("style", "display:inline")

    # Calcul des cartes pouvant être déplacée
    for groupe in range(len(cartes_limes)):
        # Prend la position de la carte à changer
        case = "case" + str(cartes_limes[groupe][1])
        # Sélectionne le bon élément à changer la couleur
        cases = document.querySelector("#" + case)
        # Applique le style de la couleur
        cases.setAttribute("style", "background-color: lime")

# La fonction clic prend en paramètre 'case', qui est un nombre entier
# représentant la position de la case sur laquelle l'utilisateur a cliqué.
# Cette fonction À CONTINUER------------------------
def clic(case, dcp_bra, pos_trous):
    # Une variable temporaire afin de stocker toutes les cases limes
    # au moment du clic
    case_limes = []
    # Créer la liste des cases limes en utilisant la liste des cartes limes
    # et leurs trous
    for carte in range(len(cartes_limes)):
        case_limes.append(cartes_limes[carte][1])

    # Si la case cliquée ne fait pas partie des cases limes et fait partie
    # des trous, l'ignorée
    if case not in case_limes or case in pos_trous:
        return ''
        
    # Boucle qui parcourt les groupes de cartes qui peuvent être déplacées
    for groupe in range(len(cartes_limes)):
        if cartes_limes[groupe][1] == case:
            # Calcul de la position du trou et de la carte pour l'échange
            trou = cartes_limes[groupe][0]
            echa = cartes_limes[groupe][1]
            # Calcul de la carte correspondant au trou et à la carte pour 
            # l'échange
            carte_trou = paq_bra[trou]
            carte_echa = paq_bra[echa]
            break

    # Effectue les échanges entre la carte selectionnée et le trou dans 
    # le paquet du jeu
    for carte in range(len(paq_bra) - 1):
        if carte == trou:
            paq_bra.pop(trou)
            paq_bra.insert(trou, carte_echa)
        elif carte == carte_echa:
            paq_bra.pop(echa)
            paq_bra.insert(echa, carte_trou)

    # Met à jour l'affichage avec HTML avec la nouvelle disposition
    html(paq_bra, paquet, dcp_bra, pos_trous)
    # Calcul les nouveau trous dans le paquet mis à jour
    pos_trous = position_des_trous(paq_bra)
    # Calculs les nouveaux déplacements possibles
    deplacements(paquet, paq_bra, pos_trous, tab_sortes, bool_paq, dcp_bra)

# La fonction html prend en paramètres 'paq_bra' qui est un tableau de nombres
# du paquet brassé, 'paquet' qui est un tableau de nombres, et 'dcp_bra' qui
# est un nombre entier représentant le nombre de brassements. Cette fonction
# génère le code HTML représentant la grille des cartes, les messages et les
# boutons interactifs.
def html(paq_bra, paquet, dcp_bra, pos_trous):
    #HTML-----------------------------------------------------------------
    # Sortes de cartes (Diamonds (carreaux), Hearts (coeurs), Clubs (trèfles),
    # Spades (piques))
    sortes = ["D", "H", "C", "S"]
    cartes = ["2", "3", "4", "5", "6", "7", "8" , "9", "10", "J", "Q", "K"]
    matrice_cartes = ["cards/absent.svg", "cards/absent.svg",
                       "cards/absent.svg", "cards/absent.svg"]
    # Création des noms des cartes svg
    for carte in cartes:
        for sorte in sortes:
            matrice_cartes.append("cards/" + carte + sorte + ".svg")

    # Construction de la grille des cartes
    grille_cartes = (
    "<style>\n"
    " #jeu table { float:none; }\n"
    " #jeu table td { border:0; padding:1px 2px; height:auto; width:auto; }\n"
    " #jeu table td img { height:140px; }\n"
    "</style>\n"
    "<div id=\"jeu\">\n"
    "    <table>\n"
    )

    i = 0
    # Boucle qui itère à travers chaque carte du paquet brassé
    for alea in paq_bra:
        # Vérifie si une nouvelle ligne doit être ajoutée à la grille
        if i % 13 == 0:
                grille_cartes += "<tr>\n"    
        
        for ordre in paquet:
            if alea == ordre:
                grille_cartes += ('<td id="case' + str(i) + '"' + 
                                  'onclick="clic(' + str(i) + ', ' + 
                                  str(dcp_bra) + ', ' + str(pos_trous) + 
                                  ')"><img src="' + matrice_cartes[alea] + 
                                  '"></td>\n')

        if i % 13 == 12:
            grille_cartes += "</tr>\n"
        i += 1
    grille_cartes += "    </table>\n</div>\n"

    # Mise à jour du contenu HTML de l'élément racine
    racine = document.querySelector("#cb-body")
    racine.innerHTML = (
        grille_cartes + """ <br>
        <!-- Possibilitée de brasser à n'importe quel moment --!>
        <div id="brass_opt">
        """
        "    Vous pouvez encore <button onclick=\"poss_bra(" + 
        str(dcp_bra) + ")\"> Brasser les cartes </button>" + " " + 
        str(dcp_bra) + " fois"
        """
        </div>

        <!-- Brassement obligatoire --!>
        <div id="brass_obl">
        """
        "    Vous devez <button onclick=\"poss_bra(" + str(dcp_bra) + 
        ")\"> Brasser les cartes </button>"
        """
        </div> 

        <!-- Plus de brassement possible --!>
        <div id="brass_fini">
            Vous ne pouvez plus brasser les cartes 
        </div> 

        <!-- Perdu --!>
        <div id="perdu_msg">
            Vous n'avez pas réussi à placer toutes les cartes... 
            Essayez à nouveau!
        </div>

        <!-- Gagné --!>
        <div id="gagne_msg">
            Vous avez réussi!  Bravo!
        </div>
        <br>
        <br>
    
        <!-- Nouvelle partie --!>
        <div>
            <button onclick="init()"> Nouvelle partie </button>
        </div>
        """
        )
    global brass_opt
    global brass_obl
    global brass_fini
    global perdu_msg
    global gagne_msg

    # Recherche des éléments HTML correspondants dans le document par leur 
    # ID
    brass_obl = document.querySelector("#brass_obl")
    brass_opt = document.querySelector("#brass_opt")
    brass_fini = document.querySelector("#brass_fini")
    perdu_msg = document.querySelector("#perdu_msg")
    gagne_msg = document.querySelector("#gagne_msg")

    # Initialisation du style des éléments HTML, les éléments sont 
    # initialement masqués
    brass_obl.setAttribute("style", "display:none")
    brass_fini.setAttribute("style", "display:none")
    brass_opt.setAttribute("style", "display:none")
    perdu_msg.setAttribute("style", "display:none")
    gagne_msg.setAttribute("style", "display:none")

# La procédure 'init' initialise les éléments nécessaires pour débuter une
# partie du jeu.
def init():
    # Valeur qui compte le nombre de brassement possibles lors d'une 
    # partie
    global dcp_bra   
    dcp_bra = 3

    # Liste qui simule les positions des cartes, définissant si elles sont 
    # bien placées
    global bool_paq
    bool_paq = [False] * 52

    # Paquet initial de 0 à 51, qui représente les 52 cartes du jeu
    global paquet
    paquet = list(range(52)) 
        
    # Créer un tableau ordonné en section de 4 afin d'identifier les 4 
    # sortes
    global tab_sortes
    tab_sortes = tri(paquet)

    # Copie du paquet pour le brassement
    global copy_paquet
    copy_paquet = paquet.copy()  
  
    # Paquet bassé aléatoirement + position des trous
    global paq_bra
    paq_bra = brassement_des_cartes(copy_paquet, bool_paq)
    pos_trous = position_des_trous(paq_bra)

    # Affichage HTML avec le paquet brassé et le nombre de brassages 
    # disponibles
    html(paq_bra, paquet, dcp_bra, pos_trous)

    # Retourne la grille avec l'échange des positions
    deplacements(paquet, paq_bra, pos_trous, tab_sortes, bool_paq, dcp_bra)


#Tests unitaires------------------------------------------------------------

def test_brassement_des_cartes():
    
    # Test avec un paquet vide
    assert brassement_des_cartes([], 52 * [False]) == ([])
    
    # Test avec une seule valeur
    assert brassement_des_cartes([2], 52 * [False]) == ([2]) 
    
    # Test avec 2 valeurs
    assert brassement_des_cartes([1,2], [True, True]) == ([1,2])
    
test_brassement_des_cartes()


def test_position_des_trous():

    # Test avec un paquet vide
    assert position_des_trous([]) == ([])

    # Test avec un paquet ordonné
    assert position_des_trous([0, 1, 2, 3, 4]) == [0, 1, 2, 3]

    # Test avec un paquet de longueur + 5 mélangé
    assert position_des_trous([0, 8, 4, 7, 10, 20]) == [0]

test_position_des_trous()


def test_tri():
    
    # Test avec le paquet de 52 cartes
    assert tri(list(range(52))) == [[0, 4, 8, 12, 16, 20, 24, 28, 
        32, 36, 40, 44, 48], [1, 5, 9, 13, 17, 21, 25, 29, 33, 37, 
        41, 45, 49], [2, 6, 10, 14, 18, 22, 26, 30, 34, 38, 42, 46, 
        50], [3, 7, 11, 15, 19, 23, 27, 31, 35, 39, 43, 47, 51]]
     
    # Test avec un paquet vide
    assert tri([]) == [[], [], [], []]
    
    # Test avec des cartes de la même sorte
    assert tri([4, 8, 12]) == [[4, 8, 12], [], [], []]
    
    # Test avec des cartes mélangées
    assert tri([10, 14, 32, 8, 6]) == [[32, 8], [], [10, 14, 6], []]
    
    # Test avec une seule carte
    assert tri([5]) == [[], [5], [], []]

test_tri()

def test_verif_cartes():
    
    # Test avec des paquets vides
    assert verif_cartes([],[],[]) == []

    # Test avec des cartes correctement placées
    assert verif_cartes([0, 1, 2, 3, 4, 5], 
                        [0, 1, 2, 3, 4, 5], [False] * 52) == [True, True, 
                        True, True, True, True, False, False, False, 
                        False, False, False, False, False, False, False,
                        False, False, False, False, False, False, False, 
                        False, False, False, False, False, False, False, 
                        False, False, False, False, False, False, False, 
                        False, False, False, False, False, False, False, 
                        False, False, False, False, False, False, False, 
                        False]

    # Test avec des paquets différents
    assert verif_cartes([0, 1, 2, 3, 4], 
                        [5, 6, 7, 8, 9], [False] * 52) == [False, False, 
                        False, False, False, False, False, False, False, 
                        False, False, False, False, False, False, False, 
                        False, False, False, False, False, False, False, 
                        False, False, False, False, False, False, False, 
                        False, False, False, False, False, False, False, 
                        False, False, False, False, False, False, False, 
                        False, False, False, False, False, False, False, 
                        False]

    # Test avec des cartes incorrectement placées
    assert verif_cartes([0, 1, 2, 3, 4, 5], 
                        [2, 3, 1, 5, 4, 0], [False] * 52) == [False, False,
                        False, False, True, False, False, False, False, 
                        False, False, False, False, False, False, False, 
                        False,  False, False, False, False, False, False, 
                        False, False, False, False, False, False, False, 
                        False, False, False, False, False, False, False, 
                        False, False, False, False, False, False, False, 
                        False, False, False, False, False, False, False, 
                        False]

test_verif_cartes()