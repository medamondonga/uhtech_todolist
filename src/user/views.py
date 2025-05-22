"""Vue permettant de lister les tâches liées à un projet spécifique."""

from rest_framework.mixins import ListModelMixin
from rest_framework.generics import GenericAPIView
from .models import Departement, Poste, User
from .serializers import DepartementSerializer, UserSerializer, PosteSerializer


class PosteDepartementView(ListModelMixin, GenericAPIView):
    """
    Vue basée sur GenericAPIView pour lister les postes d'un departement donné.

    Cette vue utilise le mixin ListModelMixin pour retourner toutes les tâches
    associées à un identifiant de projet passé via l'URL.
    """

    serializer_class = PosteSerializer

    def get_queryset(self):
        """
        Retourne les tâches associées à un projet spécifique.

        Returns:
            QuerySet: Liste des objets Tache liés à l'ID du projet.
        """
        departement = self.kwargs.get('departement')  # récupère l'ID du ps depuis l'URL
        return Poste.objects.filter(departement=departement)

    def get(self, request, *args, **kwargs):
        """
        Gère les requêtes GET en utilisant le mixin ListModelMixin.

        Args:
            request (HttpRequest): La requête HTTP envoyée par le client.
            *args: Arguments supplémentaires.
            **kwargs: Arguments nommés supplémentaires.

        Returns:
            Response: Une réponse contenant la liste des postes filtrées.
        """
        return self.list(request, *args, **kwargs)
