from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .utils import summarize_text


@api_view(['POST'])
def summarize_view(request):
    text = request.data.get('text', '')

    if not text:
        return Response({'error': 'Text is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    summary = summarize_text(text)
    return Response({'summary': summary}, status=status.HTTP_200_OK)
