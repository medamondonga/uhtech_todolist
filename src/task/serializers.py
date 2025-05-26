"""Sérialiseurs pour les modèles Tache et Projet."""

from rest_framework import serializers
from .models import Tache, Projet


class TacheSerializer(serializers.ModelSerializer):
    """Sérialiseur pour le modèle Tache."""

    class Meta:
        """Configuration du sérialiseur liée au modèle Tache."""
        model = Tache
        fields = "__all__"
        read_only_fields = ['assigne_par', 'statut',
                            'date_termine', 'taux_respect_delais',
                            'nombre_jour_execution', 'nombre_jour_reel'] 

    def create(self, validated_data):
    # Injecte automatiquement l'utilisateur connecté
        request = self.context.get('request', None)
        if request and request.user and request.user.is_authenticated:
            validated_data['assigne_par'] = request.user

    # Crée l'instance
        instance = super().create(validated_data)

    # Calcule les jours d'exécution
        instance.definir_nombre_jour_execution()
        instance.save()

        return instance
    
    def to_representation(self, instance):
        #On met à jour le statut avant de le renvoyer
        instance.update_statut_automatique()
        return super().to_representation(instance)


class ProjetSerializer(serializers.ModelSerializer):
    """Sérialiseur pour le modèle Projet."""

    class Meta:
        """Configuration du sérialiseur liée au modèle Projet."""
        model = Projet
        fields = "__all__"
        read_only_fields = ['chef_projet']

    def create(self, validated_data):
        # Injecte automatiquement l'utilisateur connecté
        request = self.context.get('request', None)
        if request and request.user and request.user.is_authenticated:
            validated_data['chef_projet'] = request.user
        return super().create(validated_data)