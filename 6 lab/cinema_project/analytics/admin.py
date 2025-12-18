from django.contrib import admin
from .models import Genre, Hall, JobPosition, Employee, Movie, Customer, Session, Ticket

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('genre_id', 'name')

@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ('hall_id', 'name', 'capacity', 'type')

@admin.register(JobPosition)
class JobPositionAdmin(admin.ModelAdmin):
    list_display = ('position_id', 'title')

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'name', 'position', 'salary')
    list_filter = ('position',)

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('movie_id', 'title', 'genre', 'release_year', 'duration')
    list_filter = ('genre', 'release_year')
    search_fields = ('title',)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_id', 'name', 'email')
    search_fields = ('name', 'email')

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'movie', 'hall', 'start_time', 'price')
    list_filter = ('hall', 'start_time')

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_id', 'session', 'customer', 'seat_number', 'purchase_date')
    list_filter = ('session__movie', 'purchase_date')