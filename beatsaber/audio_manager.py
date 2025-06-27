import pygame

class AudioManager:
    def __init__(self, file):
        pygame.mixer.init()
        self.file = file
        self.start_time = None

    def play(self):
        pygame.mixer.music.load(self.file)
        pygame.mixer.music.play()
        self.start_time = pygame.time.get_ticks()

    def get_timestamp(self):
        if self.start_time is None:
            return 0.0
        return (pygame.time.get_ticks() - self.start_time) / 1000.0

    def is_playing(self):
        return pygame.mixer.music.get_busy()
