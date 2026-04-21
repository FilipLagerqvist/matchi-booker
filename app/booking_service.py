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
            self.client.open_facility(session, self.client.facility_url)

            page = session.page
            page.screenshot(path="debug_facility_page.png")
            #print(f"Opened facility page for {target_date} at {target_time}")
            found = self.find_and_click_first_free_slot(
                page=page,
                target_time=target_time,
                duration_minutes=duration_minutes
            )

            if not found:
                print(f"No free slot found for {target_time}")

                return False
            
            print(f"Clicked first free slot for {target_time}")
            page.screenshot(path="debug_after_slot_click.png")

            return True
            #return self._book_with_open_session(session, target_date, target_time, duration_minutes)
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
    
    def find_and_click_first_free_slot(self, page, target_time: str, duration_minutes: int) -> bool:
        free_slots = page.locator("td.slot.free")
        count = free_slots.count()

        print(f"Found {count} free slots on page")

        for i in range(count):
            slot = free_slots.nth(i)

            tooltip = slot.get_attribute("data-original-title") or ""
            slot_duration = slot.get_attribute("data-slot-duration") or ""
            slot_id = slot.get_attribute("slotid")

            if not slot_id:
                continue

            if slot_duration != str(duration_minutes):
                continue

            if self.slot_matches_time(tooltip, target_time):
                link_selector = f"a#s{slot_id}"
                print(f"Matching slot found: slotid={slot_id}, tooltip={tooltip}")

                page.locator(link_selector).click()
                page.wait_for_timeout(1500)

                return True
            
        return False
    
    def slot_matches_time(self, tooltip: str, target_time: str) -> bool:
        """Tooltip example: 'Available<br>1. Tennis<br> 12:00 - 13:00'
        """
        normalized = tooltip.replace("&lt;br&gt;", " ").replace("<br>", " ").strip()

        return f"{target_time} -" in normalized