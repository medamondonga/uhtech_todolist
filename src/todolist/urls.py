"""
URL configuration for todolist project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Gestion des taches API",
      default_version='v1',
      description="""
    API RESTful pour la gestion des tâches, des utilisateurs, des projets et des performances des employés.

    Fonctionnalités principales :
    - 🔐 Authentification via token (inscription, connexion, gestion du profil)
    - 👩🏽‍💼 Gestion des utilisateurs avec rôles (manager / agent)
    - 🗂 Suivi des projets et des tâches associées (création, mise à jour, filtrage par statut ou assignation)
    - 📊 Suivi des performances : taux de respect des délais, réactivité
    - 🏢 Gestion des structures internes : départements et postes

    Cette API est conçue pour être utilisée par une interface frontend (web ou mobile) et fournit tous les endpoints nécessaires pour construire une solution complète de gestion d’équipe.

    Pour accéder aux endpoints protégés, cliquez sur le bouton **Authorize** et entrez votre token au format : Token votre_token
    """
,
      contact=openapi.Contact(email="medamondonga4@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("user.urls")),
    path("auth/", include('dj_rest_auth.urls')),
    path("task/", include('task.urls')),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
