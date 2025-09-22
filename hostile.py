#codigo é 35% IA
from settings import *
import os
class Hostile:
    def __init__(self, tela, camera_x, x, y, largura, altura, pasta='images/inimigos/jar', base_name='jar', frame_count=10, velocidade_anim=0.12):
        self.vel_x = 0
        self.direcao_x = 1
        self.limite_esquerda = x
        self.limite_direita = x
        
        self.vel_y = 0
        self.direcao_y = 1
        self.limite_superior = y
        self.limite_inferior = y
                # Área do inimigo
        self.enemy = pygame.Rect(x, y, largura, altura)

        # Carrega frames dinamicamente
        self.frames = self.carregar_frames(pasta, base_name, frame_count, largura, altura)
        self.rect = pygame.Rect(x-camera_x, y, largura+1, altura+1)
        # Controle de animação
        self.frame_index = 0
        self.velocidade_anim = velocidade_anim

    def carregar_frames(self, pasta, base_name, frame_count, largura, altura):
        """Carrega frames de animação a partir de uma pasta e padrão de nome."""
        frames = []
        for i in range(1, frame_count + 1):
            caminho_img = os.path.join(pasta, f"{base_name}_({i}).png")
            if os.path.exists(caminho_img):
                img = pygame.image.load(caminho_img).convert_alpha()
                img = pygame.transform.scale(img, (largura, altura))
                frames.append(img)
        return frames if frames else [pygame.Surface((largura, altura))]  # fallback se não houver imagem

    def draw(self, tela, camera_x, riven):
        #Atualiza animação, desenha inimigo e verifica colisão com jogador.
        # Atualiza frame
        self.frame_index += self.velocidade_anim
        if self.frame_index >= len(self.frames):
            self.frame_index = 0

        # Calcula posição relativa à câmera
        enemy_pos = pygame.Rect(
            self.enemy.x - camera_x,
            self.enemy.y,
            self.enemy.width,
            self.enemy.height
        )
        self.rect = pygame.Rect(self.enemy.x - camera_x,
            self.enemy.y,
            self.enemy.width,
            self.enemy.height)
        # Desenha frame atual
        tela.blit(self.frames[int(self.frame_index)], (enemy_pos.x, enemy_pos.y))

        # Debug da hitbox
       # pygame.draw.rect(tela, (250, 0, 0), enemy_pos, 2)
        #pygame.draw.rect(tela, (0, 250, 0), self.rect, 2)

        # Verifica colisão
        return riven.rect.colliderect(enemy_pos)

