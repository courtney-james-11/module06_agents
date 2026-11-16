# doctor_appointment_main.py
# Author: Courtney James

from doctor_appointment_assistant import DoctorAppointmentChatbot
from doctor_appointment_tool import AppointmentAvailability
from doctors_appointment_queue import DoctorAppointmentQueue
from doctors_appointment_toolbox import AppointmentToolbox
from ollama_model import OllamaModel

AVAILABILITY = {
    "monday": ["9:00 AM", "10:30 AM", "1:00 PM"],
    "tuesday": ["11:00 AM", "2:30 PM"],
    "wednesday": ["9:30 AM", "12:00 PM", "3:00 PM"],
    "thursday": ["10:00 AM", "1:30 PM"],
    "friday": ["9:00 AM", "11:30 AM", "2:00 PM"],
}

INSTRUCTIONS = """You are Stacy, an appointment assistant for Dr. Smiths family medicine office. Answer questions in one short sentance.
If the client only says hello, greet them and ask how you can help.
Dr. Smith's office is accepting new patients. The office is located at 4523 Main Street, Tampa, FL 33602.
Please bring your insurance card and your photo ID to your appointment. 
Only state facts that appear in these instructions or in tool results. If you do not know, say you do not know and offer to pass the customer to a human agent."""

appointment_schedule = AppointmentAvailability(AVAILABILITY)
appointment_queue = DoctorAppointmentQueue(appointment_schedule)
tools = AppointmentToolbox(appointment_schedule, appointment_queue)
model = OllamaModel("granite4.1:3b")
chatbot = DoctorAppointmentChatbot("Stacy", INSTRUCTIONS, tools, model)

print("Type a message, or type quit to stop.")
user_message = input("You: ")
while user_message != "quit":
    print(f"{chatbot.name}: {chatbot.respond(user_message)}")
    user_message = input("You: ")

print(f"Messages in this conversation: {len(chatbot.history)}")

print("Front desk review")
for request in appointment_queue.waiting():
    number = request["number"]
    print(
        f"Request {number}: {request['day']} at {request['time']} for {request['client']}"
    )
    answer = input("Approve? yes or no: ")
    if answer == "yes":
        print(appointment_queue.approve(number))
    else:
        print(appointment_queue.reject(number))

print(f"Appointments booked: {len(appointment_schedule.appointments)}")
