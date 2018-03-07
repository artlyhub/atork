from rest_framework import generics, permissions

from crowdfund.models import FundItem, Funder
from crowdfund.api.serializers import FundItemSerializer, FunderSerializer


class FundItemAPIView(generics.ListCreateAPIView):
    queryset = FundItem.objects.get_queryset().order_by('id')
    serializer_class = FundItemSerializer
    pagination_class = StandardResultPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(artist=self.request.user)


class FunderAPIView(generics.ListCreateAPIView):
    queryset = Funder.objects.get_queryset().order_by('id')
    serializer_class = FunderSerializer
    pagination_class = StandardResultPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(artist=self.request.user)
