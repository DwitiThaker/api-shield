import time
from collections.abc import Callable

class FixedWindowRateLimiter:
    def __init__(self, limit: int, window_seconds: int, clock: Callable[[], float] = time.time,):
        self.limit = limit
        self.window_seconds = window_seconds
        self.clock = clock
        self.clients = {}
        
    def is_allowed(self, client_id: str) -> bool:
            current_time = self.clock()
            
            client_data = self.clients.get(client_id)
            
            if client_data is None:
                self.clients[client_id] = {
                    "count":1,
                    "window_start": current_time,
                }
                return True
            
            elapsed_time = current_time - client_data["window_start"]
            
            if elapsed_time >= self.window_seconds:
                self.clients[client_id] = {
                    "count": 1,
                    "window_start": current_time,
                }
                return True
            
            if client_data["count"] >= self.limit:            
             return False
            
            client_data["count"] += 1
            return True
    
