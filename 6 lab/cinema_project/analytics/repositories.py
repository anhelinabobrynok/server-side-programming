from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar, Generic
from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from .models import (
    Genre, Hall, JobPosition, Employee,
    Movie, Customer, Session, Ticket
)

T = TypeVar('T', bound=models.Model)


class BaseRepository(ABC, Generic[T]):

    def __init__(self, model_class: type[T]):
        self._model = model_class

    def get_all(self) -> List[T]:
        return list(self._model.objects.all())

    def get_by_id(self, entity_id: int) -> Optional[T]:

        try:
            return self._model.objects.get(pk=entity_id)
        except ObjectDoesNotExist:
            return None

    def create(self, **kwargs) -> T:
        instance = self._model(**kwargs)
        instance.save()
        return instance

    def update(self, entity_id: int, **kwargs) -> Optional[T]:
        instance = self.get_by_id(entity_id)
        if instance:
            for key, value in kwargs.items():
                setattr(instance, key, value)
            instance.save()
        return instance

    def delete(self, entity_id: int) -> bool:
        instance = self.get_by_id(entity_id)
        if instance:
            instance.delete()
            return True
        return False

    def count(self) -> int:
        return self._model.objects.count()

    @abstractmethod
    def get_model_name(self) -> str:
        pass


class GenreRepository(BaseRepository[Genre]):

    def __init__(self):
        super().__init__(Genre)

    def get_model_name(self) -> str:
        return "Genre"

    def get_by_name(self, name: str) -> Optional[Genre]:
        try:
            return self._model.objects.get(name=name)
        except ObjectDoesNotExist:
            return None

    def get_popular_genres(self, limit: int = 5) -> List[Genre]:
        from django.db.models import Count
        return list(
            self._model.objects.annotate(
                movie_count=Count('movies')
            ).order_by('-movie_count')[:limit]
        )


class HallRepository(BaseRepository[Hall]):

    def __init__(self):
        super().__init__(Hall)

    def get_model_name(self) -> str:
        return "Hall"

    def get_by_type(self, hall_type: str) -> List[Hall]:
        return list(self._model.objects.filter(type=hall_type))

    def get_available_halls(self, min_capacity: int) -> List[Hall]:
        return list(self._model.objects.filter(capacity__gte=min_capacity))


class JobPositionRepository(BaseRepository[JobPosition]):

    def __init__(self):
        super().__init__(JobPosition)

    def get_model_name(self) -> str:
        return "JobPosition"

    def get_by_title(self, title: str) -> Optional[JobPosition]:
        try:
            return self._model.objects.get(title=title)
        except ObjectDoesNotExist:
            return None


class EmployeeRepository(BaseRepository[Employee]):

    def __init__(self):
        super().__init__(Employee)

    def get_model_name(self) -> str:
        return "Employee"

    def get_by_position(self, position_id: int) -> List[Employee]:
        return list(self._model.objects.filter(position_id=position_id))

    def get_by_salary_range(self, min_salary: float, max_salary: float) -> List[Employee]:
        return list(
            self._model.objects.filter(
                salary__gte=min_salary,
                salary__lte=max_salary
            )
        )

    def get_highest_paid(self, limit: int = 5) -> List[Employee]:
        return list(self._model.objects.order_by('-salary')[:limit])


class MovieRepository(BaseRepository[Movie]):

    def __init__(self):
        super().__init__(Movie)

    def get_model_name(self) -> str:
        return "Movie"

    def get_by_genre(self, genre_id: int) -> List[Movie]:
        return list(self._model.objects.filter(genre_id=genre_id))

    def get_by_year(self, year: int) -> List[Movie]:
        return list(self._model.objects.filter(release_year=year))

    def get_by_age_limit(self, max_age: int) -> List[Movie]:
        return list(self._model.objects.filter(age_limit__lte=max_age))

    def search_by_title(self, title_part: str) -> List[Movie]:
        return list(self._model.objects.filter(title__icontains=title_part))


class CustomerRepository(BaseRepository[Customer]):

    def __init__(self):
        super().__init__(Customer)

    def get_model_name(self) -> str:
        return "Customer"

    def get_by_email(self, email: str) -> Optional[Customer]:
        try:
            return self._model.objects.get(email=email)
        except ObjectDoesNotExist:
            return None

    def search_by_name(self, name_part: str) -> List[Customer]:
        return list(self._model.objects.filter(name__icontains=name_part))

    def get_active_customers(self, min_tickets: int = 1) -> List[Customer]:
        from django.db.models import Count
        return list(
            self._model.objects.annotate(
                ticket_count=Count('tickets')
            ).filter(ticket_count__gte=min_tickets)
        )


class SessionRepository(BaseRepository[Session]):
    def __init__(self):
        super().__init__(Session)

    def get_model_name(self) -> str:
        return "Session"

    def get_by_movie(self, movie_id: int) -> List[Session]:
        return list(self._model.objects.filter(movie_id=movie_id))

    def get_by_hall(self, hall_id: int) -> List[Session]:
        return list(self._model.objects.filter(hall_id=hall_id))

    def get_by_date(self, date) -> List[Session]:
        return list(
            self._model.objects.filter(
                start_time__date=date
            ).order_by('start_time')
        )

    def get_upcoming_sessions(self) -> List[Session]:
        from django.utils import timezone
        return list(
            self._model.objects.filter(
                start_time__gte=timezone.now()
            ).order_by('start_time')
        )


class TicketRepository(BaseRepository[Ticket]):

    def __init__(self):
        super().__init__(Ticket)

    def get_model_name(self) -> str:
        return "Ticket"

    def get_by_session(self, session_id: int) -> List[Ticket]:
        return list(self._model.objects.filter(session_id=session_id))

    def get_by_customer(self, customer_id: int) -> List[Ticket]:
        return list(self._model.objects.filter(customer_id=customer_id))

    def is_seat_available(self, session_id: int, seat_number: int) -> bool:
        return not self._model.objects.filter(
            session_id=session_id,
            seat_number=seat_number
        ).exists()

    def get_occupied_seats(self, session_id: int) -> List[int]:
        tickets = self._model.objects.filter(session_id=session_id)
        return [ticket.seat_number for ticket in tickets]