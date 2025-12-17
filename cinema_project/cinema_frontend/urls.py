from django.urls import path
from .views import (
    MovieListView,
    MovieDetailView,
    MovieCreateView,
    MovieUpdateView,
    MovieDeleteView,
    ExternalMoviesListView
)

urlpatterns = [

    path('movies/', MovieListView.as_view(), name='movie_list'),
    path('movies/<int:movie_id>/', MovieDetailView.as_view(), name='movie_detail'),
    path('movies/create/', MovieCreateView.as_view(), name='movie_create'),
    path('movies/<int:movie_id>/edit/', MovieUpdateView.as_view(), name='movie_update'),
    path('movies/<int:movie_id>/delete/', MovieDeleteView.as_view(), name='movie_delete'),
    

    path('external/movies/', ExternalMoviesListView.as_view(), name='external_movies_list'),
]