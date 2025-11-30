"""
WiZ-Fight - Combat Magique Épique
Point d'entrée principal du jeu
"""

import sys
from combat_v2 import start_game


if __name__ == "__main__":
    try:
        start_game()
    except KeyboardInterrupt:
        print("\n\n⚠️  Bataille interrompue par le joueur.")
        sys.exit(0)
