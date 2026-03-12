# Sistema de Referência do Dispositivo (Aula 04)
SCREEN_W = 400
SCREEN_H = 600
FPS      = 60

# Cores (modelo RGB aditivo)
SKY_TOP    = (0,   0,   20)
SKY_BOT    = (0,   0,   40)
GROUND_COL = (0,   0,   80)
GRASS_COL  = (0,   0,  120)
PIPE_COL   = (0,  80,  200)
PIPE_DARK  = (0,  40,  120)
PIPE_LIGHT = (50, 150, 255)
WHITE      = (255, 255, 255)
BLACK      = (  0,   0,   0)
YELLOW     = (255, 220,  50)
RED        = (220,  60,  60)

# Temas de fundo — mudam a cada 5 pontos
PHASES = [
    {"sky_top": (102, 178, 255), "sky_bot": (179, 229, 252)},  # azul dia
    {"sky_top": (255, 140,   0), "sky_bot": (255, 200, 100)},  # pôr do sol
    {"sky_top": ( 20,   0,  60), "sky_bot": ( 60,   0, 120)},  # roxo noite
    {"sky_top": (  0,   0,  20), "sky_bot": (  0,   0,  60)},  # azul escuro
    {"sky_top": (180,   0, 100), "sky_bot": ( 80,   0,  50)},  # rosa neon
]

# Parâmetros do jogo
GRAVITY       = 0.45
JUMP_VEL      = -9.0
PIPE_SPEED    = 3.0
PIPE_GAP      = 160
PIPE_WIDTH    = 60
PIPE_INTERVAL = 1500
GROUND_H      = 60
BIRD_RADIUS   = 20

# Ponto de início da música (em segundos)
MUSIC_START   = 65.0