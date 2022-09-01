import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "true"

from queue import Queue, Empty
from threading import Thread

import pygame as pygame

from signalio import Event
from .singleton import singleton
from ..log import logger

DEFAULT_DIMENSIONS = (720, 480)

pygame_logger = logger("pygame")


@singleton
class PygameManager:
    Quit = Event[None]()

    def __init__(self):
        self._thread = Thread(target=self._event_loop)
        self._queue = Queue()

        self.running = False

    def _event_loop(self):
        pygame_logger.info("Starting pygame event loop")

        pygame.init()
        pygame_logger.info("Initialised pygame")

        screen = pygame.display.set_mode(DEFAULT_DIMENSIONS)
        pygame_logger.info("Enabled pygame display")

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break

            if self.running:
                try:
                    for task in self._queue.get(block=False):
                        pass

                except Empty:
                    pass

        pygame_logger.info("Event loop ended. Quitting pygame...")
        pygame.quit()
        pygame_logger.info("Pygame has been quit!")
        
    def start(self):
        self.running = True
        self._thread.start()
