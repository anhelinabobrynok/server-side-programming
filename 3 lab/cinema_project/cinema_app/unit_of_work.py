from django.db import transaction
from .repositories import (
    GenreRepository,
    HallRepository,
    JobPositionRepository,
    EmployeeRepository,
    MovieRepository,
    CustomerRepository,
    SessionRepository,
    TicketRepository
)


class UnitOfWork:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
            
        self._genres = GenreRepository()
        self._halls = HallRepository()
        self._job_positions = JobPositionRepository()
        self._employees = EmployeeRepository()
        self._movies = MovieRepository()
        self._customers = CustomerRepository()
        self._sessions = SessionRepository()
        self._tickets = TicketRepository()
        
        self._initialized = True

    @property
    def genres(self) -> GenreRepository:
        return self._genres

    @property
    def halls(self) -> HallRepository:
        return self._halls

    @property
    def job_positions(self) -> JobPositionRepository:
        return self._job_positions

    @property
    def employees(self) -> EmployeeRepository:
        return self._employees

    @property
    def movies(self) -> MovieRepository:
        return self._movies

    @property
    def customers(self) -> CustomerRepository:
        return self._customers

    @property
    def sessions(self) -> SessionRepository:
        return self._sessions

    @property
    def tickets(self) -> TicketRepository:
        return self._tickets

    @transaction.atomic
    def execute_in_transaction(self, func):
        return func()

    def commit(self):
        transaction.commit()

    def rollback(self):
        transaction.rollback()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.rollback()
        return False