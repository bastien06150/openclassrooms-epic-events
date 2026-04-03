import os
import sentry_sdk
from dotenv import load_dotenv

load_dotenv()


def init_sentry():
    dsn = os.getenv("SENTRY_DSN")
    environment = os.getenv("SENTRY_ENVIRONMENT", "development")

    if not dsn:
        return

    sentry_sdk.init(
        dsn=dsn,
        environment=environment,
        sample_rate=1.0,
        traces_sample_rate=0.01,
        profiles_sample_rate=0.0,
    )
