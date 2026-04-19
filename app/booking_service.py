from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import time


class BookingService:
    def __init__(self, client, timezone: str):
        self.client = client
        self.timezone = timezone

    def wait_until_midnight(self) -> None:
        tz = ZoneInfo(self.timezone)
        now = datetime.now(tz)
        next_midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)

        while True:
            now = datetime.now(tz)
            seconds_left = (next_midnight - now).total_seconds()
            if seconds_left <= 0:
                break

            if seconds_left > 5:
                time.sleep(1)
            else:
                time.sleep(0.1)

    def try_book(self, target_date: str, target_time: str, duration_minutes: int) -> bool:
        session = self.client.start()
        try:
            self.client.login(session)
            
            return self._book_with_open_session(session, target_date, target_time, duration_minutes)
        finally:
            session.close()

    def _book_with_open_session(self, session, target_date: str, target_time: str, duration_minutes: int) -> bool:
        page = session.page

        print("Waiting until midnight...")
        self.wait_until_midnight()
        print("Midnight reached. Refreshing...")

        for attempt in range(20):
            page.reload(wait_until="domcontentloaded")
            page.wait_for_load_state("networkidle")

            try:
                # Find selectors to navigate to indoor courts, date, time slot, book
                # Loop courts

                page.locator('text="Tennis(Indoors)"').click()


                return True
            except Exception as e:
                print(f"Attempt {attempt + 1}: slot not bookable")
                time.sleep(0.4)

        return False