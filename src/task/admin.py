"""
Administration des utilisateurs
"""
from django.contrib import admin
from .models import Tache, Projet

admin.site.register(Tache)
admin.site.register(Projet)
