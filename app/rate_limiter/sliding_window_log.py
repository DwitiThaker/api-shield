import time
from collections import defaultdict
from typing import Callable

class SlidingWindowLogRateLimiter:
    def __init__(self, limit: int, window_seconds: int, clock: Callable[[], float] = time.time):
        self.limit = limit
        self.window_seconds = window_seconds
        self.clock = clock
        self.requests = defaultdict(list)
        
    def is_allowed(self, client_id: str) -> bool:
        current_time = self.clock()
        request_timestamps = self.requests[client_id]
        
        cutoff_time = current_time - self.window_seconds
        
        self.requests[client_id] = [timestamp for timestamp in request_timestamps if timestamp > cutoff_time]
        
        if len(self.requests[client_id]) >= self.limit:
            return False
        
        self.requests[client_id].append(current_time)
        return True
        