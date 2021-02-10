from game.models import Card
from rest_framework import viewsets
from rest_framework import permissions
from game.serilizators.card_serializer import CardSerializer


class CardViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Card.objects.all().order_by('-id')
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticated]

from rest_framework.views import APIView
from rest_framework.response import Response

class TestView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        return Response({'message': 'ok'})