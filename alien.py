import os, sys
import pygame
from pygame.sprite import Sprite

def resource_path(relative_path):
    """Absoluter Pfad zur Ressource, funktioniert fuer PyInstaller."""
    try:
        # PyInstaller erstellt einen temporaeren Ordner und speichert den Pfad in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath("images")

    return os.path.join(base_path, relative_path)


class Alien(Sprite):
    """Eine Klasse, die ein einzelnes Alien in der Flotte darstellt."""
    
    def __init__(self, ai_game):
        """Alien initialisieren und seine Startposition festlegen."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Alien-Bild laden und sein Rect-Attribut setzen
        self.img_path = resource_path("alien.png")
        self.image = pygame.image.load(self.img_path)
        self.rect = self.image.get_rect()

        # Neue Alien in der Naehe des oberen Bildschirmrandes beginnen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Die genaue horizontale Position des Aliens speichern
        self.x = float(self.rect.x)

    def check_edges(self):
        """Gibt True zurueck, wenn sich der Alien am Rand des Bildschirms befindet."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """Alien nach rechts oder links bewegen."""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x
