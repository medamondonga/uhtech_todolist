"""
Sérialiseur pour la gestion des utilisateurs dans l'application.
"""

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from .models import User, Poste, Departement
User = get_user_model()

class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = User.EMAIL_FIELD

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(request=self.context.get("request"), username=email, password=password)

            if not user:
                raise AuthenticationFailed(_("Cet utilisateur n'existe pas."), code="authorization")
        else:
            raise AuthenticationFailed(_("Email et mot de passe requis."), code="authorization")

        data = super().validate(attrs)
        data["user_id"] = user.id
        data["email"] = user.email
        return data



class UserSerializer(serializers.ModelSerializer):
    """
    Sérialiseur principal pour la création d'un utilisateur.
    """

    class Meta:
        """
        Configuration du serializer liée au modèle User.
        """
        model = User
        fields = [
            "first_name", "last_name", "email", "sexe", "etat_civil",
            "adresse", "telephone", "date_naissance", "password","poste",
            "role"
            ""
        ]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        """
        Crée un nouvel utilisateur à partir des données validées.

        Args:
            validated_data (dict): Données validées issues du formulaire ou de la requête.

        Returns:
            User: L'utilisateur nouvellement créé.
        """
        user = User(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            username=validated_data["first_name"] + validated_data["last_name"],
            email=validated_data["email"],
            sexe=validated_data["sexe"],
            etat_civil=validated_data["etat_civil"],
            adresse=validated_data["adresse"],
            telephone=validated_data["telephone"],
            date_naissance=validated_data["date_naissance"],
            role=validated_data["role"],
        )
        user.set_password(validated_data["password"])
        user.save()

        return user


class PosteSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle Poste.
    """

    class Meta:
        """
        Configuration du serializer liée au modèle Poste.
        """
        model = Poste
        fields = "__all__"


class DepartementSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle Departement.
    """

    class Meta:
        """
        Configuration du serializer liée au modèle Departement.
        """
        model = Departement
        fields = "__all__"


class UserListSerializer(serializers.ModelSerializer):
    #assigne_a = serializers.StringRelatedField(many=True)
    poste = serializers.StringRelatedField()
    class Meta:
        """
        Configuration du serializer liée au modèle User.
        """
        model = User
        fields = [
            "first_name", "last_name", "email", "sexe", "etat_civil",
            "adresse", "telephone", "date_naissance", "password","poste", "role"
            ""
        ]
