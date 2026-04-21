from app.config import load_settings
from app.matchi_client import MatchiClient
from app.booking_service import BookingService
# from scheduler import start_scheduler


def run_once() -> None:
    settings = load_settings()

    client = MatchiClient(
        email=settings.matchi_email,
        password=settings.matchi_password,
        facility_url=settings.facility_url,
        headless=settings.headless
    )

    service = BookingService(client=client, timezone=settings.timezone)

    success = service.try_book(
        target_date=settings.target_date,
        target_time=settings.target_time,
        duration_minutes=settings.duration_minutes
    )

    if success:
        print("Booking flow appears successful.")
    else:
        print("Booking failed or slot was not found.")


if __name__ == "__main__":
    run_once()
    
    # Later
    # start_scheduler(run_once, timezone=load_settings().timezone)  