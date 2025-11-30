#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module de gestion des modes de jeu
"""

from enum import Enum
from typing import Tuple


class GameMode(Enum):
    """Énumération des modes de jeu disponibles"""
    AUTO = "auto"           # IA vs IA
    PVE = "pve"            # Joueur vs IA
    PVP = "pvp"            # Joueur vs Joueur


class GameManager:
    """Gestionnaire principal du jeu"""
    
    def __init__(self):
        self.mode = None
        self.joueur1 = None
        self.joueur2 = None
        self.joueur1_humain = False
        self.joueur2_humain = False
    
    def choisir_mode(self) -> GameMode:
        """
        Affiche le menu de sélection du mode de jeu
        
        Returns:
            Le mode de jeu choisi
        """
        print("\n" + "="*60)
        print("🎮 SÉLECTION DU MODE DE JEU")
        print("="*60)
        print("\n1. 🤖 Mode Auto (IA vs IA)")
        print("   Regardez deux IA s'affronter automatiquement")
        print("\n2. ⚔️  Mode PvE (Joueur vs IA)")
        print("   Affrontez l'ordinateur")
        print("\n3. 👥 Mode PvP (Joueur vs Joueur)")
        print("   Combat local entre deux joueurs")
        print("\n" + "="*60)
        
        while True:
            choix = input("\nVotre choix (1-3): ").strip()
            
            if choix == "1":
                self.mode = GameMode.AUTO
                self.joueur1_humain = False
                self.joueur2_humain = False
                return GameMode.AUTO
            elif choix == "2":
                self.mode = GameMode.PVE
                self.joueur1_humain = True
                self.joueur2_humain = False
                return GameMode.PVE
            elif choix == "3":
                self.mode = GameMode.PVP
                self.joueur1_humain = True
                self.joueur2_humain = True
                return GameMode.PVP
            else:
                print("❌ Choix invalide. Veuillez choisir 1, 2 ou 3.")
    
    def choisir_personnage(self, numero_joueur: int, personnages_disponibles: list) -> str:
        """
        Permet à un joueur de choisir son personnage
        
        Args:
            numero_joueur: Numéro du joueur (1 ou 2)
            personnages_disponibles: Liste des personnages disponibles
            
        Returns:
            Le nom du personnage choisi
        """
        is_humain = (numero_joueur == 1 and self.joueur1_humain) or \
                   (numero_joueur == 2 and self.joueur2_humain)
        
        if not is_humain:
            # L'IA choisit aléatoirement
            import random
            return random.choice(personnages_disponibles)
        
        print(f"\n{'='*60}")
        print(f"👤 JOUEUR {numero_joueur} - Choix du personnage")
        print("="*60)
        
        for i, perso in enumerate(personnages_disponibles, 1):
            print(f"{i}. {perso}")
        
        while True:
            try:
                choix = input(f"\nChoisissez votre personnage (1-{len(personnages_disponibles)}): ").strip()
                index = int(choix) - 1
                
                if 0 <= index < len(personnages_disponibles):
                    return personnages_disponibles[index]
                else:
                    print(f"❌ Choix invalide. Veuillez choisir entre 1 et {len(personnages_disponibles)}.")
            except ValueError:
                print("❌ Veuillez entrer un nombre valide.")
    
    def afficher_recap_mode(self):
        """Affiche un récapitulatif du mode choisi"""
        print("\n" + "="*60)
        
        if self.mode == GameMode.AUTO:
            print("🤖 Mode: AUTO - IA vs IA")
        elif self.mode == GameMode.PVE:
            print("⚔️  Mode: PvE - Joueur vs IA")
        elif self.mode == GameMode.PVP:
            print("👥 Mode: PvP - Joueur vs Joueur")
        
        print("="*60 + "\n")
