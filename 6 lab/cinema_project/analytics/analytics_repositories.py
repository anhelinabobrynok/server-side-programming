from django.db.models import Count, Avg, Sum, Q, F, Max, Min
from django.db.models.functions import TruncMonth, TruncDate, ExtractYear
from .models import Movie, Session, Ticket, Genre, Employee, Customer, Hall


class AnalyticsRepository:
    @staticmethod
    def get_revenue_by_genre():
        return (
            Genre.objects
            .annotate(
                total_tickets=Count('movies__sessions__tickets'),
                total_revenue=Sum('movies__sessions__tickets__session__price'),
                avg_ticket_price=Avg('movies__sessions__price'),
                movie_count=Count('movies', distinct=True),
                session_count=Count('movies__sessions', distinct=True)
            )
            .filter(total_tickets__gt=0) 
            .order_by('-total_revenue')
        )
    
    @staticmethod
    def get_monthly_revenue_stats():
        return (
            Session.objects
            .annotate(month=TruncMonth('start_time'))
            .values('month')
            .annotate(
                total_sessions=Count('session_id'),
                tickets_sold=Count('tickets'),
                total_revenue=Sum(F('tickets__session__price')),
                avg_session_price=Avg('price'),
                unique_customers=Count('tickets__customer', distinct=True)
            )
            .filter(tickets_sold__gt=0)
            .order_by('month')
        )
    
    @staticmethod
    def get_hall_utilization():
        return (
            Hall.objects
            .annotate(
                total_sessions=Count('sessions'),
                total_capacity=Sum('capacity'),
                tickets_sold=Count('sessions__tickets'),
                avg_occupancy_rate=Count('sessions__tickets') * 100.0 / F('capacity'),
                total_potential_revenue=Sum(F('sessions__price') * F('capacity')),
                actual_revenue=Sum('sessions__tickets__session__price')
            )
            .filter(total_sessions__gt=0)
            .order_by('-avg_occupancy_rate')
        )
    
    @staticmethod
    def get_movie_popularity_by_year():
        return (
            Movie.objects
            .annotate(year=F('release_year'))
            .values('year')
            .annotate(
                movie_count=Count('movie_id', distinct=True),
                total_sessions=Count('sessions'),
                tickets_sold=Count('sessions__tickets'),
                avg_rating=Avg('rating'),
                total_revenue=Sum('sessions__tickets__session__price'),
                avg_price=Avg('sessions__price')
            )
            .filter(tickets_sold__gt=0)
            .order_by('-year')
        )
    
    @staticmethod
    def get_customer_segments():
        return (
            Customer.objects
            .annotate(
                tickets_purchased=Count('tickets'),
                total_spent=Sum('tickets__session__price'),
                avg_ticket_price=Avg('tickets__session__price'),
                first_purchase=Min('tickets__purchase_date'),
                last_purchase=Max('tickets__purchase_date'),
                favorite_genre=Count('tickets__session__movie__genre')
            )
            .filter(tickets_purchased__gte=1) 
            .order_by('-total_spent')
        )
    
    @staticmethod
    def get_employee_salary_by_position():
        return (
            Employee.objects
            .values('position__title', 'position_id')
            .annotate(
                employee_count=Count('employee_id'),
                avg_salary=Avg('salary'),
                min_salary=Min('salary'),
                max_salary=Max('salary'),
                total_payroll=Sum('salary'),
                salary_range=Max('salary') - Min('salary')
            )
            .filter(employee_count__gte=1)
            .order_by('-avg_salary')
        )