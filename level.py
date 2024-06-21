import pygame
from text import Text
from button import Button

class Level:
    def __init__(self, player, player2):
        self.player = player
        self.player2 = player2
        self.MenuActive = True
        self.ChoseGamemode = False
        self.WatchLeaderboard = False
        self.IntroWasPlayed = False
        self.Singleplayer = False

    def draw(self):
        # Rysowanie elementów na ekranie
        pass

    def ResetGame(self):
        self.player.Reset()
        self.player2.Reset()
        self.MenuActive = True
        self.IntroWasPlayed = False
