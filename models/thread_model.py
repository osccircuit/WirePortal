import threading
from gi.repository import GLib


class ThreadWorker:
    def __init__(self):
        self.is_running = False
        self.thread = None
        self.method_for_thread = None
        self.callback = None
        self.stop_event = threading.Event()

    def set_callback(self, callback):
        self.callback = callback

    def set_thread_method(self, method):
        self.method_for_thread = method
        
    def get_status_run(self):
        return self.is_running

    def run_loop(self):
        while not self.stop_event.is_set():
            result = self.method_for_thread()
            if self.callback and result is not None:
                GLib.idle_add(self.callback, result)
            self.stop_event.wait(timeout=10)

    def start(self):
        if not self.is_running:
            self.is_running = True
            self.stop_event.clear()
            self.thread = threading.Thread(target=self.run_loop)
            self.thread.start()

    def stop(self):
        self.is_running = False
        self.stop_event.set()
        if self.thread is not None:
            self.thread.join()
            self.thread = None
