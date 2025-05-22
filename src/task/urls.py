"""Définition des routes pour la gestion des tâches et des projets."""

from django.urls import path
from todolist.generic_crud import (
    create_customized,
    list_customized,
    detail_update_delete_customized,
)
from .models import Tache, Projet
from .serializers import TacheSerializer, ProjetSerializer
from .views import TacheProjetView

urlpatterns = [
    # Endpoint pour créer une nouvelle tâche
    path("new/",
        create_customized(Tache, TacheSerializer).as_view(),
        name="creer_tache"
    ),

    # Endpoint pour lister toutes les tâches
    path("/",
        list_customized(Tache, TacheSerializer).as_view(),
        name="liste_tache"
    ),

    # Endpoint pour afficher, modifier ou supprimer une tâche spécifique
    path("<int:pk>/",
        detail_update_delete_customized(Tache, TacheSerializer).as_view(),
        name="tache_action"
    ),

    # Endpoint pour créer un nouveau projet
    path("new/project/",
        create_customized(Projet, ProjetSerializer).as_view(),
        name="creer_projet"
    ),

    # Endpoint pour lister tous les projets
    path("project//",
        list_customized(Projet, ProjetSerializer).as_view(),
        name="liste_projet"
    ),

    # Endpoint pour afficher, modifier ou supprimer un projet spécifique
    path("project/<int:pk>/",
        detail_update_delete_customized(Projet, ProjetSerializer).as_view(),
        name="projet_action"
    ),

    #Endpoint pour lister les taches d'un projet
    path("<projet>/project/",
         TacheProjetView.as_view(),
         name="Tache_du_projet"),

]
