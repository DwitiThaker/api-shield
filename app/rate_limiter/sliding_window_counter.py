
import time
from collections import defaultdict
from typing import Callable


class SlidingWindowCounterRateLimiter:
    def __init__(
        self,
        limit: int,
        window_seconds: int,
        clock: Callable[[], float] = time.time,
    ):
        self.limit = limit
        self.window_seconds = window_seconds
        self.clock = clock

        # client_id -> {"window_start": ..., "count": ...}
        self.clients = defaultdict(
            lambda: {"window_start": None, "count": 0}
        )

    def is_allowed(self, client_id: str) -> bool:
        current_time = self.clock()

        current_window_start = (
            current_time // self.window_seconds
        ) * self.window_seconds

        elapsed_time = current_time - current_window_start

        client_data = self.clients[client_id]

        if client_data["window_start"] != current_window_start:
            previous_count = client_data["count"]
            previous_window_start = client_data["window_start"]

            if previous_window_start is None:
                previous_count = 0
            elif previous_window_start != (
                current_window_start - self.window_seconds
            ):
                previous_count = 0

            client_data["previous_count"] = previous_count
            client_data["count"] = 0
            client_data["window_start"] = current_window_start

        previous_count = client_data.get("previous_count", 0)
        current_count = client_data["count"]

        previous_weight = (
            self.window_seconds - elapsed_time
        ) / self.window_seconds

        estimated_count = (
            previous_count * previous_weight + current_count
        )

        if estimated_count >= self.limit:
            return False

        client_data["count"] += 1
        return True
