from django.urls import path
from .views import summarize_view

urlpatterns = [
    path('text-summary/', summarize_view, name='summarize'),
]
