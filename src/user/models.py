"""
Models liés à la gestions des utilisateurs
"""
import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import check_password

ROLES = [
    ("manager", "Manager"),
    ("agent", "Agent"),
]
SEXE = [
        ("homme", "Homme"),
        ("femme", "Femme")
    ]

ETAT_CIVIL = [
    ("celibataire", "Célibataire"),
    ("marie", "Marié(e)"),
    ("divorce", "Divorcé(e)"),
    ("veuf", "Veuf(ve)")
]


class Poste(models.Model):
    """
    class pour le poste
    """
    titre = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"{self.titre}"

class Departement(models.Model):
    """
    class pour le departement
    """
    nom = models.CharField(max_length=100)
    description = models.TextField()
    postes = models.ManyToManyField(Poste, related_name="departements")

    def __str__(self):
        return f"{self.nom}"

class User(AbstractUser):
    """
    class pour l'utilisateur par defaut
    """
    sexe = models.CharField(max_length=10, choices=SEXE,
                            null=False, blank=False)
    etat_civil = models.CharField(max_length=50, choices=ETAT_CIVIL,
                            null=False, blank=False)
    adresse = models.TextField()
    telephone = models.CharField(max_length=20)
    date_naissance = models.DateField(default=datetime.datetime.now)
    poste = models.ForeignKey(Poste, on_delete=models.SET_NULL, null=True)
    role = models.CharField(max_length=10, choices=ROLES)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.username}"

class Manager(User):
    """
    class propre aux managers
    """

class Agent(User):
    """
    class propre aux agents
    """
