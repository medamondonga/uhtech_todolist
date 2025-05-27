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
    class CustomCreateView(CreateModelMixin, GenericAPIView):
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
                    "status": True,
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

def list_filter_by_fields(model, serializer, filters: dict):
    """
    Retourne une vue listant les objets du modèle filtrés par plusieurs paramètres dynamiques.

    Args:
        model: Le modèle Django à utiliser.
        serializer: Le serializer correspondant au modèle.
        filters: Un dictionnaire contenant les champs et les valeurs à filtrer (ex: {"statut": "terminee"}).

    Returns:
        class: Une classe de vue Django REST Framework.
    """

    class ListFiltered(ListModelMixin, AuthenticatedAPIView):
        serializer_class = serializer

        def get_queryset(self):
            return model.objects.filter(**filters)

        def get(self, request, *args, **kwargs):
            return self.list(request, *args, **kwargs)

    return ListFiltered

def list_filter_two_fields(model, serializer, param_name: str, filters: dict):
    """
    Vue générique filtrant un modèle par un champ transmis dans l'URL + autres filtres fixes.

    Args:
        model: Le modèle à utiliser.
        serializer: Le serializer.
        param_name: Le nom du paramètre URL (ex: "projet_id").
        filters: Un dictionnaire des autres conditions à appliquer (ex: {"statut": "terminee"}).

    Exemple : /projets/<int:projet_id>/taches_terminees/
    """

    class FilteredListView(ListModelMixin, AuthenticatedAPIView):
        serializer_class = serializer

        def get_queryset(self):
            id_value = self.kwargs.get(param_name)
            return model.objects.filter(**{param_name.replace('_id', ''): id_value}, **filters)

        def get(self, request, *args, **kwargs):
            return self.list(request, *args, **kwargs)

    return FilteredListView

def list_filter_by_related_field(model, serializer, param_name: str, field_lookup: str):
    """
    Vue générique filtrant les objets par un champ ForeignKey profond, passé via l’URL.

    Args:
        model: Le modèle à interroger.
        serializer: Le serializer à utiliser.
        param_name: Le nom du paramètre URL (ex: "departement_id").
        field_lookup: Le champ à filtrer (ex: "poste__departement").

    Exemple: /departements/<int:departement_id>/employees/
    """

    class FilteredListView(ListModelMixin, AuthenticatedAPIView):
        serializer_class = serializer

        def get_queryset(self):
            value = self.kwargs.get(param_name)
            return model.objects.filter(**{field_lookup: value})

        def get(self, request, *args, **kwargs):
            return self.list(request, *args, **kwargs)

    return FilteredListView

