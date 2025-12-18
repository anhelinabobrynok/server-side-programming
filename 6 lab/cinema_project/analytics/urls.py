from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
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

# НОВИЙ ІМПОРТ
from .analytics_views import (
    RevenueByGenreAPI,
    MonthlyRevenueAPI,
    HallUtilizationAPI,
    MoviePopularityByYearAPI,
    CustomerSegmentsAPI,
    EmployeeSalaryStatsAPI
)
from .dashboard_plotly import analytics_dashboard       
from .dashboard_bokeh import bokeh_dashboard            
from .parallel_computing import parallel_performance_dashboard

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
    path('api/', include(router.urls)),
    path('report/', CinemaReportAPI.as_view(), name='report'),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    
    path('analytics/revenue-by-genre/', RevenueByGenreAPI.as_view(), name='revenue_by_genre'),
    path('analytics/monthly-revenue/', MonthlyRevenueAPI.as_view(), name='monthly_revenue'),
    path('analytics/hall-utilization/', HallUtilizationAPI.as_view(), name='hall_utilization'),
    path('analytics/movie-popularity/', MoviePopularityByYearAPI.as_view(), name='movie_popularity'),
    path('analytics/customer-segments/', CustomerSegmentsAPI.as_view(), name='customer_segments'),
    path('analytics/employee-salaries/', EmployeeSalaryStatsAPI.as_view(), name='employee_salaries'),
    
    path('dashboard/', analytics_dashboard, name='analytics_dashboard'),
    path('dashboard/bokeh/', bokeh_dashboard, name='analytics_bokeh'),
    path('dashboard/performance/', parallel_performance_dashboard, name='parallel_dashboard'),
    
]