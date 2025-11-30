#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Combat Py-Fight v2.0 - Mode PvE (Joueur vs IA)
"""

import sys
from src.models.sage import Sage
from src.models.magicien import Magicien
from src.ai.ai_player import AIPlayer
from src.utils.input_handler import InputHandler
from src.utils.menu import Menu
from src.game.save_manager import SaveManager


def combat_pve():
    """Mode de combat Joueur vs IA"""
    from src.utils import ascii_art
    
    # Écran de bienvenue
    ascii_art.afficher_ecran_bienvenue()
    
    # Menu principal
    Menu.afficher_titre()
    
    while True:
        choix = Menu.menu_principal()
        
        if choix == '1':  # Choisir personnage et jouer directement
            classe_joueur = Menu.choisir_personnage()
            nom_joueur = Menu.demander_nom_joueur(classe_joueur)
            
            # Confirmation et lancement direct
            if Menu.confirmer_combat_pve(nom_joueur, classe_joueur):
                lancer_combat_pve(nom_joueur, classe_joueur)
                return
            else:
                print("\n❌ Combat annulé.")
                input("⏎ Appuyez sur Entrée pour continuer...")
        
        elif choix == '2':  # Voir détails
            Menu.afficher_details_tous()
        
        elif choix == '3':  # Modes avancés
            mode = Menu.menu_modes_combat()
            
            if mode == '1':  # PvE
                classe_joueur = Menu.choisir_personnage()
                nom_joueur = Menu.demander_nom_joueur(classe_joueur)
                if Menu.confirmer_combat_pve(nom_joueur, classe_joueur):
                    lancer_combat_pve(nom_joueur, classe_joueur)
                    return
            elif mode == '2':  # Auto (IA vs IA)
                lancer_combat_auto()
                return
            elif mode == '3':  # PvP
                print("\n🚧 Mode PvP - En développement...")
                input("⏎ Appuyez sur Entrée pour continuer...")
            # mode == '4' retourne au menu principal
        
        elif choix == '4':  # Quitter
            print("\n👋 À bientôt!")
            sys.exit(0)


def lancer_combat_auto():
    """Lance un combat Auto (IA vs IA)"""
    import random
    from src.utils import ascii_art
    
    print("\n" + "="*70)
    print("🤖 MODE AUTO - IA vs IA")
    print("="*70)
    
    # Choix aléatoire des classes
    classes = ['sage', 'magicien']
    classe_ia1 = random.choice(classes)
    classe_ia2 = random.choice([c for c in classes if c != classe_ia1])  # Forcer des classes différentes
    
    # Créer les personnages
    if classe_ia1 == 'sage':
        ia1 = Sage("IA-Sage")
        ia2 = Magicien("IA-Magicien")
    else:
        ia1 = Magicien("IA-Magicien")
        ia2 = Sage("IA-Sage")
    
    print(f"\n🤖 {ia1.nom} VS 🤖 {ia2.nom}")
    ascii_art.afficher_vs(classe_ia1, classe_ia2)
    
    # Créer les IA
    ai_player1 = AIPlayer(ia1, difficulte='normal')
    ai_player2 = AIPlayer(ia2, difficulte='normal')
    
    print(f"\n📊 {ia1.nom}:")
    ia1.afficher_stats()
    
    print(f"\n📊 {ia2.nom}:")
    ia2.afficher_stats()
    
    input("\n⏎ Appuyez sur Entrée pour lancer le combat automatique...")
    
    # Boucle de combat
    tour = 1
    
    while ia1.est_vivant and ia2.est_vivant:
        # Tour IA1
        print("\n" + "="*70)
        print(f"⚔️  TOUR {tour} - {ia1.nom} attaque!")
        print("="*70)
        
        ia1.debut_tour(ia2)
        
        if not ia2.est_vivant:
            break
        
        skills_dispo_ia1 = [s for s in ia1.skills if ia1.peut_utiliser_skill(s)]
        skill_ia1 = ai_player1.choisir_skill(skills_dispo_ia1, ia2)
        print(f"\n🤖 {ia1.nom} utilise: {skill_ia1.get('icone', '⚔️')} {skill_ia1['nom']}")
        ia1.utiliser_skill(skill_ia1, ia2)
        
        ia1.fin_tour()
        
        if not ia2.est_vivant:
            break
        
        input("\n⏎ Appuyez sur Entrée pour continuer...")
        
        # Tour IA2
        print("\n" + "="*70)
        print(f"⚔️  TOUR {tour+1} - {ia2.nom} attaque!")
        print("="*70)
        
        ia2.debut_tour(ia1)
        
        if not ia1.est_vivant:
            break
        
        skills_dispo_ia2 = [s for s in ia2.skills if ia2.peut_utiliser_skill(s)]
        skill_ia2 = ai_player2.choisir_skill(skills_dispo_ia2, ia1)
        print(f"\n🤖 {ia2.nom} utilise: {skill_ia2.get('icone', '⚔️')} {skill_ia2['nom']}")
        ia2.utiliser_skill(skill_ia2, ia1)
        
        ia2.fin_tour()
        
        if not ia1.est_vivant:
            break
        
        input("\n⏎ Appuyez sur Entrée pour continuer...")
        
        tour += 2
    
    # Fin du combat
    if ia1.est_vivant:
        vainqueur = ia1
        perdant = ia2
    else:
        vainqueur = ia2
        perdant = ia1
    
    print("\n" + "="*70)
    ascii_art.afficher_victoire()
    print(f"🏆 {vainqueur.nom} remporte la victoire!")
    print("="*70)
    
    print(f"\n📊 STATISTIQUES FINALES:")
    print(f"\n🏆 {vainqueur.nom}:")
    vainqueur.afficher_stats()
    print(f"   💥 Dégâts infligés: {vainqueur.degats_infliges_total}")
    print(f"   ⚡ Coups critiques: {vainqueur.coups_critiques}")
    
    print(f"\n💀 {perdant.nom}:")
    perdant.afficher_stats()
    print(f"   💥 Dégâts infligés: {perdant.degats_infliges_total}")
    print(f"   ⚡ Coups critiques: {perdant.coups_critiques}")
    
    # Niveau up du vainqueur
    vainqueur.gagner_niveau()
    
    # Sauvegarde
    save_manager = SaveManager()
    save_manager.sauvegarder_partie({
        'mode': 'Auto',
        'vainqueur': vainqueur.nom,
        'perdant': perdant.nom,
        'tours': tour,
        'stats_vainqueur': {
            'hp': vainqueur.hp_actuel,
            'niveau': vainqueur.niveau,
            'degats_infliges': vainqueur.degats_infliges_total,
            'coups_critiques': vainqueur.coups_critiques
        }
    })
    
    input("\n⏎ Appuyez sur Entrée pour retourner au menu...")


def lancer_combat_pve(nom_joueur: str, classe_joueur: str):
    """Lance un combat PvE avec les paramètres donnés"""
def lancer_combat_pve(nom_joueur: str, classe_joueur: str):
    """Lance un combat PvE avec les paramètres donnés"""
    from src.utils import ascii_art
    
    # Créer les personnages
    if classe_joueur == 'sage':
        joueur = Sage(nom_joueur)
        ia = Magicien("IA")
        classe_ia = 'magicien'
    else:
        joueur = Magicien(nom_joueur)
        ia = Sage("IA")
        classe_ia = 'sage'
    
    # Créer l'IA
    ai_player = AIPlayer(ia, difficulte='normal')
    
    print("\n" + "="*70)
    print("🎭 LES COMBATTANTS ENTRENT EN SCÈNE!")
    print("="*70)
    
    ascii_art.afficher_vs(classe_joueur, classe_ia)
    
    print(f"\n👤 JOUEUR:")
    joueur.afficher_stats()
    
    print(f"\n🤖 ORDINATEUR:")
    ia.afficher_stats()
    
    input("\n⏎ Appuyez sur Entrée pour commencer le combat...")
    
    # Boucle de combat
    tour = 1
    
    while joueur.est_vivant and ia.est_vivant:
        # Tour du joueur
        print("\n" + "="*70)
        print(f"⚔️  TOUR {tour} - {joueur.nom} attaque!")
        print("="*70)
        
        joueur.debut_tour(ia)
        
        if not ia.est_vivant:
            break
        
        skill_joueur = InputHandler.choisir_skill(joueur, ia)
        joueur.utiliser_skill(skill_joueur, ia)
        
        joueur.fin_tour()
        
        if not ia.est_vivant:
            break
        
        input("\n⏎ Appuyez sur Entrée pour continuer...")
        
        # Tour de l'IA
        print("\n" + "="*70)
        print(f"⚔️  TOUR {tour+1} - {ia.nom} attaque!")
        print("="*70)
        
        ia.debut_tour(joueur)
        
        if not joueur.est_vivant:
            break
        
        # L'IA choisit parmi ses skills disponibles
        skills_ia_disponibles = [s for s in ia.skills if ia.peut_utiliser_skill(s)]
        skill_ia = ai_player.choisir_skill(skills_ia_disponibles, joueur)
        print(f"\n🤖 L'IA choisit: {skill_ia.get('icone', '⚔️')} {skill_ia['nom']}")
        ia.utiliser_skill(skill_ia, joueur)
        
        ia.fin_tour()
        
        if not joueur.est_vivant:
            break
        
        input("\n⏎ Appuyez sur Entrée pour continuer...")
        
        tour += 2
    
    # Fin du combat
    if joueur.est_vivant:
        vainqueur = joueur
        perdant = ia
    else:
        vainqueur = ia
        perdant = joueur
    
    InputHandler.afficher_message_victoire(vainqueur, perdant)
    
    # Niveau up du vainqueur
    vainqueur.gagner_niveau()
    
    # Sauvegarde
    save_manager = SaveManager()
    save_manager.sauvegarder_partie({
        'vainqueur': vainqueur.nom,
        'perdant': perdant.nom,
        'tours': tour,
        'stats_vainqueur': {
            'hp': vainqueur.hp_actuel,
            'niveau': vainqueur.niveau,
            'degats_infliges': vainqueur.degats_infliges_total,
            'coups_critiques': vainqueur.coups_critiques
        }
    })


if __name__ == "__main__":
    try:
        combat_pve()
    except KeyboardInterrupt:
        print("\n\n⚠️  Combat interrompu par le joueur.")
        sys.exit(0)
