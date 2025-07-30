from django.urls import path
from .views import summarize_view, classify_view

urlpatterns = [
    path('text-summary/', summarize_view, name='summarize'),
    path('classify-text/', classify_view, name='classify'),
]
