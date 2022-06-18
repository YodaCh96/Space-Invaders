import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard:
    """Eine Klasse zum Anzeigen von Score-Informationen."""

    def __init__(self, ai_game):
        """Initialisierung von Scorekeeping-Attributen."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Schrifteinstellungen für Score-Informationen
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # Die ersten Bilder für die Punktevergabe vorbereiten
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Umwandlung der Bewertung in ein gerendertes Bild."""
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True,
            self.text_color)
        
        # Anzeige der Punktzahl oben rechts auf dem Bildschirm
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
    
    def prep_high_score(self):
        """Umwandlung von Highscore in ein gerendertes Bild."""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
            self.text_color)
        
        # Highscore oben auf dem Bildschirm zentrieren
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = 20
    
    def prep_level(self):
        """Level in ein gerendertes Bild umwandeln."""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True,
            self.text_color)
        
        # Level unter der Punktzahl positionieren
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10
    
    def prep_ships(self):
        """Zeigt an, wie viele Schiffe noch übrig sind."""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 20
            self.ships.add(ship)
    
    def check_high_score(self):
        """Prüfen, ob es einen neuen Highscore gibt."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
    
    def show_score(self):
        """Spielergebnisse, Level und Schiffe auf den Bildschirm zeichnen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
