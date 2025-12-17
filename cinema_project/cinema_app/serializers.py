from rest_framework import serializers
from .models import Genre, Hall, JobPosition, Employee, Movie, Customer, Session, Ticket


class GenreSerializer(serializers.ModelSerializer):
    movie_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Genre
        fields = ['genre_id', 'name', 'movie_count']
        read_only_fields = ['genre_id']
    
    def get_movie_count(self, obj):
        return obj.movies.count()


class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = ['hall_id', 'name', 'capacity', 'type']
        read_only_fields = ['hall_id']


class JobPositionSerializer(serializers.ModelSerializer):
    employee_count = serializers.SerializerMethodField()
    
    class Meta:
        model = JobPosition
        fields = ['position_id', 'title', 'description', 'employee_count']
        read_only_fields = ['position_id']
    
    def get_employee_count(self, obj):
        return obj.employees.count()


class EmployeeSerializer(serializers.ModelSerializer):
    position_title = serializers.CharField(source='position.title', read_only=True)
    
    class Meta:
        model = Employee
        fields = [
            'employee_id', 'name', 'position', 'position_title',
            'salary', 'hire_date', 'phone'
        ]
        read_only_fields = ['employee_id']


class MovieSerializer(serializers.ModelSerializer):
    genre_name = serializers.CharField(source='genre.name', read_only=True)
    session_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Movie
        fields = [
            'movie_id', 'title', 'genre', 'genre_name', 'duration',
            'age_limit', 'release_year', 'description', 'rating', 'session_count'
        ]
        read_only_fields = ['movie_id']
    
    def get_session_count(self, obj):
        return obj.sessions.count()


class CustomerSerializer(serializers.ModelSerializer):
    ticket_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Customer
        fields = ['customer_id', 'name', 'email', 'phone', 'ticket_count']
        read_only_fields = ['customer_id']
    
    def get_ticket_count(self, obj):
        return obj.tickets.count()


class SessionSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    hall_name = serializers.CharField(source='hall.name', read_only=True)
    available_seats = serializers.SerializerMethodField()
    
    class Meta:
        model = Session
        fields = [
            'session_id', 'movie', 'movie_title', 'hall', 'hall_name',
            'start_time', 'price', 'available_seats'
        ]
        read_only_fields = ['session_id']
    
    def get_available_seats(self, obj):
        occupied = obj.tickets.count()
        return obj.hall.capacity - occupied


class TicketSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source='session.movie.title', read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    session_time = serializers.DateTimeField(source='session.start_time', read_only=True)
    
    class Meta:
        model = Ticket
        fields = [
            'ticket_id', 'session', 'customer', 'seat_number',
            'purchase_date', 'movie_title', 'customer_name', 'session_time'
        ]
        read_only_fields = ['ticket_id']
    
    def validate(self, data):

        session = data.get('session')
        seat_number = data.get('seat_number')
        
        if Ticket.objects.filter(session=session, seat_number=seat_number).exists():
            raise serializers.ValidationError(
                f"Місце {seat_number} вже зайняте на цьому сеансі"
            )

        if seat_number > session.hall.capacity:
            raise serializers.ValidationError(
                f"Місце {seat_number} не існує. Максимальна кількість місць: {session.hall.capacity}"
            )
        
        return data