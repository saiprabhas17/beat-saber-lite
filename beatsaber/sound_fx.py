import pygame

pygame.mixer.init()
slice_sound = pygame.mixer.Sound("assets/hit.wav")

def play_hit():
    slice_sound.play()
