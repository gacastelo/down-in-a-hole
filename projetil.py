from settings import *


class Projetil(pygame.sprite.Sprite):
    def __init__(self, boss):
        super().__init__()
        self.x = WINDOW_WIDTH * 0.12
        self.y = boss.rect.centery
        # Carrega frames
        self.image_paths = [
            "images/projetil/0.png",
            "images/projetil/1.png",
            "images/projetil/2.png",
            "images/projetil/3.png",
            "images/projetil/4.png"
        ]
        # Carrega e escala todos os frames
        frame_w = int(WINDOW_WIDTH * 0.1)
        frame_h = int(WINDOW_HEIGHT * 0.2)
        self.frames = [pygame.transform.scale(pygame.image.load(img).convert_alpha(), (frame_w, frame_h)) for img in self.image_paths]

        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(center=(self.x, self.y))

        self.speed = 1000
        self.boss = boss

        self.animation_timer = 0
        self.animation_speed = 100  # ms por frame

    def update(self, dt):
        # Move para a direita
        self.rect.x += self.speed * dt
        # Atualiza animação
        self.animation_timer += dt * 1000
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]  # usa os frames já escalados

        # Colisão com boss
        if self.rect.colliderect(self.boss.rect):
            print("Acertou! Boss HP:", self.boss.health)
            self.boss.take_damage(25)
            self.kill()

        # Saiu da tela
        if self.rect.left > WINDOW_WIDTH:
            print("Projetil fora da tela")
            self.kill()
        print("DEBUG: Projetil x:", self.rect.x, "y:", self.rect.y)