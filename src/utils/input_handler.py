#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module de gestion des inputs du joueur
"""

from typing import Dict, List
from src.models.personnage_v2 import Personnage


class InputHandler:
    """Gestionnaire des entrées du joueur"""
    
    @staticmethod
    def choisir_skill(personnage: Personnage, adversaire: Personnage) -> Dict:
        """
        Affiche le menu de sélection des skills et retourne le choix du joueur
        
        Args:
            personnage: Le personnage du joueur
            adversaire: Le personnage adverse
            
        Returns:
            Le skill choisi
        """
        print(f"\n{'='*70}")
        print(f"🎮 C'EST VOTRE TOUR - {personnage.nom}")
        print(f"{'='*70}")
        
        # Afficher les stats actuelles
        print(f"\n📊 VOS STATS:")
        personnage.afficher_stats()
        
        print(f"\n📊 ADVERSAIRE:")
        adversaire.afficher_stats()
        
        # Lister les skills disponibles
        print(f"\n⚔️  COMPÉTENCES DISPONIBLES:")
        print(f"{'='*70}")
        
        skills_disponibles = []
        for i, skill in enumerate(personnage.skills, 1):
            skill_id = skill.get('id', skill['nom'])
            skill_nom = skill['nom']
            skill_type = skill['type']
            mp_cost = skill.get('mp_cost', 0)
            icone = skill.get('icone', '⚔️')
            
            # Vérifier si le skill peut être utilisé
            peut_utiliser = personnage.peut_utiliser_skill(skill)
            
            # Obtenir les cooldowns
            cooldowns = personnage._Personnage__cooldowns
            cooldown_restant = cooldowns.get(skill_id, 0)
            
            # Formatage de l'affichage
            statut = ""
            if not peut_utiliser:
                if personnage.mp_actuel < mp_cost:
                    statut = "❌ MP insuffisant"
                elif cooldown_restant > 0:
                    statut = f"⏳ Cooldown: {cooldown_restant} tours"
            else:
                statut = "✅ Disponible"
            
            # Type de skill en français
            type_skill = {
                'attaque_legere': 'Attaque légère',
                'attaque_moyenne': 'Attaque moyenne',
                'attaque_lourde': 'Attaque lourde',
                'heal': 'Soin',
                'buff': 'Buff',
                'debuff': 'Debuff',
                'evasion': 'Évasion',
                'invocation': 'Invocation',
                'zone': 'Zone d\'effet'
            }.get(skill_type, skill_type)
            
            print(f"{i}. {icone} {skill_nom} [{type_skill}]")
            print(f"   💙 Coût MP: {mp_cost} | {statut}")
            
            skills_disponibles.append(skill)
        
        print(f"\n{'='*70}")
        
        # Demander le choix
        while True:
            try:
                choix = input(f"\nChoisissez une compétence (1-{len(skills_disponibles)}): ").strip()
                index = int(choix) - 1
                
                if 0 <= index < len(skills_disponibles):
                    skill_choisi = skills_disponibles[index]
                    
                    # Vérifier si le skill peut être utilisé
                    if personnage.peut_utiliser_skill(skill_choisi):
                        return skill_choisi
                    else:
                        skill_id = skill_choisi.get('id', skill_choisi['nom'])
                        cooldowns = personnage._Personnage__cooldowns
                        cooldown_restant = cooldowns.get(skill_id, 0)
                        
                        if personnage.mp_actuel < skill_choisi.get('mp_cost', 0):
                            print(f"❌ MP insuffisant! ({personnage.mp_actuel}/{skill_choisi.get('mp_cost', 0)})")
                        elif cooldown_restant > 0:
                            print(f"❌ Compétence en cooldown! ({cooldown_restant} tours restants)")
                else:
                    print(f"❌ Choix invalide. Choisissez entre 1 et {len(skills_disponibles)}.")
            except ValueError:
                print("❌ Veuillez entrer un nombre valide.")
            except KeyboardInterrupt:
                print("\n\n⚠️  Abandon du combat...")
                exit(0)
    
    @staticmethod
    def choisir_personnage() -> str:
        """
        Menu de sélection du personnage
        
        Returns:
            Le nom de la classe choisie ('Sage' ou 'Magicien')
        """
        print("\n" + "="*70)
        print("🎭 SÉLECTION DU PERSONNAGE")
        print("="*70)
        
        print("\n1. 🧙 Sage")
        print("   • Maître des arts mystiques")
        print("   • Récupère +10 MP à chaque compétence utilisée")
        print("   • Spécialités: Buffs puissants, surcharge critique")
        
        print("\n2. 🔮 Magicien")
        print("   • Invocateur de familiers élémentaires")
        print("   • Récupère +10 MP lors de l'invocation d'un familier")
        print("   • Spécialités: Familiers automatiques, zones de poison")
        
        print("\n" + "="*70)
        
        while True:
            choix = input("\nVotre choix (1-2): ").strip()
            
            if choix == "1":
                return "Sage"
            elif choix == "2":
                return "Magicien"
            else:
                print("❌ Choix invalide. Veuillez choisir 1 ou 2.")
    
    @staticmethod
    def confirmer_action(message: str) -> bool:
        """
        Demande une confirmation au joueur
        
        Args:
            message: Le message de confirmation
            
        Returns:
            True si confirmé, False sinon
        """
        while True:
            reponse = input(f"{message} (o/n): ").strip().lower()
            if reponse in ['o', 'oui', 'y', 'yes']:
                return True
            elif reponse in ['n', 'non', 'no']:
                return False
            else:
                print("❌ Réponse invalide. Répondez par 'o' ou 'n'.")
    
    @staticmethod
    def afficher_message_victoire(vainqueur: Personnage, perdant: Personnage):
        """Affiche le message de victoire"""
        print("\n" + "="*70)
        print("🏆" + " "*28 + "FIN DU COMBAT" + " "*28 + "🏆")
        print("="*70)
        
        if vainqueur:
            print(f"\n👑 {vainqueur.nom} remporte la victoire!")
            stats = vainqueur.get_stats_finales()
            print(f"   ❤️  HP restants: {stats['hp']}/{stats['hp_max']}")
            print(f"   💙 MP restants: {stats['mp']}/{stats['mp_max']}")
            print(f"   ⚔️  Dégâts infligés: {stats['degats_infliges']}")
            print(f"   💥 Coups critiques: {stats['coups_critiques']}")
            print(f"   ⭐ Niveau: {stats['niveau']}")
        
        if perdant:
            print(f"\n💀 {perdant.nom} est vaincu...")
            stats = perdant.get_stats_finales()
            print(f"   ⚔️  Dégâts infligés: {stats['degats_infliges']}")
            print(f"   💥 Coups critiques: {stats['coups_critiques']}")
        
        print("\n" + "="*70 + "\n")
