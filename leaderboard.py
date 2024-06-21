import pygame


class Leaderboard:
    def __init__(self, filename, image ,font_size=50, font_color=(55, 15, 0)):
        self.filename = filename
        self.font_size = font_size
        self.font_color = font_color
        self.font = pygame.font.Font(None, font_size)
        self.match_history = self.load_match_history()
        self.image = image

    def load_match_history(self):
        match_history = []
        with open(self.filename, 'r') as file:
            lines = file.readlines()
            match_history = [line.strip() for line in lines[-6:]]
        return match_history

    def display(self, surface):

        surface.blit(self.image, (1600 / 2 - 375, 900 / 2 - 310))
        table_text = "|  WON  |  LIVES  |             DATE             |"

        table = self.font.render(table_text, True, self.font_color)
        # pozycja wyników
        y_offset = 250
        x_offset = 540
        next_line_offset = 50

        surface.blit(table, (485, 160))
        for match in reversed(self.match_history):
            text_surface = self.font.render(match, True, self.font_color)
            surface.blit(text_surface, (x_offset, y_offset))
            y_offset += next_line_offset