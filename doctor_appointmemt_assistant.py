# doctor_appointment_assistant.py
# Author: Courtney James

HANDOFF_WORDS = ["reschedule", "cancel", "emergency", "agent", "book"]


class DoctorAppointmentChatbot:
    """An appointment chatbot. Rules are first executed and an AI model answers the rest."""

    def __init__(self, name, instructions, appointment_availability_tool, model):
        """Sets up one chatbot with its own name, instructions, tool, and history."""
        self.name = name
        self.instructions = instructions
        self.appointment_availability_tool = appointment_availability_tool
        self.model = model
        self.history = []

    def respond(self, user_message):
        """Records the user's message, chooses a reply, records it, and returns it."""
        self.history.append({"role": "user", "content": user_message})
        reply = self.choose_reply(user_message)
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def choose_reply(self, user_message):
        """choose a reply with keyword rules. If none applies, ask the AI model"""
        text = user_message.lower()
        if self.needs_human(text):
            return "I can only list available times. I'm passing you to a human agent."
        if "appointment" in text or "available" in text:
            return self.appointment_reply(user_message)
        return self.model_reply()

    def model_reply(self):
        """The model is asked to reply, if model has no reply a proper response is given."""
        reply = self.model.reply(self.instructions, self.history)
        if reply is None:
            return "I'm not sure how to help with that. I can check appointment availability for Dr. Smiths Office."
        return reply

    def needs_human(self, text):
        """Return True if the message is about something a person must handle"""
        for word in HANDOFF_WORDS:
            if word in text:
                return True
        return False

    def appointment_reply(self, user_message):
        """Use the appointment availability tool to answer a question about an appointment times."""
        day = self.appointment_availability_tool.find_available_days(user_message)
        if day is None:
            return "Which day? Our office is only open Monday through Friday,"
        times = self.appointment_availability_tool.available_times_for(day)
        return f"On {day}, the available appointment times are: {times}."
