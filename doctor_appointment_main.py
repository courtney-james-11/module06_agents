# doctor_appointment_main.py
# Author: Courtney James

from doctor_appointment_assistant import DoctorAppointmentChatbot
from doctor_appointment_tool import AppointmentAvailability

OPEN_APPOINTMENTS = {
    "monday": ["9:00 AM", "10:30 AM", "1:00 PM"],
    "tuesday": ["11:00 AM", "2:30 PM"],
    "wednesday": ["9:30 AM", "12:00 PM", "3:00 PM"],
    "thursday": ["10:00 AM", "1:30 PM"],
    "friday": ["9:00 AM", "11:30 AM", "2:00 PM"],
}

appointment_availability = AppointmentAvailability(OPEN_APPOINTMENTS)
chatbot = DoctorAppointmentChatbot(
    "Dr. Smith's Office Assistant",
    "You are an appointment assistant for Dr. Smith's office.",
    appointment_availability,
)

print("Type a message, or type quit to stop.")
user_message = input("You: ")
while user_message != "quit":
    print(f"{chatbot.name}: {chatbot.respond(user_message)}")
    user_message = input("You: ")

print(f"Messages in this conversation: {len(chatbot.history)}")
