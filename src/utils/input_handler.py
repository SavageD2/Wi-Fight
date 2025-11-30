"""
Module de gestion des entrées du joueur
"""

from typing import Dict, List
from src.models.personnage_v2 import Personnage


class InputHandler:
    """Gestion des entrées du joueur"""
    
    @staticmethod
    def choose_skill(character: Personnage, opponent: Personnage) -> Dict:
        """
        Affiche le menu de sélection des compétences et retourne le choix du joueur
        
        Args:
            character: Personnage du joueur
            opponent: Personnage de l'adversaire
            
        Returns:
            Compétence choisie
        """
        print(f"\n{'='*70}")
        print(f"🎮 C'EST VOTRE TOUR - {character.nom}")
        print(f"{'='*70}")
        
        # Affiche les stats actuelles
        print(f"\n📊 VOS STATS :")
        character.display_stats()
        
        print(f"\n📊 ADVERSAIRE :")
        opponent.display_stats()
        
        # Liste des compétences disponibles
        print(f"\n⚔️  COMPÉTENCES DISPONIBLES :")
        print(f"{'='*70}")
        
        available_skills = []
        for i, skill in enumerate(character.skills, 1):
            skill_id = skill.get('id', skill['nom'])
            skill_name = skill['nom']
            skill_type = skill['type']
            mp_cost = skill.get('cout_mp', 0)
            icon = skill.get('icone', '⚔️')
            
            # Véruifie si la compétence peut être utilisée
            can_use = character.can_use_skill(skill)
            
            # Obtient le cooldown restant
            cooldowns = character._Personnage__cooldowns
            remaining_cooldown = cooldowns.get(skill_id, 0)
            
            # Affichage formaté
            status = ""
            if not can_use:
                if character.current_mp < mp_cost:
                    status = "❌ MP insuffisants"
                elif remaining_cooldown > 0:
                    status = f"⏳ Cooldown : {remaining_cooldown} tours"
            else:
                status = "✅ Disponible"
            
            # Type de compétence
            type_mapping = {
                'attaque_legere': 'Attaque légère',
                'attaque_moyenne': 'Attaque moyenne',
                'attaque_lourde': 'Attaque lourde',
                'heal': 'Soin',
                'buff': 'Buff',
                'debuff': 'Debuff',
                'evasion': 'Evasion',
                'invocation': 'Invocation',
                'zone': 'Zone AoE'
            }.get(skill_type, skill_type)
            
            # Amélioration de l'affichage
            print(f"\n┌─ {i}. {icon} {skill_name}")
            print(f"│  📋 Type: {type_mapping}")
            print(f"│  💙 Coût: {mp_cost} MP")
            if cooldown := skill.get('cooldown', 0):
                cooldown_status = f"{remaining_cooldown} tours" if remaining_cooldown > 0 else "Prêt"
                print(f"│  ⏱️  Cooldown: {cooldown_status}")
            print(f"└─ {status}")
            
            available_skills.append(skill)
        
        print(f"\n{'='*70}")
        
        # Demande du choix
        while True:
            try:
                choice = input(f"\nChoisissez une compétence (1-{len(available_skills)}): ").strip()
                index = int(choice) - 1
                
                if 0 <= index < len(available_skills):
                    chosen_skill = available_skills[index]
                    
                    # Vérifie si la compétence peut être utilisée
                    if character.can_use_skill(chosen_skill):
                        return chosen_skill
                    else:
                        skill_id = chosen_skill.get('id', chosen_skill['nom'])
                        cooldowns = character._Personnage__cooldowns
                        remaining_cooldown = cooldowns.get(skill_id, 0)
                        
                        if character.current_mp < chosen_skill.get('cout_mp', 0):
                            print(f"❌ MP insuffisants ! ({character.current_mp}/{chosen_skill.get('cout_mp', 0)})")
                        elif remaining_cooldown > 0:
                            print(f"❌ Compétence en cooldown ! ({remaining_cooldown} tours restants)")
                else:
                    print(f"❌ Choix invalide. Choisissez entre 1 et {len(available_skills)}.")
            except ValueError:
                print("❌ Veuillez entrer un nombre valide.")
            except KeyboardInterrupt:
                print("\n\n⚠️  Abandon de la bataille...")
                exit(0)
    
    @staticmethod
    def display_victory_message(winner: Personnage, loser: Personnage):
        """Affiche le message de victoire"""
        print("\n" + "="*70)
        print("🏆" + " "*28 + "FIN DE LA BATAILLE" + " "*28 + "🏆")
        print("="*70)
        
        if winner:
            print(f"\n👑 {winner.nom} a gagné !")
            stats = winner.get_final_stats()
            print(f"   ❤️  HP restant : {stats['hp']}/{stats['hp_max']}")
            print(f"   💙 MP restant : {stats['mp']}/{stats['mp_max']}")
            print(f"   ⚔️  Dégâts infligés : {stats['degats_infliges']}")
            print(f"   💥 Coups critiques : {stats['coups_critiques']}")
            print(f"   ⭐ Niveau : {stats['niveau']}")
        
        if loser:
            print(f"\n💀 {loser.nom} est vaincu...")
            stats = loser.get_final_stats()
            print(f"   ⚔️  Dégâts infligés : {stats['degats_infliges']}")
            print(f"   💥 Coups critiques : {stats['coups_critiques']}")
        
        print("\n" + "="*70 + "\n")
