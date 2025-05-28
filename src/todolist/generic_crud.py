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
def create_customized(model, serializer, permissions=None):
    """
    Reçoit un modèle et un serializer, et retourne une vue qui permet la création d'un objet.
    """
    class CustomCreateView(CreateModelMixin, GenericAPIView):
        """
        Vue générique pour créer un objet.
        """
        queryset = model.objects.all()
        serializer_class = serializer
        permission_classes = AuthenticatedAPIView.permission_classes + (permissions or [])

        def post(self, request, *args, **kwargs):
            """
            Gère la requête POST pour créer un objet.
            """
            response = self.create(request, *args, **kwargs)

            if response.status_code == status.HTTP_201_CREATED:
                return Response({
                    "status": True,
                    "message": f"{CREATED}"
                }, status=status.HTTP_201_CREATED)
            return response

    return CustomCreateView

#Fonction générique pour lister les objets
def list_customized(model, serializer, permissions=None):
    class ListCustomView(ListModelMixin, AuthenticatedAPIView):
        queryset = model.objects.all()
        serializer_class = serializer
        permission_classes = AuthenticatedAPIView.permission_classes + (permissions or [])

        def get(self, request, *args, **kwargs):
            return self.list(request, *args, **kwargs)

    return ListCustomView

def detail_customized(model, serializer, permissions=None):
    """
    Vue permettant  de recuperer les informations d'un element
    """
    class DetailCustomView(RetrieveModelMixin, AuthenticatedAPIView):
        """
        Vue pour afficher les détails d’un objet.
        """
        queryset = model.objects.all()
        serializer_class = serializer
        permission_classes = AuthenticatedAPIView.permission_classes + (permissions or [])

        def get(self, request, *args, **kwargs):
            """
            Gère la requête GET pour un seul objet (via son ID).
            """
            if kwargs.get('pk'):
                return self.retrieve(request, *args, **kwargs)
    return DetailCustomView


#Fonction générique pour les détails, la mise à jour et la suppression
def update_delete_customized(model, serializer, permissions=None):
    class UpdateCustomView(UpdateModelMixin, AuthenticatedAPIView):
        queryset = model.objects.all()
        serializer_class = serializer
        permission_classes = AuthenticatedAPIView.permission_classes + (permissions or [])

        def put(self, request, *args, **kwargs):
            response = self.update(request, *args, **kwargs)
            if response.status_code == status.HTTP_200_OK:
                return Response({"message": f"{MODIFIED}"}, status=status.HTTP_200_OK)
            return response

        def patch(self, request, *args, **kwargs):
            response = self.partial_update(request, *args, **kwargs)
            if response.status_code == status.HTTP_200_OK:
                return Response({"message": f"{MODIFIED}"}, status=status.HTTP_200_OK)
            return response

    class DeleteCustomView(DestroyModelMixin, AuthenticatedAPIView):
        queryset = model.objects.all()
        serializer_class = serializer
        permission_classes = AuthenticatedAPIView.permission_classes + (permissions or [])

        def delete(self, request, *args, **kwargs):
            instance = self.get_object()

            # Suppression logique ici
            instance.delete()  # Appelle le delete() redéfini dans SoftDeleteModel

            return Response({
                "message": f"{DELETED}"
            }, status=status.HTTP_204_NO_CONTENT)

    class CombineActionView(UpdateCustomView, DeleteCustomView):
        """
        Vue combinée pour gérer les actions :
        - PUT/PATCH : modifier
        - DELETE : supprimer logiquement
        """

    return CombineActionView


#Fonction générique pour afficher des elements grace à des filtre
def list_filtered_view(model, serializer, filters=None, url_param=None,
                       field_lookup=None, permissions=None):
    """
    Crée une vue de type GET filtrée selon un ou plusieurs critères.
    """

    class FilteredListView(ListModelMixin, AuthenticatedAPIView):
        serializer_class = serializer
        permission_classes = AuthenticatedAPIView.permission_classes + (permissions or [])

        def get_queryset(self):
            query = model.objects.all()

            # Filtrage dynamique depuis l’URL
            if url_param and field_lookup:
                value = self.kwargs.get(url_param)
                query = query.filter(**{field_lookup: value})

            # Copie locale des filtres pour éviter conflits entre instances
            local_filters = filters.copy() if filters else {}
            if local_filters:
                query = query.filter(**local_filters)

            return query

        def get(self, request, *args, **kwargs):
            return self.list(request, *args, **kwargs)

    return FilteredListView
