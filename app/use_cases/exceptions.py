from uuid import UUID

class DoctorNotFoundError(Exception):
    def __init__(self, doctor_id: UUID):
        self.doctor_id = doctor_id
        super().__init__(f"Doctor not found: {doctor_id}")

class UserNotFoundError(Exception):
    def __init__(self, user_id: UUID):
        self.user_id = user_id
        super().__init__(f"User not found: {user_id}")

class AppointmentNotFoundError(Exception):
    def __init__(self, appointment_id: UUID):
        self.appointment_id = appointment_id
        super().__init__(f"Appointment not found: {appointment_id}")

class RoomNotFoundError(Exception):
    def __init__(self, room_id: UUID):
        self.room_id = room_id
        super().__init__(f"Room not found: {room_id}")

class DoctorAlreadyExistsError(Exception):
    def __init__(self, doctor_id: UUID):
        self.doctor_id = doctor_id
        super().__init__(f"Doctor already exists: {doctor_id}")

class InvalidDoctorDataError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(f"Invalid doctor data: {message}")