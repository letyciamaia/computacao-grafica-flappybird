
#  game.py — Loop principal do jogo


import pygame
import sys
import random
import os
from src.config import *
from src.draw import (draw_gradient_rect, draw_clouds, draw_pipe,
                      draw_ground, draw_bird, draw_score, draw_stars, draw_explosion)


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


def run_game(screen, clock, fonts, photo_surf=None, snd_jump=None, snd_score=None, snd_die=None, joystick=None):
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

    # Estrelas — pontos P(x,y) com brilho variável (Aula 03)
    stars = [(random.randint(0, SCREEN_W),
              random.randint(0, SCREEN_H - GROUND_H),
              random.randint(1, 2),
              random.randint(100, 255)) for _ in range(60)]

    try:
        pygame.mixer.music.play(-1, start=MUSIC_START)
    except:
        pass

    while True:
        clock.tick(FPS)

        #Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                try: pygame.mixer.music.stop()
                except: pass
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Pause
                    paused = True
                    try: pygame.mixer.music.pause()
                    except: pass
                    while paused:
                        for e in pygame.event.get():
                            if e.type == pygame.QUIT:
                                pygame.quit(); sys.exit()
                            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                                paused = False
                                try: pygame.mixer.music.unpause()
                                except: pass
                        pause_txt = font_med.render("ESC para continuar", True, WHITE)
                        screen.blit(pause_txt, pause_txt.get_rect(center=(SCREEN_W//2, SCREEN_H//2)))
                        pygame.display.flip()
                        clock.tick(FPS)
                else:
                    bird_vy = JUMP_VEL
                    if snd_jump: snd_jump.play()
            if event.type == pygame.MOUSEBUTTONDOWN:
                bird_vy = JUMP_VEL
                if snd_jump: snd_jump.play()
            if event.type == pygame.JOYBUTTONDOWN:
                bird_vy = JUMP_VEL
                if snd_jump: snd_jump.play()

        #Física
        bird_vy += GRAVITY
        bird_y  += bird_vy
        bird_angle = max(-25, min(90, bird_vy * 4.5))

        #Gera novos canos
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

        #Translação dos canos: V=(-PIPE_SPEED, 0)
        for p in pipes:
            p['x'] -= PIPE_SPEED

        # Clipping (Aula 04): remove fora da viewport
        pipes = [p for p in pipes if p['x'] > -PIPE_WIDTH - 20]

        #Pontuação
        for p in pipes:
            if not p['scored'] and p['x'] + PIPE_WIDTH < bird_x:
                p['scored'] = True
                score += 1
                phase = (score // 5) % len(PHASES)
                if snd_score: snd_score.play()

        #Scroll do chão
        ground_offset = (ground_offset + PIPE_SPEED) % 40

        #Parallax das nuvens
        clouds = [((cx - 0.6) % (SCREEN_W + 60) - 30, cy, sc)
                  for cx, cy, sc in clouds]

        #Pisca as estrelas
        stars = [(x, y, s, max(80, min(255, b + random.randint(-10, 10))))
                 for x, y, s, b in stars]

        #Colisão (AABB simplificado)
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
            # Animação de explosão
            for frame in range(8):
                draw_gradient_rect(screen, PHASES[phase]["sky_top"], PHASES[phase]["sky_bot"], (0, 0, SCREEN_W, SCREEN_H))
                if phase in (2, 3, 4):
                    draw_stars(screen, stars)
                draw_clouds(screen, clouds)
                for p in pipes:
                    draw_pipe(screen, int(p['x']), p['top'], p['bot'])
                draw_ground(screen, ground_offset)
                draw_explosion(screen, bird_x, bird_y, frame)
                pygame.display.flip()
                pygame.time.wait(50)
            try: pygame.mixer.music.stop()
            except: pass
            pygame.time.wait(100)
            hi = max(score, hi)
            save_hi(hi)
            return score, hi

        #RENDERIZAÇÃO (framebuffer — Aula 02)
        draw_gradient_rect(screen,
                           PHASES[phase]["sky_top"],
                           PHASES[phase]["sky_bot"],
                           (0, 0, SCREEN_W, SCREEN_H))
        if phase in (2, 3, 4):
            draw_stars(screen, stars)
        draw_clouds(screen, clouds)
        for p in pipes:
            draw_pipe(screen, int(p['x']), p['top'], p['bot'])
        draw_ground(screen, ground_offset)
        draw_bird(screen, bird_x, bird_y, bird_angle, photo_surf)
        draw_score(screen, score, hi, font_big, font_tiny)
        pygame.display.flip()
