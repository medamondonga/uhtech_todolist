from django.db import models

class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(est_supprime=False)


class SoftDeleteModel(models.Model):
    """
    Modèle abstrait pour suppression logique.
    Tous les objets ayant est_supprime=True sont masqués automatiquement.
    """
    est_supprime = models.BooleanField(default=False)

    # Managers
    objects = SoftDeleteManager()  # Par défaut, filtre les supprimés
    all_objects = models.Manager()  # Accès brut sans filtre

    class Meta:
        abstract = True  # Important : ne pas créer une table pour ce modèle

    def delete(self, *args, **kwargs):
        """
        Ne supprime pas physiquement, mais marque comme supprimé.
        """
        self.est_supprime = True
        self.save(update_fields=["est_supprime"])
