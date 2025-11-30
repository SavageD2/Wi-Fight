"""
Module utilitaire pour l'affichage du jeu
"""

import json
import os
from src.models.personnage_v2 import Personnage


def charger_config():
    """Charge la configuration du jeu depuis le fichier JSON"""
    config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'game_config.json')
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # Configuration par défaut
        return {
            "game": {
                "title": "COMBAT ÉPIQUE",
                "subtitle": "Gandalf le Blanc VS Le Roi Sorcier d'Angmar",
                "version": "1.0.0"
            },
            "combat": {
                "chance_esquive": 0.20,
                "delai_tour": 0.5,
                "vie_initiale": 100
            },
            "affichage": {
                "largeur_separateur": 60,
                "couleurs": {
                    "vie_haute": "\033[92m",
                    "vie_moyenne": "\033[93m",
                    "vie_basse": "\033[91m",
                    "reset": "\033[0m"
                },
                "seuils_vie": {
                    "haute": 50,
                    "basse": 20
                }
            }
        }


def afficher_titre():
    """Affiche le titre du jeu"""
    config = charger_config()
    game_config = config['game']
    largeur = config['affichage']['largeur_separateur']
    
    title = game_config['title']
    subtitle = game_config['subtitle']
    
    print("\n" + "="*largeur)
    print(f"⚔️  {title.center(largeur-6)} ⚔️")
    print("="*largeur)
    print(f"🌟 {subtitle} 🌟")
    print("="*largeur + "\n")


def afficher_tour(numero_tour: int, attaquant: Personnage):
    """Affiche les informations du tour"""
    config = charger_config()
    largeur = config['affichage']['largeur_separateur']
    
    print(f"\n{'='*largeur}")
    print(f"⚔️  TOUR {numero_tour} - {attaquant.nom} attaque!")
    print(f"{'='*largeur}")


def afficher_introduction(joueur1: Personnage, joueur2: Personnage):
    """Affiche l'introduction du combat"""
    print(f"🎭 Les combattants entrent en scène!\n")
    print(f"   {joueur1.nom}")
    joueur1.afficher_stats()
    print(f"\n   {joueur2.nom}")
    joueur2.afficher_stats()
    print()


def afficher_victoire(vainqueur: Personnage, perdant: Personnage):
    """Affiche l'écran de victoire"""
    config = charger_config()
    largeur = config['affichage']['largeur_separateur']
    
    print(f"\n{'='*largeur}")
    print("🏆" + "FIN DU COMBAT".center(largeur-2) + "🏆")
    print(f"{'='*largeur}\n")
    
    print(f"👑 {vainqueur.nom} remporte la victoire!")
    print(f"   ✨ Expérience finale: {vainqueur.experience}")
    print(f"   ❤️  Vie restante: {vainqueur.vie_restante()}/100")
    print()
    print(f"💀 {perdant.nom} est vaincu...")
    print(f"   ✨ Expérience finale: {perdant.experience}")
    print(f"   ❤️  Vie restante: {perdant.vie_restante()}/100")
    print(f"\n{'='*largeur}\n")
