# Flappy Me 
Um Jogo estilo Flappy Bird desenvolvido em Python com Pygame como trabalho da disciplina de Computação Gráfica.

## Integrantes
- Letycia Maia e Samuel Nóbrega

## Como jogar
- Pressione qualquer tecla ou clique para pular
- Passe pelos canos sem bater
- A cada 5 pontos veja o fundo mudar!

## Conceitos de CG aplicados
- Aula 02: Framebuffer — `pygame.Surface` e `display.flip()`
- Aula 03: Pontos `P(x,y)`, Vetores `V=(dx,dy)`, Translação, Rotação, Escala e Primitivas gráficas (retângulos, círculos, elipses, polígonos)
- Aula 04: Sistema de referência universo x dispositivo, Viewport, Clipping e Mapeamento de coordenadas

## Estrutura do projeto
```
├── assets/
│   └── sounds/   ← música (music.mp3)
├── src/
│   ├── config.py
│   ├── draw.py
│   ├── sounds.py
│   ├── screens.py
│   └── game.py
└── main.py
```

## ▶ Como rodar
```bash
pip install pygame==2.5.2
python main.py
```
