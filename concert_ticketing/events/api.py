from rest_framework import serializers, viewsets
from .models import Event, Ticket

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=True)
    
    class Meta:
        model = Event
        fields = '__all__'

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer