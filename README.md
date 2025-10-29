# Gestion de Stock - Les Martial de Informatique

Système de gestion d'inventaire pour les matériels informatiques développé avec Flask, SQLite, HTML et CSS.

## Fonctionnalités

### 🏠 Tableau de Bord
- Vue d'ensemble des statistiques de stock
- Alertes de stock faible
- Historique des transactions récentes
- Actions rapides

### 📦 Gestion des Matériels
- Ajout, modification et suppression de matériels
- Recherche et filtrage par catégorie
- Gestion des stocks et alertes
- Informations détaillées (marque, modèle, prix, fournisseur)

### 📊 Transactions de Stock
- Entrées et sorties de stock
- Suivi des mouvements avec raisons
- Gestion des utilisateurs
- Aperçu en temps réel des stocks

### 📈 Rapports et Analyses
- Rapport par catégorie
- Analyse des stocks faibles
- Recommandations de réapprovisionnement
- Export et impression

### 🔧 API REST
- Endpoints pour intégration externe
- Accès aux données des matériels
- Historique des transactions

## Installation et Configuration

### Prérequis
- Python 3.7+
- pip (gestionnaire de paquets Python)

### Installation

1. **Cloner ou télécharger le projet**
```bash
# Si vous avez git installé
git clone <repository-url>
cd Application
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Initialiser la base de données**
```bash
python app.PY
```

4. **Lancer l'application**
```bash
python app.PY
```

L'application sera accessible à l'adresse : `http://localhost:5000`

## Structure du Projet

```
Application/
├── app.PY                 # Application Flask principale
├── DATA.SQL              # Schéma de base de données
├── INTRFACE.HTML         # Interface HTML (templates)
├── STAYL.CSS             # Styles CSS
├── requirements.txt      # Dépendances Python
├── templates/           # Templates HTML
│   ├── base.html
│   ├── index.html
│   ├── materials.html
│   ├── add_material.html
│   ├── edit_material.html
│   ├── transaction.html
│   └── reports.html
├── static/              # Fichiers statiques
│   ├── style.css
│   └── script.js
└── inventory.db         # Base de données SQLite (créée automatiquement)
```

## Utilisation

### 1. Accès au Système
- Ouvrez votre navigateur
- Allez à `http://localhost:5000`
- Vous verrez le tableau de bord principal

### 2. Ajouter un Matériel
1. Cliquez sur "Ajouter Matériel" ou "Matériels" → "Ajouter"
2. Remplissez le formulaire avec les informations :
   - Nom du matériel (obligatoire)
   - Catégorie (obligatoire)
   - Marque et modèle
   - Prix (obligatoire)
   - Quantité en stock (obligatoire)
   - Stock minimum (obligatoire)
   - Fournisseur
   - Description
3. Cliquez sur "Enregistrer"

### 3. Gérer les Stocks
1. Allez dans "Matériels"
2. Utilisez les filtres pour trouver le matériel
3. Cliquez sur l'icône de transaction (↔)
4. Sélectionnez le type (Entrée/Sortie)
5. Entrez la quantité et la raison
6. Confirmez la transaction

### 4. Consulter les Rapports
1. Allez dans "Rapports"
2. Consultez les analyses par catégorie
3. Vérifiez les stocks faibles
4. Suivez les recommandations

## Catégories de Matériels

Le système inclut les catégories suivantes :
- **Ordinateurs** : PC de bureau et portables
- **Périphériques** : Souris, claviers, écrans, imprimantes
- **Réseau** : Routeurs, switches, câbles réseau
- **Stockage** : Disques durs, SSD, clés USB
- **Logiciels** : Licences et logiciels
- **Accessoires** : Autres accessoires informatiques
- **Composants** : Processeurs, RAM, cartes graphiques
- **Sécurité** : Antivirus, pare-feu, systèmes de sécurité

## API Endpoints

### Matériels
- `GET /api/materials` - Liste tous les matériels
- `GET /api/materials/<id>` - Détails d'un matériel

### Transactions
- `GET /api/transactions` - Historique des transactions

## Base de Données

### Tables Principales
- **materials** : Informations des matériels
- **categories** : Catégories de produits
- **transactions** : Historique des mouvements
- **suppliers** : Informations des fournisseurs
- **users** : Utilisateurs du système

### Vues Utiles
- **low_stock_materials** : Matériels en stock faible
- **stock_value_by_category** : Valeur par catégorie
- **recent_transactions** : Transactions récentes

## Personnalisation

### Modifier les Catégories
Éditez le fichier `DATA.SQL` pour ajouter/modifier les catégories :
```sql
INSERT INTO categories (name, description) VALUES 
('Nouvelle Catégorie', 'Description de la catégorie');
```

### Modifier les Styles
Éditez `static/style.css` pour personnaliser l'apparence :
- Couleurs dans les variables CSS `:root`
- Layouts et responsive design
- Animations et transitions

### Ajouter des Fonctionnalités
Modifiez `app.PY` pour :
- Ajouter de nouveaux endpoints
- Créer de nouvelles pages
- Intégrer des fonctionnalités avancées

## Dépannage

### Problèmes Courants

1. **Erreur de port déjà utilisé**
   - Changez le port dans `app.PY` : `app.run(port=5001)`

2. **Base de données corrompue**
   - Supprimez `inventory.db` et relancez l'application

3. **Erreurs de dépendances**
   - Réinstallez : `pip install -r requirements.txt --force-reinstall`

4. **Problèmes de permissions**
   - Vérifiez les permissions d'écriture dans le dossier

### Logs et Debug
Activez le mode debug dans `app.PY` :
```python
app.run(debug=True)
```

## Support et Contribution

Pour toute question ou suggestion :
1. Vérifiez la documentation
2. Consultez les logs d'erreur
3. Testez avec des données d'exemple

## Licence

Ce projet est développé pour "Les Martial de Informatique" - Usage interne uniquement.

---

**Version** : 1.0  
**Dernière mise à jour** : Octobre 2024  
**Développeur** : Assistant IA Claude
