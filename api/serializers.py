from rest_framework import serializers
from events.models import Event, Booking
from django.contrib.auth.models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',]

class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'



class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        new_user = User(username=username)
        new_user.set_password(password)
        new_user.save()
        return validated_data

class EventCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'name',
            'dateandtime',
            'time',
            'description',
            'place',
            'number_of_tickets',
            'poster',
        ]       

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['__all__']

class EventDetailSerializer(serializers.ModelSerializer):
  
    people_who_booked_my_event = serializers.SerializerMethodField()
    class Meta:
        model = Event
        fields = [
            'id',
            'name',
            'description',
            'organizer',
            'people_who_booked_my_event',
            'number_of_tickets',
            ]

    def get_people_who_booked_my_event(self, obj):
        people_who_booked_my_event = Booking.objects.filter(event=obj).values_list("user__username")
        return people_who_booked_my_event


class MyBookingsSerializer(serializers.ModelSerializer):

    event = EventListSerializer()
    class Meta:
        model = Booking
        fields = ['event', 'number_of_booking']


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = [
            'event',
            'number_of_booking',
        ]
    
    def validate(self, data):
        event_object = data.get('event')
        seats_left = int(data.get('number_of_booking'))
        if event_object.seats_left() == 0:
            raise serializers.ValidationError("no seats avilable at theis time ") 
        elif seats_left > event_object.seats_left():
            raise serializers.ValidationError("you exceede the number of seats ")
        return data