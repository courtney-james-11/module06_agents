# doctors_appointment_toolbox.py
# Author: Courtney James


class AppointmentToolbox:
    """Each tool the model requests to use is sent through class and checked."""

    def __init__(self, appointment_schedule, appointment_queue):
        """Store the tools the model is allowed to ask for."""
        self.appointment_schedule = appointment_schedule
        self.appointment_queue = appointment_queue

    def tool_list(self):
        """Return the exact tool the model requets."""
        return [
            self.appointment_schedule.check_availability,
            self.appointment_queue.request_appointment,
        ]

    def run(self, name, arguments, history):
        """Check and run tool only if every check passes."""
        if name == "find_available_days":
            day = self.clean(arguments, "day")
            if day == "":
                return "The day is missing. Ask the customer for it."
            return self.appointment_schedule.find_available_days(day)
        if name == "request_appointment":
            day = self.clean(arguments, "day")
            time = self.clean(arguments, "time")
            client = self.clean(arguments, "client")
            if day == "" or time == "" or client == "":
                return "The day, time, and client name are all needed."
            if not self.customer_said(history, time):
                return "The customer has not given that time. Ask them for it."
            if not self.customer_said(history, client):
                return "The customer has not given that name. Ask them for it."
            return self.appointment_queue.request_appointment(day, time, client)
        return f"There is no tool named {name}."

    def clean(self, arguments, key):
        """Return string argument without extra spaces, or "" if it is missing."""
        return str(arguments.get(key, "")).strip()

    def customer_said(self, history, text):
        """Return True if text appears in a message the customer typed."""
        for message in history:
            if message["role"] == "user" and text.lower() in message["content"].lower():
                return True
        return False
