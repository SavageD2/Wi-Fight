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
    
    def choose_skill(self, available_skills: List[Dict], opponent) -> Dict:
        """
        Choisit une compétence à utiliser en fonction de la situation
        
        Args:
            available_skills: Liste des compétences que le personnage peut utiliser
            opponent: Personnage adversaire
            
        Returns:
            Compétence choisie
        """
        hp_percent = self.personnage.current_hp / self.personnage.hp_max
        current_mp = self.personnage.current_mp
        opponent_hp_percent = opponent.current_hp / opponent.hp_max
        
        # 1ère priorité : Soigner si les PV sont bas
        if hp_percent < 0.3:
            heal_skills = [s for s in available_skills if s['type'] == 'heal' and s.get('cout_mp', 0) <= current_mp]
            if heal_skills:
                return random.choice(heal_skills)
        
        # 2nd priorité: Utilise l'attaque ultime si l'adversaire est faible
        if opponent_hp_percent < 0.4 and current_mp > 140:
            ultimate_skills = [s for s in available_skills if s['type'] == 'attaque_ultime' and s.get('cout_mp', 0) <= current_mp]
            if ultimate_skills:
                return random.choice(ultimate_skills)
        
        # 3ème priorité : Buff si pas déjà actif
        if random.random() < 0.2:  # 20% chance de buff
            buff_skills = [s for s in available_skills if s['type'] == 'buff' and s.get('cout_mp', 0) <= current_mp]
            if buff_skills:
                return random.choice(buff_skills)
        
        # 4ème priorité : Debuff pour affaiblir l'adversaire
        if random.random() < 0.15 and opponent_hp_percent > 0.5:
            debuff_skills = [s for s in available_skills if s['type'] == 'debuff' and s.get('cout_mp', 0) <= current_mp]
            if debuff_skills:
                return random.choice(debuff_skills)
        
        # 5ème priorité : Évasion si les PV sont critiques
        if hp_percent < 0.2 and random.random() < 0.3:
            evasion_skills = [s for s in available_skills if s['type'] == 'evasion' and s.get('cout_mp', 0) <= current_mp]
            if evasion_skills:
                return random.choice(evasion_skills)
        
        # 6ème priorité : Attaque moyenne ou légère
        if self.strategie_agressive or current_mp > 100:
            # Préfère les attaques moyennes
            attack_skills = [s for s in available_skills if s['type'] in ['attaque_moyenne', 'attaque_legere'] and s.get('cout_mp', 0) <= current_mp]
        else:
            # Préfère les attaques légères pour économiser du MP
            attack_skills = [s for s in available_skills if s['type'] == 'attaque_legere' and s.get('cout_mp', 0) <= current_mp]
        
        if attack_skills:
            # Choisir en fonction de la difficulté
            if self.difficulte == "difficile":
                # IA difficile choisit la meilleure compétence
                return max(attack_skills, key=lambda s: s.get('degats_base', 0))
            elif self.difficulte == "facile":
                # IA facile choisit au hasard
                return random.choice(attack_skills)
            else:
                # IA normale : 70% meilleure compétence, 30% aléatoire
                if random.random() < 0.7:
                    return max(attack_skills, key=lambda s: s.get('degats_base', 0))
                else:
                    return random.choice(attack_skills)
        
        # Par défaut : première compétence disponible (attaque de base)
        usable_skills = [s for s in available_skills if s.get('cout_mp', 0) <= current_mp]
        if usable_skills:
            return usable_skills[0]
        elif available_skills:
            # Si aucune compétence n'est utilisable avec le MP actuel, retourner la moins chère
            return min(available_skills, key=lambda s: s.get('cout_mp', 0))
        else:
            # Si aucune compétence n'est disponible, retourner None (ne devrait jamais arriver)
            return None
    
    def ajuster_strategie(self, situation: str):
        """
        Ajuste la stratégie de l'IA en fonction de la situation
        
        Args:
            Situation: "gagnante" ou "perdante"
        """
        if situation == "perdante":
            self.strategie_agressive = False  # Devenir plus défensif
        elif situation == "gagnante":
            self.strategie_agressive = True   # Devenir plus agressif
# Geez que c'est long en vrai XD