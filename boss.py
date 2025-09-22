from settings import *

class Boss:
    def __init__(self):
        self.image = pygame.image.load("images/boss/6.png").convert_alpha()
        self.health = 100
        self.counter = 50

        self.dchannel = pygame.mixer.Channel(1)
        self.achannel = pygame.mixer.Channel(2)
        self.bchannel = pygame.mixer.Channel(3)


        self.sound_entry = pygame.mixer.Sound('music/entry.mp3')
        self.sound_laugh = pygame.mixer.Sound('music/laugh.mp3')
        self.sound_auch = pygame.mixer.Sound('music/auch.mp3')
        self.battle = pygame.mixer.Sound('music/Them_Bones.mp3')
        self.sound_heal = pygame.mixer.Sound('music/heal.mp3')

        self.freaky_started = False
        self.laugh_played = False
        self.start_time = 0
        self.cutscene = False
        self.update_rect()

    def update_rect(self):
        """Atualiza o rect do boss proporcional à tela."""
        screen = pygame.display.get_surface()
        if screen:
            self.rect = pygame.Rect(
                int(WINDOW_WIDTH * 0.90),
                int(WINDOW_HEIGHT * 0.5) - int(WINDOW_HEIGHT * 0.5),
                int(WINDOW_WIDTH * 0.5),
                int(WINDOW_HEIGHT)
            )

    def take_damage(self, damage=10):
        self.health -= damage
        self.dchannel.play(self.sound_auch)
        self.change_fase()

    def heal(self, amount=20):
        self.health = min(self.health + amount, 100)
        self.dchannel.play(self.sound_heal)
        self.change_fase()

    def is_alive(self):
        return self.health > 0

    def change_fase(self):
        if self.health > 60:
            self.image = pygame.image.load("images/boss/6.png").convert_alpha()
        elif self.health > 40:
            self.image = pygame.image.load("images/boss/8.png").convert_alpha()
        else:
            self.image = pygame.image.load("images/boss/9.png").convert_alpha()

    def draw(self, tela, died=False):
        boss_h = WINDOW_HEIGHT  # mantém proporção
        boss_w = int(self.image.get_width() * (boss_h / self.image.get_height()))
        pos_img = pygame.transform.scale(self.image, (boss_w, boss_h))
        
        # Posição: mais à esquerda
        pos_x = WINDOW_WIDTH - boss_w * 0.8
        pos_y = (WINDOW_HEIGHT - boss_h) // 2  # centraliza verticalmente
        
        if not died:
            tela.blit(pos_img, (pos_x, pos_y))
        else:
            self.rect.y += self.counter
            tela.fill((0, 0, 0))
            tela.blit(pos_img, (pos_x, self.rect.y))
            self.counter += 100
            self.dchannel.play(self.sound_auch)
            pygame.time.wait(200)
            
        #self.debug(tela)

    def fora_da_tela(self):
        return self.rect.top > WINDOW_HEIGHT + 100
    
    def debug(self, tela):
        pygame.draw.rect(tela, (0, 255, 0), self.rect, 2)

    def freaky(self):
        now = pygame.time.get_ticks()
        if not self.freaky_started:
            self.achannel.play(self.sound_entry)
            self.start_time = now
            self.freaky_started = True
        elif not self.laugh_played and now - self.start_time > 2000:
            self.bchannel.play(self.sound_laugh)
            self.laugh_played = True
        elif self.laugh_played and now - self.start_time > 12000:
            self.achannel.stop()
            return True

    def reset(self):
        self.__init__()

    def start(self, tela):
        # limpa tela
        pygame.draw.rect(tela, (0, 0, 0), (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))
        self.draw(tela)

        sigma_img = pygame.image.load('images/boss/sigma.png').convert_alpha()
        sigma_scaled = pygame.transform.scale(sigma_img, (WINDOW_WIDTH//2, WINDOW_HEIGHT))
        

        sigma_h = WINDOW_HEIGHT  # mantém proporção
        sigma_w = int(self.image.get_width() * (sigma_h / self.image.get_height()))
        pos_img = pygame.transform.scale(self.image, (sigma_w, sigma_h))
        
        # Posição: mais à esquerda
        pos_x = 0 - sigma_w * 0.2
        pos_y = (WINDOW_HEIGHT - sigma_h) // 2 
        tela.blit(sigma_scaled, (pos_x, pos_y))

        vs_img = pygame.image.load('images/boss/vs.png').convert_alpha()

        vs_scaled_w = int(WINDOW_WIDTH * 0.3)
        vs_scaled_h = int(WINDOW_HEIGHT * 0.4)
        vs_scaled = pygame.transform.scale(vs_img, (vs_scaled_w, vs_scaled_h))

        vs_x = (WINDOW_WIDTH - vs_scaled_w) // 2
        vs_y = (WINDOW_HEIGHT - vs_scaled_h) // 2

        tela.blit(vs_scaled, (vs_x, vs_y))

