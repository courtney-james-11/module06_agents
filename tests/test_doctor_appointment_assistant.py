from doctor_appointment_assistant import DoctorAppointmentChatbot
from doctor_appointment_tool import AppointmentAvailability


def make_bot():
    """Build a fresh chatbot with its own tool for each test."""
    appointment_availability = AppointmentAvailability(
        {
            "monday": ["9:00 AM", "10:30 AM", "1:00 PM"],
            "tuesday": ["11:00 AM", "2:30 PM"],
            "wednesday": ["9:30 AM", "12:00 PM", "3:00 PM"],
            "thursday": ["10:00 AM", "1:30 PM"],
            "friday": ["9:00 AM", "11:30 AM", "2:00 PM"],
        }
    )
    return DoctorAppointmentChatbot(
        "Dr. Smith's Office Assistant",
        "You are an appointment assistant.",
        appointment_availability,
    )


def test_tool_finds_known_day():
    tool = AppointmentAvailability({"monday": ["9:00 AM"]})
    assert tool.find_available_days("I want an appointment on Monday.") == "monday"


def test_tool_returns_none_for_unknown_day():
    tool = AppointmentAvailability({"monday": ["9:00 AM"]})
    assert tool.find_available_days("I want an appointment on Sunday.") is None


def test_respond_records_both_messages():
    bot = make_bot()
    bot.respond("hello")
    assert len(bot.history) == 2
    assert bot.history[0]["role"] == "user"
    assert bot.history[1]["role"] == "assistant"


def test_handoff_request_goes_to_human():
    bot = make_bot()
    assert "human" in bot.respond("I need to cancel my appointment.")
