# ════════════════════════════════════════════════
#  screens.py — Tela inicial e game over
# ════════════════════════════════════════════════

import pygame
import sys
import math
import random
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
    is_record = score >= hi and score > 0

    # Partículas de fundo
    particles = [{
        'x': random.randint(0, SCREEN_W),
        'y': random.randint(0, SCREEN_H),
        'vy': random.uniform(-0.5, -2.0),
        'size': random.randint(2, 5),
        'color': random.choice([
            (255, 80,  80),
            (255, 180, 50),
            (255, 255, 100),
            (200, 100, 255),
        ]),
        'alpha': random.randint(100, 255),
    } for _ in range(40)]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN, pygame.JOYBUTTONDOWN):
                if timer > 60:
                    return

        t = pygame.time.get_ticks() / 1000.0

        # Fundo com gradiente animado
        r1 = int(40 + 20 * math.sin(t * 0.7))
        r2 = int(10 + 10 * math.sin(t * 0.5))
        draw_gradient_rect(screen, (0, 0, r1+80), (0, 0, r2+40), (0, 0, SCREEN_W, SCREEN_H))

        # Atualiza e desenha partículas
        for p in particles:
            p['y'] += p['vy']
            p['x'] += math.sin(t + p['y'] * 0.05) * 0.5
            if p['y'] < -10:
                p['y'] = SCREEN_H + 10
                p['x'] = random.randint(0, SCREEN_W)
            surf = pygame.Surface((p['size']*2, p['size']*2), pygame.SRCALPHA)
            pygame.draw.circle(surf, (*p['color'], p['alpha']),
                               (p['size'], p['size']), p['size'])
            screen.blit(surf, (int(p['x']), int(p['y'])))

        # Painel central com bordas arredondadas simuladas
        panel_w, panel_h = 320, 260
        panel_x = SCREEN_W//2 - panel_w//2
        panel_y = SCREEN_H//2 - panel_h//2

        # Sombra do painel
        shadow = pygame.Surface((panel_w + 10, panel_h + 10), pygame.SRCALPHA)
        shadow.fill((0, 0, 0, 80))
        screen.blit(shadow, (panel_x - 5 + 5, panel_y - 5 + 5))

        # Painel principal
        panel = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        panel.fill((0, 20, 80, 200))
        screen.blit(panel, (panel_x, panel_y))

        # Borda brilhante animada
        border_color = (
            int(180 + 75 * math.sin(t * 3)),
            int(50  + 50 * math.sin(t * 2)),
            int(200 + 55 * math.sin(t * 2.5)),
        )
        pygame.draw.rect(screen, border_color,
                         (panel_x, panel_y, panel_w, panel_h), 2)

        # Título GAME OVER com pulso
        scale = 1.0 + 0.04 * math.sin(t * 4)
        go_surf = font_big.render("GAME OVER", True, (50, 150, 255))
        w = int(go_surf.get_width() * scale)
        h = int(go_surf.get_height() * scale)
        go_scaled = pygame.transform.scale(go_surf, (w, h))
        screen.blit(go_scaled, go_scaled.get_rect(center=(SCREEN_W//2, panel_y + 55)))

        # Linha separadora
        pygame.draw.line(screen, border_color,
                         (panel_x + 20, panel_y + 90),
                         (panel_x + panel_w - 20, panel_y + 90), 1)

        # Pontuação
        sc_txt = font_med.render(f"Pontuação: {score}", True, WHITE)
        screen.blit(sc_txt, sc_txt.get_rect(center=(SCREEN_W//2, panel_y + 120)))

        # Recorde
        hi_color = YELLOW if is_record else (180, 180, 180)
        hi_txt = font_med.render(f"Recorde: {hi}", True, hi_color)
        screen.blit(hi_txt, hi_txt.get_rect(center=(SCREEN_W//2, panel_y + 160)))

        # Novo recorde
        if is_record:
            pulse = abs(math.sin(t * 5))
            rec_color = (
                int(255 * pulse),
                int(220 * pulse),
                int(50  * pulse),
            )
            new_rec = font_small.render("NOVO RECORDE!", True, rec_color)
            screen.blit(new_rec, new_rec.get_rect(center=(SCREEN_W//2, panel_y + 200)))

        # Instrução pisca
        if timer > 60 and int(t * 2) % 2 == 0:
            restart = font_tiny.render("Pressione qualquer tecla para jogar de novo", True, (160, 160, 200))
            screen.blit(restart, restart.get_rect(center=(SCREEN_W//2, panel_y + panel_h + 20)))

        timer += 1
        pygame.display.flip()
        clock.tick(FPS)