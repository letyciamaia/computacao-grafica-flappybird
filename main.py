# ════════════════════════════════════════════════
#  main.py — Ponto de entrada do jogo
# ════════════════════════════════════════════════
#
#  FLAPPY ME — Trabalho de Computação Gráfica
#  Conceitos aplicados:
#  - Aula 02: Framebuffer (pygame.Surface / display.flip)
#  - Aula 03: Pontos P(x,y), Vetores V=(dx,dy),
#             Translação, Escala, Rotação, Primitivas gráficas
#  - Aula 04: Sistema de referência universo x dispositivo,
#             Viewport/Clipping, Mapeamento de coordenadas

import pygame
import sys
import os

from src.config  import SCREEN_W, SCREEN_H, FPS, BIRD_RADIUS
from src.sounds  import make_beep, make_death_sound, load_music
from src.screens import screen_start, screen_gameover
from src.game    import run_game

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Flappy Me — CG")
clock = pygame.time.Clock()

font_big   = pygame.font.SysFont("Arial", 52, bold=True)
font_med   = pygame.font.SysFont("Arial", 28, bold=True)
font_small = pygame.font.SysFont("Arial", 18)
font_tiny  = pygame.font.SysFont("Arial", 13)
fonts = (font_big, font_med, font_small, font_tiny)


def load_photo():
    """
    Carrega assets/images/player.png ou player.jpg.
    Aplica escala (transformação geométrica, Aula 03) e máscara circular.
    """
    base = os.path.dirname(__file__)
    for name in ["player.png", "player.jpg"]:
        p = os.path.join(base, "assets", "images", name)
        if os.path.exists(p):
            try:
                img = pygame.image.load(p).convert_alpha()
                d = BIRD_RADIUS * 2
                img = pygame.transform.scale(img, (d, d))
                mask = pygame.Surface((d, d), pygame.SRCALPHA)
                pygame.draw.circle(mask, (255, 255, 255, 255),
                                   (BIRD_RADIUS, BIRD_RADIUS), BIRD_RADIUS)
                img.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
                return img
            except:
                pass
    return None


def main():
    photo     = load_photo()
    snd_jump  = make_beep(freq=600,  duration_ms=60,  volume=0.25)
    snd_score = make_beep(freq=880,  duration_ms=100, volume=0.3)
    snd_die   = make_death_sound()
    load_music()

    while True:
        screen_start(screen, clock, fonts, photo)
        score, hi = run_game(screen, clock, fonts, photo, snd_jump, snd_score, snd_die)
        screen_gameover(screen, clock, fonts, score, hi, photo)


if __name__ == "__main__":
    main()