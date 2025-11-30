"""
Module définissant la classe Sage
"""

import json
import os
from src.models.personnage_v2 import Personnage, Familier


class Sage(Personnage):
    """Classe représentant le Sage - Maître des arts mystiques"""
    
    def __init__(self, nom_custom: str = None):
        # Chargement de la configuration
        config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'sage.json')
        
        with open(config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Utiliser le nom personnalisé ou celui du config
        nom_final = nom_custom if nom_custom else data['nom']
        
        # Initialisation via la classe mère
        super().__init__(nom_final, data['skills'], data['stats'])
        
        self.classe = data['classe']
        self.description = data['description']
        self.passif = data['passif']
    
    def utiliser_skill(self, skill: dict, adversaire: 'Personnage'):
        """Override pour ajouter la récupération de mana passive"""
        # Utiliser le skill normalement
        super().utiliser_skill(skill, adversaire)
        
        # Passif: Récupération de mana +10 par skill utilisé
        self.mp_actuel = self.mp_actuel + self.passif['valeur']
        print(f"   🔮 Récupération mana passive: +{self.passif['valeur']} MP")
