import pygame, os, random, datetime
import pygame.mixer

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
AI_Attack = pygame.USEREVENT + 3

# -------------------------------DŹWIĘKI-------------------------------
pygame.mixer.init()
# sound_main = pygame.mixer.Sound('-------')
sound_hover = pygame.mixer.Sound('sounds/hover.wav')
sound_click = pygame.mixer.Sound('sounds/click.wav')
sound_attack = pygame.mixer.Sound('sounds/attack.wav')
sound_failed_attack = pygame.mixer.Sound('sounds/failed1.wav')
sound_hit = pygame.mixer.Sound('sounds/hit1.wav')
# sound_final = pygame.mixer.Sound('--------')
sound_event = pygame.mixer.Sound('sounds/click2.wav')
# ---------------------------------------------------------------------
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
        self.sound_attacked = sound_attack
        self.sound_hitted = sound_hit

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def Attack(self):

        if exclamation.AllowAttack and self.FailedAttack == False:
            if self.image == IMAGES['PLAYER2']:
                self.image = IMAGES['PLAYER2ATTACK']
                self.sound_attacked.play()
                player.lives -= 1
                exclamation.AllowAttack = False
                player2.IsAttacking = True
                player.image = IMAGES['PLAYER1DAMAGE']
                # self.sound_hitted.play()
            elif self.image == IMAGES['PLAYER']:
                self.image = IMAGES['PLAYER1ATTACK']
                self.sound_attacked.play()
                player2.lives -= 1
                exclamation.AllowAttack = False
                player2.image = IMAGES['PLAYER2DAMAGE']
                # self.sound_hitted.play()
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
        self.sound_played = False

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
                if self.sound_played == False:
                    sound_event.play()
                    self.sound_played = True

            else:
                exclamation.AllowAttack = False
                self.start_time = None
                player.CanAttack = False
                player2.CanAttack = False
                self.sound_played = False
                if level.Singleplayer:
                    los = 500 + self.random_interval
                    pygame.time.set_timer(AI_Attack, los, 1)

    def startTimer(self):
        current_time2 = pygame.time.get_ticks()
        if self.start_time2 is None:
            self.start_time2 = current_time2
            self.random_interval = random.randint(2000, 4000)  # Generate new random interval
            print(self.random_interval / 1000)
            if level.Singleplayer:
                los = 500 + self.random_interval
                pygame.time.set_timer(AI_Attack, los, 1)
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
        self.sound_played = False

    def draw(self, surface):
        if self.drawing:
            surface.blit(self.image, self.rect)
            if not self.sound_played:
                sound_event.play()
                self.sound_played = True
        else:
            self.sound_played = False


class Level():
    def __init__(self, player, player2):
        self.player1 = player
        self.player2 = player2
        self.IntroWasPlayed = False
        self.MenuActive = True
        self.WatchLeaderboard = False
        self.Singleplayer = False

    def draw(self):
        if self.WatchLeaderboard:
            screen.blit(MENU, [0, 0])
            Leaderboard('Match_history.txt').display(screen)
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
    def __init__(self, image, image2, cx, cy):
        super().__init__()
        self.image = image
        self.image2 = image2
        self.rect = self.image.get_rect()
        self.rect.center = cx, cy
        self.sound_hovered = sound_hover
        self.hover_sound_played = False

    def draw(self, surface):
        if not self.rect.collidepoint(pygame.mouse.get_pos()):
            surface.blit(self.image, self.rect)
            self.hover_sound_played = False
        else:
            surface.blit(self.image2, self.rect)
            if not self.hover_sound_played:
                self.sound_hovered.play()
                self.hover_sound_played = True


class Leaderboard:
    def __init__(self, filename, font_size=50, font_color=(55, 15, 0)):
        self.filename = filename
        self.font_size = font_size
        self.font_color = font_color
        self.font = pygame.font.Font(None, font_size)
        self.match_history = self.load_match_history()

    def load_match_history(self):
        match_history = []
        with open(self.filename, 'r') as file:
            lines = file.readlines()
            match_history = [line.strip() for line in lines[-10:]]
        return match_history

    def display(self, surface):
        # pozycja wyników sigmy
        y_offset = 300
        x_offset = 600
        next_line_offset = 50
        for match in reversed(self.match_history):
            text_surface = self.font.render(match, True, self.font_color)
            surface.blit(text_surface, (x_offset, y_offset))
            y_offset += next_line_offset


# konkretyzacja obiektów
player = Player(IMAGES['PLAYER'], -150, 500)
player2 = Player(IMAGES['PLAYER2'], 1750, 300)
level = Level(player, player2)
exclamation = Exclamation(IMAGES['EXCLAMATION'], 800, 400)
cross = Cross(IMAGES['CROSS'], 550, 500)
cross2 = Cross(IMAGES['CROSS'], 1050, 300)
P1_win_text = Text("P1 WINS!", RED, *screen.get_rect().center, font_size=250, font_type="Ink Free")
P2_win_text = Text("P2 WINS!", RED, *screen.get_rect().center, font_size=250, font_type="Ink Free")
play = Button(IMAGES['PLAY01'], IMAGES['PLAY02'], WIDTH / 2, HEIGHT / 2 - 140)
leaderboard = Button(IMAGES['LEADERBOARD01'], IMAGES['LEADERBOARD02'], WIDTH / 2, HEIGHT / 2)
home = Button(IMAGES['HOME01'], IMAGES['HOME02'], WIDTH / 2, HEIGHT / 2 + 140)

# pętla gry
window_open = True

while window_open:
    # rysowanie i aktualizacja obiektów
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
                    print("Remis(Bardzo mała szansa)")
                # ATAKI GRACZY
                elif event.key == pygame.K_RIGHT:
                    player2.Attack()
                elif event.key == pygame.K_LEFT:
                    player.Attack()

            if event.type == pygame.QUIT:
                window_open = False
            if event.type == AI_Attack:
                player2.Attack()
                print("DEBUG")
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
                    pygame.display.flip()
                    data = datetime.datetime.now()
                    data = data.replace(second=0, microsecond=0)
                    data = data.strftime("%Y-%m-%d %H:%M")
                    with open('Match_history.txt', 'a') as file:
                        file.write(f"P1 {player.lives}-{player2.lives} {data}\n")
                    pygame.time.delay(5000)
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
                    pygame.display.flip()
                    data = datetime.datetime.now()
                    data = data.replace(second=0, microsecond=0)
                    data = data.strftime("%Y-%m-%d %H:%M")
                    with open('Match_history.txt', 'a') as file:
                        file.write(f"P2 {player.lives}-{player2.lives} {data}\n")
                    pygame.time.delay(5000)
                    level.MenuActive = True
                    level.ResetGame()
        exclamation.checkAttack()
    else:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if level.WatchLeaderboard:
                        level.WatchLeaderboard = False
                    else:
                        window_open = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play.rect.collidepoint(pygame.mouse.get_pos()):
                    sound_click.play()
                    level.MenuActive = False
                    pygame.time.delay(600)
                if leaderboard.rect.collidepoint(pygame.mouse.get_pos()):
                    sound_click.play()
                    level.WatchLeaderboard = True
                if home.rect.collidepoint(pygame.mouse.get_pos()):
                    sound_click.play()
                    window_open = False

    # aktualizacja okna gry
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
