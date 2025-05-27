# 📊 API de Gestion des Tâches et Performances Employés

Bienvenue dans ce projet de backend développé en Django et Django REST Framework.  
Il a pour but de fournir une API RESTful pour gérer les tâches, projets et performances des employés.

---

## 🚀 Fonctionnalités

- ✅ Authentification via `dj-rest-auth`
- 📁 Gestion des **projets**
- 📌 Création et suivi des **tâches**
- 👥 Attribution des tâches à plusieurs **employés**
- 📈 Calcul de **performances** (respect des délais, durée réelle...)
- 🔒 Permissions basées sur les rôles

---

## 🏗️ Stack technique

| Outil | Description |
|-------|-------------|
| Django | Framework backend principal |
| Django REST Framework | Création d'API RESTful |
| dj-rest-auth | Authentification simplifiée (login, logout, registration) |
| Django Admin | Gestion rapide des données |
| SQLite / PostgreSQL | Base de données relationnelle (choix selon environnement) |

---

## ⚙️ Installation

### 1. Cloner le projet

```bash
git clone https://github.com/medamondonga/uhtech_todolist.git
cd uhtech_todolist
```
### 2. Créer un environnement virtuel
```bash
python -m venv env
source env/bin/activate  # Linux/macOS
env\Scripts\activate     # Windows
```
### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```
### 4. Appliquer les migrations
```bash
python manage.py migrate
```
### 5. Lancer le serveur
```bash
python manage.py runserver
```
## 🔐 Authentification
L’API utilise dj-rest-auth pour gérer :

Login / Logout

Inscription

Récupération de mot de passe

Jetons d’authentification (TokenAuthentication ou JWT)

## 🧠 Concepts clés utilisés
Serializers : pour transformer les objets Python <-> JSON

Viewsets & Mixins : pour créer des vues CRUD rapides

Routers : pour générer automatiquement les URLs

Permissions personnalisées : pour sécuriser les routes selon les rôles


## 👤 Auteur
Nom : Meda Mondonga

Rôle : Développeuse backend

Organisation : UHTech (projet de stage)

Email : [medamondonga4@gmail.com]