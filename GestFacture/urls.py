from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Factures.urls')),  # Remplacez 'nom_de_votre_application' par le nom de votre application
]

