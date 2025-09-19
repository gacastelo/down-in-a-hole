from settings import *
class Player:
    def __init__(self):
        
        # Carregar frames 
        sprite_wid = 100
        sprite_hei = 110
      
        frames_right_orig = [
            pygame.transform.scale(
            pygame.image.load('rivem_ani/1_riven_moviment.png'), (sprite_wid, sprite_hei)),
            pygame.transform.scale(
            pygame.image.load('rivem_ani/2_riven_moviment.png'),(sprite_wid, sprite_hei)),
            pygame.transform.scale(
            pygame.image.load('rivem_ani/3_riven_moviment.png'),(sprite_wid, sprite_hei)),
        ]

        # Escalar frames para o tamanho
        self.frames_right = [pygame.transform.scale(frame, (sprite_wid, sprite_hei)) for frame in frames_right_orig]

        # Criar frames para esquerda com flip horizontal
        self.frames_left = [pygame.transform.flip(frame, True, False) for frame in self.frames_right]

        # Frame de pulo (escalado)
        self.imagem_pulo = pygame.transform.scale(
            pygame.image.load('rivem_ani/4_riven_moviment.png'), (sprite_wid, sprite_hei)
        )
        # Versão flipada para esquerda do pulo
        self.imagem_pulo_esquerda = pygame.transform.flip(self.imagem_pulo, True, False)

        # Sprite parado (escalado)
        self.imagem_parado = pygame.transform.scale(
            pygame.image.load('rivem_ani/riven-parado.png'), (sprite_wid, sprite_hei)
        )
        self.imagem_parado_esquerda = pygame.transform.flip(self.imagem_parado, True, False)

        # Controle de animação
        self.frame_index = 0
        self.velocidade_anim = 0.15
        self.tempo_anim = 0
        self.direction = "right"
        self.moving = False

        # Posição e física
        self.pos_x = 1000
        self.pos_y = 535
        self.vel_max = 10
        self.vel_x = 0
        self.atrito = 0.5

        self.vel_y = 0
        self.gravidade = 0.5
        self.pulo_forca = -9

        # Pulo variável
        self.pulo_ativo = False
        self.tempo_pulo_max = 10
        self.tempo_pulo_atual = 0

        self.no_chao = False
        self.rect = pygame.Rect(self.pos_x, self.pos_y, 50, 65)

    def mover(self, teclas, objetos_colisao):
        # Movimento horizontal e animação
        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
            self.vel_x = -self.vel_max
            self.direction = "left"
            self.moving = True
        elif teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
            self.vel_x = self.vel_max
            self.direction = "right"
            self.moving = True
        else:
            self.moving = False
            if self.vel_x > 0:
                self.vel_x -= self.atrito
                if self.vel_x < 0:
                    self.vel_x = 0
            elif self.vel_x < 0:
                self.vel_x += self.atrito
                if self.vel_x > 0:
                    self.vel_x = 0

        self.pos_x += self.vel_x
        self.rect.topleft = (self.pos_x, self.pos_y)

        # Colisão horizontal
        for obj in objetos_colisao:
            if self.rect.colliderect(obj):
                if self.vel_x > 0:
                    self.pos_x = obj.left - self.rect.width
                elif self.vel_x < 0:
                    self.pos_x = obj.right
                self.vel_x = 0
                self.rect.topleft = (self.pos_x, self.pos_y)

        # Pulo variável
        if (teclas[pygame.K_w] or teclas[pygame.K_SPACE] or teclas[pygame.K_UP]) and self.no_chao:
            self.vel_y = self.pulo_forca
            self.no_chao = False
            self.pulo_ativo = True
            self.tempo_pulo_atual = 0
        elif self.pulo_ativo and self.tempo_pulo_atual < self.tempo_pulo_max and (
            teclas[pygame.K_w] or teclas[pygame.K_SPACE] or teclas[pygame.K_UP]
        ):
            self.vel_y += -0.7
            self.tempo_pulo_atual += 1
        else:
            self.pulo_ativo = False

        self.vel_y += self.gravidade

        if not self.no_chao and (teclas[pygame.K_s] or teclas[pygame.K_DOWN]):
            self.vel_y += 0.5

        self.pos_y += self.vel_y
        self.rect.topleft = (self.pos_x, self.pos_y)

        # Colisão vertical
        colidiu_no_chao = False
        for obj in objetos_colisao:
            if self.rect.colliderect(obj):
                if self.vel_y > 0:
                    self.pos_y = obj.top - self.rect.height
                    self.vel_y = 0
                    colidiu_no_chao = True
                    self.pulo_ativo = False
                elif self.vel_y < 0:
                    self.pos_y = obj.bottom
                    self.vel_y = 0
                self.rect.topleft = (self.pos_x, self.pos_y)

        self.no_chao = colidiu_no_chao

        # Atualiza animação se estiver andando
        if self.moving:
            self.tempo_anim += self.velocidade_anim
            if self.tempo_anim >= 1:
                self.tempo_anim = 0
                self.frame_index = (self.frame_index + 1) % len(self.frames_right)
        else:
            self.frame_index = 0

    def desenhar(self, tela, boss=False):
        if not boss:
            if not self.no_chao:
                if self.direction == "right":
                    imagem = self.imagem_pulo
                else:
                    imagem = self.imagem_pulo_esquerda
            elif self.moving:
                if self.direction == "right":
                    imagem = self.frames_right[self.frame_index]
                else:
                    imagem = self.frames_left[self.frame_index]
            else:
                if self.direction == "right":
                    imagem = self.imagem_parado
                else:
                    imagem = self.imagem_parado_esquerda

            # Ajuste vertical (exemplo: 0 para nenhum ajuste)
            ajuste_vertical = 6

            offset_x = (imagem.get_width() - self.rect.width) // 2
            offset_y = (imagem.get_height() - self.rect.height) - ajuste_vertical

            # Usar offsets para desenhar o sprite centralizado em relação à hitbox
            tela.blit(imagem, (int(self.pos_x - offset_x), int(self.pos_y - offset_y)))
        else:
            imagem = pygame.transform.scale(pygame.image.load("rivem_ani/4_riven_moviment.png"), (self.rect.width, self.rect.height))
            tela.blit(imagem, self.rect)