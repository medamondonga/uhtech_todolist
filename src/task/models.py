"""
Models liés à la gestion des taches
"""
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL
STATUT_CHOICES = [
        ("en_attente", "En attente"),
        ("en_cours", "En cours"),
        ("terminee", "Terminée"),
    ]



class Projet(models.Model):
    """
    Classe représentant un projet, composé de plusieurs tâches.
    """
    nom = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    chef_projet = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.nom}"


class Tache(models.Model):
    """
    Classe représentant une tâche individuelle assignée à un ou plusieurs utilisateurs.
    """
    titre = models.CharField(max_length=200)
    description = models.TextField()
    date_debut = models.DateField()
    date_fin = models.DateField()
    date_termine = models.DateField(null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default="en_attente")

    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, related_name="taches", null=True, blank=True)

    assigne_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="taches_attribuees")
    assigne_a = models.ManyToManyField(User, related_name="taches_reçues")

    taux_respect_delais = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.titre}"
