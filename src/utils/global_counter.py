from threading import Lock


class GlobalCounter:
    # aiohttp can spawn multiple threads that's why
    # threading lock is used
    lock = Lock()
    _value: int = 0

    @classmethod
    def increment(cls):
        increment_done = False

        while not increment_done:
            lock_acquired = cls.lock.acquire(blocking=True)

            if lock_acquired:
                try:
                    cls._value += 1
                finally:
                    cls.lock.release()

            increment_done = lock_acquired

    @classmethod
    def get(cls):
        # reading is thread safe
        return cls._value
