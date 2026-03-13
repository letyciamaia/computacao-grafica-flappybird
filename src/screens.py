import pygame
import sys
import math
from src.config import *
from src.draw import draw_gradient_rect, draw_clouds, draw_ground, draw_bird


def screen_start(screen, clock, fonts, photo_surf=None):
    font_big, font_med, font_small, font_tiny = fonts
    clouds = [(80, 80, 1.0), (250, 50, 1.3), (340, 120, 0.8)]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN, pygame.JOYBUTTONDOWN):
                return

        draw_gradient_rect(screen, SKY_TOP, SKY_BOT, (0, 0, SCREEN_W, SCREEN_H))
        draw_clouds(screen, clouds)
        draw_ground(screen, 0)

        bird_y = SCREEN_H//2 - 40 + math.sin(pygame.time.get_ticks()/400) * 8
        draw_bird(screen, SCREEN_W//2, bird_y, 0, photo_surf)

        shadow_t = font_big.render("FLAPPY ME", True, (50, 50, 120))
        title    = font_big.render("FLAPPY ME", True, WHITE)
        screen.blit(shadow_t, shadow_t.get_rect(center=(SCREEN_W//2+3, SCREEN_H//2+63)))
        screen.blit(title,    title.get_rect(center=(SCREEN_W//2,   SCREEN_H//2+60)))

        sub = font_small.render("Pressione qualquer tecla para jogar", True, WHITE)
        screen.blit(sub, sub.get_rect(center=(SCREEN_W//2, SCREEN_H//2+110)))

        cg = font_tiny.render("Computação Gráfica", True, (200, 230, 255))
        screen.blit(cg, cg.get_rect(center=(SCREEN_W//2, SCREEN_H - 20)))

        pygame.display.flip()
        clock.tick(FPS)


def screen_gameover(screen, clock, fonts, score, hi, photo_surf=None):
    font_big, font_med, font_small, font_tiny = fonts
    timer = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN, pygame.JOYBUTTONDOWN):
                if timer > 60:
                    return

        draw_gradient_rect(screen, (0, 0, 40), (0, 0, 15), (0, 0, SCREEN_W, SCREEN_H))

        panel = pygame.Surface((300, 230), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 140))
        screen.blit(panel, panel.get_rect(center=(SCREEN_W//2, SCREEN_H//2)))

        go = font_big.render("Tente de novo :( ", True, RED)
        screen.blit(go, go.get_rect(center=(SCREEN_W//2, SCREEN_H//2 - 70)))

        sc_txt = font_med.render(f"Pontuação: {score}", True, WHITE)
        screen.blit(sc_txt, sc_txt.get_rect(center=(SCREEN_W//2, SCREEN_H//2 - 10)))

        hi_txt = font_med.render(f"Recorde: {hi}", True, YELLOW)
        screen.blit(hi_txt, hi_txt.get_rect(center=(SCREEN_W//2, SCREEN_H//2 + 35)))

        if score >= hi and score > 0:
            new_rec = font_small.render("Yup, novo recorde!", True, YELLOW)
            screen.blit(new_rec, new_rec.get_rect(center=(SCREEN_W//2, SCREEN_H//2 + 75)))

        if timer > 60:
            restart = font_small.render("Pressione qualquer tecla", True, (180, 180, 180))
            screen.blit(restart, restart.get_rect(center=(SCREEN_W//2, SCREEN_H//2 + 110)))

        timer += 1
        pygame.display.flip()
        clock.tick(FPS)