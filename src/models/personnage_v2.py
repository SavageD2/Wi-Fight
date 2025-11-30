#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module définissant la classe abstraite Personnage v2.0
Avec système de stats étendues, buffs/debuffs, familiers, zones
"""

from abc import ABC, abstractmethod
import random
from typing import Dict, List, Optional


class Effet:
    """Classe représentant un effet temporaire (buff/debuff)"""
    
    def __init__(self, type_effet: str, stat: str, valeur: float, duree: int, nom: str = ""):
        self.type = type_effet  # 'buff' ou 'debuff'
        self.stat = stat
        self.valeur = valeur
        self.duree = duree
        self.nom = nom
    
    def __repr__(self):
        signe = "+" if self.valeur >= 0 else ""
        return f"{self.nom} ({signe}{self.valeur} {self.stat}, {self.duree} tours)"


class Familier:
    """Classe représentant un familier invoqué"""
    
    def __init__(self, nom: str, element: str, degats: int, duree: int):
        self.nom = nom
        self.element = element
        self.degats = degats
        self.duree = duree
        self.tours_restants = duree
    
    def attaquer(self) -> int:
        """Retourne les dégâts du familier"""
        if self.tours_restants > 0:
            return self.degats
        return 0
    
    def __repr__(self):
        return f"{self.nom} ({self.element}, {self.tours_restants} tours restants)"


class ZoneEffet:
    """Classe représentant une zone d'effet au sol"""
    
    def __init__(self, nom: str, degats: int, intervalle: int, duree_totale: int, effet_debuff: Optional[Dict] = None):
        self.nom = nom
        self.degats = degats
        self.intervalle = intervalle
        self.duree_totale = duree_totale
        self.tours_ecoules = 0
        self.effet_debuff = effet_debuff
    
    def appliquer_degats(self) -> int:
        """Applique les dégâts si l'intervalle est atteint"""
        self.tours_ecoules += 1
        if self.tours_ecoules % self.intervalle == 0:
            return self.degats
        return 0
    
    def est_active(self) -> bool:
        """Vérifie si la zone est encore active"""
        return self.tours_ecoules < self.duree_totale
    
    def __repr__(self):
        return f"{self.nom} ({self.tours_ecoules}/{self.duree_totale} tours)"


class Personnage(ABC):
    """Classe abstraite représentant un personnage de combat v2.0"""
    
    # Propriété de classe publique pour gérer le tour
    tour = 'joueur1'
    
    def __init__(self, nom: str, skills: List[Dict], stats: Dict):
        """
        Initialise un personnage
        
        Args:
            nom: Le nom du personnage
            skills: Liste des skills possibles
            stats: Dictionnaire des stats de base
        """
        self.__nom = nom
        self.__skills = skills
        
        # Stats de base
        self.__hp_max = stats.get('hp_max', 500)
        self.__mp_max = stats.get('mp_max', 450)
        self.__attack_base = stats.get('attack', 250)
        self.__defense_base = stats.get('defense', 300)
        self.__endurance_max = stats.get('endurance', 1500)
        self.__niveau = stats.get('niveau', 1)
        
        # Stats actuelles
        self.__hp_actuel = self.__hp_max
        self.__mp_actuel = self.__mp_max
        self.__endurance_actuel = self.__endurance_max
        
        # Stats temporaires (avec buffs/debuffs)
        self.__attack = self.__attack_base
        self.__defense = self.__defense_base
        self.__reduction_degats = 0  # Pourcentage de réduction
        self.__bonus_crit = 0
        
        # Effets actifs
        self.__buffs: List[Effet] = []
        self.__debuffs: List[Effet] = []
        
        # Cooldowns des skills
        self.__cooldowns: Dict[str, int] = {}
        
        # Familiers et zones
        self.__familiers: List[Familier] = []
        self.__zones_effet: List[ZoneEffet] = []
        
        # Statistiques de combat
        self.__degats_infliges_total = 0
        self.__degats_recus_total = 0
        self.__coups_critiques = 0
        self.__skills_utilises: Dict[str, int] = {}
        
        # Mécaniques spéciales
        self.__skills_surchargees = False
    
    # === GETTERS ET SETTERS ===
    
    @property
    def nom(self) -> str:
        return self.__nom
    
    @property
    def hp_max(self) -> int:
        return self.__hp_max
    
    @property
    def hp_actuel(self) -> int:
        return self.__hp_actuel
    
    @hp_actuel.setter
    def hp_actuel(self, valeur: int):
        self.__hp_actuel = max(0, min(valeur, self.__hp_max))
    
    @property
    def mp_max(self) -> int:
        return self.__mp_max
    
    @property
    def mp_actuel(self) -> int:
        return self.__mp_actuel
    
    @mp_actuel.setter
    def mp_actuel(self, valeur: int):
        self.__mp_actuel = max(0, min(valeur, self.__mp_max))
    
    @property
    def attack(self) -> int:
        return self.__attack
    
    @property
    def defense(self) -> int:
        return self.__defense
    
    @property
    def niveau(self) -> int:
        return self.__niveau
    
    @property
    def skills(self) -> List[Dict]:
        return self.__skills
    
    @property
    def buffs(self) -> List[Effet]:
        return self.__buffs
    
    @property
    def debuffs(self) -> List[Effet]:
        return self.__debuffs
    
    @property
    def familiers(self) -> List[Familier]:
        return self.__familiers
    
    @property
    def degats_infliges_total(self) -> int:
        return self.__degats_infliges_total
    
    @property
    def coups_critiques(self) -> int:
        return self.__coups_critiques
    
    # === MÉTHODES DE GESTION DES STATS ===
    
    def recalculer_stats(self):
        """Recalcule les stats en tenant compte des buffs/debuffs"""
        self.__attack = self.__attack_base
        self.__defense = self.__defense_base
        self.__reduction_degats = 0
        self.__bonus_crit = 0
        
        # Appliquer les buffs
        for buff in self.__buffs:
            if buff.stat == 'attack':
                self.__attack += buff.valeur
            elif buff.stat == 'defense':
                self.__defense += buff.valeur
            elif buff.stat == 'reduction_degats':
                self.__reduction_degats += buff.valeur
            elif buff.stat == 'bonus_crit':
                self.__bonus_crit += buff.valeur
        
        # Appliquer les debuffs
        for debuff in self.__debuffs:
            if debuff.stat == 'attack':
                self.__attack += debuff.valeur  # valeur négative
            elif debuff.stat == 'defense':
                self.__defense += debuff.valeur
            elif debuff.stat == 'reduction_degats':
                self.__reduction_degats += debuff.valeur
        
        # S'assurer que les stats ne deviennent pas négatives
        self.__attack = max(0, self.__attack)
        self.__defense = max(0, self.__defense)
    
    def ajouter_buff(self, buff: Effet):
        """Ajoute un buff au personnage"""
        self.__buffs.append(buff)
        self.recalculer_stats()
    
    def ajouter_debuff(self, debuff: Effet):
        """Ajoute un debuff au personnage"""
        self.__debuffs.append(debuff)
        self.recalculer_stats()
    
    def mettre_a_jour_effets(self):
        """Met à jour la durée des effets et les retire s'ils sont expirés"""
        # Buffs
        self.__buffs = [b for b in self.__buffs if b.duree > 0]
        for buff in self.__buffs:
            buff.duree -= 1
        
        # Debuffs
        self.__debuffs = [d for d in self.__debuffs if d.duree > 0]
        for debuff in self.__debuffs:
            debuff.duree -= 1
        
        self.recalculer_stats()
    
    # === MÉTHODES DE GESTION DES FAMILIERS ET ZONES ===
    
    def ajouter_familier(self, familier: Familier):
        """Ajoute un familier invoqué"""
        self.__familiers.append(familier)
        print(f"   🐾 {familier.nom} invoqué! ({familier.element})")
    
    def mettre_a_jour_familiers(self):
        """Met à jour les familiers et retire ceux expirés"""
        for familier in self.__familiers:
            familier.tours_restants -= 1
        
        self.__familiers = [f for f in self.__familiers if f.tours_restants > 0]
    
    def attaque_familiers(self, adversaire: 'Personnage') -> int:
        """Les familiers attaquent automatiquement"""
        degats_total = 0
        for familier in self.__familiers:
            degats = familier.attaquer()
            if degats > 0:
                degats_total += degats
                print(f"   🐾 {familier.nom} attaque! (+{degats} dégâts)")
        
        if degats_total > 0:
            adversaire.recevoir_degats(degats_total, ignore_defense=False)
        
        return degats_total
    
    def ajouter_zone(self, zone: ZoneEffet):
        """Ajoute une zone d'effet"""
        self.__zones_effet.append(zone)
        print(f"   🌊 {zone.nom} créée!")
    
    def mettre_a_jour_zones(self, adversaire: 'Personnage'):
        """Met à jour les zones et applique leurs effets"""
        for zone in self.__zones_effet[:]:
            degats = zone.appliquer_degats()
            if degats > 0:
                adversaire.recevoir_degats(degats, ignore_defense=True)
                print(f"   🌊 {zone.nom} inflige {degats} dégâts!")
            
            # Appliquer le debuff si présent
            if zone.effet_debuff and zone.tours_ecoules == 1:
                debuff = Effet(
                    'debuff',
                    zone.effet_debuff['stat'],
                    zone.effet_debuff['valeur'],
                    zone.duree_totale,
                    zone.nom
                )
                adversaire.ajouter_debuff(debuff)
        
        self.__zones_effet = [z for z in self.__zones_effet if z.est_active()]
    
    # === MÉTHODES DE COMBAT ===
    
    def peut_utiliser_skill(self, skill: Dict) -> bool:
        """Vérifie si un skill peut être utilisé"""
        # Vérifier le MP
        if self.__mp_actuel < skill.get('mp_cost', 0):
            return False
        
        # Vérifier le cooldown
        skill_id = skill.get('id', skill['nom'])
        if skill_id in self.__cooldowns and self.__cooldowns[skill_id] > 0:
            return False
        
        return True
    
    def utiliser_skill(self, skill: Dict, adversaire: 'Personnage'):
        """Utilise un skill sur l'adversaire"""
        skill_id = skill.get('id', skill['nom'])
        skill_nom = skill['nom']
        skill_type = skill['type']
        
        # Consommer le MP
        mp_cost = skill.get('mp_cost', 0)
        self.__mp_actuel -= mp_cost
        
        # Appliquer le cooldown
        if 'cooldown' in skill and skill['cooldown'] > 0:
            self.__cooldowns[skill_id] = skill['cooldown']
        
        # Statistiques
        if skill_nom not in self.__skills_utilises:
            self.__skills_utilises[skill_nom] = 0
        self.__skills_utilises[skill_nom] += 1
        
        # Afficher l'utilisation
        icone = skill.get('icone', '⚔️')
        print(f"\n🎯 {self.nom} utilise: {icone} {skill_nom}")
        print(f"   💙 MP: {self.__mp_actuel}/{self.__mp_max} (-{mp_cost})")
        
        # Appliquer les effets selon le type
        if skill_type in ['attaque_legere', 'attaque_moyenne', 'attaque_lourde']:
            self._appliquer_attaque(skill, adversaire)
        elif skill_type == 'heal':
            self._appliquer_heal(skill)
        elif skill_type == 'buff':
            self._appliquer_buff(skill)
        elif skill_type == 'debuff':
            self._appliquer_debuff(skill, adversaire)
        elif skill_type == 'evasion':
            self._appliquer_evasion(skill)
        elif skill_type == 'invocation':
            self._appliquer_invocation(skill)
        elif skill_type == 'zone':
            self._appliquer_zone(skill, adversaire)
    
    def _appliquer_attaque(self, skill: Dict, adversaire: 'Personnage'):
        """Applique une attaque"""
        degats_base = skill.get('degats', 0)
        
        # Calcul des dégâts
        degats = degats_base
        
        # Coup critique?
        chance_crit = 0.15 + (self.__bonus_crit / 100)
        if self.__skills_surchargees:
            chance_crit += 0.30
        
        est_critique = random.random() < chance_crit
        if est_critique:
            degats = int(degats * 1.5)
            self.__coups_critiques += 1
            print(f"   💥 COUP CRITIQUE!")
        
        # Appliquer les dégâts
        adversaire.recevoir_degats(degats)
        self.__degats_infliges_total += degats
        
        # Effets additionnels du skill
        if 'effets' in skill:
            for effet in skill['effets']:
                if effet['type'] == 'debuff':
                    debuff = Effet(
                        'debuff',
                        effet['stat'],
                        effet['valeur'],
                        effet['duree'],
                        skill['nom']
                    )
                    adversaire.ajouter_debuff(debuff)
                    print(f"   🔻 {adversaire.nom} subit: {debuff}")
    
    def _appliquer_heal(self, skill: Dict):
        """Applique un soin"""
        heal = skill.get('heal', 0)
        hp_avant = self.__hp_actuel
        self.hp_actuel = self.__hp_actuel + heal
        heal_effectif = self.__hp_actuel - hp_avant
        print(f"   💚 {self.nom} récupère {heal_effectif} HP!")
    
    def _appliquer_buff(self, skill: Dict):
        """Applique un buff"""
        if 'effets' in skill:
            for effet in skill['effets']:
                if effet['type'] == 'buff':
                    buff = Effet(
                        'buff',
                        effet['stat'],
                        effet['valeur'],
                        effet['duree'],
                        skill['nom']
                    )
                    self.ajouter_buff(buff)
                    print(f"   🔺 {self.nom} gagne: {buff}")
        
        # Effets spéciaux
        if 'special' in skill:
            if skill['special'] == 'surcharge':
                self.__skills_surchargees = True
                print(f"   ⚡ Compétences surchargées!")
    
    def _appliquer_debuff(self, skill: Dict, adversaire: 'Personnage'):
        """Applique un debuff"""
        # Dégâts du skill debuff
        if 'degats' in skill:
            degats = skill['degats']
            adversaire.recevoir_degats(degats)
            self.__degats_infliges_total += degats
        
        # Appliquer les debuffs
        if 'effets' in skill:
            for effet in skill['effets']:
                if effet['type'] == 'debuff':
                    debuff = Effet(
                        'debuff',
                        effet['stat'],
                        effet['valeur'],
                        effet['duree'],
                        skill['nom']
                    )
                    adversaire.ajouter_debuff(debuff)
                    print(f"   🔻 {adversaire.nom} subit: {debuff}")
    
    def _appliquer_evasion(self, skill: Dict):
        """Applique une évasion d'urgence"""
        # Ajouter un buff d'évasion temporaire
        buff = Effet('buff', 'evasion', 100, 1, skill['nom'])
        self.ajouter_buff(buff)
        print(f"   💨 {self.nom} esquive!")
    
    def _appliquer_invocation(self, skill: Dict):
        """Applique une invocation de familier"""
        if 'familier' in skill:
            fam_data = skill['familier']
            familier = Familier(
                fam_data['nom'],
                fam_data['element'],
                fam_data['degats'],
                fam_data['duree']
            )
            self.ajouter_familier(familier)
    
    def _appliquer_zone(self, skill: Dict, adversaire: 'Personnage'):
        """Applique une zone d'effet"""
        if 'zone' in skill:
            zone_data = skill['zone']
            zone = ZoneEffet(
                skill['nom'],
                zone_data['degats'],
                zone_data['intervalle'],
                zone_data['duree'],
                zone_data.get('debuff')
            )
            self.ajouter_zone(zone)
            adversaire  # La zone affectera l'adversaire
    
    def recevoir_degats(self, degats: int, ignore_defense: bool = False):
        """Reçoit des dégâts"""
        if not ignore_defense:
            # Réduction par défense (formule ajustée: DEF réduit 2% des dégâts par 100 points)
            reduction_percent = min(50, self.__defense / 100 * 2)  # Max 50% de réduction
            degats_reduits = degats * (1 - reduction_percent / 100)
            
            # Réduction additionnelle par buffs
            if self.__reduction_degats > 0:
                degats_reduits *= (1 - self.__reduction_degats / 100)
            
            degats_finaux = max(1, int(degats_reduits))  # Minimum 1 dégât
        else:
            degats_finaux = degats
        
        self.__hp_actuel -= degats_finaux
        self.__degats_recus_total += degats_finaux
        
        print(f"   💔 {self.nom} subit {degats_finaux} dégâts! (HP: {self.__hp_actuel}/{self.__hp_max})")
    
    def mettre_a_jour_cooldowns(self):
        """Réduit les cooldowns de 1"""
        for skill_id in list(self.__cooldowns.keys()):
            self.__cooldowns[skill_id] -= 1
            if self.__cooldowns[skill_id] <= 0:
                del self.__cooldowns[skill_id]
    
    def debut_tour(self, adversaire: 'Personnage'):
        """Actions au début du tour"""
        # Attaque des familiers
        self.attaque_familiers(adversaire)
        
        # Effets des zones
        self.mettre_a_jour_zones(adversaire)
        
        # Mise à jour des effets
        self.mettre_a_jour_effets()
        self.mettre_a_jour_familiers()
        self.mettre_a_jour_cooldowns()
    
    def fin_tour(self):
        """Actions à la fin du tour"""
        pass
    
    def est_vivant(self) -> bool:
        """Vérifie si le personnage est vivant"""
        return self.__hp_actuel > 0
    
    def gagner_niveau(self):
        """Augmente le niveau et les stats"""
        self.__niveau += 1
        bonus_stats = 5
        
        self.__hp_max += bonus_stats
        self.__mp_max += bonus_stats
        self.__attack_base += bonus_stats
        self.__defense_base += bonus_stats
        
        # Guérison complète
        self.__hp_actuel = self.__hp_max
        self.__mp_actuel = self.__mp_max
        
        print(f"\n🎉 {self.nom} monte au niveau {self.__niveau}!")
        print(f"   +{bonus_stats} à toutes les stats!")
    
    def afficher_stats(self):
        """Affiche les stats du personnage"""
        hp_percent = (self.__hp_actuel / self.__hp_max) * 100
        mp_percent = (self.__mp_actuel / self.__mp_max) * 100
        
        # Couleur HP
        if hp_percent > 60:
            couleur_hp = "\033[92m"
        elif hp_percent > 30:
            couleur_hp = "\033[93m"
        else:
            couleur_hp = "\033[91m"
        
        # Couleur MP
        if mp_percent > 50:
            couleur_mp = "\033[94m"
        else:
            couleur_mp = "\033[95m"
        
        reset = "\033[0m"
        
        print(f"   {couleur_hp}❤️  HP: {self.__hp_actuel}/{self.__hp_max}{reset}")
        print(f"   {couleur_mp}💙 MP: {self.__mp_actuel}/{self.__mp_max}{reset}")
        print(f"   ⚔️  ATK: {self.__attack} | 🛡️  DEF: {self.__defense}")
        print(f"   ⭐ Niveau: {self.__niveau}")
        
        # Afficher buffs/debuffs actifs
        if self.__buffs:
            print(f"   🔺 Buffs: {', '.join([b.nom for b in self.__buffs])}")
        if self.__debuffs:
            print(f"   🔻 Debuffs: {', '.join([d.nom for d in self.__debuffs])}")
        if self.__familiers:
            print(f"   🐾 Familiers: {', '.join([f.nom for f in self.__familiers])}")
        if self.__zones_effet:
            print(f"   🌊 Zones: {', '.join([z.nom for z in self.__zones_effet])}")
    
    def get_stats_finales(self) -> Dict:
        """Retourne les stats finales pour sauvegarde"""
        return {
            'hp': self.__hp_actuel,
            'hp_max': self.__hp_max,
            'mp': self.__mp_actuel,
            'mp_max': self.__mp_max,
            'attack': self.__attack,
            'defense': self.__defense,
            'niveau': self.__niveau,
            'degats_infliges': self.__degats_infliges_total,
            'degats_recus': self.__degats_recus_total,
            'coups_critiques': self.__coups_critiques,
            'skills_utilises': self.__skills_utilises
        }
