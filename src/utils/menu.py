"""
Module menu - Gestion des menus principaux du jeu
"""

from typing import Optional, Tuple
from src.models.sage import Sage
from src.models.magicien import Magicien
from src.utils import ascii_art


class Menu:
    """Gestionnaire du menu du jeu"""
    
    @staticmethod
    def display_title():
        """Affiche le titre du jeu"""
        ascii_art.display_logo()
    
    @staticmethod
    def main_menu() -> str:
        """Affiche le menu principal"""
        print("\n" + "="*70)
        print("🎯 MENU PRINCIPAL")
        print("="*70)
        print("\n1. 🎮 Choisir mon personnage et jouer")
        print("2. 📖 Voir les détails du personnage")
        print("3. 🎲 Modes de combat avancés")
        print("4. 🚪 Quitter")
        print("\n" + "="*70)
        
        while True:
            choice = input("\nVotre choix (1-4) : ").strip()
            if choice in ['1', '2', '3', '4']:
                return choice
            print("❌ Choix invalide !")
    
    @staticmethod
    def choose_character() -> str:
        """Affiche le menu de sélection du personnage"""
        print("\n" + "="*70)
        print("🎭 SÉLECTION DU PERSONNAGE")
        print("="*70)
        
        print("\n1. 🧙 Sage")
        ascii_art.display_character_skin('sage', mini=True)
        print("   • Maître des arts mystiques")
        print("   • Récupère +10 MP à chaque utilisation de compétence")
        
        print("\n2. 🔮 Magicien")
        ascii_art.display_character_skin('magicien', mini=True)
        print("   • Invocateur de familiers élémentaires")
        print("   • Récupère +10 MP lors de l'invocation d'un familier")
        
        print("\n" + "="*70)
        
        while True:
            choice = input("\nVotre choix (1-2) : ").strip()
            if choice == '1':
                return 'sage'
            elif choice == '2':
                return 'magicien'
            print("❌ Choix invalide !")
    
    @staticmethod
    def ask_player_name(player_class: str) -> str:
        """Demande le nom du joueur après le choix de la classe"""
        icon = "🧙" if player_class == 'sage' else "🔮"
        print(f"\n✨ Vous avez choisi : {icon} {player_class.title()}")
        
        while True:
            name = input(f"\n📝 Quel est votre nom, {player_class.title()} ? ").strip()
            if name:
                return name
            print("❌ Le nom ne peut pas être vide !")
    
    @staticmethod
    def show_character_details(player_class: str):
        """Affiche les détails complets du personnage"""
        if player_class == 'sage':
            character = Sage()
            icon = "🧙"
        else:
            character = Magicien()
            icon = "🔮"
        
        print("\n" + "="*70)
        print(f"📖 DETAILS - {icon} {player_class.upper()}")
        print("="*70)
        
        # Stats de base
        print(f"\n📊 STATS DE BASE :")
        print(f"   ❤️  HP : {character.hp_max}")
        print(f"   💙 MP : {character.mp_max}")
        print(f"   ⚔️  ATQ : {character.attack}")
        print(f"   🛡️  DEF : {character.defense}")
        
        # Passif
        print(f"\n✨ CAPACITÉ PASSIVE :")
        if player_class == 'sage':
            print(f"   🔮 Récupération mystique")
            print(f"   • +10 MP à chaque utilisation de compétence")
        else:
            print(f"   🐾 Maître des familiers")
            print(f"   • +10 MP lors de l'invocation d'un familier")
            print(f"   • Invocations automatiques avec certaines compétences")
        
        # Skills
        print(f"\n⚔️  COMPÉTENCES DISPONIBLES :")
        print("="*70)
        
        for i, skill in enumerate(character.skills, 1):
            skill_icon = skill.get('icone', '⚔️')
            name = skill['nom']
            skill_type = skill['type'].replace('_', ' ').title()
            mp_cost = skill.get('cout_mp', skill.get('mp_cost', 0))
            cooldown = skill.get('cooldown', 0)
            desc = skill['description']
            
            print(f"\n{'─'*70}")
            print(f"{i}. {skill_icon} {name} [{skill_type}]")
            print(f"   💙 Coût : {mp_cost} MP")
            if cooldown > 0:
                print(f"   ⏱️  Cooldown: {cooldown} tours")
            print(f"   📝 {desc}")
            
            # Détails des effets
            if 'degats' in skill:
                print(f"   💥 Dégâts : {skill['degats']}")
            
            if 'heal' in skill:
                print(f"   💚 Soin : {skill['heal']} HP")
            
            if 'effets' in skill:
                for effect in skill['effets']:
                    if effect['type'] == 'buff':
                        print(f"   🔺 Buff: +{effect['valeur']} {effect['stat']} ({effect['duree']} tours)")
                    elif effect['type'] == 'debuff':
                        print(f"   🔻 Debuff: {effect['valeur']} {effect['stat']} ({effect['duree']} tours)")
            
            if 'familier' in skill:
                fam = skill['familier']
                print(f"   🐾 Invocations : {fam['nom']} ({fam['element']}) - {fam['degats']} dégâts/tour ({fam['duree']} tours)")
            
            if 'zone' in skill:
                zone = skill['zone']
                print(f"   🌊 Zone: {zone['degats']} dégâts/tour pendant {zone['duree']} tours")
        
        print("\n" + "="*70)
        input("\n⏎ Appuyez sur Entrée pour revenir au menu...")
    
    @staticmethod
    def show_all_details():
        """Affiche les détails de tous les personnages"""
        Menu.show_character_details('sage')
        Menu.show_character_details('magicien')
    
    @staticmethod
    def battle_modes_menu() -> str:
        """Affiche le sous-menu des modes de combat"""
        print("\n" + "="*70)
        print("🎲 MODES DE COMBAT")
        print("="*70)
        print("\n1. 👤 vs 🤖 Joueur contre IA (PvE) - Par défaut")
        print("2. 🤖 vs 🤖 IA contre IA (Auto)")
        print("3. 👤 vs 👤 Joueur contre Joueur (PvP)")
        print("4. 🔙 Retour au menu principal")
        print("\n" + "="*70)
        
        while True:
            choice = input("\nVotre choix (1-4) : ").strip()
            if choice in ['1', '2', '3', '4']:
                return choice
            print("❌ Choix invalide !")
    
    @staticmethod
    def confirm_pve_battle(player_name: str, player_class: str) -> bool:
        """Confirme le début d'une bataille PvE"""
        icon = "🧙" if player_class == 'sage' else "🔮"
        ai_class = "Magicien" if player_class == 'sage' else "Sage"
        ai_icon = "🔮" if player_class == 'sage' else "🧙"
        
        print("\n" + "="*70)
        print("⚔️  BATAILLE PvE")
        print("="*70)
        print(f"\n👤 Joueur : {player_name} ({icon} {player_class.title()})")
        print(f"🤖 Adversaire : IA ({ai_icon} {ai_class})")
        print("\n" + "="*70)
        
        choice = input("\n🎮 Démarrer la bataille ? (o/n) : ").strip().lower()
        return choice == 'o'