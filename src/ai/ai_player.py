#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module de l'intelligence artificielle
"""

import random
from typing import Dict, List


class AIPlayer:
    """Intelligence artificielle pour contrôler un personnage"""
    
    def __init__(self, personnage, difficulte="normal"):
        """
        Initialise l'IA
        
        Args:
            personnage: Le personnage contrôlé par l'IA
            difficulte: Niveau de difficulté ('facile', 'normal', 'difficile')
        """
        self.personnage = personnage
        self.difficulte = difficulte
        self.strategie_agressive = random.random() > 0.5  # 50% chance d'être agressif
    
    def choisir_skill(self, skills_disponibles: List[Dict], adversaire) -> Dict:
        """
        Choisit intelligemment le skill à utiliser
        
        Args:
            skills_disponibles: Liste des skills que le personnage peut utiliser
            adversaire: Le personnage adverse
            
        Returns:
            Le skill choisi
        """
        hp_percent = self.personnage.hp_actuel / self.personnage.hp_max
        mp_actuel = self.personnage.mp_actuel
        adversaire_hp_percent = adversaire.hp_actuel / adversaire.hp_max
        
        # Priorité 1: Heal si HP bas
        if hp_percent < 0.3:
            skills_heal = [s for s in skills_disponibles if s['type'] == 'heal' and s['mp_cost'] <= mp_actuel]
            if skills_heal:
                return random.choice(skills_heal)
        
        # Priorité 2: Ultime si adversaire affaibli et MP suffisant
        if adversaire_hp_percent < 0.4 and mp_actuel > 140:
            skills_ultime = [s for s in skills_disponibles if s['type'] == 'attaque_ultime' and s['mp_cost'] <= mp_actuel]
            if skills_ultime:
                return random.choice(skills_ultime)
        
        # Priorité 3: Buff si pas déjà actif (à implémenter avec système de buffs)
        if random.random() < 0.2:  # 20% de chance de buff
            skills_buff = [s for s in skills_disponibles if s['type'] == 'buff' and s['mp_cost'] <= mp_actuel]
            if skills_buff:
                return random.choice(skills_buff)
        
        # Priorité 4: Debuff pour affaiblir l'adversaire
        if random.random() < 0.15 and adversaire_hp_percent > 0.5:
            skills_debuff = [s for s in skills_disponibles if s['type'] == 'debuff' and s['mp_cost'] <= mp_actuel]
            if skills_debuff:
                return random.choice(skills_debuff)
        
        # Priorité 5: Évasion si HP critique
        if hp_percent < 0.2 and random.random() < 0.3:
            skills_evasion = [s for s in skills_disponibles if s['type'] == 'evasion' and s['mp_cost'] <= mp_actuel]
            if skills_evasion:
                return random.choice(skills_evasion)
        
        # Priorité 6: Attaque moyenne ou légère
        if self.strategie_agressive or mp_actuel > 100:
            # Préfère les attaques moyennes
            skills_attaque = [s for s in skills_disponibles if s['type'] in ['attaque_moyenne', 'attaque_legere'] and s['mp_cost'] <= mp_actuel]
        else:
            # Préfère les attaques légères pour économiser MP
            skills_attaque = [s for s in skills_disponibles if s['type'] == 'attaque_legere' and s['mp_cost'] <= mp_actuel]
        
        if skills_attaque:
            # Choisir en fonction de la difficulté
            if self.difficulte == "difficile":
                # IA difficile choisit le meilleur skill
                return max(skills_attaque, key=lambda s: s.get('degats_base', 0))
            elif self.difficulte == "facile":
                # IA facile choisit aléatoirement
                return random.choice(skills_attaque)
            else:
                # IA normale: 70% meilleur skill, 30% aléatoire
                if random.random() < 0.7:
                    return max(skills_attaque, key=lambda s: s.get('degats_base', 0))
                else:
                    return random.choice(skills_attaque)
        
        # Par défaut: premier skill disponible (attaque de base)
        skills_utilisables = [s for s in skills_disponibles if s['mp_cost'] <= mp_actuel]
        return skills_utilisables[0] if skills_utilisables else skills_disponibles[0]
    
    def ajuster_strategie(self, situation: str):
        """
        Ajuste la stratégie de l'IA en fonction de la situation
        
        Args:
            situation: 'winning', 'losing', 'equal'
        """
        if situation == "losing":
            self.strategie_agressive = False  # Devenir plus défensif
        elif situation == "winning":
            self.strategie_agressive = True   # Devenir plus agressif
