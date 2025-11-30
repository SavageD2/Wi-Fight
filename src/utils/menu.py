#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module menu - Gestion des menus principaux du jeu
"""

from typing import Optional, Tuple
from src.models.sage import Sage
from src.models.magicien import Magicien
from src.utils import ascii_art


class Menu:
    """Gestionnaire des menus du jeu"""
    
    @staticmethod
    def afficher_titre():
        """Affiche le titre du jeu"""
        ascii_art.afficher_logo()
    
    @staticmethod
    def menu_principal() -> str:
        """Affiche le menu principal et retourne le choix"""
        print("\n" + "="*70)
        print("🎯 MENU PRINCIPAL")
        print("="*70)
        print("\n1. 🎮 Choisir mon personnage et jouer")
        print("2. 📖 Voir les détails des personnages")
        print("3. 🎲 Modes de combat avancés")
        print("4. 🚪 Quitter")
        print("\n" + "="*70)
        
        while True:
            choix = input("\nVotre choix (1-4): ").strip()
            if choix in ['1', '2', '3', '4']:
                return choix
            print("❌ Choix invalide!")
    
    @staticmethod
    def choisir_personnage() -> str:
        """Affiche le menu de sélection de personnage"""
        print("\n" + "="*70)
        print("🎭 SÉLECTION DU PERSONNAGE")
        print("="*70)
        
        print("\n1. 🧙 Sage")
        ascii_art.afficher_skin_personnage('sage', mini=True)
        print("   • Maître des arts mystiques")
        print("   • Récupère +10 MP à chaque compétence utilisée")
        
        print("\n2. 🔮 Magicien")
        ascii_art.afficher_skin_personnage('magicien', mini=True)
        print("   • Invocateur de familiers élémentaires")
        print("   • Récupère +10 MP lors de l'invocation d'un familier")
        
        print("\n" + "="*70)
        
        while True:
            choix = input("\nVotre choix (1-2): ").strip()
            if choix == '1':
                return 'sage'
            elif choix == '2':
                return 'magicien'
            print("❌ Choix invalide!")
    
    @staticmethod
    def demander_nom_joueur(classe: str) -> str:
        """Demande le nom du joueur après choix de classe"""
        icone = "🧙" if classe == 'sage' else "🔮"
        print(f"\n✨ Vous avez choisi: {icone} {classe.title()}")
        
        while True:
            nom = input(f"\n📝 Quel est votre nom, {classe.title()}? ").strip()
            if nom:
                return nom
            print("❌ Le nom ne peut pas être vide!")
    
    @staticmethod
    def afficher_details_personnage(classe: str):
        """Affiche les détails complets d'un personnage"""
        if classe == 'sage':
            perso = Sage()
            icone = "🧙"
        else:
            perso = Magicien()
            icone = "🔮"
        
        print("\n" + "="*70)
        print(f"📖 DÉTAILS - {icone} {classe.upper()}")
        print("="*70)
        
        # Stats de base
        print(f"\n📊 STATISTIQUES DE BASE:")
        print(f"   ❤️  HP: {perso.hp_max}")
        print(f"   💙 MP: {perso.mp_max}")
        print(f"   ⚔️  ATK: {perso.attack}")
        print(f"   🛡️  DEF: {perso.defense}")
        
        # Passif
        print(f"\n✨ CAPACITÉ PASSIVE:")
        if classe == 'sage':
            print(f"   🔮 Récupération Mystique")
            print(f"   • +10 MP à chaque fois qu'une compétence est utilisée")
        else:
            print(f"   🐾 Maître des Familiers")
            print(f"   • +10 MP lors de l'invocation d'un familier")
            print(f"   • Invocations automatiques avec certaines compétences")
        
        # Compétences
        print(f"\n⚔️  COMPÉTENCES DISPONIBLES:")
        print("="*70)
        
        for i, skill in enumerate(perso.skills, 1):
            icone_skill = skill.get('icone', '⚔️')
            nom = skill['nom']
            type_skill = skill['type'].replace('_', ' ').title()
            mp_cost = skill['mp_cost']
            cooldown = skill.get('cooldown', 0)
            desc = skill['description']
            
            print(f"\n{i}. {icone_skill} {nom} [{type_skill}]")
            print(f"   💙 Coût: {mp_cost} MP")
            if cooldown > 0:
                print(f"   ⏱️  Cooldown: {cooldown} tours")
            print(f"   📝 {desc}")
            
            # Détails des effets
            if 'degats' in skill:
                print(f"   💥 Dégâts: {skill['degats']}")
            
            if 'heal' in skill:
                print(f"   💚 Soin: {skill['heal']} HP")
            
            if 'effets' in skill:
                for effet in skill['effets']:
                    if effet['type'] == 'buff':
                        print(f"   🔺 Buff: +{effet['valeur']} {effet['stat']} ({effet['duree']} tours)")
                    elif effet['type'] == 'debuff':
                        print(f"   🔻 Debuff: {effet['valeur']} {effet['stat']} ({effet['duree']} tours)")
            
            if 'familier' in skill:
                fam = skill['familier']
                print(f"   🐾 Invoque: {fam['nom']} ({fam['element']}) - {fam['degats']} dmg/tour ({fam['duree']} tours)")
            
            if 'zone' in skill:
                zone = skill['zone']
                print(f"   🌊 Zone: {zone['degats']} dmg/tour pendant {zone['duree']} tours")
        
        print("\n" + "="*70)
        input("\n⏎ Appuyez sur Entrée pour revenir au menu...")
    
    @staticmethod
    def afficher_details_tous():
        """Affiche les détails de tous les personnages"""
        Menu.afficher_details_personnage('sage')
        Menu.afficher_details_personnage('magicien')
    
    @staticmethod
    def menu_modes_combat() -> str:
        """Affiche le sous-menu des modes de combat"""
        print("\n" + "="*70)
        print("🎲 MODES DE COMBAT")
        print("="*70)
        print("\n1. 👤 vs 🤖 Joueur vs IA (PvE) - Par défaut")
        print("2. 🤖 vs 🤖 IA vs IA (Auto)")
        print("3. 👤 vs 👤 Joueur vs Joueur (PvP)")
        print("4. 🔙 Retour au menu principal")
        print("\n" + "="*70)
        
        while True:
            choix = input("\nVotre choix (1-4): ").strip()
            if choix in ['1', '2', '3', '4']:
                return choix
            print("❌ Choix invalide!")
    
    @staticmethod
    def confirmer_combat_pve(nom_joueur: str, classe_joueur: str) -> bool:
        """Confirme le début du combat PvE"""
        icone = "🧙" if classe_joueur == 'sage' else "🔮"
        classe_ia = "Magicien" if classe_joueur == 'sage' else "Sage"
        icone_ia = "🔮" if classe_joueur == 'sage' else "🧙"
        
        print("\n" + "="*70)
        print("⚔️  COMBAT PvE")
        print("="*70)
        print(f"\n👤 Joueur: {nom_joueur} ({icone} {classe_joueur.title()})")
        print(f"🤖 Adversaire: IA ({icone_ia} {classe_ia})")
        print("\n" + "="*70)
        
        choix = input("\n🎮 Commencer le combat? (o/n): ").strip().lower()
        return choix == 'o'
