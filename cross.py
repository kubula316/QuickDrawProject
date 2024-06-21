import pygame


class Cross():

    def __init__(self, image, cx, cy):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = cx, cy
        self.drawing = False
        self.sound_played = False
        self.Failsound = pygame.mixer.Sound('sounds/failed1.wav')

    def draw(self, surface):
        if self.drawing:
            surface.blit(self.image, self.rect)
            if not self.sound_played:
                self.Failsound.play()
                self.sound_played = True
        else:
            self.sound_played = False
