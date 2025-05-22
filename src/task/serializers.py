"""Sérialiseurs pour les modèles Tache et Projet."""

from rest_framework import serializers
from .models import Tache, Projet


class TacheSerializer(serializers.ModelSerializer):
    """Sérialiseur pour le modèle Tache."""

    class Meta:
        """Configuration du sérialiseur liée au modèle Tache."""
        model = Tache
        fields = "__all__"


class ProjetSerializer(serializers.ModelSerializer):
    """Sérialiseur pour le modèle Projet."""

    class Meta:
        """Configuration du sérialiseur liée au modèle Projet."""
        model = Projet
        fields = "__all__"
