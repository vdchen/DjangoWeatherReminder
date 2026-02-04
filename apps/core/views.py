from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Subscription
from .serializers import SubscriptionSerializer

class SubscriptionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows subscriptions to be viewed or edited.
    """
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # IMPORTANT: Only return subscriptions belonging to the current user
        return Subscription.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # The serializer needs the request context to access 'request.user'
        serializer.save()