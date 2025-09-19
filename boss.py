from settings import *
import random
class Boss:
    def __init__(self):
        self.image = pygame.image.load("images/boss/6.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (WINDOW_WIDTH, WINDOW_HEIGHT - 200)
        self.health = 100
        self.counter = 50

        # canais
        self.dchannel = pygame.mixer.Channel(1)
        self.achannel = pygame.mixer.Channel(2)
        self.bchannel = pygame.mixer.Channel(3)

        # sons
        self.sound_entry = pygame.mixer.Sound('music/entry.mp3')
        self.sound_laugh = pygame.mixer.Sound('music/laugh.mp3')
        self.sound_auch = pygame.mixer.Sound('music/auch.mp3')
        self.battle = pygame.mixer.Sound('music/Them_Bones.mp3')
        self.sound_heal = pygame.mixer.Sound('music/heal.mp3')

        # controle do freaky
        self.freaky_started = False
        self.laugh_played = False
        self.start_time = 0

    def take_damage(self, damage=10):
        self.health -= damage
        self.dchannel.play(self.sound_auch)
        self.change_fase()

    def heal(self, amount=20):
        if self.health + amount > 100:
            self.health = 100
        else:
            self.health += amount
        self.dchannel.play(self.sound_heal)
        self.change_fase()
    
    def is_alive(self):
        return self.health > 0
    
    def change_fase(self):
        if self.health>60:
            self.image = pygame.image.load("images/boss/6.png")
        elif self.health <= 60 and self.health > 40:
            self.image = pygame.image.load("images/boss/8.png")
        elif self.health <= 40 and self.health > 0:
            self.image = pygame.image.load("images/boss/9.png")
        self.draw(pygame.display.get_surface())

    def draw(self, tela, died=False):
        pos_img = pygame.transform.scale(self.image, (800, 800))
        if not died:
            tela.blit(pos_img, self.rect)
        else:
            tela.blit(pos_img, (self.rect.x + self.counter, self.rect.y + self.counter))
            self.counter -= 100

    def freaky(self):
        now = pygame.time.get_ticks()

        if not self.freaky_started:
            self.achannel.play(self.sound_entry)
            self.start_time = now
            self.freaky_started = True

        elif self.freaky_started and not self.laugh_played:
            if now - self.start_time > 2000:  # 2 segundos
                self.bchannel.play(self.sound_laugh)
                self.laugh_played = True

        elif self.freaky_started and self.laugh_played:
            if now - self.start_time > 12000:  # 12 segundos
                self.achannel.stop()
                self.achannel.play(self.battle)
                return True



    def start(self, tela):
        pygame.draw.rect(tela, (0, 0, 0), (0, 0, WINDOW_WIDTH*2, WINDOW_HEIGHT*2))
        self.draw(tela)
        sigma = pygame.Rect(-200, 100, 700, 250)
        sigma_img = pygame.image.load('images/boss/sigma.png').convert_alpha()
        sigma_img_a = pygame.transform.scale(sigma_img, (800, 800))
        tela.blit(sigma_img_a, sigma.topleft)
        vs = pygame.Rect((WINDOW_WIDTH//2)-200, (WINDOW_HEIGHT//2)-200, 1, 1)
        vs_img = pygame.image.load('images/boss/vs.png').convert_alpha()
        vs_img_a = pygame.transform.scale(vs_img, (400, 400))
        tela.blit(vs_img_a, vs.topleft)