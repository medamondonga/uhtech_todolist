"""Vue permettant de lister les tâches liées à un projet spécifique."""

from django.shortcuts import get_object_or_404
from rest_framework.mixins import ListModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Tache
from .serializers import TacheSerializer




class AcceptTache(APIView):
    def patch(self, request, id_tache):
        tache = get_object_or_404(Tache, id=id_tache)
        agent = request.user
        tache.assigne_a.add(agent) 
        try:
            tache.pending_task(agent)
            return Response({
                "message": "Tache accepté"
            },
                            status=status.HTTP_200_OK)
        except ValueError :
            return Response({
                "message": "erreur"
            })
