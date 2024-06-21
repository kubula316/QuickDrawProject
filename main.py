import pygame, os, random, datetime
import pygame.mixer
from player import Player
from cross import Cross
from text import Text
from button import Button
from leaderboard import Leaderboard
from exclamation import Exclamation

pygame.init()

SIZESCREEN = WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode(SIZESCREEN)
clock = pygame.time.Clock()
# wczytywanie grafik
path = os.path.join(os.getcwd(), 'images')
file_names = os.listdir(path)
LIGHTGREEN = pygame.color.THECOLORS['lightgreen']
RED = pygame.color.THECOLORS['red']
BLACK = pygame.color.THECOLORS['black']
ORANGE = (255, 77, 0)
BACKGROUND = pygame.image.load(os.path.join(path, 'Background.png')).convert()
BOARD = pygame.image.load(os.path.join(path, 'board.png')).convert()
MENU = pygame.image.load(os.path.join(path, 'MENU.png')).convert()
Failed_Attack_P1 = pygame.USEREVENT + 1
Failed_Attack_P2 = pygame.USEREVENT + 2
AI_Attack = pygame.USEREVENT + 3

# -------------------------------DŹWIĘKI-------------------------------
pygame.mixer.init()
sound_main = pygame.mixer.Sound('sounds/background.wav')
sound_click = pygame.mixer.Sound('sounds/click.wav')
sound_attack = pygame.mixer.Sound('sounds/attack.wav')
sound_hit = pygame.mixer.Sound('sounds/hit1.wav')
sound_win = pygame.mixer.Sound('sounds/win.wav')

# ---------------------------------------------------------------------
file_names.remove('Background.png')
IMAGES = {}
for file_name in file_names:
    image_name = file_name[:-4].upper()
    IMAGES[image_name] = pygame.image.load(os.path.join(path, file_name)).convert_alpha(BACKGROUND)


class Level():
    def __init__(self, player, player2):
        self.player1 = player
        self.player2 = player2
        self.IntroWasPlayed = False
        self.MenuActive = True
        self.WatchLeaderboard = False
        self.ChoseGamemode = False
        self.Singleplayer = False

    def draw(self):
        if self.WatchLeaderboard:
            screen.blit(MENU, [0, 0])
            Leaderboard('Match_history.txt', BOARD).display(screen)
            home3.draw(screen)
        elif self.ChoseGamemode:
            screen.blit(MENU, [0, 0])
            singleplayer.draw(screen)
            multiplayer.draw(screen)
            home2.draw(screen)
        elif not self.MenuActive:
            screen.blit(BACKGROUND, [0, 0])
            player.draw(screen)
            player2.draw(screen)
            cross.draw(screen)
            cross2.draw(screen)
            for i in range(self.player1.lives):
                screen.blit(IMAGES['HEARTH2'], (20 + i * 120, 750))
            for i in range(self.player2.lives):
                screen.blit(IMAGES['HEARTH2'], (1460 - i * 120, 20))
            if exclamation.AllowAttack:
                if exclamation.IsDraw:
                    exclamation.draw(screen)

        else:
            screen.blit(MENU, [0, 0])
            play.draw(screen)
            leaderboard.draw(screen)
            home.draw(screen)

    def ResetGame(self):
        self.player1.lives = 3
        self.player1.CanAttack = False
        self.player1.FailedAttack = False
        self.player1.IsAttacking = False
        self.player2.lives = 3
        self.player2.CanAttack = False
        self.player2.FailedAttack = False
        self.player2.IsAttacking = False
        self.IntroWasPlayed = False
        self.MenuActive = True
        self.Singleplayer = False
        self.ChoseGamemode = False
        cross.drawing = False
        cross2.drawing = False
        player.rect.center = -150, 500
        player2.rect.center = 1750, 300
        player.image = IMAGES['PLAYER']
        player2.image = IMAGES["PLAYER2"]


# konkretyzacja obiektów
exclamation = Exclamation(IMAGES['EXCLAMATION'], 800, 400, None, None, None, AI_Attack)
cross = Cross(IMAGES['CROSS'], 550, 500)
cross2 = Cross(IMAGES['CROSS'], 1050, 300)
player = Player(IMAGES['PLAYER'], -150, 500, exclamation, None, cross, IMAGES, Failed_Attack_P1)
player2 = Player(IMAGES['PLAYER2'], 1750, 300, exclamation, player, cross2, IMAGES, Failed_Attack_P2)
level = Level(player, player2)

exclamation.levelRef = level
exclamation.player1 = player
exclamation.player2 = player2
player.Enemy = player2


P1_win_text = Text("P1 WINS!", ORANGE, screen.get_width() - 550, screen.get_height() - 150, font_size=250,
                   font_type="ARCADECLASSIC.ttf")
P2_win_text = Text("P2 WINS!", ORANGE, screen.get_width() - 950, 125, font_size=250, font_type="ARCADECLASSIC.ttf")
play = Button(IMAGES['PLAY01'], IMAGES['PLAY02'], WIDTH / 2, HEIGHT / 2 - 140)
singleplayer = Button(IMAGES['SINGLE'], IMAGES['SINGLE2'], WIDTH / 2 - 330, HEIGHT / 2)
multiplayer = Button(IMAGES['MULTI'], IMAGES['MULTI2'], WIDTH / 2 + 330, HEIGHT / 2)
leaderboard = Button(IMAGES['LEADERBOARD01'], IMAGES['LEADERBOARD02'], WIDTH / 2, HEIGHT / 2)
home = Button(IMAGES['HOME01'], IMAGES['HOME02'], WIDTH / 2, HEIGHT / 2 + 140)
home2 = Button(IMAGES['HOME01'], IMAGES['HOME02'], WIDTH / 2, HEIGHT / 2 + 250)
home3 = Button(IMAGES['HOME01'], IMAGES['HOME02'], WIDTH / 2, HEIGHT / 2 - 370)

# pętla gry
window_open = True
sound_main.set_volume(0.05)
sound_main.play(loops=-1)
print(IMAGES)
while window_open:
    # rysowanie i aktualizacja obiektów
    level.draw()
    # pętla zdarzeń
    if not level.MenuActive and not level.ChoseGamemode:
        if not level.IntroWasPlayed:
            if player.rect.x < 550 - 190 and player2.rect.x > 1050 - 190:
                player.rect.x += 10
                player2.rect.x -= 10
            else:
                level.IntroWasPlayed = True
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    level.MenuActive = True
                    level.ResetGame()
                if event.key == pygame.K_RIGHT and event.key == pygame.K_LEFT:
                    print("Remis(Bardzo mała szansa)")
                # ATAKI GRACZY
                elif event.key == pygame.K_RIGHT:
                    player2.Attack()
                elif event.key == pygame.K_LEFT:
                    player.Attack()

            if event.type == pygame.QUIT:
                window_open = False
            if event.type == AI_Attack and exclamation.AllowAttack:
                player2.Attack()
                player2.CanAttack = False
            if event.type == Failed_Attack_P1:
                player.FailedAttack = False
                cross.drawing = False
            if event.type == Failed_Attack_P2:
                player2.FailedAttack = False
                cross2.drawing = False

        exclamation.startTimer()

        if player.IsAttacking:
            if player.rect.x < 600:
                player.rect.x += 60
            if player.rect.y > 200:
                player.rect.y -= 20
            if player.rect.x > 600 and player.rect.y < 200:
                if player2.lives > 0:
                    pygame.time.delay(100)
                    sound_hit.play()
                    pygame.time.delay(400)
                    player.image = IMAGES['PLAYER']
                    player2.image = IMAGES["PLAYER2"]
                    player.rect.center = 550, 500
                    player2.FailedAttack = False
                    cross2.drawing = False
                    player.IsAttacking = False
                else:
                    P1_win_text.draw(screen)
                    sound_win.play()
                    pygame.display.flip()
                    data = datetime.datetime.now()
                    data = data.replace(second=0, microsecond=0)
                    data = data.strftime("%Y-%m-%d %H:%M")
                    with open('Match_history.txt', 'a') as file:
                        file.write(f"P1         {player.lives}-{player2.lives}         {data}\n")
                    pygame.time.delay(3000)
                    level.MenuActive = True
                    level.ResetGame()

        if player2.IsAttacking:
            if player2.rect.x > 600:
                player2.rect.x -= 60
            if player2.rect.y < 400:
                player2.rect.y += 20
            if player2.rect.x < 600 and player.rect.y > 200:
                pygame.time.delay(100)
                sound_hit.play()
                pygame.time.delay(400)

                if player.lives > 0:
                    player2.image = IMAGES['PLAYER2']
                    player.image = IMAGES["PLAYER"]
                    player2.rect.center = 1050, 300
                    player.FailedAttack = False
                    cross.drawing = False
                    player2.IsAttacking = False
                else:
                    P2_win_text.draw(screen)
                    sound_win.play()
                    pygame.display.flip()
                    data = datetime.datetime.now()
                    data = data.replace(second=0, microsecond=0)
                    data = data.strftime("%Y-%m-%d %H:%M")
                    with open('Match_history.txt', 'a') as file:
                        file.write(f"P2         {player.lives}-{player2.lives}         {data}\n")
                    pygame.time.delay(3000)
                    level.MenuActive = True
                    level.ResetGame()
        exclamation.checkAttack()
    else:
        # Pętla menu
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if level.ChoseGamemode:
                        level.ChoseGamemode = False
                    elif level.WatchLeaderboard:
                        level.WatchLeaderboard = False
                    else:
                        window_open = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play.rect.collidepoint(
                        pygame.mouse.get_pos()) and not level.ChoseGamemode and not level.WatchLeaderboard:
                    sound_click.play()
                    level.ChoseGamemode = True
                    pygame.time.delay(150)
                if singleplayer.rect.collidepoint(
                        pygame.mouse.get_pos()) and level.ChoseGamemode and not level.WatchLeaderboard:
                    sound_click.play()
                    level.Singleplayer = True
                    level.MenuActive = False
                    level.ChoseGamemode = False
                    pygame.time.delay(150)
                if multiplayer.rect.collidepoint(
                        pygame.mouse.get_pos()) and level.ChoseGamemode and not level.WatchLeaderboard:
                    sound_click.play()
                    level.MenuActive = False
                    level.ChoseGamemode = False
                    pygame.time.delay(150)
                if home2.rect.collidepoint(pygame.mouse.get_pos()) and level.ChoseGamemode:
                    sound_click.play()
                    level.ChoseGamemode = False
                    pygame.time.delay(150)
                if leaderboard.rect.collidepoint(
                        pygame.mouse.get_pos()) and not level.ChoseGamemode and not level.WatchLeaderboard:
                    sound_click.play()
                    level.WatchLeaderboard = True
                    pygame.time.delay(150)
                if home3.rect.collidepoint(pygame.mouse.get_pos()) and level.WatchLeaderboard:
                    sound_click.play()
                    level.WatchLeaderboard = False
                    pygame.time.delay(150)
                if (home.rect.collidepoint(pygame.mouse.get_pos())
                        and not level.ChoseGamemode
                        and not level.WatchLeaderboard):
                    sound_click.play()
                    window_open = False
                    pygame.time.delay(150)

    # aktualizacja okna gry
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
