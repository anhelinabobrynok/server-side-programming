from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg

from .models import Genre, Hall, JobPosition, Employee, Movie, Customer, Session, Ticket
from .serializers import (
    GenreSerializer, HallSerializer, JobPositionSerializer,
    EmployeeSerializer, MovieSerializer, CustomerSerializer,
    SessionSerializer, TicketSerializer
)
from .unit_of_work import UnitOfWork

class CinemaReportAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        try:
            total_movies = Movie.objects.count()
            
            aggregation = Movie.objects.aggregate(avg_val=Avg('duration'))
            avg_duration = aggregation['avg_val']
            
            if avg_duration is None:
                avg_duration = 0

            report_data = {
                "report_name": "Cinema General Statistics",
                "total_movies_count": total_movies,
                "average_duration_minutes": round(avg_duration, 1),
                "status": "success"
            }

            return Response(report_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {
                    "error": "Internal Server Error", 
                    "details": str(e)
                }, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class GenreViewSet(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.uow = UnitOfWork()
    
    def get_queryset(self):
        return self.uow.genres.get_all()

    @action(detail=False, methods=['get'])
    def popular(self, request):
        limit = int(request.query_params.get('limit', 5))
        genres = self.uow.genres.get_popular_genres(limit=limit)
        serializer = self.get_serializer(genres, many=True)
        return Response(serializer.data)


class MovieViewSet(viewsets.ModelViewSet):
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.uow = UnitOfWork()
    
    def get_queryset(self):
        return self.uow.movies.get_all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        movie = self.uow.movies.create(**serializer.validated_data)
        return Response(self.get_serializer(movie).data, status=status.HTTP_201_CREATED)


class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.uow = UnitOfWork()
    
    def get_queryset(self):
        return self.uow.customers.get_all()

    @action(detail=False, methods=['get'])
    def active(self, request):
        customers = self.uow.customers.get_active_customers()
        serializer = self.get_serializer(customers, many=True)
        return Response(serializer.data)


class SessionViewSet(viewsets.ModelViewSet):
    serializer_class = SessionSerializer
    permission_classes = [IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.uow = UnitOfWork()
    
    def get_queryset(self):
        return self.uow.sessions.get_all()

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        sessions = self.uow.sessions.get_upcoming_sessions()
        serializer = self.get_serializer(sessions, many=True)
        return Response(serializer.data)


class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.uow = UnitOfWork()
    
    def get_queryset(self):
        return self.uow.tickets.get_all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        session_input = serializer.validated_data.get('session')
        session_id = session_input.id if hasattr(session_input, 'id') else session_input
        seat_number = serializer.validated_data['seat_number']
        
        if not self.uow.tickets.is_seat_available(session_id, seat_number):
            return Response(
                {'error': f'Seat {seat_number} is already taken'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        ticket = self.uow.tickets.create(**serializer.validated_data)
        return Response(self.get_serializer(ticket).data, status=status.HTTP_201_CREATED)


class HallViewSet(viewsets.ModelViewSet):
    serializer_class = HallSerializer
    permission_classes = [IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.uow = UnitOfWork()
    
    def get_queryset(self):
        return self.uow.halls.get_all()


class EmployeeViewSet(viewsets.ModelViewSet):
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.uow = UnitOfWork()
    
    def get_queryset(self):
        return self.uow.employees.get_all()


class JobPositionViewSet(viewsets.ModelViewSet):
    serializer_class = JobPositionSerializer
    permission_classes = [IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.uow = UnitOfWork()
    
    def get_queryset(self):
        return self.uow.job_positions.get_all()