class Movie:
    def __init__(self, title: str, duration: int, rating: float):
        self.title = title              
        self.duration = duration        
        self.__rating = rating          

    def show_info(self):
        print(f"Фільм: {self.title}, тривалість: {self.duration} хв, рейтинг: {self.__rating}/10")

    def update_rating(self, new_rating: float):
        if 0 <= new_rating <= 10:
            self.__rating = new_rating
            print(f"Рейтинг фільму '{self.title}' оновлено до {self.__rating}")
        else:
            print("Помилка: рейтинг має бути від 0 до 10")

    @staticmethod
    def is_long_movie(duration: int) -> bool:
        return duration > 120


class Session(Movie):
    def __init__(self, title: str, duration: int, rating: float, hall_number: int, time: str):
        super().__init__(title, duration, rating)
        self.hall_number = hall_number
        self.time = time

    def show_info(self):
        print(f"Сеанс фільму '{self.title}' о {self.time} в залі №{self.hall_number}")


class SnackBar:
    def __init__(self, snack_menu: dict):
        self.snack_menu = snack_menu

    def show_menu(self):
        print("Меню буфету:")
        for name, price in self.snack_menu.items():
            print(f" - {name}: {price} грн")


class CinemaHall(Session, SnackBar):
    def __init__(self, title: str, duration: int, rating: float,
                 hall_number: int, time: str, snack_menu: dict, seats: int):
        Session.__init__(self, title, duration, rating, hall_number, time)
        SnackBar.__init__(self, snack_menu)
        self.seats = seats
        self.sold_tickets = 0

    def sell_ticket(self, quantity: int = 1):
        if self.sold_tickets + quantity <= self.seats:
            self.sold_tickets += quantity
            print(f"Продано {quantity} квиток(и). Залишилось місць: {self.seats - self.sold_tickets}")
        else:
            print("Недостатньо місць у залі!")

    def show_info(self):
        print(f"Фільм '{self.title}' — зал №{self.hall_number}, час: {self.time}, "
              f"місць: {self.seats}, продано: {self.sold_tickets}")


if __name__ == "__main__":

    movie1 = Movie("Інтерстеллар", 169, 8.6)
    movie2 = Movie("Воно", 135, 7.4)

    movie1.show_info()
    print("Фільм довгий?", Movie.is_long_movie(movie1.duration))

    movie2.update_rating(8.0)

    session1 = Session("Дюна", 155, 8.3, 1, "18:00")
    session1.show_info() 

    hall1 = CinemaHall(
        "Аватар 2", 192, 7.9,
        hall_number=3,
        time="20:30",
        snack_menu={"Попкорн": 80, "Кола": 50, "Начос": 70},
        seats=50
    )

    hall1.show_info()
    hall1.sell_ticket(3)
    hall1.sell_ticket(48) 
    hall1.show_menu()
