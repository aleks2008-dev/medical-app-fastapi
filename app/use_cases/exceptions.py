from uuid import UUID

class DomainException(Exception):
    """Base domain exception"""
    status_code: int = 400

class NotFoundError(DomainException):
    """Base not found exception"""
    status_code: int = 404

class DoctorNotFoundError(NotFoundError):
    def __init__(self, doctor_id: UUID):
        self.doctor_id = doctor_id
        super().__init__(f"Doctor not found: {doctor_id}")

class UserNotFoundError(NotFoundError):
    def __init__(self, user_id: UUID):
        self.user_id = user_id
        super().__init__(f"User not found: {user_id}")

class AppointmentNotFoundError(NotFoundError):
    def __init__(self, appointment_id: UUID):
        self.appointment_id = appointment_id
        super().__init__(f"Appointment not found: {appointment_id}")

class RoomNotFoundError(NotFoundError):
    def __init__(self, room_id: UUID):
        self.room_id = room_id
        super().__init__(f"Room not found: {room_id}")

class DoctorAlreadyExistsError(DomainException):
    def __init__(self, doctor_id: UUID):
        self.doctor_id = doctor_id
        super().__init__(f"Doctor already exists: {doctor_id}")

class InvalidDoctorDataError(DomainException):
    def __init__(self, message: str):
        self.message = message
        super().__init__(f"Invalid doctor data: {message}")