from ctypes import pythonapi, py_object
from threading import Thread, _active


class Parallel(Thread):
    def __init__(self, callback):
        super().__init__(daemon=False)

        self._callback = callback

    def run(self):
        try:
            self._callback()

        except Exception as e:
            raise e

        # finally:
        #     return

    def get_id(self):
        if hasattr(self, "_thread_id"):
            return self._thread_id

        else:
            for id, thread in _active.items():
                if thread is self:
                    return id

    def cancel(self):
        t_id = self.get_id()

        pythonapi.PyThreadState_SetAsyncExc(t_id, py_object(SystemExit))
