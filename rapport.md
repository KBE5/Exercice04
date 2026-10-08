# Rapport de réalisation — Observatoire de fréquentation

## 1. Vue d'ensemble du projet
* Développement d'une application complète pour publier les chiffres de fréquentation des médiathèques et réserver un bilan aux comptes habilités.

## 2. Backend & Sécurité (FastAPI & PostgreSQL)
* **Base de données :** Modélisation avec SQLAlchemy (tables `users` et `frequentations`). Jeu de données initialisé avec 24 observations et 2 comptes de test (`reader01` et `analyst01`).
* **Sécurité :** Mots de passe hachés avec `bcrypt`. Authentification via JWT (`POST /auth/login`) et contrôle d'accès par rôle (RBAC) directement dans l'API.
* **API REST :**
  * `POST /auth/login` : Connexion et émission du token Bearer.
  * `GET /frequentations` : Consultation publique avec pagination stable (`page`, `page_size`, `total`, `pages`). Rejet `422` en cas de paramètres invalides.
  * `GET /analytics/bilan` : Accès restreint au rôle `analyst`. Calcul dynamique des agrégats (`nb_observations`, `total_visiteurs`, `moyenne_visiteurs`). Retours `401` sans token et `403` pour le rôle `reader`.

## 3. Interface utilisateur (Streamlit)
* **Structure modulaire :** Séparation entre les vues, la gestion des sessions et la couche HTTP.
* **Gestion du token :** Stockage du JWT dans `st.session_state` (mots de passe jamais conservés). Déconnexion complète disponible.
* **Pages :**
  * Page de connexion (authentification `reader` / `analyst`).
  * Page publique de consultation avec pagination (boutons **Précédent** / **Suivant**).
  * Page privée du bilan analytique réservée au rôle `analyst`.

## 4. Tests automatisés
* **Isolation (`conftest.py`) :** Base PostgreSQL de test dédiée (`DATABASE_URL_TEST`). Chaque test tourne dans une transaction annulée à la fin (`rollback()`) pour garantir une base propre.
* **Tests d'intégration API (`pytest` + `TestClient`) :**
  * `test_auth.py` : Connexions réussies et échecs (`401`).
  * `test_frequentations.py` : Accès public, pagination, total d'enregistrements et rejet `422`.
  * `test_analytics.py` : Matrice des rôles (`401`, `403`, `200`) et vérification des valeurs de l'oracle (24 observations, 75 660 visiteurs, moyenne de 3 152,5).
* **Test End-to-End 852(`test_e2e.py` + Playwright) :** Parcours complet dans un vrai navigateur Chromium (Navigateur → Streamlit → FastAPI → PostgreSQL) pour vérifier la connexion analyste et l'affichage des valeurs du bilan.

## 5. Livrables
* Fichiers `.env.example`, `.gitignore` et `requirements.txt` unique à la racine.
* Fichier `README.md` avec toutes les commandes Windows PowerShell (`python -m ...`) pour installer, lancer les serveurs, exécuter la base et démarrer la suite de tests.