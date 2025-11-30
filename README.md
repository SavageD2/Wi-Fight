# 🎮 WiZ-FIGHT v2.0
**Combat Magique Épique** - Projet POO Python par Savage

---

## 📖 Description du projet

WiZ-Fight est un jeu de combat tour par tour mettant en scène deux mages légendaires inspirés de Black Desert Online. Le projet met en œuvre les concepts avancés de Programmation Orientée Objet en Python.

**Créé pour Jean Christophe** 🎓 - Merci de nous avoir appris la POO !

---

## 🧙 Les Personnages

### **Sage** - Maître des arcanes anciennes
**Passif:** Récupération de mana automatique +10 MP par skill utilisé

**Compétences:**
1. **Annihilation Radieuse** (attaque légère)
   - Dégâts: 20 | Coût: 40 MP | Cooldown: 3 tours

2. **Lance de Sauron** (debuff)
   - Dégâts: 25 | Debuff: -24 DEF (3 tours) | Coût: 60 MP | Cooldown: 2 tours

3. **Galvanisation** (buff)
   - Buff: +30 ATK, +20 DEF, +5% réduction dégâts (4 tours) | Coût: 70 MP | Cooldown: 3 tours

4. **Surcharge d'éclair** (buff critique)
   - Buff: +30% coups critiques + surcharge toutes compétences (3 tours) | Coût: 80 MP | Cooldown: 4 tours

5. **Dernier recours** (évasion)
   - Esquive totale | Coût: 50 MP | Cooldown: 20 tours

6. **Tempête de la faille** (attaque lourde)
   - Dégâts: 50 | Coût: 100 MP | Cooldown: 5 tours

---

### **Magicien** - Invocateur de familiers élémentaires
**Passif:** Récupération de mana automatique +10 MP lors de l'invocation d'un familier

**Compétences:**
1. **Psyche de la sphère d'Aad** (buff multiple)
   - Buff: +20 ATK, +15% réduction dégâts | Récupère: 80 MP | Coût: 0 MP | Cooldown: 4 tours

2. **Defense Techtonique** (protection)
   - Buff: +30% réduction dégâts (3 tours) | Coût: 60 MP | Cooldown: 3 tours

3. **Invocation Familier** (invocation)
   - Invoque Gardien Gorr (terre) ou Gardien Tett (foudre)
   - Attaque auto: 10 dégâts/tour pendant 6 tours | Coût: 80 MP | Cooldown: 5 tours

4. **Inondation toxique** (zone poison)
   - Zone: 15 dégâts/tour pendant 6 tours | Coût: 90 MP | Cooldown: 4 tours

5. **Dernier recours** (évasion)
   - Esquive totale | Coût: 50 MP | Cooldown: 20 tours

6. **Barrage d'éclair** (attaque légère + invocation)
   - Dégâts: 10 | Invoque auto Gardien Tett | Coût: 40 MP | Cooldown: 3 tours

7. **Vague de fissure** (attaque lourde + invocation)
   - Dégâts: 50 | Invoque auto Gardien Gorr | Coût: 100 MP | Cooldown: 5 tours

---

## 📊 Stats communes

| Stat | Valeur | Description |
|------|--------|-------------|
| **HP** | 500 | Points de vie |
| **MP** | 450 | Points de mana |
| **ATK** | 250 | Puissance d'attaque |
| **DEF** | 300 | Points de défense |
| **Endurance** | 1500 | Résistance |
| **Niveau** | 1 | Niveau de départ |

**Progression:** +1 niveau par victoire | +5 à toutes les stats par niveau

---

## 🎮 Modes de jeu

1. **PvE** - Joueur vs IA
   - Choisissez votre personnage et affrontez l'ordinateur
   - L'IA choisit automatiquement le personnage opposé

2. **Auto** - IA vs IA
   - Regardez deux IA s'affronter en spectateur
   - Classes choisies aléatoirement

3. **PvP** - Joueur vs Joueur *(en développement)*
   - Affrontez un ami en local

---

## 🏗️ Architecture du projet

```
Py-Fight/
├── combat_v2.py              # Point d'entrée principal
├── run.sh                    # Lanceur rapide
├── README.md                 # Ce fichier
│
├── src/
│   ├── models/               # Classes des personnages
│   │   ├── personnage_v2.py  # Classe abstraite de base
│   │   ├── sage.py           # Classe Sage
│   │   └── magicien.py       # Classe Magicien
│   │
│   ├── game/                 # Logique du jeu
│   │   ├── game_manager.py   # Gestion des modes de jeu
│   │   └── save_manager.py   # Sauvegarde/chargement
│   │
│   ├── ai/                   # Intelligence artificielle
│   │   └── ai_player.py      # IA avec 3 niveaux de difficulté
│   │                         # Décisions stratégiques adaptatives
│   │
│   └── utils/                # Utilitaires
│       ├── ascii_art.py      # Logo et skins ASCII
│       ├── input_handler.py  # Gestion des inputs joueur
│       ├── menu.py           # Menus du jeu
│       └── affichage.py      # Affichages divers
│
├── config/                   # Configurations JSON
│   ├── sage.json            # Stats et skills du Sage
│   ├── magicien.json        # Stats et skills du Magicien
│   └── game_config.json     # Config générale
│
├── saves/                    # Sauvegardes des parties
│   └── combat_*.json        # Historique des combats
│
└── assets/                   # Assets (skins, etc.)
    └── skins/               # Skins ASCII des personnages
```

---

## 🔧 Composants principaux

### 📦 `src/models/` - Classes des personnages

**`personnage_v2.py`** - Classe abstraite de base avec:
- Système de stats complet (HP, MP, ATK, DEF)
- Gestion des buffs/debuffs temporaires avec durée
- Cooldowns sur les compétences
- Familiers (invocations) avec attaques automatiques
- Zones d'effet persistantes
- Coups critiques et surcharge
- Passifs spécifiques par personnage

**`sage.py` / `magicien.py`** - Héritent de Personnage avec:
- Chargement des skills depuis JSON
- Override des méthodes pour passifs uniques
- Mécaniques spécifiques (invocations auto, récup MP, etc.)

### 🤖 `src/ai/` - Intelligence artificielle

**`ai_player.py`** - IA stratégique avec:
- **3 niveaux de difficulté:** facile, normal, difficile
- **Priorités tactiques:**
  - HP bas (<30%) → Heal ou évasion
  - Ennemi HP bas (<40%) → Attaque ultime
  - Début combat → Buffs
  - Ennemi buffé → Debuffs
  - Sinon → Attaque équilibrée
- Choix intelligent basé sur situation de combat
- **Rôle:** L'IA analyse l'état du combat et choisit la meilleure action parmi les skills disponibles selon une stratégie adaptative

### 🎯 `src/game/` - Gestion du jeu

**`game_manager.py`** - Orchestration des modes:
- Sélection du mode (Auto/PvE/PvP)
- Choix des personnages
- Lancement des combats

**`save_manager.py`** - Persistance:
- Sauvegarde automatique après chaque combat
- Historique des parties
- Replay des combats passés

### 🎨 `src/utils/` - Utilitaires

**`ascii_art.py`** - Art visuel:
- Logo WiZ-Fight en ASCII
- Écran de bienvenue avec message pour Jean Christophe
- Skins mini des personnages
- Bannières victoire/défaite
- Écran VS

**`menu.py`** - Menus interactifs:
- Menu principal
- Sélection personnage avec preview
- Détails complets des personnages
- Sous-menu modes de combat

**`input_handler.py`** - Interface joueur:
- Sélection des skills avec infos (MP, cooldown, statut)
- Affichage stats joueur/adversaire
- Messages de victoire

---

## 🎯 Fonctionnalités implémentées

### ✅ Combat complet
- [x] Tour par tour avec gestion des priorités
- [x] Calcul des dégâts avec formule équilibrée (DEF réduit 2% par 100 points, max 50%)
- [x] Coups critiques (15% base + buffs)
- [x] Cooldowns sur toutes les compétences
- [x] Buffs/debuffs temporaires avec durée
- [x] Familiers avec attaques automatiques chaque tour
- [x] Zones d'effet persistantes
- [x] Passifs uniques par personnage

### ✅ Interface
- [x] Logo ASCII WiZ-Fight
- [x] Écran de bienvenue immersif
- [x] Skins ASCII pour personnages
- [x] Menu avec nom après choix classe
- [x] Affichage skills simplifié en combat (nom, MP, cooldown)
- [x] Détails complets accessibles hors combat
- [x] Stats colorées (HP vert/jaune/rouge, MP bleu)

### ✅ Intelligence Artificielle
- [x] 3 niveaux de difficulté
- [x] Prise de décision stratégique
- [x] Adaptation selon situation
- [x] Mode Auto (IA vs IA) fonctionnel

### ✅ Système de progression
- [x] Gain de niveau à la victoire
- [x] +5 stats par niveau
- [x] Heal complet après victoire
- [x] Sauvegarde auto de l'historique

---

## 🚀 Comment jouer

### Lancement
```bash
# Méthode 1: Directement
python combat_v2.py

# Méthode 2: Avec le script
./run.sh
```

### Déroulement
1. **Écran de bienvenue** - Appuyez sur Entrée
2. **Menu principal:**
   - Option 1: Choisir personnage → Lance directement PvE
   - Option 2: Voir détails des personnages
   - Option 3: Modes avancés (Auto, PvP)
3. **Sélection personnage** - Sage ou Magicien
4. **Saisie du nom** - "Quel est votre nom, [classe]?"
5. **Combat!** - Choisissez vos skills tour par tour

---

## 💡 Suggestions d'améliorations

### 🎨 Affichage des skills (prioritaire)
**Problème actuel:** Liste simple avec numéros

**Suggestions:**

#### Option 1: Catégorisation par type
```
⚔️  ATTAQUES                           🛡️  DÉFENSE
1. ✨ Annihilation Radieuse (40 MP)   3. ⚡ Galvanisation (70 MP)
6. 🌪️ Tempête de la faille (100 MP)  5. 💨 Dernier recours (50 MP)

💥 SPÉCIAL
2. 🗡️ Lance de Sauron (60 MP) [Debuff]
4. ⚡💥 Surcharge d'éclair (80 MP) [Critique]
```

#### Option 2: Barres de cooldown visuelles
```
1. ✨ Annihilation Radieuse    40 MP  [▓▓▓▓▓▓▓▓▓▓] Prêt!
2. 🗡️ Lance de Sauron         60 MP  [████░░░░░░] 2 tours
3. ⚡ Galvanisation            70 MP  [▓▓▓▓▓▓▓▓▓▓] Prêt!
```

#### Option 3: Affichage compact avec codes couleur
```
[1] ✨ Annihilation (40)  [2] 🗡️ Lance (60) ⏳2  [3] ⚡ Galva (70)
[4] 💥 Surcharge (80)     [5] 💨 Évasion (50) ⏳20  [6] 🌪️ Tempête (100) ⏳4
```

#### Option 4: Style menu interactif (recommandé)
```
╔════════════════ VOS COMPÉTENCES ════════════════╗
║                                                  ║
║  ⚔️  ATTAQUES                                    ║
║  [1] ✨ Annihilation Radieuse       40 MP  ✅    ║
║  [6] 🌪️ Tempête de la faille       100 MP ✅    ║
║                                                  ║
║  🎯 TACTIQUE                                     ║
║  [2] 🗡️ Lance de Sauron            60 MP  ✅    ║
║  [3] ⚡ Galvanisation               70 MP  ✅    ║
║  [4] ⚡💥 Surcharge d'éclair         80 MP  ✅    ║
║                                                  ║
║  🛡️  DÉFENSE                                     ║
║  [5] 💨 Dernier recours             50 MP  ⏳20  ║
║                                                  ║
╚══════════════════════════════════════════════════╝
```

### Interface
- [ ] Implémenter affichage skills amélioré
- [ ] Animations ASCII pour les attaques
- [ ] Barre de vie graphique (██████░░░░)
- [ ] Effets visuels pour coups critiques
- [ ] Son/bip pour actions importantes

### Gameplay
- [ ] Mode PvP local complet
- [ ] Plus de personnages (Sorcière, Guerrier, etc.)
- [ ] Système d'équipement
- [ ] Shop pour améliorer stats
- [ ] Tournois avec bracket

### Technique
- [ ] Tests unitaires (pytest)
- [ ] Configuration des contrôles
- [ ] Mode replay amélioré avec animations
- [ ] Statistiques détaillées post-combat
- [ ] Leaderboard persistant

---

## 🛠️ Technologies utilisées

- **Python 3.6+** - Langage principal
- **Programmation Orientée Objet:**
  - Classes abstraites (ABC)
  - Héritage
  - Encapsulation (@property)
  - Polymorphisme
  - Type hints (typing)
- **Bibliothèques standard uniquement:**
  - json (configs et saves)
  - random (RNG pour critiques/IA)
  - os (paths)
  - datetime (timestamps)
  - time (pauses)

**Pas de dépendances externes !** 🎉

---

## 📝 Notes de développement

### Formule de dégâts
```python
reduction_percent = min(50, defense / 100 * 2)  # Max 50%
degats_finaux = degats_base * (1 - reduction_percent / 100) * (1 - buffs_reduction / 100)
```

### Cooldowns
- Attaques légères: 3 tours
- Attaques lourdes: 5 tours
- Dernier recours: 20 tours
- Autres: 2-4 tours

### Balance
- DEF 300 → ~6% de réduction
- Buffs additionnent avec DEF
- Familiers: 10 dmg/tour, 6 tours de durée
- Zones: 15 dmg/tour, 6 tours de durée

---

## 👨‍💻 Auteur

**Savage** - Étudiant passionné de POO

---

## 🙏 Remerciements

**Jean Christophe** 🎓 - Pour l'enseignement de la POO en Python

*"By the way c'était vraiment galère cet affichage ASCII 🤣"*

---

## 📜 Licence

Projet éducatif - POO Python
