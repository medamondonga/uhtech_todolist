"""
Models liés à la gestion des utilisateurs.
"""

import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import check_password
from todolist.models_mixins import SoftDeleteModel

# Choix possibles pour les rôles d'utilisateur
ROLES = [
    ("admin", "Admin"),
    ("manager", "Manager"),
    ("agent", "Agent"),
]

# Choix pour le champ sexe
SEXE = [
    ("homme", "Homme"),
    ("femme", "Femme"),
]

# Choix pour l'état civil
ETAT_CIVIL = [
    ("celibataire", "Célibataire"),
    ("marie", "Marié(e)"),
    ("divorce", "Divorcé(e)"),
    ("veuf", "Veuf(ve)"),
]


class Departement(SoftDeleteModel):
    """
    Classe représentant un département.
    """
    nom = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        """
        Représentation textuelle de l'objet Département.
        """
        return f"{self.nom}"


class Poste(SoftDeleteModel):
    """
    Classe représentant un poste dans un département.
    """
    titre = models.CharField(max_length=100)
    description = models.TextField()
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE)

    def __str__(self):
        """
        Représentation textuelle de l'objet Poste.
        """
        return f"{self.titre}"


class User(AbstractUser):
    """
    Classe représentant l'utilisateur principal du système.
    Hérite de AbstractUser pour intégrer l'authentification.
    """
    sexe = models.CharField(max_length=10, choices=SEXE, null=False, blank=False)
    etat_civil = models.CharField(max_length=50, choices=ETAT_CIVIL, null=False, blank=False)
    adresse = models.TextField()
    telephone = models.CharField(max_length=20)
    date_naissance = models.DateField(default=datetime.datetime.now)
    poste = models.ForeignKey(Poste, on_delete=models.SET_NULL, null=True)
    role = models.CharField(max_length=10, choices=ROLES)

    def check_password(self, raw_password):
        """
        Vérifie la correspondance entre le mot de passe brut et celui enregistré.
        """
        return check_password(raw_password, self.password)

    def __str__(self):
        """
        Représentation textuelle de l'utilisateur.
        """
        return f"{self.email}"


class Manager(User):
    """
    Classe propre aux utilisateurs ayant le rôle de manager.
    """



class Agent(User):
    """
    Classe propre aux utilisateurs ayant le rôle d'agent.
    """
