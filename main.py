import pygame, os, random

pygame.init()

SIZESCREEN = WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode(SIZESCREEN)
clock = pygame.time.Clock()
# wczytywanie grafik
path = os.path.join(os.getcwd(), 'images')
file_names = os.listdir(path)
LIGHTGREEN = pygame.color.THECOLORS['lightgreen']
RED = pygame.color.THECOLORS['red']
BACKGROUND = pygame.image.load(os.path.join(path, 'Background.png')).convert()
MENU = pygame.image.load(os.path.join(path, 'MENU.png')).convert()
Failed_Attack_P1 = pygame.USEREVENT + 1
Failed_Attack_P2 = pygame.USEREVENT + 2

file_names.remove('Background.png')
IMAGES = {}
for file_name in file_names:
    image_name = file_name[:-4].upper()
    IMAGES[image_name] = pygame.image.load(os.path.join(path, file_name)).convert_alpha(BACKGROUND)


# klasa reprezentująca gracza
class Player(pygame.sprite.Sprite):
    def __init__(self, image, cx, cy):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = cx, cy
        self.lives = 3
        self.CanAttack = False
        self.FailedAttack = False
        self.IsAttacking = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def Attack(self):

        if exclamation.AllowAttack and self.FailedAttack == False:
            if self.image == IMAGES['PLAYER2']:
                self.image = IMAGES['PLAYER2ATTACK']
                player.lives -= 1
                exclamation.AllowAttack = False
                player2.IsAttacking = True
                player.image = IMAGES['PLAYER1DAMAGE']
            elif self.image == IMAGES['PLAYER']:
                self.image = IMAGES['PLAYER1ATTACK']
                player2.lives -= 1
                exclamation.AllowAttack = False
                player2.image = IMAGES['PLAYER2DAMAGE']
                player.IsAttacking = True
        else:
            print("Atak Zjeabyy")
            self.FailedAttack = True
            if self.image == IMAGES['PLAYER']:
                cross.drawing = True
                pygame.time.set_timer(Failed_Attack_P1, 3000, 1)
            if self.image == IMAGES['PLAYER2']:
                cross2.drawing = True
                pygame.time.set_timer(Failed_Attack_P2, 3000, 1)


class Exclamation():
    def __init__(self, image, cx, cy):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = cx, cy
        self.AllowAttack = False
        self.IsDraw = False
        self.start_time = None
        self.start_time2 = None
        self.random_interval = random.randint(1000, 3000)  # Random interval between 1 and 3 seconds

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def checkAttack(self):
        if exclamation.AllowAttack:
            if self.start_time is None:
                self.start_time = pygame.time.get_ticks()
            # Check the time elapsed
            current_time = pygame.time.get_ticks()
            if current_time - self.start_time <= 500:  # 2000 milliseconds = 2 seconds
                exclamation.draw(screen)
                player.CanAttack = True
                player2.CanAttack = True
            else:
                exclamation.AllowAttack = False
                self.start_time = None
                player.CanAttack = False
                player2.CanAttack = False

    def startTimer(self):
        current_time2 = pygame.time.get_ticks()
        if self.start_time2 is None:
            self.start_time2 = current_time2
            self.random_interval = random.randint(2000, 4000)  # Generate new random interval
            print(self.random_interval / 1000)
        if current_time2 - self.start_time2 >= self.random_interval:
            # Perform the action
            self.AllowAttack = True
            # Reset the timer
            self.start_time2 = current_time2
            self.random_interval = random.randint(2000, 4000)  # Generate new random interval for next action
            print(self.random_interval / 1000)


class Cross():
    def __init__(self, image, cx, cy):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = cx, cy
        self.drawing = False

    def draw(self, surface):
        if self.drawing:
            surface.blit(self.image, self.rect)


class Level():
    def __init__(self, player, player2):
        self.player1 = player
        self.player2 = player2
        self.IntroWasPlayed = False
        self.GameHasEnded = False
        self.MenuActive = True

    def draw(self):
        if not self.MenuActive:
            screen.blit(BACKGROUND, [0, 0])
            player.draw(screen)
            player2.draw(screen)
            cross.draw(screen)
            cross2.draw(screen)
            for i in range(self.player1.lives):
                screen.blit(IMAGES['HEARTH2'], (20 + i * 120, 750))
            for i in range(self.player2.lives):
                screen.blit(IMAGES['HEARTH2'], (1460 - i * 120, 20))
        else:
            screen.blit(MENU, [0, 0])
            play.draw(screen)

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
        self.GameHasEnded = True
        self.MenuActive = True
        self.P1Won = False
        self.P2Won = False
        player.rect.center = -150, 500
        player2.rect.center = 1750, 300
        player.image = IMAGES['PLAYER']
        player2.image = IMAGES["PLAYER2"]

class Text:
    def __init__(self, text, text_color, pc_x, pc_y, font_size=36, font_type=None):
        self.text = str(text)
        self.text_color = text_color
        self.font_size = font_size
        self.font_type = font_type
        self.font = pygame.font.SysFont(self.font_type, self.font_size)
        self.pc_x = pc_x
        self.pc_y = pc_y

    def draw(self, surface):
        self.image = self.font.render(self.text, True, self.text_color)
        self.rect = self.image.get_rect()
        self.rect.center = self.pc_x, self.pc_y
        surface.blit(self.image, self.rect)


class Button(pygame.sprite.Sprite):
    def __init__(self, image, cx, cy):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = cx, cy

    def draw(self, surface):
        if not self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image = IMAGES['PLAY01']
            surface.blit(self.image, self.rect)
        else:
            self.image = IMAGES['PLAY02']
            surface.blit(self.image, self.rect)



# konkretyzacja obiektów
player = Player(IMAGES['PLAYER'], -150, 500)
player2 = Player(IMAGES['PLAYER2'], 1750, 300)
level = Level(player, player2)
exclamation = Exclamation(IMAGES['EXCLAMATION'], 800, 400)
cross = Cross(IMAGES['CROSS'], 550, 500)
cross2 = Cross(IMAGES['CROSS'], 1050, 300)
P1_win_text = Text("P1 WINS!", RED, *screen.get_rect().center, font_size=250, font_type="Ink Free")
play = Button(IMAGES['PLAY01'], WIDTH/2, HEIGHT/2)
# pętla gry
window_open = True

while window_open:
    level.draw()
    # pętla zdarzeń
    if not level.MenuActive:
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
                    print("Remis")
                # ATAKI GRACZY
                if event.key == pygame.K_RIGHT:
                    player2.Attack()
                if event.key == pygame.K_LEFT:
                    player.Attack()

            if event.type == pygame.QUIT:
                window_open = False
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
                    pygame.time.delay(500)
                    player.image = IMAGES['PLAYER']
                    player2.image = IMAGES["PLAYER2"]
                    player.rect.center = 550, 500
                    player2.FailedAttack = False
                    cross2.drawing = False
                    player.IsAttacking = False
                else:
                    print("P1 wygrywa!")
                    level.GameHasEnded = True
                    level.P1Won = True
                    P1_win_text.draw(screen)
                    pygame.display.flip()
                    with open('Match_history.txt', 'a') as file:
                        file.write("P1Wins\n")
                    pygame.time.delay(5000)
                    level.MenuActive = True
                    level.ResetGame()

        if player2.IsAttacking:
            if player2.rect.x > 600:
                player2.rect.x -= 60
            if player2.rect.y < 400:
                player2.rect.y += 20
            if player2.rect.x < 600 and player.rect.y > 200:
                pygame.time.delay(500)
                if player.lives > 0:
                    player2.image = IMAGES['PLAYER2']
                    player.image = IMAGES["PLAYER"]
                    player2.rect.center = 1050, 300
                    player.FailedAttack = False
                    cross.drawing = False
                    player2.IsAttacking = False
                else:
                    print("P2 wygrywa!")
                    level.GameHasEnded = True
        exclamation.checkAttack()
    else:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    window_open = False
                if event.key == pygame.K_UP:
                    level.MenuActive = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play.rect.collidepoint(pygame.mouse.get_pos()):
                    level.MenuActive = False
                    pygame.time.delay(600)

    # rysowanie i aktualizacja obiektów

    # aktualizacja okna gry
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
