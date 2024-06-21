import pygame, random
class Exclamation():
    def __init__(self, image, cx, cy, player1, player2, levelRef, AiEvent):
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
        self.player1 = player1
        self.player2 = player2
        self.sound_event = pygame.mixer.Sound('sounds/click2.wav')
        self.levelRef = levelRef
        self.AiEvent = AiEvent


    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def checkAttack(self):

        if self.AllowAttack:
            if self.start_time is None:
                self.start_time = pygame.time.get_ticks()
            current_time = pygame.time.get_ticks()
            if current_time - self.start_time <= 500:
                self.IsDraw = True
                self.player1.CanAttack = True
                self.player2.CanAttack = True
                if not self.sound_played:
                    self.sound_event.play()
                    self.sound_played = True

            else:
                self.AllowAttack = False
                self.start_time = None
                self.player1.CanAttack = False
                self.player2.CanAttack = False
                self.sound_played = False

    def startTimer(self):
        current_time2 = pygame.time.get_ticks()
        if self.start_time2 is None:
            self.start_time2 = current_time2
            self.random_interval = random.randint(3000, 5000)
        if current_time2 - self.start_time2 >= self.random_interval:
            self.AllowAttack = True
            self.start_time2 = current_time2
            self.random_interval = random.randint(1500, 3500)
            if self.levelRef.Singleplayer:
                los = random.randint(250, 450)
                pygame.time.set_timer(self.AiEvent, los, 1)