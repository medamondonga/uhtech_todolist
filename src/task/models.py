"""
Models liés à la gestion des taches
"""
from datetime import datetime, date
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

PENDING = "en_cours"
LATE = "en_retard"
FINISHED = "terminee"

STATUT_CHOICES = [
        (LATE, "En retard"),
        (PENDING, "En cours"),
        (FINISHED, "Terminée"),
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
    titre = models.CharField(max_length=200)
    description = models.TextField()
    date_debut = models.DateField()
    date_fin = models.DateField()
    date_termine = models.DateField(null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default=PENDING)

    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, related_name="projet")

    assigne_par = models.ForeignKey(User, on_delete=models.CASCADE, related_name="taches_attribuees", blank=True, null=True)
    assigne_a = models.ManyToManyField(User, related_name="taches_reçues")

    taux_respect_delais = models.FloatField(null=True, blank=True)

    def update_statut_automatique(self):
        if self.statut == PENDING and self.date_fin and self.date_fin < date.today():
            self.statut = LATE
            self.save(update_fields=["statut"])


    def finish_task(self, *args,**kwargs):
        if self.statut == PENDING:
            self.statut = FINISHED
            self.date_termine = datetime.now()
        super().save(*args,**kwargs)

    def __str__(self):
        return f"{self.titre}"
