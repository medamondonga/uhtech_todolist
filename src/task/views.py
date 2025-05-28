"""Vue permettant de lister les tâches liées à un projet spécifique."""
from datetime import datetime, timedelta
from django.db.models import Avg
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from todolist.generic_crud import list_filtered_view
from todolist.permissions import IsAdmin, IsAgent, IsManager
from .models import Tache, Projet
from .serializers import TacheListSerializer, ProjetListSerializer



User = get_user_model()



class FinishTache(APIView):
    """
    Vue permettant de marquer une tâche comme terminée.
    """
    permission_classes = [IsAuthenticated]

    def patch(self, request, id_tache):
        """
        Méthode PATCH pour mettre à jour le statut d'une tâche comme terminée.
        """
        tache = get_object_or_404(Tache, id=id_tache)
        agent =tache.assigne_a
        manager = tache.assigne_par
        try:
            if request.user == agent or request.user == manager:
                tache.finish_task()
                return Response(
                    {"message": "Tache terminée"},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"message": "Cette tache ne vous apartient pas! "},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        except ValueError:
            return Response(
                {"message": "erreur"},
                status=status.HTTP_400_BAD_REQUEST
            )


class AssigneTacheAPIView(APIView):
    """
    Vue pour assigner une tâche à un seul agent (champ ForeignKey).
    """
    permission_classes = [IsAuthenticated, IsManager]

    def patch(self, request, id_tache):
        tache = get_object_or_404(Tache, id=id_tache)
        id_agent = request.data.get("agent")

        if not id_agent:
            return Response(
                {"message": "L'ID de l'agent est requis."},
                status=status.HTTP_400_BAD_REQUEST
            )

        agent = get_object_or_404(User, id=id_agent)
        tache.assignee_tache(agent)

        return Response(
            {"message": "Tâche assignée avec succès."},
            status=status.HTTP_200_OK
        )



# Vue listant toutes les tâches dont le statut est "terminée"
ListTacheProjet = list_filtered_view(
    model= Tache,
    serializer= TacheListSerializer,
    url_param = "projet_id"
)

ListTachesTerminees = list_filtered_view(
    model=Tache,
    serializer=TacheListSerializer,
    url_param="projet_id",
    filters={"statut": "terminee"}
)

# Vue listant les tâches terminées pour un projet donné
TachesTermineesParProjet = list_filtered_view(
    model=Tache,
    serializer=TacheListSerializer,
    url_param="projet_id",
    field_lookup="projet",
    filters={"statut": "terminee"}
)

# Vue listant les tâches en cours pour un projet donné
TachesEncoursParProjet = list_filtered_view(
    model=Tache,
    serializer=TacheListSerializer,
    url_param="projet_id",
    field_lookup="projet",
    filters={"statut": "en_cours"}
)

TachesEnretardParProjet = list_filtered_view(
    model=Tache,
    serializer= TacheListSerializer,
    url_param="projet_id",
    field_lookup="projet",
    filters={"statut": "en_retard"}
)

ListTacheAgent= list_filtered_view(
    model=Tache,
    serializer=TacheListSerializer,
    url_param="assigne_a_id",
    field_lookup="assigne_a"

)



class PerformanceAgent(APIView):
    """
    Vue pour calculer la performance (taux de réactivité + taux de respect)
    d’un agent sur une période de X jours.
    """

    def get(self, request, id_agent, nombre_jour):
        try:
            agent = User.objects.get(id=id_agent)
        except User.DoesNotExist:
            return Response({"detail": "Agent introuvable"}, status=status.HTTP_404_NOT_FOUND)

        date_limite = datetime.now().date() - timedelta(days=nombre_jour)

        # Toutes les tâches assignées à cet agent, commencées depuis X jours
        taches = Tache.objects.filter(
            assigne_a=agent,
            date_debut__gte=date_limite
        ).distinct()

        total = taches.count()

        # Tâches terminées uniquement
        taches_terminees = taches.filter(statut="terminee")
        nb_terminees = taches_terminees.count()

        # Moyenne des taux de respect de délais
        if nb_terminees > 0:
            moyenne_respect = taches_terminees.aggregate(
                moyenne=Avg("taux_respect_delais")
            )["moyenne"]
        else:
            moyenne_respect = 0

        # Taux de réactivité = % de tâches terminées dans la période
        taux_reactivite = (nb_terminees / total * 100) if total else 0

        return Response({
            "agent": agent.username,
            "periode": f"{nombre_jour} derniers jours",
            "nombre_taches_total": total,
            "taux_reactivite": f"{round(taux_reactivite, 2)}%",
            "taux_respect_delais": f"{round(moyenne_respect or 0, 2)}%",
        })
