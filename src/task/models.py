"""
Models liés à la gestion des taches
"""
from datetime import datetime, date
from django.db import models
from django.conf import settings

# Récupère le modèle utilisateur défini dans les settings
User = settings.AUTH_USER_MODEL

# Constantes pour les statuts de tâche
PENDING = "en_cours"
LATE = "en_retard"
FINISHED = "terminee"

# Choix possibles pour le champ 'statut'
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
        """
        Représentation textuelle de l'objet Projet.
        """
        return f"{self.nom}"


class Tache(models.Model):
    """
    Classe représentant une tâche liée à un projet.
    """
    titre = models.CharField(max_length=200)
    description = models.TextField()
    date_debut = models.DateField()
    date_fin = models.DateField()
    date_termine = models.DateField(null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default=PENDING)

    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, related_name="projet")

    assigne_par = models.ForeignKey(User, on_delete=models.CASCADE, related_name="taches_attribuees", blank=True, null=True)
    assigne_a = models.ManyToManyField(User, related_name="taches_reçues")

    nombre_jour_execution = models.IntegerField(null=True, blank=True)
    nombre_jour_reel = models.IntegerField(null=True, blank=True)
    taux_respect_delais = models.FloatField(null=True, blank=True)

    def update_statut_automatique(self):
        """
        Met à jour automatiquement le statut de la tâche si la date est dépassée.
        """
        if self.statut == PENDING and self.date_fin and self.date_fin < date.today():
            self.statut = LATE
            self.save(update_fields=["statut"])

    def finish_task(self, *args, **kwargs):
        """
        Marque la tâche comme terminée et calcule les indicateurs associés.
        """
        if self.statut == PENDING or self.statut == LATE:
            self.statut = FINISHED
            self.date_termine = datetime.now()
            self.nombre_jour_reel = (datetime.now().date() - self.date_debut).days
            ecart = self.nombre_jour_execution - self.nombre_jour_reel
            self.taux_respect_delais = round((ecart / self.nombre_jour_execution) * 100, 2)
        super().save(*args, **kwargs)

    def definir_nombre_jour_execution(self):
        """
        Définit la durée prévue pour l'exécution de la tâche.
        """
        if self.date_debut and self.date_fin:
            self.nombre_jour_execution = (self.date_fin - self.date_debut).days

    def assignee_tache(self, utilisateur_assignateur, liste_utilisateurs_assignes):
        self.assigne_par = utilisateur_assignateur
        self.save(update_fields=["assigne_par"])
        self.assigne_a.add(liste_utilisateurs_assignes)
        self.save()



    def __str__(self):
        """
        Représentation textuelle de l'objet Tache.
        """
        return f"{self.titre}"
