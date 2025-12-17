import os
import django
from datetime import datetime, date
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinema_project.settings')
django.setup()

from cinema_app.unit_of_work import UnitOfWork


def print_separator(title: str):
    print(f"  {title}")


def demo_genre_repository(uow: UnitOfWork):
    print_separator("ДЕМОНСТРАЦІЯ: Genre Repository")

    print("\n1. Всі жанри:")
    genres = uow.genres.get_all()
    for genre in genres:
        print(f"   {genre}")

    print("\n2. Пошук жанру за ID = 1:")
    genre = uow.genres.get_by_id(1)
    if genre:
        print(f"   Знайдено: {genre}")
        print(f"   Деталі: {repr(genre)}")

    print("\n3. Додавання нового жанру 'Документальний':")
    try:
        new_genre = uow.genres.create(name='Документальний')
        print(f"   ✓ Створено: {new_genre}")

        print("\n4. Перевірка - всі жанри після додавання:")
        genres = uow.genres.get_all()
        for genre in genres:
            print(f"   {genre}")
    except Exception as e:
        print(f"   ✗ Помилка: {e}")

    print("\n5. Топ-3 популярних жанри (за кількістю фільмів):")
    popular = uow.genres.get_popular_genres(limit=3)
    for genre in popular:
        movie_count = genre.movies.count()
        print(f"   {genre.name}: {movie_count} фільм(ів)")


def demo_movie_repository(uow: UnitOfWork):
    print_separator("ДЕМОНСТРАЦІЯ: Movie Repository")

    print("\n1. Всі фільми:")
    movies = uow.movies.get_all()
    for movie in movies:
        print(f"   {movie} | Жанр: {movie.genre.name} | Тривалість: {movie.duration} хв")

    print("\n2. Пошук фільму за ID = 1:")
    movie = uow.movies.get_by_id(1)
    if movie:
        print(f"   Назва: {movie.title}")
        print(f"   Жанр: {movie.genre.name}")
        print(f"   Рік: {movie.release_year}")
        print(f"   Віковий ліміт: {movie.age_limit}+")
        print(f"   Опис: {movie.description}")

    print("\n3. Додавання нового фільму 'Дюна: Частина третя':")
    try:
        genre_fantastic = uow.genres.get_by_name('Фантастика')
        if genre_fantastic:
            new_movie = uow.movies.create(
                title='Дюна: Частина третя',
                genre=genre_fantastic,
                duration=170,
                age_limit=12,
                release_year=2025,
                description='Продовження епічної саги про пустельну планету',
                rating=Decimal('8.5')
            )
            print(f"   ✓ Створено: {new_movie}")
            print(f"   ✓ ID: {new_movie.movie_id}")

            print("\n4. Перевірка - фільми після додавання:")
            all_movies = uow.movies.get_all()
            print(f"   Загальна кількість фільмів: {len(all_movies)}")
            print(f"   Останній доданий: {all_movies[-1]}")
        else:
            print("   ✗ Жанр 'Фантастика' не знайдено")
    except Exception as e:
        print(f"   ✗ Помилка: {e}")

    print("\n5. Фільми жанру 'Фантастика':")
    if genre_fantastic:
        fantastic_movies = uow.movies.get_by_genre(genre_fantastic.genre_id)
        for movie in fantastic_movies:
            print(f"   {movie}")


def demo_customer_repository(uow: UnitOfWork):

    print_separator("ДЕМОНСТРАЦІЯ: Customer Repository")

    print("\n1. Всі клієнти:")
    customers = uow.customers.get_all()
    for customer in customers:
        print(f"   {customer} | Телефон: {customer.phone}")

    print("\n2. Пошук клієнта за ID = 1:")
    customer = uow.customers.get_by_id(1)
    if customer:
        print(f"   Ім'я: {customer.name}")
        print(f"   Email: {customer.email}")
        print(f"   Телефон: {customer.phone}")

    print("\n3. Додавання нового клієнта 'Тарас Шевченко':")
    try:
        new_customer = uow.customers.create(
            name='Тарас Шевченко',
            email='taras.shevchenko@email.com',
            phone='380991234567'
        )
        print(f"   ✓ Створено: {new_customer}")
        print(f"   ✓ ID: {new_customer.customer_id}")

        print("\n4. Перевірка - пошук за email:")
        found = uow.customers.get_by_email('taras.shevchenko@email.com')
        if found:
            print(f"   ✓ Знайдено: {found}")
    except Exception as e:
        print(f"   ✗ Помилка: {e}")

    print("\n5. Активні клієнти (які купили квитки):")
    active = uow.customers.get_active_customers()
    for customer in active[:5]:
        ticket_count = customer.tickets.count()
        print(f"   {customer.name}: {ticket_count} квиток")


def demo_session_repository(uow: UnitOfWork):

    print_separator("ДЕМОНСТРАЦІЯ: Session Repository")
    
    print("\n1. Майбутні сеанси:")
    upcoming = uow.sessions.get_upcoming_sessions()[:5]
    for session in upcoming:
        print(f"   {session.movie.title}")
        print(f"      Зал: {session.hall.name} | Час: {session.start_time} | Ціна: {session.price} грн")

    print("\n2. Пошук сеансу за ID = 1:")
    session = uow.sessions.get_by_id(1)
    if session:
        print(f"   Фільм: {session.movie.title}")
        print(f"   Зал: {session.hall.name}")
        print(f"   Час: {session.start_time}")
        print(f"   Ціна: {session.price} грн")

    print("\n3. Сеанси на 2025-10-23:")
    today_sessions = uow.sessions.get_by_date(date(2025, 10, 23))
    for session in today_sessions:
        print(f"   {session.start_time.strftime('%H:%M')} - {session.movie.title} ({session.hall.name})")


def demo_ticket_repository(uow: UnitOfWork):

    print_separator("ДЕМОНСТРАЦІЯ: Ticket Repository")

    print("\n1. Перші 5 квитків:")
    tickets = uow.tickets.get_all()[:5]
    for ticket in tickets:
        print(f"   Квиток #{ticket.ticket_id}")
        print(f"      Фільм: {ticket.session.movie.title}")
        print(f"      Клієнт: {ticket.customer.name}")
        print(f"      Місце: {ticket.seat_number}")

    print("\n2. Зайняті місця на сеансі ID=1:")
    occupied = uow.tickets.get_occupied_seats(1)
    print(f"   Зайняті місця: {occupied}")
    
    print("\n3. Перевірка доступності місць:")
    session_id = 1
    test_seats = [15, 16, 17]
    for seat in test_seats:
        available = uow.tickets.is_seat_available(session_id, seat)
        status = "✓ Вільне" if available else "✗ Зайняте"
        print(f"   Місце {seat}: {status}")


def main():

    print("  Cinema Database Management System")
    
    uow = UnitOfWork()
    
    demo_genre_repository(uow)
    demo_movie_repository(uow)
    demo_customer_repository(uow)
    demo_session_repository(uow)
    demo_ticket_repository(uow)



if __name__ == '__main__':
    main()