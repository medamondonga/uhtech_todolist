"""
Administration des utilisateurs
"""
from django.contrib import admin
from .models import User, Departement, Poste

admin.site.register(User)
admin.site.register(Departement)
admin.site.register(Poste)

