from doctor_appointment_assistant import DoctorAppointmentChatbot
from doctor_appointment_tool import AppointmentAvailability
from doctors_appointment_queue import DoctorAppointmentQueue
from doctors_appointment_toolbox import AppointmentToolbox
from fake_model import FakeModel


def make_helper(model):
    """Build a fresh helper with its own tools and the model it is given."""
    appointment_availability = AppointmentAvailability(
        {
            "monday": ["9:00 AM", "10:30 AM", "1:00 PM"],
            "tuesday": ["11:00 AM", "2:30 PM"],
            "wednesday": ["9:30 AM", "12:00 PM", "3:00 PM"],
            "thursday": ["10:00 AM", "1:30 PM"],
            "friday": ["9:00 AM", "11:30 AM", "2:00 PM"],
        }
    )
    tools = AppointmentToolbox(
        appointment_availability, DoctorAppointmentQueue(appointment_availability)
    )
    return DoctorAppointmentChatbot(
        "Stacy",
        "You are an appointment assistant.",
        tools,
        model,
    )


def booking(day, time, client):
    """Build the decision a model returns when it wants to request a booking."""
    arguments = {"day": day, "time": time, "client": client}
    return {"tool": "request_appointment", "arguments": arguments}


def test_model_can_ask_for_open_times():
    model = FakeModel(
        [
            {"tool": "find_available_days", "arguments": {"day": "Monday"}},
            {"text": "Monday has 9:00 am and 2:30 pm."},
        ]
    )
    helper = make_helper(model)
    helper.respond("When can I come in on Monday?")
    assert helper.history[1]["content"] == "Open times on monday: 9:00 am and 2:30 pm."


def test_booking_waits_for_staff():
    model = FakeModel([booking("monday", "9:00 am", "Dana Cruz"), {"text": "Sent."}])
    helper = make_helper(model)
    helper.respond("Please book Monday at 9:00 am for Dana Cruz")
    assert len(helper.tools.appointment_queue.waiting()) == 1
    assert helper.tools.appointment_schedule.appointments == []
