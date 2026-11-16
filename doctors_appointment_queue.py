# doctors_appointment_queue.py
# Author: Courtney James


class DoctorAppointmentQueue:
    """Appointment bookings that are waiting to be approved."""

    def __init__(self, appointment_schedule):
        """Start with no requests. Appoinments that are approved go to the appointment schedule."""
        self.appointment_schedule = appointment_schedule
        self.requests = []

    def request_appointment(self, day, time, client):
        """Ask the doctors office to book an appointment. Staff must approve it.

        Args:
            day: The day of the week, like Monday.
            time: The time of day, like 10:00 AM.
            client: The name of the client requesting the appointment.
        """
        found = self.appointment_schedule.find_available_days(day)
        if found is None:
            return "That day was not found. I can check Monday through Friday."
        number = len(self.requests) + 1
        request = {
            "number": number,
            "day": found,
            "time": time,
            "client": client,
            "status": "waiting",
        }
        self.requests.append(request)
        return f"Request {number} was sent to Dr. Smiths front office staff. The appointment has not been booked yet."

    def waiting(self):
        """Compile the requests that are waiting to be approved or denied."""
        result = []
        for request in self.requests:
            if request["status"] == "waiting":
                result.append(request)
        return result

    def find(self, number):
        """Find a request by its number."""
        for request in self.requests:
            if request["number"] == number:
                return request
        return None

    def approve(self, number):
        """Approve a request and add it to the appointment schedule."""
        request = self.find(number)
        if request is None:
            return f"There is no request {number}."
        if request["status"] != "waiting":
            return f"Request {number} is already {request['status']}."
        request["status"] = "approved"
        self.appointment_schedule.book_appointment(
            request["day"], request["time"], request["client"]
        )
        return f"Request {number} approved."

    def reject(self, number):
        """Reject a request, will not be added to the appointment schedule."""
        request = self.find(number)
        if request is None:
            return f"There is no request {number}."
        if request["status"] != "waiting":
            return f"Request {number} is already {request['status']}."
        request["status"] = "rejected"
        return f"Request {number} rejected."
