from rest_framework import viewsets, generics
from rest_framework import filters
from .serializers import IndexSerializer
from .models import Index


class IndexViewSet(viewsets.ModelViewSet):
    # search_fields = ['words']
    search_fields = ['^words']
    # search_fields = ['@words']
    filter_backends = (filters.SearchFilter,)
    queryset = Index.objects.all().order_by('-occurrences')
    serializer_class = IndexSerializer
