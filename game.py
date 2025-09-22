from player import Player
from mapa import Mapa
from settings import *
from music import Music
from hostile import Hostile
from boss import Boss
from projetil import Projetil
import random
import json


pygame.init()

# Configuração principal
tela = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Two Beers for Alice')
icon = pygame.image.load('images/icon.png').convert_alpha()
pygame.display.set_icon(icon)
relogio = pygame.time.Clock()

# Estado do jogo
death = False
executando = True
cut_scene = False
#-----------------
no_menu = True 
ranqueado = False
camera_x = 0  # deslocamento do mundo
# Recursos
riven = Player()
riven_dead = pygame.image.load('images/player_dead.png').convert_alpha()
riven_dead = pygame.transform.scale(riven_dead, (200, 215))


# ------- Carregamento único das imagens -----------------------------------------
texura_ba = pygame.image.load('images/barreira/olho_barreira.png').convert_alpha()
texura_ba = pygame.transform.scale(texura_ba, (500, 400))

textura_teto1 = pygame.image.load('images/plat_papelao.png').convert_alpha()
textura_teto1 = pygame.transform.scale(textura_teto1, (100, 90))

textura_teto2 = pygame.image.load('images/plat_caixa.png').convert_alpha()
textura_teto2 = pygame.transform.scale(textura_teto2, (120, 110))

textura_teto3 = pygame.transform.scale(textura_teto1, (100, 90))

textura_chao = pygame.image.load('images/chão.png').convert_alpha()
textura_chao = pygame.transform.scale(textura_chao, (1500, 200))

# novas cargas fora do loop
tex_in1_img = pygame.image.load('images/plat_viva.png').convert_alpha()
tex_in1_img = pygame.transform.scale(tex_in1_img, (700, 290))

ponte1_img = pygame.image.load('images/ponte_1.png').convert_alpha()
ponte1_img = pygame.transform.scale(ponte1_img, (1500, 400))

ladder_img = pygame.image.load('images/ladder.png').convert_alpha()
ladder_img = pygame.transform.scale(ladder_img, (700, 490))
# ------------------------------------------------------------------

# Inimigos
inimigos = [
    Hostile(tela,camera_x, 1680, 50, 250, 230, pasta='images/inimigos/sun', base_name='sun', frame_count=7),
    Hostile(tela,camera_x, 1000, 590, 100, 110, pasta='images/inimigos/jar', base_name='jar', frame_count=10),
    Hostile(tela,camera_x, 2300, 590, 100, 110, pasta='images/inimigos/jar', base_name='jar', frame_count=10),
    Hostile(tela,camera_x, 2600, 550, 125, 150, pasta='images/inimigos/caixad', base_name='caixa', frame_count=2),
    Hostile(tela,camera_x, 4000, 560, 155, 140, pasta='images/inimigos/caranguejo', base_name='caranguejo', frame_count=10),
    Hostile(tela,camera_x, 5300, 560, 155, 140, pasta='images/inimigos/caranguejo', base_name='caranguejo', frame_count=10),
    Hostile(tela,camera_x, 5500, 50, 250, 230, pasta='images/inimigos/sun', base_name='sun', frame_count=7),
    Hostile(tela,camera_x, 8000, 50, 250, 230, pasta='images/inimigos/sun', base_name='sun', frame_count=7),
    Hostile(tela,camera_x, 5800, 550, 125, 150, pasta='images/inimigos/caixad', base_name='caixa', frame_count=2),
    Hostile(tela,camera_x, 7000, 550, 125, 150, pasta='images/inimigos/caixad', base_name='caixa', frame_count=2),
    Hostile(tela,camera_x, 5500, 560, 155, 140, pasta='images/inimigos/caranguejo', base_name='caranguejo', frame_count=10),
    Hostile(tela,camera_x, 8000, 550, 125, 150, pasta='images/inimigos/caixad', base_name='caixa', frame_count=2),
    Hostile(tela,camera_x, 7500, 590, 100, 110, pasta='images/inimigos/jar', base_name='jar', frame_count=10),
    Hostile(tela,camera_x, 6500, 590, 100, 110, pasta='images/inimigos/jar', base_name='jar', frame_count=10),
]

# configurações de inimigos
inimigos[0].vel_x = 5
inimigos[0].limite_esquerda = 1500
inimigos[0].limite_direita = 1750
inimigos[0].vel_y = 5
inimigos[0].limite_inferior += 540
inimigos[6].vel_x = 7
inimigos[6].limite_esquerda = 5499
inimigos[6].limite_direita = 9200
inimigos[6].vel_y = 7
inimigos[6].limite_inferior += 420
inimigos[7].vel_x = 7
inimigos[7].limite_esquerda = 5499
inimigos[7].limite_direita = 9201
inimigos[7].vel_y = 7
inimigos[7].limite_inferior += 420
inimigos[3].vel_y = 5
inimigos[3].limite_superior -= 150
inimigos[3].limite_inferior += 1
inimigos[8].vel_y = 5
inimigos[8].limite_superior -= 150
inimigos[8].limite_inferior += 1
inimigos[9].vel_y = 5
inimigos[9].limite_superior -= 150
inimigos[9].limite_inferior += 1
inimigos[11].vel_y = 4
inimigos[11].limite_superior -= 150
inimigos[11].limite_inferior += 1
inimigos[4].vel_x = 8
inimigos[4].limite_esquerda = 4000
inimigos[4].limite_direita = 5300
inimigos[5].vel_x = 10
inimigos[5].limite_esquerda = 4000
inimigos[5].limite_direita = 5301
inimigos[10].vel_x = 8
inimigos[10].limite_esquerda = 5499
inimigos[10].limite_direita = 9200

mapa = Mapa()


#-------------------------------------
#               Corações
#-------------------------------------

full_heart = pygame.transform.scale(pygame.image.load('images/rock_heart.png').convert_alpha(), (150,150))
empty_heart =pygame.transform.scale(pygame.image.load('images/rock_heart_auch.png').convert_alpha(), (150,150))

def camera_update(riven):
    global camera_x
    limite_camera = 742
    limite_camera2 = 500
    if riven.pos_x > limite_camera:
        camera_x += riven.vel_x
        riven.pos_x = limite_camera
        riven.rect.topleft = (riven.pos_x, riven.pos_y)
    if riven.pos_x < limite_camera2:
        camera_x += riven.vel_x
        riven.pos_x = limite_camera2
        riven.rect.topleft = (riven.pos_x, riven.pos_y)

def reset_player():
    global camera_x
    riven.pos_x = 10
    riven.pos_y = 535
    riven.rect.topleft = (riven.pos_x, riven.pos_y)
    riven.vel_x = 0
    riven.vel_y = 0
    riven.no_chao = False
    riven.pulo_ativo = False
    riven.tempo_pulo_atual = 0
    camera_x = 0

def get_player_name(tela):
    clock = pygame.time.Clock()
    input_text = ""
    ativo = True

    # Fonte proporcional ao tamanho da tela
    font_size = int(WINDOW_HEIGHT * 0.08)  # ~8% da altura da tela
    fonte = pygame.font.Font('font/Gameplay.ttf', font_size)

    while ativo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return None

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    ativo = False
                elif evento.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif len(input_text) >= 8:
                    pass  # Limite de caracteres
                else:
                    if evento.unicode.isprintable():
                        input_text += evento.unicode

        tela.fill((0, 0, 0))

        # Mensagem
        msg = fonte.render("Digite seu nome:", True, (255, 255, 255))
        msg_rect = msg.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))
        tela.blit(msg, msg_rect)

        # Texto digitado
        txt_surface = fonte.render(input_text, True, (0, 255, 0))
        txt_rect = txt_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        tela.blit(txt_surface, txt_rect)

        pygame.display.flip()
        clock.tick(30)

    return input_text



def rank():

    nome = get_player_name(tela)
    if not nome:  # jogador fechou tocando janela
        return

    data = {
        'nome': nome,
        'minutos': minutos,
        'segundos': segundos,
        'milisegundos': milissegundos
    }

    try:
        with open("db/rank.json", "r", encoding="utf-8") as f:
            ranking = json.load(f)
    except FileNotFoundError:
        ranking = []

    ranking.append(data)

    with open("db/rank.json", "w", encoding="utf-8") as f:
        json.dump(ranking, f, indent=4, ensure_ascii=False)

    print("Ranking salvo:", data)
    global ranqueado
    ranqueado = True

def mostrar_ranking(tela):
    try:
        with open("db/rank.json", "r", encoding="utf-8") as f:
            ranking = json.load(f)
    except FileNotFoundError:
        ranking = []

    # Ordena pelo tempo total (minutos*60 + segundos + milisegundos)
    ranking.sort(key=lambda x: x["minutos"]*60 + x["segundos"] + x["milisegundos"] / 1000)

    # Fonte proporcional à tela
    fonte_titulo = pygame.font.Font('font/Gameplay.ttf', int(WINDOW_HEIGHT * 0.06))  # título maior
    fonte_item = pygame.font.Font('font/Gameplay.ttf', int(WINDOW_HEIGHT * 0.04))    # itens do ranking
    fonte_out = pygame.font.Font('font/Gameplay.ttf', int(WINDOW_HEIGHT * 0.03))     # instruções

    titulo = fonte_titulo.render("RANKING", True, (255, 215, 0))
    out = fonte_out.render("Pressione Enter p/ sair", True, (255, 215, 0))

    # Limpa o fundo
    tela.fill((0, 0, 0))

    # Retângulo do placar proporcional
    placar_w = int(WINDOW_WIDTH * 0.35)
    placar_h = int(WINDOW_HEIGHT * 0.75)
    placar_x = WINDOW_WIDTH - placar_w - int(WINDOW_WIDTH * 0.02)
    placar_y = int(WINDOW_HEIGHT * 0.05)
    placar_rect = pygame.Rect(placar_x, placar_y, placar_w, placar_h)

    # Controle de scroll
    pos = 0
    rodando = True
    clock = pygame.time.Clock()

    pygame.mixer.init()
    pygame.mixer.music.load('music/Would.mp3')
    pygame.mixer.music.play(-1)

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    pygame.mixer.music.stop()
                    rodando = False
                    reset_game()  # reset do jogo quando sai do ranking

        # fundo semi-transparente do placar
        pygame.draw.rect(tela, (0, 0, 0), placar_rect)
        pygame.draw.rect(tela, (255, 215, 0), placar_rect, 3)

        # título e instrução
        tela.blit(titulo, (placar_rect.x + placar_w//2 - titulo.get_width()//2, placar_rect.y + int(WINDOW_HEIGHT*0.02)))
        tela.blit(out, (int(WINDOW_WIDTH*0.02), int(WINDOW_HEIGHT*0.02)))

        # Riven Sigma responsivo
        sigma_img = pygame.image.load('images/boss/sigma.png').convert_alpha()
        sigma_w = int(WINDOW_WIDTH * 0.5)
        sigma_h = int(WINDOW_HEIGHT * 0.8)
        sigma_img_a = pygame.transform.scale(sigma_img, (sigma_w, sigma_h))
        tela.blit(sigma_img_a, (int(WINDOW_WIDTH*0.02), int(WINDOW_HEIGHT*0.1)))

        # mostra até 10 nomes de acordo com o scroll
        item_spacing = int(WINDOW_HEIGHT * 0.06)
        for i, entry in enumerate(ranking[pos:pos+10]):
            nome = entry["nome"]
            tempo = f"{entry['minutos']:02}:{entry['segundos']:02}.{entry['milisegundos']:03}"
            texto = fonte_item.render(f"{pos+i+1}. {nome} - {tempo}", True, (255, 255, 255))
            tela.blit(texto, (placar_rect.x + int(placar_w*0.03), placar_rect.y + int(WINDOW_HEIGHT*0.1) + i*item_spacing))

        pygame.display.flip()
        clock.tick(30)


def reset_game(reset=False):
    global no_menu, ranqueado, bossfight, cut_scene, death
    global tempo_inicial, riven, boss, sequencia, indice_seq, cont, tocando, tocando_boss, projectiles

    # estado
    no_menu = True if not reset else False
    ranqueado = False
    bossfight = False
    cut_scene = False
    death = False

    # player novo
    riven = Player()
    reset_player()

    # boss novo
    boss = Boss()
    sequencia = []
    indice_seq = 0
    cont = 0
    tocando = False
    tocando_boss = False

    # cronômetro reinicia
    tempo_inicial = pygame.time.get_ticks()
    projectiles = pygame.sprite.Group()


def handle_death_screen(teclas):
    global death, tempo_inicial
    tela.fill((0, 0, 0))

    tela.blit(
        riven_dead,
        (WINDOW_WIDTH // 2 - riven_dead.get_width() // 2,
         WINDOW_HEIGHT // 2 + riven_dead.get_height() // 2)
    )

    font_size_big = max(40, WINDOW_WIDTH // 15)
    font_size_small = max(20, WINDOW_WIDTH // 48)
    font = pygame.font.Font('font/Gameplay.ttf', font_size_big)
    font1 = pygame.font.Font('font/Gameplay.ttf', font_size_small)

    text_game_over = font.render("GAME-OVER", True, (128, 0, 0))
    text_restart = font1.render("Pressione R para continuar", True, (128, 0, 0))

    rect_w = int(WINDOW_WIDTH * 0.6)
    rect_h = int(WINDOW_HEIGHT * 0.3)
    rect_x = (WINDOW_WIDTH - rect_w) // 2
    rect_y = (WINDOW_HEIGHT - rect_h) // 3
    
    # centraliza os textos
    tela.blit(
        text_game_over,
        (WINDOW_WIDTH // 2 - text_game_over.get_width() // 2,
         rect_y + rect_h // 6)
    )
    tela.blit(
        text_restart,
        (WINDOW_WIDTH // 2 - text_restart.get_width() // 2,
         rect_y + rect_h * 0.8)
    )
    # reiniciar
    if teclas[pygame.K_r]:
        death = False
        reset_player()
        reset_game(True)
        tempo_inicial = pygame.time.get_ticks()


def draw_world(camera_x):
    ba = pygame.Rect(0 - camera_x, 250, 500, 400)
    tela.blit(texura_ba, ba.topleft)
    teto1 = pygame.Rect(830 - camera_x, 500, 100, 90)
    tela.blit(textura_teto1, teto1.topleft)
    teto2 = pygame.Rect(2600 - camera_x, 295, 120, 110)
    tela.blit(textura_teto2, teto2.topleft)
    teto3 = pygame.Rect(4800 - camera_x, 500, 120, 105)
    tela.blit(textura_teto2, teto3.topleft)
    plat1 = pygame.Rect(0 - camera_x, 700, 1500, 2000)
    tela.blit(textura_chao, plat1.topleft)
    plat3 = pygame.Rect(2000 - camera_x, 700, 1500, 2000)
    tela.blit(textura_chao, plat3.topleft)
    plat4 = pygame.Rect(4000 - camera_x, 700, 1500, 2000)
    tela.blit(textura_chao, plat4.topleft)
    plat5 = pygame.Rect(7000 - camera_x, 700, 1500, 2000)
    tela.blit(textura_chao, plat5.topleft)
    plat6 = pygame.Rect(8000 - camera_x, 700, 1500, 2000)
    tela.blit(textura_chao, plat6.topleft)
    ladder1 = pygame.Rect(9500- camera_x, 602, 100, 90)
    ladder2 = pygame.Rect(9620- camera_x, 503, 100, 90)
    ladder3 = pygame.Rect(9735- camera_x, 405, 100, 90)
    ladder4 = pygame.Rect(9850- camera_x, 307, 100, 90)
    ladder5 = pygame.Rect(9967- camera_x, 208, 240, 90)
    plat_in1 = pygame.Rect(2900 - camera_x, 500, 600, 600)
    plat_in2 = pygame.Rect(5500 - camera_x, 700, 1500, 2000)
    return [plat1, teto1, ba, plat3, teto2, plat4, plat5, teto3, plat_in1, plat_in2, plat6, ladder1, ladder2, ladder3, ladder4, ladder5]


# MENU INICIAL ---
def menu_inicial():

    # desenha o fundo do menu
    fundo_menu = pygame.image.load('images/img_menu.png').convert()
    fundo_menu = pygame.transform.scale(fundo_menu, (WINDOW_WIDTH, WINDOW_HEIGHT))
    tela.blit(fundo_menu, (0, 0))
    pygame.display.flip()

def gerar_sequencia():
    teclas_possiveis = [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]
    return [random.choice(teclas_possiveis) for _ in range(4)]

# Loop do menu inicial
while no_menu:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            no_menu = False
            executando = False
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_RETURN]:
        no_menu = False
    if teclas[pygame.K_ESCAPE]:
        no_menu = False
        executando = False
    if teclas[pygame.K_r]:
        mostrar_ranking(tela)
        pass

        

    menu_inicial()
    resetou = True
    relogio.tick(30)

if resetou:
    tempo_inicial = pygame.time.get_ticks()
    bossfight = False
    rolando = False
    tocando = False
    tocando_boss = False
    sequencia = []
    indice_seq = 0
    cont = 0
    boss = Boss()
    resetou = False
    health_up = 0
    projectiles = pygame.sprite.Group()


fundo1 = pygame.image.load("images/back_b1.png").convert_alpha()
fundo1 = pygame.transform.scale(fundo1, (WINDOW_WIDTH, WINDOW_HEIGHT))
fundo2 = pygame.image.load("images/back_b22.png").convert_alpha()
fundo2 = pygame.transform.scale(fundo2, (WINDOW_WIDTH, WINDOW_HEIGHT))
scroll1 = 0
scroll2 = 0
velocidade1 = 5   # mais lento (longe)
velocidade2 =  10  # mais rápido (perto)
    
# --- LOOP PRINCIPAL ---
while executando:
    eventos = pygame.event.get()
    # Cronômetro
    for evento in eventos:
        if evento.type == pygame.QUIT:
            executando = False
    teclas = pygame.key.get_pressed()
    if not tocando:
        Love_Hate_Love = Music('music/Again.mp3')
        tocando = True
    if not bossfight:
        for enemy in inimigos:
            if enemy.vel_x != 0:
                enemy.enemy.x += enemy.vel_x * enemy.direcao_x
            if enemy.enemy.x <= enemy.limite_esquerda or enemy.enemy.x >= enemy.limite_direita:
                enemy.direcao_x *= -1
        for enemy in inimigos:
            if enemy.vel_y != 0:
                enemy.enemy.y += enemy.vel_y * enemy.direcao_y
            if enemy.enemy.y <= enemy.limite_superior or enemy.enemy.y >= enemy.limite_inferior:
                enemy.direcao_y *= -1

        if death:
            handle_death_screen(teclas)
            pygame.display.flip()
            relogio.tick(10)
            continue

        mapa.paint(tela,camera_x)
        camera_update(riven)
        objetos_colisao = draw_world(camera_x)
        riven.mover(teclas, objetos_colisao, inimigos)
        riven.desenhar(tela)

        tex = pygame.Rect(2840 - camera_x, 410, 700, 290)
        tela.blit(tex_in1_img, tex.topleft)

        ponte = pygame.Rect(5500 - camera_x, 476, 1500, 400)
        tela.blit(ponte1_img, ponte.topleft)

        tex_ladder = pygame.Rect(9500 - camera_x, 210, 700, 490)
        tela.blit(ladder_img, tex_ladder.topleft)

        boss_init = pygame.Rect(9750 - camera_x, 600, 7000, 250)

        if boss_init.colliderect(riven.rect):
            bossfight = True
            print("Bossfight")

        if riven.is_alive():
            if riven.vida == 3:
                coracao1 = full_heart
                coracao2 = full_heart
                coracao3 = full_heart
            elif riven.vida == 2:
                coracao1 = full_heart
                coracao2 = full_heart
                coracao3 = empty_heart
            elif riven.vida == 1:
                coracao1 = full_heart
                coracao2 = empty_heart
                coracao3 = empty_heart
        else:
            coracao1 = empty_heart
            coracao2 = empty_heart
            coracao3 = empty_heart
            death = True

        tela.blit(coracao1, (50, 50))
        tela.blit(coracao2, (150, 50))
        tela.blit(coracao3, (250, 50))

        for enemy in inimigos:
            if enemy.draw(tela, camera_x, riven):
                riven.tomar_dano() 
                pass
        if riven.pos_y >= 2000 and not bossfight:
            death = True
    else:

        if death:
            bossfight = False
            handle_death_screen(teclas)
            pygame.display.flip()
            relogio.tick(10)
            canal.stop()
            

        Love_Hate_Love.stop_music()
        boss.start(tela)
        if boss.freaky() and boss.is_alive():
            if not tocando_boss:
                canal = pygame.mixer.Channel(0)
                canal.play(boss.battle,-1)
                tocando_boss = True

            
            tela.fill((0, 0, 0))

            # Atualizar o scroll (subindo)
            scroll1 -= velocidade1
            scroll2 -= velocidade2
            # Reset para loop infinito
            if scroll1 <= -WINDOW_HEIGHT:
                scroll1 = 0
            if scroll2 <= -WINDOW_HEIGHT:
                scroll2 = 0
            # Desenhar cada fundo 2x para "tapar buraco"
            tela.blit(fundo1, (0, scroll1))
            tela.blit(fundo1, (0, scroll1 + WINDOW_HEIGHT))
            tela.blit(fundo2, (0, scroll2))
            tela.blit(fundo2, (0, scroll2 + WINDOW_HEIGHT))

            boss.draw(tela)
            riven.rect.center = (WINDOW_WIDTH*0.08, (WINDOW_HEIGHT//2))
            riven.desenhar(tela, True)


            bar_w = int(WINDOW_WIDTH * 0.4)   # barra ocupa 40% da largura da tela
            bar_h = int(WINDOW_HEIGHT * 0.03) # altura proporcional à tela
            bar_x = (WINDOW_WIDTH - bar_w) // 2  # centraliza horizontalmente
            bar_y = int(WINDOW_HEIGHT * 0.05)   # 5% do topo da tela

            # barra vermelha (fundo)
            pygame.draw.rect(tela, (255, 0, 0), (bar_x, bar_y, bar_w, bar_h))

            # barra verde (vida atual)
            pygame.draw.rect(tela, (0, 255, 0), (bar_x, bar_y, int(bar_w * (boss.health / 100)), bar_h))
            
            if riven.is_alive():
                if riven.vida == 3:
                    coracao1 = full_heart
                    coracao2 = full_heart
                    coracao3 = full_heart
                elif riven.vida == 2:
                    coracao1 = full_heart
                    coracao2 = full_heart
                    coracao3 = empty_heart
                elif riven.vida == 1:
                    coracao1 = full_heart
                    coracao2 = empty_heart
                    coracao3 = empty_heart
            else:
                coracao1 = empty_heart
                coracao2 = empty_heart
                coracao3 = empty_heart
                death = True

            tela.blit(coracao1, (50, 50))
            tela.blit(coracao2, (150, 50))
            tela.blit(coracao3, (250, 50))


            if not sequencia:
                sequencia = gerar_sequencia()
                r_x, r_y = random.randint(0, WINDOW_WIDTH//2), random.randint(0, int(WINDOW_HEIGHT*0.90))
                indice_seq = 0
                print("Sequência:", [pygame.key.name(t).upper() for t in sequencia])
            
            fonte = pygame.font.Font('font/Gameplay.ttf', 50)
            for i, tecla in enumerate(sequencia):
                cor = (255, 255, 255)
                if i < indice_seq:
                    cor = (0, 255, 0)
                texto = fonte.render(pygame.key.name(tecla).upper(), True, cor) 
                tela.blit(texto, (r_x + i*60, r_y))


            for evento in eventos:
                if evento.type == pygame.KEYDOWN:
                    if evento.key == sequencia[indice_seq]:
                        indice_seq += 1
                        if indice_seq >= len(sequencia):
                            new_proj = Projetil(boss)
                            projectiles.add(new_proj)
                            print("Acertou! Boss HP:", boss.health)
                            sequencia = []
                            health_up += 1
                    else:
                        print("Errou! Reiniciando sequência")
                        boss.heal(25)
                        riven.tomar_dano()
                        indice_seq = 0

            if health_up >= 3:
                riven.recuperar_vida()
                health_up = 0
                
        if not boss.is_alive():
            boss.draw(tela, True)
            if not ranqueado and boss.fora_da_tela():
                pygame.time.wait(1000)
                canal.stop()
                rank()
                mostrar_ranking(tela)


        
    # Cronômetro MM:SS
    tempo_decorrido = (pygame.time.get_ticks() - tempo_inicial) // 1000 if boss.is_alive() else tempo_decorrido
    minutos = tempo_decorrido // 60
    segundos = tempo_decorrido % 60
    milissegundos = (pygame.time.get_ticks() - tempo_inicial) % 1000
    font_cronometro = pygame.font.Font('font/Gameplay.ttf', 40)
    texto_cronometro = font_cronometro.render(f"{minutos:02}:{segundos:02}.{milissegundos:03}", True, (255, 255, 255))
    if not bossfight or boss.is_alive():
        tela.blit(texto_cronometro, (WINDOW_WIDTH - 250, 20 ))
    dt = relogio.get_time() / 1000
    projectiles.update(dt)
    projectiles.draw(tela)
    pygame.display.flip()
    relogio.tick(60)

pygame.quit()
