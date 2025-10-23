from django.db import models


class Genre(models.Model):
    genre_id = models.AutoField(db_column='GenreID', primary_key=True)
    name = models.CharField(db_column='Name', max_length=50)

    class Meta:
        db_table = 'Genre'
        managed = False

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Genre(id={self.genre_id}, name='{self.name}')"


class Hall(models.Model):
    hall_id = models.AutoField(db_column='HallID', primary_key=True)
    name = models.CharField(db_column='Name', max_length=50)
    capacity = models.PositiveIntegerField(db_column='Capacity')
    type = models.CharField(db_column='Type', max_length=30)

    class Meta:
        db_table = 'Hall'
        managed = False

    def __str__(self):
        return f"{self.name} ({self.type})"

    def __repr__(self):
        return f"Hall(id={self.hall_id}, name='{self.name}', capacity={self.capacity}, type='{self.type}')"


class JobPosition(models.Model):
    position_id = models.AutoField(db_column='PositionID', primary_key=True)
    title = models.CharField(db_column='Title', max_length=100)
    description = models.TextField(db_column='Description', null=True, blank=True)

    class Meta:
        db_table = 'JobPosition'
        managed = False

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"JobPosition(id={self.position_id}, title='{self.title}')"


class Employee(models.Model):
    employee_id = models.AutoField(db_column='EmployeeID', primary_key=True)
    name = models.CharField(db_column='Name', max_length=100)
    position = models.ForeignKey(
        JobPosition,
        on_delete=models.DO_NOTHING,
        db_column='PositionID',
        related_name='employees'
    )
    salary = models.DecimalField(db_column='Salary', max_digits=10, decimal_places=2)
    hire_date = models.DateField(db_column='HireDate', null=True, blank=True)
    phone = models.CharField(db_column='Phone', max_length=15, null=True, blank=True)

    class Meta:
        db_table = 'Employee'
        managed = False

    def __str__(self):
        return f"{self.name} - {self.position.title}"

    def __repr__(self):
        return f"Employee(id={self.employee_id}, name='{self.name}', position_id={self.position_id})"


class Movie(models.Model):
    movie_id = models.AutoField(db_column='MovieID', primary_key=True)
    title = models.CharField(db_column='Title', max_length=200)
    genre = models.ForeignKey(
        Genre,
        on_delete=models.DO_NOTHING,
        db_column='GenreID',
        related_name='movies'
    )
    duration = models.PositiveIntegerField(db_column='Duration')
    age_limit = models.PositiveIntegerField(db_column='AgeLimit')
    release_year = models.PositiveIntegerField(db_column='ReleaseYear')
    description = models.TextField(db_column='Description', null=True, blank=True)
    rating = models.DecimalField(
        db_column='Rating',
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'Movie'
        managed = False

    def __str__(self):
        return f"{self.title} ({self.release_year})"

    def __repr__(self):
        return f"Movie(id={self.movie_id}, title='{self.title}', genre_id={self.genre_id})"


class Customer(models.Model):
    customer_id = models.AutoField(db_column='CustomerID', primary_key=True)
    name = models.CharField(db_column='Name', max_length=100)
    email = models.CharField(db_column='Email', max_length=150, unique=True)
    phone = models.CharField(db_column='Phone', max_length=15, null=True, blank=True)

    class Meta:
        db_table = 'Customer'
        managed = False

    def __str__(self):
        return f"{self.name} ({self.email})"

    def __repr__(self):
        return f"Customer(id={self.customer_id}, name='{self.name}', email='{self.email}')"


class Session(models.Model):
    session_id = models.AutoField(db_column='SessionID', primary_key=True)
    movie = models.ForeignKey(
        Movie,
        on_delete=models.DO_NOTHING,
        db_column='MovieID',
        related_name='sessions'
    )
    hall = models.ForeignKey(
        Hall,
        on_delete=models.DO_NOTHING,
        db_column='HallID',
        related_name='sessions'
    )
    start_time = models.DateTimeField(db_column='StartTime')
    price = models.DecimalField(db_column='Price', max_digits=8, decimal_places=2)

    class Meta:
        db_table = 'Session'
        managed = False

    def __str__(self):
        return f"{self.movie.title} - {self.start_time}"

    def __repr__(self):
        return f"Session(id={self.session_id}, movie_id={self.movie_id}, hall_id={self.hall_id})"


class Ticket(models.Model):
    ticket_id = models.AutoField(db_column='TicketID', primary_key=True)
    session = models.ForeignKey(
        Session,
        on_delete=models.DO_NOTHING,
        db_column='SessionID',
        related_name='tickets'
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.DO_NOTHING,
        db_column='CustomerID',
        related_name='tickets'
    )
    seat_number = models.PositiveIntegerField(db_column='SeatNumber')
    purchase_date = models.DecimalField(
        db_column='PurchaseDate',
        max_digits=8,
        decimal_places=2
    )

    class Meta:
        db_table = 'Ticket'
        managed = False
        unique_together = (('session', 'seat_number'),)

    def __str__(self):
        return f"Ticket #{self.ticket_id} - Seat {self.seat_number}"

    def __repr__(self):
        return f"Ticket(id={self.ticket_id}, session_id={self.session_id}, customer_id={self.customer_id})"