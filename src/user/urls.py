"""
Fichier de configuration des routes URL pour l'application user.
"""

from django.urls import path
from todolist.generic_crud import (
    create_customized,
    list_customized,
    detail_update_delete_customized,
    list_filter_one_parameter
)
from .models import User, Departement, Poste
from .serializers import UserSerializer, PosteSerializer, DepartementSerializer
from .views import EmployeesByDepartement, RegisterView

# Définition des routes de l'API pour les opérations sur les utilisateurs, postes et départements
urlpatterns = [
    # Endpoint pour l'enregistrement d'un nouvel utilisateur
    path("auth/register/",
        RegisterView.as_view(),
        name="inscription"
    ),

    # Endpoint pour récupérer, modifier ou supprimer le profil utilisateur
    path("auth/profile/<int:pk>/",
        detail_update_delete_customized(User, UserSerializer).as_view(),
        name="user_action"
    ),

    # Endpoint pour créer un nouveau poste
    path("poste/new/",
        create_customized(Poste, PosteSerializer).as_view(),
        name="creer_poste"
    ),

    # Endpoint pour lister tous les postes
    path("poste/liste/",
        list_customized(Poste, PosteSerializer).as_view(),
        name="liste_de_tous_les_postes"
    ),

    # Endpoint pour consulter, modifier ou supprimer un poste spécifique
    path("poste/<int:pk>/",
        detail_update_delete_customized(Poste, PosteSerializer).as_view(),
        name="poste_action"
    ),

    # Endpoint pour créer un nouveau département
    path("departement/new/",
        create_customized(Departement, DepartementSerializer).as_view(),
        name="creer_departement"
    ),

    # Endpoint pour lister tous les départements
    path("departement/liste/",
        list_customized(Departement, DepartementSerializer).as_view(),
        name="liste_departement"
    ),

    # Endpoint pour consulter, modifier ou supprimer un département spécifique
    path("departement/<int:pk>/",
        detail_update_delete_customized(Departement, DepartementSerializer).as_view(),
        name="departement_action"
    ),

    # Endpoint pour filtrer les postes d’un département
    path("departement/<int:departement_id>/postes/",
        list_filter_one_parameter(Poste, PosteSerializer, "departement_id").as_view(),
        name="liste_poste_du_departement"
    ),

    # Endpoint pour récupérer les employés d’un département (via ForeignKey poste__departement)
    path("departement/<int:departement_id>/employees/",
        EmployeesByDepartement.as_view(),
        name="employes-par-departement"
    ),
]
