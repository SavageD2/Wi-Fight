#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module de gestion des sauvegardes
"""

import json
import os
from datetime import datetime
from typing import Dict, List


class SaveManager:
    """Gestionnaire de sauvegardes des parties"""
    
    def __init__(self, save_dir="saves"):
        """
        Initialise le gestionnaire de sauvegardes
        
        Args:
            save_dir: Répertoire où stocker les sauvegardes
        """
        self.save_dir = save_dir
        self._ensure_save_dir()
    
    def _ensure_save_dir(self):
        """Crée le répertoire de sauvegarde s'il n'existe pas"""
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
    
    def save_game(self, game_data: Dict) -> str:
        """
        Saves a completed game
        
        Args:
            game_data: Dictionary containing game data
            
        Returns:
            Path to save file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"combat_{timestamp}.json"
        filepath = os.path.join(self.save_dir, filename)
        
        # Add metadata
        game_data['metadata'] = {
            'date': datetime.now().isoformat(),
            'timestamp': timestamp,
            'version': '2.0.0'
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(game_data, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    def charger_partie(self, filename: str) -> Dict:
        """
        Charge une partie sauvegardée
        
        Args:
            filename: Nom du fichier de sauvegarde
            
        Returns:
            Les données de la partie
        """
        filepath = os.path.join(self.save_dir, filename)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def lister_sauvegardes(self) -> List[Dict]:
        """
        Liste toutes les sauvegardes disponibles
        
        Returns:
            Liste de dictionnaires avec les infos des sauvegardes
        """
        sauvegardes = []
        
        if not os.path.exists(self.save_dir):
            return sauvegardes
        
        for filename in os.listdir(self.save_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.save_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        sauvegardes.append({
                            'filename': filename,
                            'date': data.get('metadata', {}).get('date', 'Inconnue'),
                            'vainqueur': data.get('vainqueur', {}).get('nom', 'Inconnu'),
                            'mode': data.get('mode', 'Inconnu'),
                            'duree_tours': data.get('nombre_tours', 0)
                        })
                except Exception:
                    continue
        
        # Trier par date décroissante
        sauvegardes.sort(key=lambda x: x['date'], reverse=True)
        return sauvegardes
    
    def afficher_historique(self):
        """Affiche l'historique des parties"""
        sauvegardes = self.lister_sauvegardes()
        
        if not sauvegardes:
            print("\n📂 Aucune partie sauvegardée.\n")
            return
        
        print("\n" + "="*80)
        print("📂 HISTORIQUE DES PARTIES")
        print("="*80)
        
        for i, save in enumerate(sauvegardes, 1):
            print(f"\n{i}. {save['filename']}")
            print(f"   📅 Date: {save['date'][:19]}")
            print(f"   🎮 Mode: {save['mode']}")
            print(f"   👑 Vainqueur: {save['vainqueur']}")
            print(f"   ⏱️  Durée: {save['duree_tours']} tours")
        
        print("\n" + "="*80 + "\n")
    
    def afficher_replay(self, filename: str):
        """
        Affiche le replay d'une partie
        
        Args:
            filename: Nom du fichier de sauvegarde
        """
        try:
            data = self.charger_partie(filename)
            
            print("\n" + "="*80)
            print("🎬 REPLAY DE LA PARTIE")
            print("="*80)
            
            print(f"\n📅 Date: {data.get('metadata', {}).get('date', 'Inconnue')}")
            print(f"🎮 Mode: {data.get('mode', 'Inconnu')}")
            print(f"\n⚔️  {data.get('joueur1', {}).get('nom', 'Joueur 1')} VS {data.get('joueur2', {}).get('nom', 'Joueur 2')}")
            
            print(f"\n📊 STATISTIQUES FINALES:")
            print("="*80)
            
            # Joueur 1
            j1 = data.get('joueur1_final', {})
            print(f"\n{data.get('joueur1', {}).get('nom', 'Joueur 1')}:")
            print(f"   ❤️  HP: {j1.get('hp', 0)}/{j1.get('hp_max', 0)}")
            print(f"   💙 MP: {j1.get('mp', 0)}/{j1.get('mp_max', 0)}")
            print(f"   ✨ Dégâts infligés: {j1.get('degats_infliges', 0)}")
            print(f"   🎯 Coups critiques: {j1.get('coups_critiques', 0)}")
            
            # Joueur 2
            j2 = data.get('joueur2_final', {})
            print(f"\n{data.get('joueur2', {}).get('nom', 'Joueur 2')}:")
            print(f"   ❤️  HP: {j2.get('hp', 0)}/{j2.get('hp_max', 0)}")
            print(f"   💙 MP: {j2.get('mp', 0)}/{j2.get('mp_max', 0)}")
            print(f"   ✨ Dégâts infligés: {j2.get('degats_infliges', 0)}")
            print(f"   🎯 Coups critiques: {j2.get('coups_critiques', 0)}")
            
            print(f"\n👑 VAINQUEUR: {data.get('vainqueur', {}).get('nom', 'Inconnu')}")
            print(f"⏱️  Nombre de tours: {data.get('nombre_tours', 0)}")
            
            print("\n" + "="*80 + "\n")
            
        except FileNotFoundError:
            print(f"❌ Fichier de sauvegarde '{filename}' introuvable.")
        except Exception as e:
            print(f"❌ Erreur lors du chargement du replay: {e}")
    
    def supprimer_sauvegarde(self, filename: str) -> bool:
        """
        Supprime une sauvegarde
        
        Args:
            filename: Nom du fichier à supprimer
            
        Returns:
            True si suppression réussie, False sinon
        """
        filepath = os.path.join(self.save_dir, filename)
        
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                return True
            return False
        except Exception:
            return False
