import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .analytics_repositories import AnalyticsRepository


class RevenueByGenreAPI(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            queryset = AnalyticsRepository.get_revenue_by_genre()
            data = list(queryset.values(
                'name',
                'total_tickets',
                'total_revenue',
                'avg_ticket_price',
                'movie_count',
                'session_count'
            ))
            
            for item in data:
                if item['total_revenue']:
                    item['total_revenue'] = float(item['total_revenue'])
                if item['avg_ticket_price']:
                    item['avg_ticket_price'] = float(item['avg_ticket_price'])
            
            return Response({
                'success': True,
                'data': data,
                'count': len(data)
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MonthlyRevenueAPI(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            queryset = AnalyticsRepository.get_monthly_revenue_stats()
            data = list(queryset)

            formatted_data = []
            for item in data:
                formatted_item = {
                    'month': item['month'].strftime('%Y-%m') if item['month'] else None,
                    'total_sessions': item['total_sessions'],
                    'tickets_sold': item['tickets_sold'],
                    'total_revenue': float(item['total_revenue']) if item['total_revenue'] else 0,
                    'avg_session_price': float(item['avg_session_price']) if item['avg_session_price'] else 0,
                    'unique_customers': item['unique_customers']
                }
                formatted_data.append(formatted_item)
            
            return Response({
                'success': True,
                'data': formatted_data,
                'count': len(formatted_data)
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class HallUtilizationAPI(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            queryset = AnalyticsRepository.get_hall_utilization()
            data = list(queryset.values(
                'name',
                'capacity',
                'type',
                'total_sessions',
                'tickets_sold',
                'avg_occupancy_rate',
                'total_potential_revenue',
                'actual_revenue'
            ))
            
            for item in data:
                if item['avg_occupancy_rate']:
                    item['avg_occupancy_rate'] = float(item['avg_occupancy_rate'])
                if item['total_potential_revenue']:
                    item['total_potential_revenue'] = float(item['total_potential_revenue'])
                if item['actual_revenue']:
                    item['actual_revenue'] = float(item['actual_revenue'])
            
            return Response({
                'success': True,
                'data': data,
                'count': len(data)
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MoviePopularityByYearAPI(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            queryset = AnalyticsRepository.get_movie_popularity_by_year()
            data = list(queryset)
            
            formatted_data = []
            for item in data:
                formatted_item = {
                    'year': item['year'],
                    'movie_count': item['movie_count'],
                    'total_sessions': item['total_sessions'],
                    'tickets_sold': item['tickets_sold'],
                    'avg_rating': float(item['avg_rating']) if item['avg_rating'] else 0,
                    'total_revenue': float(item['total_revenue']) if item['total_revenue'] else 0,
                    'avg_price': float(item['avg_price']) if item['avg_price'] else 0
                }
                formatted_data.append(formatted_item)
            
            return Response({
                'success': True,
                'data': formatted_data,
                'count': len(formatted_data)
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomerSegmentsAPI(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            queryset = AnalyticsRepository.get_customer_segments()
            data = list(queryset.values(
                'customer_id',
                'name',
                'email',
                'tickets_purchased',
                'total_spent',
                'avg_ticket_price',
                'first_purchase',
                'last_purchase'
            )[:100])  

            for item in data:
                if item['total_spent']:
                    item['total_spent'] = float(item['total_spent'])
                if item['avg_ticket_price']:
                    item['avg_ticket_price'] = float(item['avg_ticket_price'])
                if item['first_purchase']:
                    item['first_purchase'] = float(item['first_purchase'])
                if item['last_purchase']:
                    item['last_purchase'] = float(item['last_purchase'])
            
            return Response({
                'success': True,
                'data': data,
                'count': len(data)
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EmployeeSalaryStatsAPI(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            queryset = AnalyticsRepository.get_employee_salary_by_position()
            data = list(queryset)
            
            formatted_data = []
            for item in data:
                formatted_item = {
                    'position_title': item['position__title'],
                    'employee_count': item['employee_count'],
                    'avg_salary': float(item['avg_salary']) if item['avg_salary'] else 0,
                    'min_salary': float(item['min_salary']) if item['min_salary'] else 0,
                    'max_salary': float(item['max_salary']) if item['max_salary'] else 0,
                    'total_payroll': float(item['total_payroll']) if item['total_payroll'] else 0,
                    'salary_range': float(item['salary_range']) if item['salary_range'] else 0
                }
                formatted_data.append(formatted_item)
            
            return Response({
                'success': True,
                'data': formatted_data,
                'count': len(formatted_data)
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)