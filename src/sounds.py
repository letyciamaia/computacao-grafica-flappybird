
#  sounds.py — Sons e música


import pygame
import math
import os


def make_beep(freq=440, duration_ms=80, volume=0.3):
    """Gera um beep sintético."""
    sample_rate = 44100
    n = int(sample_rate * duration_ms / 1000)
    buf = bytearray(n * 2)
    for i in range(n):
        val = int(volume * 32767 * math.sin(2 * math.pi * freq * i / sample_rate))
        val = max(-32768, min(32767, val))
        buf[2*i] = val & 0xFF
        buf[2*i+1] = (val >> 8) & 0xFF
    return pygame.mixer.Sound(buffer=bytes(buf))


def make_death_sound():
    """Som de morte"""
    sample_rate = 44100
    n = int(sample_rate * 0.3)
    buf = bytearray(n * 2)
    for i in range(n):
        freq = 300 - 250 * (i / n)
        val = int(0.4 * 32767 * math.sin(2 * math.pi * freq * i / sample_rate))
        val = max(-32768, min(32767, val))
        buf[2*i] = val & 0xFF
        buf[2*i+1] = (val >> 8) & 0xFF
    return pygame.mixer.Sound(buffer=bytes(buf))


def load_music():
    """Carrega assets/sounds/music.mp3 no mixer do pygame."""
    base = os.path.dirname(os.path.dirname(__file__))
    p = os.path.join(base, "assets", "sounds", "music.mp3")
    if os.path.exists(p):
        pygame.mixer.music.load(p)
        return True
    return False