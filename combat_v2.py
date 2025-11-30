"""
Combat Py-Fight/WiZ-Fight v2.0 - Mode PvE (Joueur vs IA) Choix du nom en cours...
"""

import sys
import os

# Force UTF-8 encoding pour Windows car il y a eu des couacs au lancement sorry XD
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

from src.models.sage import Sage
from src.models.magicien import Magicien
from src.ai.ai_player import AIPlayer
from src.utils.input_handler import InputHandler
from src.utils.menu import Menu
from src.game.save_manager import SaveManager


def start_game():
    """Joueur vs IA - Démarre le jeu et gère le menu principal"""
    from src.utils import ascii_art
    
    ascii_art.display_welcome_screen()
    
    Menu.display_title()
    
    while True:
        choice = Menu.main_menu()
        
        if choice == '1':  # Choisir un personnage et jouer directement
            player_class = Menu.choose_character()
            player_name = Menu.ask_player_name(player_class)
            
            # Confirmation et lancement direct
            if Menu.confirm_pve_battle(player_name, player_class):
                start_pve_battle(player_name, player_class)
                return
            else:
                print("\n❌ Combat annulé.")
                input("⏎ Appuyez sur Entrée pour continuer...")
        
        elif choice == '2':  # Voir les détails/infos des personnages
            Menu.show_all_details()
        
        elif choice == '3':  # Modes avancés
            mode = Menu.battle_modes_menu()
            
            if mode == '1':  # PvE
                player_class = Menu.choose_character()
                player_name = Menu.ask_player_name(player_class)
                if Menu.confirm_pve_battle(player_name, player_class):
                    start_pve_battle(player_name, player_class)
                    return
            elif mode == '2':  # Auto (AI vs AI)
                start_auto_battle()
                return
            elif mode == '3':  # PvP
                print("\n🚧 Mode PvP - En développement...")
                input("⏎ Appuyez sur Entrée pour continuer...")
            # mode == '4' retour au menu principal
        
        elif choice == '4':  # Quitter
            print("\n👋 À bientôt !")
            sys.exit(0)


def start_auto_battle():
    """Mode automatique (IA vs IA)"""
    import random
    from src.utils import ascii_art
    
    print("\n" + "="*70)
    print("🤖 MODE AUTO - IA vs IA")
    print("="*70)
    
    # Sélection aléatoire des classes
    classes = ['sage', 'magicien']
    ai1_class = random.choice(classes)
    ai2_class = random.choice([c for c in classes if c != ai1_class])  # Force different classes
    
    # Création des personnages
    if ai1_class == 'sage':
        ai1 = Sage("IA-Sage")
        ai2 = Magicien("IA-Magicien")
    else:
        ai1 = Magicien("IA-Magicien")
        ai2 = Sage("IA-Sage")
    
    print(f"\n🤖 {ai1.nom} VS 🤖 {ai2.nom}")
    ascii_art.display_vs(ai1_class, ai2_class)
    
    # Création des IA
    ai_player1 = AIPlayer(ai1, difficulte='normal') # Ce n'est pas Elden Ring mais bon...
    ai_player2 = AIPlayer(ai2, difficulte='normal')
    
    print(f"\n📊 {ai1.nom}:")
    ai1.display_stats()
    
    print(f"\n📊 {ai2.nom}:")
    ai2.display_stats()
    
    input("\n⏎ Appuyez sur Entrée pour commencer...")
    
    # Boucle de combat
    turn = 1
    
    while ai1.is_alive and ai2.is_alive:
        # Tour de l'IA 1
        print("\n" + "="*70)
        print(f"⚔️  TOUR {turn} - {ai1.nom} attaque !")
        print("="*70)
        
        ai1.start_turn(ai2)
        
        if not ai2.is_alive:
            break
        
        available_skills_ai1 = [s for s in ai1.skills if ai1.can_use_skill(s)]
        if not available_skills_ai1:
            print(f"\n⚠️  {ai1.nom} n'a plus de MP pour utiliser ses compétences!")
            ai1.end_turn()
            if not ai2.is_alive:
                break
            input("\n⏎ Appuyez sur Entrée pour continuer...")
            continue
        
        skill_ai1 = ai_player1.choose_skill(available_skills_ai1, ai2)
        if skill_ai1:
            print(f"\n🤖 {ai1.nom} utilise : {skill_ai1.get('icone', '⚔️')} {skill_ai1['nom']}")
            ai1.use_skill(skill_ai1, ai2)
        
        ai1.end_turn()
        
        if not ai2.is_alive:
            break
        
        input("\n⏎ Appuyez sur Entrée pour continuer...")
        
        # Tour de l'IA 2
        print("\n" + "="*70)
        print(f"⚔️  TOUR {turn+1} - {ai2.nom} attaque !")
        print("="*70)
        
        ai2.start_turn(ai1)
        
        if not ai1.is_alive:
            break
        
        available_skills_ai2 = [s for s in ai2.skills if ai2.can_use_skill(s)]
        if not available_skills_ai2:
            print(f"\n⚠️  {ai2.nom} n'a plus de MP pour utiliser ses compétences!")
            ai2.end_turn()
            if not ai1.is_alive:
                break
            input("\n⏎ Appuyez sur Entrée pour continuer...")
            turn += 2
            continue
        
        skill_ai2 = ai_player2.choose_skill(available_skills_ai2, ai1)
        if skill_ai2:
            print(f"\n🤖 {ai2.nom} utilise : {skill_ai2.get('icone', '⚔️')} {skill_ai2['nom']}")
            ai2.use_skill(skill_ai2, ai1)
        
        ai2.end_turn()
        
        if not ai1.is_alive:
            break
        
        input("\n⏎ Appuyez sur Entrée pour continuer...")
        
        turn += 2
    
    # Fin du combat
    if ai1.is_alive:
        winner = ai1
        loser = ai2
    else:
        winner = ai2
        loser = ai1
    
    print("\n" + "="*70)
    ascii_art.display_victory()
    print(f"🏆 {winner.nom} gagne !")
    print("="*70)
    
    print(f"\n📊 STATS FINALES:")
    print(f"\n🏆 {winner.nom}:")
    winner.display_stats()
    print(f"   💥 Dégâts infligés: {winner.total_damage_dealt}")
    print(f"   ⚡ Coups critiques: {winner.critical_hits}")
    
    print(f"\n💀 {loser.nom}:")
    loser.display_stats()
    print(f"   💥 Dégâts infligés: {loser.total_damage_dealt}")
    print(f"   ⚡ Coups critiques: {loser.critical_hits}")
    
    # Montée de niveau du vainqueur
    winner.gain_level()
    
    # Sauvegarde
    save_manager = SaveManager()
    save_manager.save_game({
        'mode': 'Auto',
        'vainqueur': winner.nom,
        'perdant': loser.nom,
        'tours': turn,
        'stats_vainqueur': {
            'hp': winner.current_hp,
            'niveau': winner.level,
            'degats_infliges': winner.total_damage_dealt,
            'coups_critiques': winner.critical_hits
        }
    })
    


def start_pve_battle(player_name: str, player_class: str):
    """Démarre une bataille PvE avec les paramètres donnés"""
    from src.utils import ascii_art
    
    # Création des personnages
    if player_class == 'sage':
        player = Sage(player_name)
        ai = Magicien("AI")
        ai_class = 'magicien'
    else:
        player = Magicien(player_name)
        ai = Sage("AI")
        ai_class = 'sage'
    
    # Créer l'IA
    ai_player = AIPlayer(ai, difficulte='normal')
    
    print("\n" + "="*70)
    print("🎭 LES COMBATTANTS ENTRENT EN SCÈNE !")
    print("="*70)
    
    ascii_art.display_vs(player_class, ai_class)
    
    print(f"\n👤 JOUEUR :")
    player.display_stats()
    
    print(f"\n🤖 ORDINATEUR :")
    ai.display_stats()
    
    input("\n⏎ Appuyez sur Entrée pour commencer la bataille...")
    
    # Boucle de combat
    turn = 1
    
    while player.is_alive and ai.is_alive:
        # Tour du joueur
        print("\n" + "="*70)
        print(f"⚔️  TOUR {turn} - {player.nom} attaque !")
        print("="*70)
        
        player.start_turn(ai)
        
        if not ai.is_alive:
            break
        
        player_skill = InputHandler.choose_skill(player, ai)
        player.use_skill(player_skill, ai)
        
        player.end_turn()
        
        if not ai.is_alive:
            break
        
        input("\n⏎ Appuyez sur Entrée pour continuer...")
        
        # Tour de l'IA
        print("\n" + "="*70)
        print(f"⚔️  TOUR {turn+1} - {ai.nom} attaque !")
        print("="*70)
        
        ai.start_turn(player)
        
        if not player.is_alive:
            break
        
        # L'IA choisit parmi les compétences disponibles
        available_ai_skills = [s for s in ai.skills if ai.can_use_skill(s)]
        if not available_ai_skills:
            print(f"\n⚠️  {ai.nom} n'a plus de PM pour utiliser ses compétences!")
            ai.end_turn()
            if not player.is_alive:
                break
            input("\n⏎ Appuyez sur Entrée pour continuer...")
            turn += 2
            continue
        
        ai_skill = ai_player.choose_skill(available_ai_skills, player)
        if ai_skill:
            print(f"\n🤖 L'IA choisit : {ai_skill.get('icone', '⚔️')} {ai_skill['nom']}")
            ai.use_skill(ai_skill, player)
        
        ai.end_turn()
        
        if not player.is_alive:
            break
        
        input("\n⏎ Appuyez sur Entrée pour continuer...")
        
        turn += 2
    
    # Fin du combat
    if player.is_alive:
        winner = player
        loser = ai
    else:
        winner = ai
        loser = player
    
    InputHandler.display_victory_message(winner, loser)
    
    # Montée de niveau du vainqueur
    winner.gain_level()
    
    # Sauvegarde
    save_manager = SaveManager()
    save_manager.save_game({
        'vainqueur': winner.nom,
        'perdant': loser.nom,
        'tours': turn,
        'stats_vainqueur': {
            'hp': winner.current_hp,
            'niveau': winner.level,
            'degats_infliges': winner.total_damage_dealt,
            'coups_critiques': winner.critical_hits
        }
    })


if __name__ == "__main__":
    try:
        start_game()
    except KeyboardInterrupt:
        print("\n\n⚠️  Bataille interrompue par le joueur.")
        sys.exit(0)
