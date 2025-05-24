"""
Fichier des mixins pour l'application de gestion de stock
"""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import (
    ListModelMixin, CreateModelMixin,
    UpdateModelMixin, RetrieveModelMixin,
    DestroyModelMixin
)
from rest_framework.generics import GenericAPIView

# Messages personnalisés de retour
CREATED = "Création réussie"
DELETED = "Suppression réussie"
MODIFIED = "Modification réussie"

class AuthenticatedAPIView(GenericAPIView):
    """
    Vue Generic qui protège les endpoints
    """
    permission_classes = [IsAuthenticated]


#Fonction générique de création
def create_customized(model, serializer):
    """
    Reçoit un modèle et un serializer, et retourne une vue qui permet la création d'un objet.
    """
    class CustomCreateView(CreateModelMixin, AuthenticatedAPIView):
        """
        Vue générique pour créer un objet.
        """
        queryset = model.objects.all()
        serializer_class = serializer

        def post(self, request, *args, **kwargs):
            """
            Gère la requête POST pour créer un objet.
            """
            response = self.create(request, *args, **kwargs)

            if response.status_code == status.HTTP_201_CREATED:
                return Response({
                    "message": f"{CREATED}"
                }, status=status.HTTP_201_CREATED)
            return response

    return CustomCreateView

#Fonction générique pour lister les objets
def list_customized(model, serializer):
    """
    Reçoit un modèle et un serializer, et retourne une vue qui permet de lister les objets.
    """
    class ListCustomView(ListModelMixin, AuthenticatedAPIView):
        """
        Vue générique pour lister les objets.
        """
        queryset = model.objects.all()
        serializer_class = serializer

        def get(self, request, *args, **kwargs):
            """
            Gère la requête GET pour retourner tous les objets.
            """
            return self.list(request, *args, **kwargs)

    return ListCustomView

#Fonction générique pour les détails, la mise à jour et la suppression
def detail_update_delete_customized(model, serializer):
    """
    Reçoit un modèle et un serializer, et retourne une vue permettant :
    - d'obtenir les détails d'un objet
    - de le modifier
    - de le supprimer
    """

    class DetailCustomView(RetrieveModelMixin, AuthenticatedAPIView):
        """
        Vue pour afficher les détails d’un objet.
        """
        queryset = model.objects.all()
        serializer_class = serializer

        def get(self, request, *args, **kwargs):
            """
            Gère la requête GET pour un seul objet (via son ID).
            """
            if kwargs.get('pk'):
                return self.retrieve(request, *args, **kwargs)

    class UpdateCustomView(UpdateModelMixin, AuthenticatedAPIView):
        """
        Vue pour mettre à jour un objet.
        """
        queryset = model.objects.all()
        serializer_class = serializer

        def put(self, request, *args, **kwargs):
            """
            Gère la requête PUT pour modifier **tout** l'objet.
            """
            response = self.update(request, *args, **kwargs)
            if response.status_code == status.HTTP_200_OK:
                return Response({
                    "message": f"{MODIFIED}"
                }, status=status.HTTP_200_OK)
            return response

        def patch(self, request, *args, **kwargs):
            """
            Gère la requête PATCH pour modifier **partiellement** l'objet.
            """
            response = self.partial_update(request, *args, **kwargs)
            if response.status_code == status.HTTP_200_OK:
                return Response({
                    "message": f"{MODIFIED}"
                }, status=status.HTTP_200_OK)
            return response

    class DeleteCustomView(DestroyModelMixin, AuthenticatedAPIView):
        """
        Vue pour supprimer un objet.
        """
        queryset = model.objects.all()
        serializer_class = serializer

        def delete(self, request, *args, **kwargs):
            """
            Gère la requête DELETE pour supprimer un objet.
            """
            response = self.destroy(request, *args, **kwargs)
            if response.status_code == status.HTTP_204_NO_CONTENT:
                return Response({
                    "message": f"{DELETED}"
                }, status=status.HTTP_204_NO_CONTENT)
            return response

    class CombineActionView(UpdateCustomView, DetailCustomView, DeleteCustomView):
        """
        Vue combinée pour gérer les actions :
        - GET : afficher les détails
        - PUT/PATCH : modifier
        - DELETE : supprimer
        """

    return CombineActionView

#Fonction générique pour afficher des elements grace à des filtre
def list_filter_one_parameter(model, serializer, element):
    """
    Retourne une vue listant les objets du modèle filtrés par un paramètre dynamique.
    
    Args:
        model: Le modèle Django à utiliser.
        serializer: Le serializer correspondant au modèle.
        element: Le nom du champ utilisé pour filtrer (doit être dans les kwargs).
    
    Returns:
        class: Une classe de vue Django REST Framework.
    """

    class ListFilterOne(ListModelMixin, AuthenticatedAPIView):
        """
        Vue générique pour lister les objets filtrés par un paramètre donné via l'URL.
        """

        serializer_class = serializer

        def get_queryset(self):
            """
            Récupère les objets du modèle filtrés dynamiquement avec le champ spécifié.
            """
            value = self.kwargs.get(element)  # Récupère la valeur passée dans l'URL
            return model.objects.filter(**{element: value})  # Utilisation du nom de champ dynamique

        def get(self, request, *args, **kwargs):
            """
            Gère la requête GET pour retourner la liste filtrée.
            """
            return self.list(request, *args, **kwargs)

    return ListFilterOne
