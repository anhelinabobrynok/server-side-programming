from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cinema_app.urls')),
    path('', include('cinema_frontend.urls')),
]