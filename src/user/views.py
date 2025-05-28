from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin
from rest_framework.generics import GenericAPIView
from todolist.generic_crud import list_filtered_view
from .models import User
from .serializers import UserSerializer

CREATED = "Création réussie"

class RegisterView(CreateModelMixin, GenericAPIView):
        """
        Vue générique pour créer un objet.
        """
        queryset = User.objects.all()
        serializer_class = UserSerializer
        permission_classes = [AllowAny]

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


EmployeesByDepartement =list_filtered_view(
    model=User,
    serializer=UserSerializer,
    url_param="poste_id",
    field_lookup="poste__departement"
)
