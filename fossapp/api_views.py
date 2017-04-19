from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import News
from .serializers import NewsSerializer


@api_view(['GET', ])
def news_detail(request, pk):
    try:
        obj = News.objects.get(pk=pk)
    except News.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = NewsSerializer(obj)
        return Response(serializer.data)

