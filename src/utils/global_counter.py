from threading import Lock


class GlobalCounter:
    # aiohttp can spawn multiple threads that's why
    # lock is used
    lock = Lock()
    _value: int = 0

    @classmethod
    def increment(cls):
        increment_done = False

        while not increment_done:
            # from python docs
            # `The return value is True if the lock is acquired successfully, False if not.`
            increment_done = cls.lock.acquire(blocking=True)

            try:
                cls._value += 1
            except Exception:
                increment_done = False
            finally:
                cls.lock.release()

    @classmethod
    def get(cls):
        # reading is thread safe
        return cls._value
