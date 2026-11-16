# doctor_appointment_tool.py
# Author: Courtney James


class AppointmentAvailability:
    """A tool that knows which days and times are available for doctor appointments."""

    def __init__(self, availability):
        """Store the availability this tool can look up. Appointments start at empty."""
        self.availability = availability
        self.appointments = []

    def find_available_days(self, text):
        """Return the first known day mentioned in text, or None."""
        for day in self.availability:
            if day in text.lower():
                return day
        return None

    def available_times_for(self, day):
        """Return the available times for one day, or None if unknown."""
        if day in self.availability:
            return self.availability[day]
        return None

    def check_availability(self, day):
        """Check the times available on one day.

        Args:
            day: The day, like Friday.
        """
        found = self.find_available_days(day)
        if found is None:
            return "That day was not found. I can check Monday through Friday."
        return (
            f"Open appointment times on {found} are: {self.available_times_for(found)}."
        )

    def book_appointment(self, day, time, client):
        """Add a booking, only if it was approved."""
        self.appointments.append({"day": day, "time": time, "client": client})
