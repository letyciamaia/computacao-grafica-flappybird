import pygame
import math
from src.config import *


def draw_gradient_rect(surface, color_top, color_bot, rect):
    """Gradiente vertical — mapeamento linear de cor por linha (Aula 04)."""
    x, y, w, h = rect
    for i in range(h):
        t = i / h
        r = int(color_top[0] + t * (color_bot[0] - color_top[0]))
        g = int(color_top[1] + t * (color_bot[1] - color_top[1]))
        b = int(color_top[2] + t * (color_bot[2] - color_top[2]))
        pygame.draw.line(surface, (r, g, b), (x, y + i), (x + w, y + i))


def draw_pipe(surface, pipe_x, pipe_top_h, pipe_bot_y):
    """
    Canos com primitivas retângulos e linhas (Aula 03).
    Ponto base P(pipe_x, 0) — sistema de referência do objeto -> tela.
    """
    cap_h, cap_extra = 18, 6

    # Cano superior
    pygame.draw.rect(surface, PIPE_COL,   (pipe_x, 0, PIPE_WIDTH, pipe_top_h - cap_h))
    pygame.draw.rect(surface, PIPE_DARK,  (pipe_x + PIPE_WIDTH - 8, 0, 8, pipe_top_h - cap_h))
    pygame.draw.rect(surface, PIPE_LIGHT, (pipe_x, 0, 6, pipe_top_h - cap_h))
    cap_top = pygame.Rect(pipe_x - cap_extra, pipe_top_h - cap_h, PIPE_WIDTH + cap_extra*2, cap_h)
    pygame.draw.rect(surface, PIPE_COL,   cap_top)
    pygame.draw.rect(surface, PIPE_DARK,  (cap_top.right - 8, cap_top.y, 8, cap_h))
    pygame.draw.rect(surface, PIPE_LIGHT, (cap_top.x, cap_top.y, 6, cap_h))

    # Cano inferior
    bot_body_y = pipe_bot_y + cap_h
    bot_body_h = SCREEN_H - bot_body_y - GROUND_H
    pygame.draw.rect(surface, PIPE_COL,   (pipe_x, bot_body_y, PIPE_WIDTH, bot_body_h))
    pygame.draw.rect(surface, PIPE_DARK,  (pipe_x + PIPE_WIDTH - 8, bot_body_y, 8, bot_body_h))
    pygame.draw.rect(surface, PIPE_LIGHT, (pipe_x, bot_body_y, 6, bot_body_h))
    cap_bot = pygame.Rect(pipe_x - cap_extra, pipe_bot_y, PIPE_WIDTH + cap_extra*2, cap_h)
    pygame.draw.rect(surface, PIPE_COL,   cap_bot)
    pygame.draw.rect(surface, PIPE_DARK,  (cap_bot.right - 8, cap_bot.y, 8, cap_h))
    pygame.draw.rect(surface, PIPE_LIGHT, (cap_bot.x, cap_bot.y, 6, cap_h))


def draw_pixel_bird_bg(surface, cx, cy, scale=2):
    """
    Passarinho decorativo em pixel art no fundo.
    Primitivas: retângulos coloridos (Aula 03).
    """
    pixels = [
        "..XXX...",
        ".XOOOX..",
        "XOOOOX..",
        "XOEWOX..",
        "XOOOOX..",
        ".XXBXX..",
        "..X.X...",
    ]
    colors = {
        'X': (255, 220,  50),
        'O': (255, 255, 255),
        'E': (  0,   0,   0),
        'W': (255, 140,   0),
        'B': (200, 160,   0),
    }
    s = scale
    for row, line in enumerate(pixels):
        for col, ch in enumerate(line):
            if ch in colors:
                pygame.draw.rect(surface, colors[ch],
                    (int(cx) + col*s - len(line)*s//2,
                     int(cy) + row*s - len(pixels)*s//2,
                     s, s))


def draw_clouds(surface, clouds):
    """Nuvens compostas por elipses (primitivas, Aula 03)."""
    for cx, cy, scale in clouds:
        for dx, dy, r in [(-18, 5, 16), (0, 0, 22), (18, 5, 16), (8, 10, 14)]:
            pygame.draw.circle(surface, WHITE,
                               (int(cx + dx*scale), int(cy + dy*scale)), int(r*scale))


def draw_bird(surface, cx, cy, angle_deg, photo_surf=None):
    """
    Personagem no ponto P(cx, cy).
    Rotação aplicada como transformação geométrica (Aula 03).
    """
    if photo_surf:
        rotated = pygame.transform.rotate(photo_surf, -angle_deg)
        rect = rotated.get_rect(center=(int(cx), int(cy)))
        surface.blit(rotated, rect)
    else:
        pygame.draw.circle(surface, YELLOW, (int(cx), int(cy)), BIRD_RADIUS)
        eye_x = int(cx + BIRD_RADIUS * 0.4)
        eye_y = int(cy - BIRD_RADIUS * 0.2)
        pygame.draw.circle(surface, WHITE, (eye_x, eye_y), 5)
        pygame.draw.circle(surface, BLACK, (eye_x + 1, eye_y), 3)
        beak = [(int(cx + BIRD_RADIUS*0.7), int(cy+2)),
                (int(cx + BIRD_RADIUS*1.3), int(cy+2)),
                (int(cx + BIRD_RADIUS*0.9), int(cy+9))]
        pygame.draw.polygon(surface, (255, 140, 0), beak)
        wing_rect = pygame.Rect(int(cx - BIRD_RADIUS*0.9), int(cy + BIRD_RADIUS*0.2),
                                int(BIRD_RADIUS*1.0), int(BIRD_RADIUS*0.5))
        pygame.draw.ellipse(surface, (200, 160, 0), wing_rect)


def draw_ground(surface, offset):
    """Chão com scroll — translação V=(-PIPE_SPEED, 0) acumulada (Aula 03)."""
    ground_y = SCREEN_H - GROUND_H
    pygame.draw.rect(surface, GROUND_COL, (0, ground_y + 12, SCREEN_W, GROUND_H))
    pygame.draw.rect(surface, GRASS_COL,  (0, ground_y, SCREEN_W, 14))
    stripe_w = 40
    for i in range(-1, SCREEN_W // stripe_w + 2):
        x = i * stripe_w - offset % stripe_w
        pygame.draw.rect(surface, (90, 155, 75), (x, ground_y, stripe_w // 2, 14))


def draw_score(surface, score, hi, font_big, font_tiny):
    """HUD — renderização de texto como primitiva gráfica."""
    shadow = font_big.render(str(score), True, BLACK)
    surface.blit(shadow, shadow.get_rect(center=(SCREEN_W//2+2, 52)))
    txt = font_big.render(str(score), True, WHITE)
    surface.blit(txt, txt.get_rect(center=(SCREEN_W//2, 50)))
    hi_txt = font_tiny.render(f"RECORDE: {hi}", True, WHITE)
    surface.blit(hi_txt, (SCREEN_W - hi_txt.get_width() - 8, 8))
    
def draw_stars(surface, stars):
    """Partículas — pontos P(x,y) com brilho variável (Aula 03)."""
    for x, y, size, bright in stars:
        c = int(bright)
        pygame.draw.circle(surface, (c, c, c), (int(x), int(y)), size)


def draw_explosion(surface, cx, cy, frame):
    """Explosão — translação radial de partículas (Aula 03)."""
    import math
    for i in range(12):
        angle = i * 30
        dist = frame * 6
        x = int(cx + dist * math.cos(math.radians(angle)))
        y = int(cy + dist * math.sin(math.radians(angle)))
        radius = max(1, 6 - frame)
        color = (255, max(0, 200 - frame * 20), 0)
        pygame.draw.circle(surface, color, (x, y), radius)