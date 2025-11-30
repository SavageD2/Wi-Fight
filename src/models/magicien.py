"""
Module définissant la classe Magicien
"""

import json
import os
from src.models.personnage_v2 import Personnage, Familier


class Magicien(Personnage):
    """Classe représentant le Magicien - Invocateur de familiers"""
    
    def __init__(self, nom_custom: str = None):
        # Chargement de la configuration
        config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'magicien.json')
        
        with open(config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Utiliser le nom personnalisé ou celui du config
        nom_final = nom_custom if nom_custom else data['nom']
        
        # Initialisation via la classe mère
        super().__init__(nom_final, data['skills'], data['stats'])
        
        self.classe = data['classe']
        self.description = data['description']
        self.passif = data['passif']
    
    def _appliquer_invocation(self, skill: dict):
        """Override pour ajouter le choix de familier et récupération mana"""
        if 'familier_choice' in skill and skill['familier_choice']:
            # Choix entre les deux familiers
            print(f"\n   🐉 Choisissez un familier:")
            for i, fam in enumerate(skill['familiers'], 1):
                print(f"   {i}. {fam['nom']} ({fam['element']}) - {fam['degats']} dégâts/tour")
            
            # Pour l'instant, choix aléatoire (sera remplacé par input joueur)
            import random
            fam_data = random.choice(skill['familiers'])
        else:
            fam_data = skill.get('familier')
        
        if fam_data:
            familier = Familier(
                fam_data['nom'],
                fam_data['element'],
                fam_data['degats'],
                fam_data['duree']
            )
            self.ajouter_familier(familier)
            
            # Passif: Récupération de mana lors de l'invocation
            self.mp_actuel = self.mp_actuel + self.passif['valeur']
            print(f"   🔮 Récupération mana passive: +{self.passif['valeur']} MP")
    
    def _appliquer_attaque(self, skill: dict, adversaire: 'Personnage'):
        """Override pour gérer les auto-invocations"""
        # Attaque normale
        super()._appliquer_attaque(skill, adversaire)
        
        # Vérifier auto-invocation
        if 'auto_invocation' in skill:
            inv_data = skill['auto_invocation']
            familier = Familier(
                inv_data['nom'],
                inv_data['element'],
                inv_data['degats'],
                inv_data['duree']
            )
            self.ajouter_familier(familier)
            
            # Passif: Récupération de mana
            self.mp_actuel = self.mp_actuel + self.passif['valeur']
            print(f"   🔮 Récupération mana passive: +{self.passif['valeur']} MP")
    
    def _appliquer_buff(self, skill: dict):
        """Override pour gérer la récupération de MP du skill Psyche"""
        super()._appliquer_buff(skill)
        
        # Skill spécial Psyche qui récupère du MP
        if 'heal_mp' in skill:
            mp_avant = self.mp_actuel
            self.mp_actuel = self.mp_actuel + skill['heal_mp']
            mp_gagne = self.mp_actuel - mp_avant
            print(f"   💙 {self.nom} récupère {mp_gagne} MP!")
