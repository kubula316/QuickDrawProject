import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, image, cx, cy, exref, enemy, crossref, images, eventRef):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = cx, cy
        self.lives = 3
        self.CanAttack = False
        self.FailedAttack = False
        self.IsAttacking = False
        self.sound_attacked = pygame.mixer.Sound('sounds/attack.wav')
        self.sound_hitted = pygame.mixer.Sound('sounds/hit1.wav')
        self.ExRef = exref
        self.Enemy = enemy
        self.CrossRef = crossref
        self.images = images
        self.FailEventRef = eventRef

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def Attack(self):

        if self.ExRef.AllowAttack and self.FailedAttack == False:
            if self.image == self.images['PLAYER2']:
                self.image = self.images['PLAYER2ATTACK']
                self.sound_attacked.play()
                self.Enemy.lives -= 1
                self.ExRef.AllowAttack = False
                self.IsAttacking = True
                self.Enemy.image = self.images['PLAYER1DAMAGE']
                # self.sound_hitted.play()
            elif self.image == self.images['PLAYER']:
                self.image = self.images['PLAYER1ATTACK']
                self.sound_attacked.play()
                self.Enemy.lives -= 1
                self.ExRef.AllowAttack = False
                self.Enemy.image = self.images['PLAYER2DAMAGE']
                # self.sound_hitted.play()
                self.IsAttacking = True

        else:
            self.FailedAttack = True
            self.CrossRef.drawing = True
            pygame.time.set_timer(self.FailEventRef, 3000, 1)

