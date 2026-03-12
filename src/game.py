import pygame
import sys
import random
import os
from src.config import *
from src.draw import (draw_gradient_rect, draw_clouds, draw_pipe,
                      draw_ground, draw_bird, draw_score)


HI_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "hiscore.txt")


def load_hi():
    try:
        with open(HI_FILE) as f:
            return int(f.read().strip())
    except:
        return 0


def save_hi(val):
    try:
        with open(HI_FILE, "w") as f:
            f.write(str(val))
    except:
        pass


def run_game(screen, clock, fonts, photo_surf=None, snd_jump=None, snd_score=None, snd_die=None):
    font_big, font_med, font_small, font_tiny = fonts

    # Ponto inicial do pássaro: P(SCREEN_W*0.25, SCREEN_H*0.5)
    bird_x     = SCREEN_W * 0.25
    bird_y     = float(SCREEN_H // 2)
    bird_vy    = 0.0
    bird_angle = 0.0

    pipes          = []
    last_pipe_time = pygame.time.get_ticks()
    ground_offset  = 0.0
    clouds         = [(80, 70, 1.0), (220, 45, 1.2), (350, 90, 0.85)]
    score          = 0
    hi             = load_hi()
    phase          = 0

    try:
        pygame.mixer.music.play(-1, start=MUSIC_START)
    except:
        pass

    while True:
        clock.tick(FPS)

        # ── Eventos ──────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                try: pygame.mixer.music.stop()
                except: pass
                pygame.quit(); sys.exit()
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                # Vetor impulso: V = (0, JUMP_VEL)
                bird_vy = JUMP_VEL
                if snd_jump: snd_jump.play()

        # ── Física ───────────────────────────────
        # Vetor gravidade acumulado a cada frame: V_novo = V_antigo + (0, GRAVITY)
        bird_vy += GRAVITY
        bird_y  += bird_vy
        # Mapeamento velocidade -> ângulo (transformação geométrica, Aula 03)
        bird_angle = max(-25, min(90, bird_vy * 4.5))

        # ── Gera novos canos ─────────────────────
        now = pygame.time.get_ticks()
        if now - last_pipe_time > PIPE_INTERVAL:
            gap_center = random.randint(int(SCREEN_H*0.25), int(SCREEN_H*0.70))
            pipes.append({
                'x':      float(SCREEN_W + 10),
                'top':    gap_center - PIPE_GAP // 2,
                'bot':    gap_center + PIPE_GAP // 2,
                'scored': False
            })
            last_pipe_time = now

        # ── Translação dos canos: V=(-PIPE_SPEED, 0) ──
        for p in pipes:
            p['x'] -= PIPE_SPEED

        # ── Clipping (Aula 04): remove fora da viewport ──
        pipes = [p for p in pipes if p['x'] > -PIPE_WIDTH - 20]

        # ── Pontuação ────────────────────────────
        for p in pipes:
            if not p['scored'] and p['x'] + PIPE_WIDTH < bird_x:
                p['scored'] = True
                score += 1
                phase = (score // 5) % len(PHASES)
                if snd_score: snd_score.play()

        # ── Scroll do chão ───────────────────────
        ground_offset = (ground_offset + PIPE_SPEED) % 40

        # ── Parallax das nuvens ──────────────────
        clouds = [((cx - 0.6) % (SCREEN_W + 60) - 30, cy, sc)
                  for cx, cy, sc in clouds]

        # ── Colisão (AABB simplificado) ──────────
        bird_rect = pygame.Rect(
            int(bird_x) - BIRD_RADIUS + 4,
            int(bird_y) - BIRD_RADIUS + 4,
            BIRD_RADIUS * 2 - 8,
            BIRD_RADIUS * 2 - 8
        )
        hit = False
        for p in pipes:
            px = int(p['x'])
            if (bird_rect.colliderect(pygame.Rect(px-6, 0, PIPE_WIDTH+12, p['top'])) or
                bird_rect.colliderect(pygame.Rect(px-6, p['bot'], PIPE_WIDTH+12, SCREEN_H))):
                hit = True; break

        if bird_y + BIRD_RADIUS >= SCREEN_H - GROUND_H or bird_y - BIRD_RADIUS <= 0:
            hit = True

        if hit:
            if snd_die: snd_die.play()
            try: pygame.mixer.music.stop()
            except: pass
            pygame.time.wait(200)
            hi = max(score, hi)
            save_hi(hi)
            return score, hi

        # ── RENDERIZAÇÃO (escrita no framebuffer — Aula 02) ──
        draw_gradient_rect(screen,
                           PHASES[phase]["sky_top"],
                           PHASES[phase]["sky_bot"],
                           (0, 0, SCREEN_W, SCREEN_H))
        draw_clouds(screen, clouds)
        for p in pipes:
            draw_pipe(screen, int(p['x']), p['top'], p['bot'])
        draw_ground(screen, ground_offset)
        draw_bird(screen, bird_x, bird_y, bird_angle, photo_surf)
        draw_score(screen, score, hi, font_big, font_tiny)
        pygame.display.flip()  # envia framebuffer ao monitor (Aula 02)