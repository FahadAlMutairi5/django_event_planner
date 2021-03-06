from django.shortcuts import render
from rest_framework.generics import (
ListAPIView,
CreateAPIView,
RetrieveUpdateAPIView,
RetrieveAPIView,
)
from rest_framework.views import APIView
from events.models import Event, Booking
import datetime
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .permissions import IsOrganizer
from .serializers import (
EventListSerializer,
UserCreateSerializer,
EventCreateUpdateSerializer,
EventDetailSerializer,
MyBookingsSerializer,
BookSerializer,
)


class EventListView(ListAPIView):
    queryset = Event.objects.all().filter(dateandtime__gte = datetime.datetime.today())
    serializer_class = EventListSerializer
    permission_classes = [AllowAny]



class UserCreateView(CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]

class EventCreateView(CreateAPIView):
    serializer_class = EventCreateUpdateSerializer
    permission_classes = [IsAdminUser,]
    def perform_create(self, serializer):
        serializer.save(organizer = self.request.user)

class EventUpdateView(RetrieveUpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventCreateUpdateSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'event_id'
    permission_classes = [IsAuthenticated,IsOrganizer]


class EventDetailView(RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventDetailSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'event_id'
    permission_classes = [AllowAny,]

class OrganizerEventsView(ListAPIView):
    serializer_class = EventListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Event.objects.filter(organizer= self.request.user)


class MyBookingsView(ListAPIView):
    serializer_class = MyBookingsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):        
        # bookings = Booking.objects.filter(user=self.request.user)
        bookings = self.request.user.bookings.all()
        return bookings


class BookView(CreateAPIView):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated,]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user,)

