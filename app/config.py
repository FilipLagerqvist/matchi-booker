from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseModel):
    matchi_email: str
    matchi_password: str
    facility_url: str
    target_date: str
    target_time: str
    duration_minutes: int
    timezone: str = "Europe/Stockholm"
    headless: bool = False

def load_settings() -> Settings:
    return Settings(
        matchi_email=os.environ["MATCHI_EMAIL"],
        matchi_password=os.environ["MATCHI_PASSWORD"],
        facility_url=os.environ["FACILITY_URL"],
        target_date=os.environ["TARGET_DATE"],
        target_time=os.environ["TARGET_TIME"],
        duration_minutes=int(os.environ.get("DURATION_MINUTES", "60")),
        timezone=os.environ.get("TIMEZONE", "Europe/Stockholm"),
        headless=os.environ.get("HEADLESS", "false").lower() == "true",
    )