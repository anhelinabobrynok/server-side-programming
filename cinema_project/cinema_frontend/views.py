from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from cinema_app.models import Movie, Genre
from cinema_app.repositories import MovieRepository, GenreRepository
from .NetworkHelper import NetworkHelper


class MovieListView(View):
    """View для відображення списку всіх фільмів"""
    
    def get(self, request):
        repository = MovieRepository()
        movies = repository.get_all()
        
        context = {
            'movies': movies,
            'title': 'Список фільмів'
        }
        return render(request, 'cinema_frontend/movie_list.html', context)


class MovieDetailView(View):
    """View для відображення деталей конкретного фільму"""
    
    def get(self, request, movie_id):
        repository = MovieRepository()
        movie = repository.get_by_id(movie_id)
        
        if not movie:
            return render(request, 'cinema_frontend/404.html', status=404)
        
        context = {
            'movie': movie,
            'title': f'Фільм: {movie.title}'
        }
        return render(request, 'cinema_frontend/movie_detail.html', context)


class MovieCreateView(View):
    """View для створення нового фільму"""
    
    def get(self, request):
        genre_repository = GenreRepository()
        genres = genre_repository.get_all()
        
        context = {
            'genres': genres,
            'title': 'Додати новий фільм',
            'action': 'create'
        }
        return render(request, 'cinema_frontend/movie_form.html', context)
    
    def post(self, request):
        repository = MovieRepository()
        
        # Отримання даних з форми
        title = request.POST.get('title')
        genre_id = request.POST.get('genre')
        duration = request.POST.get('duration')
        age_limit = request.POST.get('age_limit')
        release_year = request.POST.get('release_year')
        description = request.POST.get('description', '')
        rating = request.POST.get('rating', None)
        
        # Валідація обов'язкових полів
        if not title or not genre_id or not duration or not age_limit or not release_year:
            genre_repository = GenreRepository()
            genres = genre_repository.get_all()
            context = {
                'genres': genres,
                'title': 'Додати новий фільм',
                'action': 'create',
                'error': 'Заповніть всі обов\'язкові поля'
            }
            return render(request, 'cinema_frontend/movie_form.html', context)
        
        # Підготовка даних для створення
        movie_data = {
            'title': title,
            'genre_id': int(genre_id),
            'duration': int(duration),
            'age_limit': int(age_limit),
            'release_year': int(release_year),
            'description': description,
        }
        
        if rating:
            movie_data['rating'] = float(rating)
        
        # Створення фільму
        movie = repository.create(**movie_data)
        
        # Перенаправлення на сторінку деталей
        return redirect('movie_detail', movie_id=movie.movie_id)


class MovieUpdateView(View):
    """View для редагування існуючого фільму"""
    
    def get(self, request, movie_id):
        movie_repository = MovieRepository()
        genre_repository = GenreRepository()
        
        movie = movie_repository.get_by_id(movie_id)
        if not movie:
            return render(request, 'cinema_frontend/404.html', status=404)
        
        genres = genre_repository.get_all()
        
        context = {
            'movie': movie,
            'genres': genres,
            'title': f'Редагувати: {movie.title}',
            'action': 'update'
        }
        return render(request, 'cinema_frontend/movie_form.html', context)
    
    def post(self, request, movie_id):
        repository = MovieRepository()
        
        movie = repository.get_by_id(movie_id)
        if not movie:
            return render(request, 'cinema_frontend/404.html', status=404)
        
        # Отримання даних з форми
        title = request.POST.get('title')
        genre_id = request.POST.get('genre')
        duration = request.POST.get('duration')
        age_limit = request.POST.get('age_limit')
        release_year = request.POST.get('release_year')
        description = request.POST.get('description', '')
        rating = request.POST.get('rating', None)
        
        # Підготовка даних для оновлення
        update_data = {
            'title': title,
            'genre_id': int(genre_id),
            'duration': int(duration),
            'age_limit': int(age_limit),
            'release_year': int(release_year),
            'description': description,
        }
        
        if rating:
            update_data['rating'] = float(rating)
        
        # Оновлення фільму
        repository.update(movie_id, **update_data)
        
        # Перенаправлення на сторінку деталей
        return redirect('movie_detail', movie_id=movie_id)


class MovieDeleteView(View):
    """View для видалення фільму"""
    
    def post(self, request, movie_id):
        repository = MovieRepository()
        
        movie = repository.get_by_id(movie_id)
        if not movie:
            return render(request, 'cinema_frontend/404.html', status=404)
        
        # Видалення фільму
        repository.delete(movie_id)
        
        # Перенаправлення на список фільмів
        return redirect('movie_list')


class ExternalMoviesListView(View):
    """
    View для відображення списку об'єктів з зовнішнього REST API колеги
    з можливістю видалення через кнопку Delete.
    """
    
    def get(self, request):
        helper = NetworkHelper(
            # ✅ Тут все було вірно
            base_url='http://127.0.0.1:8001/api', 
            username='admin',                  
            password='admin'                   
        )
        
        endpoint = 'patients'
        
        items = helper.get_list(endpoint)
        
        error_message = None
        if items is None: # Краще перевіряти на None, бо порожній список [] це не помилка
            error_message = "Не вдалося отримати дані з API. Перевірте підключення."
        
        context = {
            'items': items,
            'endpoint': endpoint,
            'title': f'Зовнішні дані: {endpoint}',
            'error': error_message
        }
        
        return render(request, 'cinema_frontend/external_movies_list.html', context)
    
    def post(self, request):
        """
        Обробка POST запиту для видалення.
        """
        item_id = request.POST.get('item_id')
        
        # ⚠️ ВАЖЛИВО: Тут теж має бути 'patients', бо ми видаляємо пацієнтів
        endpoint = 'patients' 
        
        if not item_id:
            return redirect('external_movies_list')
        
        helper = NetworkHelper(
            # 👇 ТУТ БУЛА ПОМИЛКА: було без /api
            # Краще використовувати 127.0.0.1 всюди однаково
            base_url='http://127.0.0.1:8001/api', 
            username='admin',                   
            password='admin'                    
        )
        
        # Видалити об'єкт через API
        success = helper.delete_item(endpoint, item_id)
        
        # Перенаправити назад на список
        return redirect('external_movies_list')