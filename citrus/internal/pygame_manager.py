from threading import Thread

import pygame as pygame

from .singleton import singleton


@singleton
class PygameManager:
    def __init__(self):
        self._thread = Thread(target=PygameManager._event_loop)

    def _event_loop(self):
        pass

    def start(self):
        self._thread.start()
