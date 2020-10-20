import time


class TimeUtil:
    @staticmethod
    def get_current_time_ms() -> int:
        return int(round(time.time() * 1000))
