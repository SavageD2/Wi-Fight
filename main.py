#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module principal gérant la logique de combat
"""

import random
import time
from src.models import MagicienBlanc, RoiSorcier
from src.models.personnage import Personnage
from src.utils import (
    afficher_titre,
    afficher_tour,
    afficher_introduction,
    afficher_victoire,
    charger_config
)


def executer_tour(attaquant: Personnage, defenseur: Personnage):
    """
    Exécute un tour de combat
    
    Args:
        attaquant: Le personnage qui attaque
        defenseur: Le personnage qui défend
    """
    # Choisir une frappe aléatoire
    frappe_choisie = random.choice(attaquant.frappes)
    
    print(f"\n🎯 {attaquant.nom} utilise: {frappe_choisie['icone']} {frappe_choisie['nom']}")
    print(f"   {frappe_choisie['description']}")
    
    # Exécuter l'attaque
    attaquant.frappe(defenseur, frappe_choisie)
    
    # Afficher les stats du défenseur
    print(f"\n📊 État de {defenseur.nom}:")
    defenseur.afficher_stats()


def boucle_combat(joueur1: Personnage, joueur2: Personnage):
    """
    Gère la boucle principale du combat
    
    Args:
        joueur1: Le premier joueur
        joueur2: Le second joueur
        
    Returns:
        Le personnage vainqueur
    """
    config = charger_config()
    delai = config['combat']['delai_tour']
    
    tour = 1
    
    while joueur1.est_vivant() and joueur2.est_vivant():
        # Déterminer l'attaquant et le défenseur
        if Personnage.tour == 'joueur1':
            attaquant = joueur1
            defenseur = joueur2
        else:
            attaquant = joueur2
            defenseur = joueur1
        
        afficher_tour(tour, attaquant)
        executer_tour(attaquant, defenseur)
        
        # Changer de tour
        Personnage.tour = 'joueur2' if Personnage.tour == 'joueur1' else 'joueur1'
        tour += 1
        
        # Petite pause pour la lisibilité
        time.sleep(delai)
    
    # Retourner le vainqueur
    return joueur1 if joueur1.est_vivant() else joueur2


def main():
    """Fonction principale du programme"""
    # Afficher le titre
    afficher_titre()
    
    # Création des personnages
    magicien = MagicienBlanc()
    roi_sorcier = RoiSorcier()
    
    # Afficher l'introduction
    afficher_introduction(magicien, roi_sorcier)
    
    # Lancer le combat
    vainqueur = boucle_combat(magicien, roi_sorcier)
    perdant = roi_sorcier if vainqueur == magicien else magicien
    
    # Afficher le résultat
    afficher_victoire(vainqueur, perdant)


if __name__ == "__main__":
    main()
