
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    GenreViewSet,
    HallViewSet,
    JobPositionViewSet,
    EmployeeViewSet,
    MovieViewSet,
    CustomerViewSet,
    SessionViewSet,
    TicketViewSet,
    CinemaReportAPI
)


router = DefaultRouter()

router.register(r'genres', GenreViewSet, basename='genre')
router.register(r'halls', HallViewSet, basename='hall')
router.register(r'positions', JobPositionViewSet, basename='position')
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'movies', MovieViewSet, basename='movie')
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'sessions', SessionViewSet, basename='session')
router.register(r'tickets', TicketViewSet, basename='ticket')


urlpatterns = [
    path('', include(router.urls)),
    path('report/', CinemaReportAPI.as_view(), name='report'),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),

]