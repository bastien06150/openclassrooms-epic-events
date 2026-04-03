# Epic Events CRM (CLI)

Application en ligne de commande (CLI) permettant de gérer des clients, contrats et événements, avec authentification sécurisée, gestion des permissions et journalisation avec Sentry.

---

## 🚀 Fonctionnalités

- Authentification avec JWT
- Gestion des rôles (management, sales, support)
- CRUD complet :
  - Clients
  - Contrats
  - Événements
  - Collaborateurs
- Interface CLI avec Click
- Journalisation des erreurs et événements avec Sentry

---

## 🛠️ Technologies utilisées

- Python 3
- SQLAlchemy
- PostgreSQL
- Click (CLI)
- Sentry (logging & monitoring)

---

## ⚙️ Installation

1. Cloner le projet :

   ```
    git clone https://github.com/TON_USERNAME/openclassrooms-epic-events.git](https://github.com/bastien06150/openclassrooms-epic-events.git
    cd openclassrooms-epic-events
    ```
2. Installer l'environement virtuel :

   ```
   python -m venv env

   ```

3. Activer l'environement virtuel :

   ```
   .\env\scripts\activate.ps1.

   ```

4. Installer les dépendances :

   ```
   pip install -r requirements.txt

   ```

5. Initialiser la base de données :

   ```
   python create_tables.py
   ```
---
## Utilisation 

### Authentification

- python main.py login
- python main.py current-user
- python main.py logout

### Clients

- python main.py client list
- python main.py client create

### Contrats

- python main.py contract list
- python main.py contract create
- python main.py contract update
- python main.py contract delete

### Evénements

- python main.py event list
- python main.py event create
- python main.py event update
- python main.py event delete

### Collaborateurs

- python main.py employee create
- python main.py employee update
- python main.py employee delete
   
---

## Permissions

- Management :  Accès complet (CRUD)

- Sales :  Gestion des clients et contrats

- Support :  Gestion des événements assignés


