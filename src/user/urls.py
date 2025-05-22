from django.urls import path
from todolist.generic_crud import (create_customized, list_customized,
                                   detail_update_delete_customized)
from .models import User, Departement, Poste
from .serializers import UserSerializer, PosteSerializer, DepartementSerializer
from .views import PosteDepartementView

urlpatterns=[
    path("register/",
        create_customized(User, UserSerializer).as_view(), name="inscription"),
    path("auth/profile/<int:pk>/",
         detail_update_delete_customized(User, UserSerializer).as_view(),
         name="user_action"),


    path("poste/new/",
         create_customized(Poste, PosteSerializer).as_view(),
         name="creer_poste"),
    path("poste//",
         list_customized(Poste, PosteSerializer).as_view(),
         name='liste_poste'),
    path("poste/<int:pk>/",
        detail_update_delete_customized(Poste, PosteSerializer).as_view(),
         name="poste_action"),


    path("departement/new/",
         create_customized(Departement, DepartementSerializer).as_view(),
         name="creer_departement"),
    path("departement//",
         list_customized(Departement, DepartementSerializer).as_view(),
         name='liste_departement'),
    path("departement/<int:pk>/",
         detail_update_delete_customized(Departement, DepartementSerializer).as_view(),
         name="departement_action"),

    path("<departement>/postes/",
         PosteDepartementView.as_view(),
         name="liste_poste"),
    
]