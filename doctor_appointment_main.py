# doctor_appointment_main.py
# Author: Courtney James

from doctor_appointment_assistant import DoctorAppointmentChatbot
from doctor_appointment_tool import AppointmentAvailability
from ollama_model import OllamaModel

OPEN_APPOINTMENTS = {
    "monday": ["9:00 AM", "10:30 AM", "1:00 PM"],
    "tuesday": ["11:00 AM", "2:30 PM"],
    "wednesday": ["9:30 AM", "12:00 PM", "3:00 PM"],
    "thursday": ["10:00 AM", "1:30 PM"],
    "friday": ["9:00 AM", "11:30 AM", "2:00 PM"],
}

INSTRUCTIONS = """You are Stacy, an appointment assistant for Dr. Smiths family medicine office. Answer questions in one short sentance.
Dr. Smith's office is accepting new patients. The office is located at 4523 Main Street, Tampa, FL 33602.
Please bring your insurance card and your photo ID to your appointment. 
Only state facts that appear in these instructions. If you do not know, say you do not know and offer to pass the customer to a human agent."""

appointment_availability = AppointmentAvailability(OPEN_APPOINTMENTS)
model = OllamaModel("granite4.1:3b")
chatbot = DoctorAppointmentChatbot(
    "Stacy", INSTRUCTIONS, appointment_availability, model
)

print("Type a message, or type quit to stop.")
user_message = input("You: ")
while user_message != "quit":
    print(f"{chatbot.name}: {chatbot.respond(user_message)}")
    user_message = input("You: ")

print(f"Messages in this conversation: {len(chatbot.history)}")
