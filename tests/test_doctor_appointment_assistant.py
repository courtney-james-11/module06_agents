from doctor_appointment_assistant import DoctorAppointmentChatbot
from doctor_appointment_tool import AppointmentAvailability
from doctors_appointment_queue import DoctorAppointmentQueue
from doctors_appointment_toolbox import AppointmentToolbox
from fake_model import FakeModel


def make_helper(model):
    """Build a fresh helper with its own tools and the model it is given."""
    schedule = AppointmentAvailability(
        {
            "monday": ["9:00 AM", "10:30 AM", "1:00 PM"],
            "tuesday": ["11:00 AM", "2:30 PM"],
            "wednesday": ["9:30 AM", "12:00 PM", "3:00 PM"],
            "thursday": ["10:00 AM", "1:30 PM"],
            "friday": ["9:00 AM", "11:30 AM", "2:00 PM"],
        }
    )
    tools = AppointmentToolbox(schedule, DoctorAppointmentQueue(schedule))
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


def test_booking_waits_for_staff():
    model = FakeModel([booking("monday", "9:00 am", "Dana Cruz"), {"text": "Sent."}])
    helper = make_helper(model)
    helper.respond("Please book Monday at 9:00 am for Dana Cruz")
    assert len(helper.tools.appointment_queue.waiting()) == 1
    assert helper.tools.appointment_schedule.appointments == []


def test_made_up_name_is_refused():
    model = FakeModel([booking("monday", "9:00 am", "Jane Doe"), {"text": "Name?"}])
    helper = make_helper(model)
    helper.respond("Please book Monday at 9:00 am")
    assert "has not given that name" in helper.history[1]["content"]
    assert helper.tools.appointment_queue.waiting() == []


def test_cancellation_goes_to_the_front_desk():
    helper = make_helper(FakeModel([]))
    assert "human agent" in helper.respond("Please cancel my appointment")
