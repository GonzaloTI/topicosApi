from django.urls import path
from .views import consulta

urlpatterns = [
    path('query/', consulta, name='document-query'),
]