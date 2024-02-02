import time

class Stopwatch:
    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start(self):
        self.start_time = time.time()

    def stop(self):
        self.end_time = time.time()

    def elapsed_time(self):
        if self.start_time is None:
            raise ValueError("Stopwatch has not been started.")
        if self.end_time is None:
            raise ValueError("Stopwatch has not been stopped.")
        return self.end_time - self.start_time

