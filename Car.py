import datetime

class Car:
    def __init__(self, category, mileage=0):
        self.category = category
        self.mileage = mileage
        self.is_rented = False

    def rent(self):
        if not self.is_rented:
            self.is_rented = True
            return True
        return False

    def return_car(self):
        if self.is_rented:
            self.is_rented = False
            return True
        return False


class CarRentalSystem:
    def __init__(self, base_day_rental, kilometer_price):
        self.base_day_rental = base_day_rental
        self.kilometer_price = kilometer_price
        self.reservations = {}

    def register_reservation(self, booking_number, customer_name, category, rental_time, mileage=0):
        if booking_number in self.reservations:
            return "Error: Booking number already exists. Please choose a different booking number."

        if category not in ["compact", "premium", "minivan"]:
            return "Error: Invalid car category."

        if category == "compact":
            car_price = self.base_day_rental
        elif category == "premium":
            car_price = self.base_day_rental * 1.2
        else:
            car_price = self.base_day_rental * 1.7

        car = Car(category, mileage)
        self.reservations[booking_number] = {
            "customer_name": customer_name,
            "car": car,
            "rental_time": rental_time,
            "price": car_price,
        }
        return f"Reservation with booking number {booking_number} has been successfully registered."

    def calculate_rental_price(self, booking_number, return_time, return_mileage):
        if booking_number not in self.reservations:
            return "Error: Reservation not found."

        reservation = self.reservations[booking_number]
        car = reservation["car"]
        if not car.is_rented:
            return "Error: Car not rented."

        rental_days = (return_time - reservation["rental_time"]).days
        rental_kilometers = return_mileage - car.mileage

        if rental_days <= 0:
            return "Error: Invalid return time. Rental period should be at least one day."

        price = reservation["price"] * rental_days + self.kilometer_price * rental_kilometers

        if car.category == "minivan":
            price += self.kilometer_price * rental_kilometers * 1.5

        car.mileage = return_mileage
        car.return_car()
        del self.reservations[booking_number]

        return f"Rental price for booking number {booking_number}: ${price:.2f}"


# Example Usage
base_day_rental = 50
kilometer_price = 0.2
rental_system = CarRentalSystem(base_day_rental, kilometer_price)

# U1: Rental Registration
registration_response = rental_system.register_reservation(
    booking_number="ABC123",
    customer_name="John Doe",
    category="premium",
    rental_time=datetime.datetime(2023, 8, 5),
    mileage=5000,
)
print(registration_response)

# U2: Car Return and Price Calculation
return_time = datetime.datetime(2023, 8, 10)
return_mileage = 5500
price_response = rental_system.calculate_rental_price("ABC123", return_time, return_mileage)
print(price_response)
