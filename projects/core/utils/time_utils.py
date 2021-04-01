import time


class TimeUtil:
    SECOND_MS = 1000
    MINUTE_MS = 60 * SECOND_MS
    HOUR_MS = 60 * MINUTE_MS
    DAY_MS = 24 * HOUR_MS

    @staticmethod
    def get_current_time_ms() -> int:
        return int(round(time.time() * 1000))
