from django.urls import path
from .views import summarize_view, classify_view, sentiment_view, keywords_view

urlpatterns = [
    path('text-summary/', summarize_view, name='summarize'),
    path('classify-text/', classify_view, name='classify'),
    path('sentiment/', sentiment_view, name='sentiment'),
    path('keywords/', keywords_view, name='keywords'),
]
