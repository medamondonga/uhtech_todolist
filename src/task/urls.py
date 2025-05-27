"""Définition des routes pour la gestion des tâches et des projets."""

from django.urls import path
from todolist.generic_crud import (
    create_customized,
    list_customized,
    detail_update_delete_customized,
    list_filter_one_parameter,
)
from .models import Tache, Projet
from .serializers import (TacheSerializer, ProjetSerializer,
                          TacheListSerializer, ProjetListSerializer)
from .views import (FinishTache, ListTachesTerminees, 
                    TachesTermineesParProjet, TachesEncoursParProjet,
                    PerformanceAgent, AssigneTacheAPIView)

urlpatterns = [
    # Endpoint pour créer une nouvelle tâche
    path("new/",
        create_customized(Tache, TacheSerializer).as_view(),
        name="creer_tache"
    ),

    # Endpoint pour lister toutes les tâches
    path("list/",
        list_customized(Tache, TacheListSerializer).as_view(),
        name="liste_tache"
    ),

    # Endpoint pour afficher, modifier ou supprimer une tâche spécifique
    path("<int:pk>/",
        detail_update_delete_customized(Tache, TacheSerializer).as_view(),
        name="tache_action"
    ),

    # Endpoint pour marquer une tâche comme terminée
    path("<int:id_tache>/finish/",
        FinishTache.as_view(),
        name="Finish-tache"
    ),

    path("<int:id_tache>/assigner/", AssigneTacheAPIView.as_view(), name="assigner-tache"),


    # Endpoint pour créer un nouveau projet
    path("project/new/",
        create_customized(Projet, ProjetSerializer).as_view(),
        name="creer_projet"
    ),

    # Endpoint pour lister tous les projets
    path("project/list/",
        list_customized(Projet, ProjetListSerializer).as_view(),
        name="liste_projet"
    ),

    # Endpoint pour afficher, modifier ou supprimer un projet spécifique
    path("project/<int:pk>/",
        detail_update_delete_customized(Projet, ProjetSerializer).as_view(),
        name="projet_action"
    ),

    # Endpoint pour lister les tâches d’un projet donné
    path("project/<int:projet_id>/",
        list_filter_one_parameter(Tache, TacheSerializer, "projet_id").as_view(),
        name="Tache_du_projet"
    ),

    # Endpoint pour lister les tâches assignées à un agent spécifique
    path("<int:assigne_a>/agent/",
        list_filter_one_parameter(Tache, TacheListSerializer, "assigne_a").as_view(),
        name="Tache_d_un_agent"
    ),

    # Endpoint pour lister toutes les tâches terminées
    path("terminees/",
        ListTachesTerminees.as_view(),
        name="taches-terminees"
    ),

    # Endpoint pour lister les tâches terminées d’un projet
    path("projets/<int:projet_id>/taches_terminees/",
        TachesTermineesParProjet.as_view(),
        name="taches-terminees-par-projet"
    ),

    # Endpoint pour lister les tâches en cours d’un projet
    path("projets/<int:projet_id>/taches_encours/",
        TachesEncoursParProjet.as_view(),
        name="taches-encours-par-projet"
    ),

    path("agent/<int:id_agent>/performance/<int:nombre_jour>/", 
         PerformanceAgent.as_view(), 
         name="performance-agent")

]
