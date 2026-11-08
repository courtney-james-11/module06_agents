# doctor_appointment_tool.py
# Author: Courtney James


class AppointmentAvailability:
    """A tool that knows which days and times are available for doctor appointments."""

    def __init__(self, availability):
        """Store the availability this tool can look up."""
        self.availability = availability

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
