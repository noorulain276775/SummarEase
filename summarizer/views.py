from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .utils import (
    summarize_text,
    classify_text,
    analyze_sentiment,
    extract_keywords,
    classify_with_confidence,
)


@api_view(['POST'])
def summarize_view(request):
    text = request.data.get('text', '')
    max_sentences = request.data.get('max_sentences') or request.query_params.get('max_sentences')
    try:
        max_sentences = int(max_sentences) if max_sentences is not None else 3
    except ValueError:
        return Response({'error': 'max_sentences must be an integer'}, status=status.HTTP_400_BAD_REQUEST)

    if not text:
        return Response({'error': 'Text is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    summary = summarize_text(text, max_sentences=max_sentences)
    return Response({'summary': summary, 'max_sentences': max_sentences}, status=status.HTTP_200_OK)


@api_view(['POST'])
def classify_view(request):
    text = request.data.get('text', '')
    top_k = request.data.get('top_k') or request.query_params.get('top_k')
    try:
        top_k = int(top_k) if top_k is not None else 3
    except ValueError:
        return Response({'error': 'top_k must be an integer'}, status=400)

    if not text:
        return Response({'error': 'Text is required'}, status=400)

    category = classify_text(text)
    top = classify_with_confidence(text, top_k=top_k)
    return Response({'category': category, 'top': top})


@api_view(['POST'])
def sentiment_view(request):
    text = request.data.get('text', '')
    if not text:
        return Response({'error': 'Text is required'}, status=status.HTTP_400_BAD_REQUEST)
    sentiment = analyze_sentiment(text)
    return Response(sentiment, status=status.HTTP_200_OK)


@api_view(['POST'])
def keywords_view(request):
    text = request.data.get('text', '')
    top_k = request.data.get('top_k') or request.query_params.get('top_k')
    try:
        top_k = int(top_k) if top_k is not None else 10
    except ValueError:
        return Response({'error': 'top_k must be an integer'}, status=status.HTTP_400_BAD_REQUEST)
    if not text:
        return Response({'error': 'Text is required'}, status=status.HTTP_400_BAD_REQUEST)
    keywords = extract_keywords(text, top_k=top_k)
    return Response({'keywords': keywords}, status=status.HTTP_200_OK)