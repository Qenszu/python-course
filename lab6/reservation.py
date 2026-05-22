class NoSeatsAvailableError(Exception):
    pass

class AlreadyReservedError(Exception):
    pass

class ReservationNotFoundError(Exception):
    pass


class ReservationSystem:
    def __init__(self, seats_num):
        self.seats_num = seats_num
        self.reservation = []

    def reserve(self, user_id):
        if user_id in self.reservation:
            raise AlreadyReservedError("Juz posiadasz rezerwacje")
        elif len(self.reservation) == self.seats_num:
            raise NoSeatsAvailableError("Nie ma wolnych miejsc")
        else:
            self.reservation.append(user_id)

    def cancel(self, user_id):
        if user_id not in self.reservation:
            raise ReservationNotFoundError("Brak rezerwacji")
        else:
            self.reservation.remove(user_id)

    def available_seats(self):
        return self.seats_num - len(self.reservation)

    def is_reserved(self, user_id):
        return user_id in self.reservation



import pytest

def test_reservation():
    R = ReservationSystem(5)
    R.reserve(1)
    R.reserve(2)
    assert R.available_seats() == 3

def test_unavailable_reservation():
    R = ReservationSystem(1)
    R.reserve(1)
    with pytest.raises(NoSeatsAvailableError):
        R.reserve(2)

def test_user_already_reserved_seat():
    R = ReservationSystem(10)
    R.reserve(1)
    with pytest.raises(AlreadyReservedError):
        R.reserve(1)

def test_cancel_reservation_with_reservation():
    R = ReservationSystem(5)
    R.reserve(1)
    R.reserve(2)
    R.cancel(1)
    assert R.available_seats() == 4

def test_cancel_reservation_without_reservation():
    R = ReservationSystem(5)
    with pytest.raises(ReservationNotFoundError):
        R.cancel(1)

def test_seats_number_counter():
    R = ReservationSystem(5)
    R.reserve(1)
    R.reserve(2)
    assert R.available_seats() == 3

def test_reservation_is_registered():
    R = ReservationSystem(5)
    R.reserve(1)
    R.reserve(2)
    R.reserve(3)
    assert R.is_reserved(1) == True
    assert R.is_reserved(4) == False

