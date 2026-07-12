import heapq

class Environment:
    def __init__(self, initial_time=0):
        self.now = initial_time
        self._queue = []
    def process(self, generator):
        event = Process(self, generator)
        event._resume()
        return event
    def run(self, until=None):
        while self._queue and (until is None or self.now < until):
            time, _, event = heapq.heappop(self._queue)
            self.now = time
            event._resume()
    def timeout(self, delay):
        return Timeout(self, delay)

class Event:
    def __init__(self, env):
        self.env = env
        self.callbacks = []
    def _resume(self):
        for callback in self.callbacks:
            callback(self)

class Timeout(Event):
    def __init__(self, env, delay):
        super().__init__(env)
        heapq.heappush(env._queue, (env.now + delay, id(self), self))

class Process(Event):
    def __init__(self, env, generator):
        super().__init__(env)
        self.generator = generator
    def _resume(self):
        try:
            next_event = next(self.generator)
            if isinstance(next_event, Event):
                next_event.callbacks.append(lambda _: self._resume())
        except StopIteration:
            pass
