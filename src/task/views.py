"""Vue permettant de lister les tâches liées à un projet spécifique."""
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from todolist.generic_crud import list_filter_by_fields, list_filter_two_fields
from .models import Tache
from .serializers import TacheSerializer
from django.db.models import Avg


User = get_user_model()



class FinishTache(APIView):
    """
    Vue permettant de marquer une tâche comme terminée.
    """

    def patch(self, request, id_tache):
        """
        Méthode PATCH pour mettre à jour le statut d'une tâche comme terminée.
        """
        tache = get_object_or_404(Tache, id=id_tache)
        try:
            tache.finish_task()
            return Response(
                {"message": "Tache terminée"},
                status=status.HTTP_200_OK
            )
        except ValueError:
            return Response(
                {"message": "erreur"},
                status=status.HTTP_400_BAD_REQUEST
            )

class AssigneTacheAPIView(APIView):
    """
    Vue permettant d'assigner une tâche à un ou plusieurs agents.
    """

    def patch(self, request, id_tache):
        tache = get_object_or_404(Tache, id=id_tache)
        assignateur = request.user

        ids_agents = request.data.get("agents")  # Expects a list of user IDs

        if not ids_agents:
            return Response(
                {"message": "Liste d'agents requise pour l'assignation."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            agents = User.objects.filter(id__in=ids_agents)
            if not agents.exists():
                return Response(
                    {"message": "Aucun agent valide trouvé."},
                    status=status.HTTP_404_NOT_FOUND
                )

            tache.assignee_tache(assignateur, agents)

            return Response(
                {"message": "Tâche assignée avec succès."},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"message": f"Erreur lors de l'assignation : {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

# Vue listant toutes les tâches dont le statut est "terminée"
ListTachesTerminees = list_filter_by_fields(
    model=Tache,
    serializer=TacheSerializer,
    filters={"statut": "terminee"}
)

# Vue listant les tâches terminées pour un projet donné
TachesTermineesParProjet = list_filter_two_fields(
    model=Tache,
    serializer=TacheSerializer,
    param_name="projet_id",
    filters={"statut": "terminee"}
)

# Vue listant les tâches en cours pour un projet donné
TachesEncoursParProjet = list_filter_two_fields(
    model=Tache,
    serializer=TacheSerializer,
    param_name="projet_id",
    filters={"statut": "en_cours"}
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
