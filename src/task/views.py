"""Vue permettant de lister les tâches liées à un projet spécifique."""

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from todolist.generic_crud import list_filter_by_fields, list_filter_two_fields
from .models import Tache
from .serializers import TacheSerializer



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
